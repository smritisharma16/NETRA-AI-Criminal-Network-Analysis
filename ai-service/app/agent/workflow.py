from app.config import config
from typing import Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from app.agent.state import InvestigationState
from app.agent.tools import get_all_tools
from app.agent.prompts import SYSTEM_PROMPT
import json
import logging
import re

def sanitize_answer(text: str) -> str:
    if not text:
        return text
    # Remove raw <tool_call> blocks
    text = re.sub(r'<tool_call>.*?</tool_call>', '', text, flags=re.DOTALL)
    # Remove <function=...> blocks
    text = re.sub(r'<function=.*?>.*?</function>', '', text, flags=re.DOTALL)
    
    # Strip LLM hallucinated metadata sections (e.g. "**Suggested Actions:**\n- **Trace...**")
    text = re.sub(r'(?i)\n*#* *\*?Suggested Actions:?\*?.*', '', text, flags=re.DOTALL)
    text = re.sub(r'(?i)\n*#* *\*?Actions:?\*?.*', '', text, flags=re.DOTALL)
    
    # Strip LLM hallucinated fields in plain text
    text = re.sub(r'(?im)^.*(Target ID:|Type:|Prompt:|is_recommended:).*$\n?', '', text)
    
    # Strip any leading/trailing whitespace
    return text.strip()

from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver

import os
DB_URI = f"postgresql://{os.getenv('POSTGRES_USER', 'postgres')}:{os.getenv('POSTGRES_PASSWORD', 'postgres')}@{os.getenv('POSTGRES_HOST', '127.0.0.1')}:{os.getenv('POSTGRES_PORT', '5433')}/{os.getenv('POSTGRES_DB', 'postgres')}"
pool = ConnectionPool(conninfo=DB_URI, max_size=10, kwargs={"autocommit": True})
checkpointer = PostgresSaver(pool)
checkpointer.setup()


logger = logging.getLogger(__name__)

tools = get_all_tools()
tool_node = ToolNode(tools)

# Use Qwen compatible OpenAI endpoint, or fallback to a mock/mock-endpoint for tests
llm = ChatOpenAI(
    base_url=f"{config.QWEN_BASE_URL}/v1",
    api_key="sk-no-key",
    model="qwen"
)
llm_with_tools = llm.bind_tools(tools)

def interpret_query(state: InvestigationState) -> InvestigationState:
    messages = state.get("messages", [])
    
    # Context Propagation
    context = state.get("context", {})
    context_str = ""
    if context:
        context_str = "CURRENT CHAT CONTEXT (Use this to resolve 'it', 'this person', 'they', etc):\n"
        for k, v in context.items():
            context_str += f"- {k}: {v}\n"
        context_str += "\n"
        
    new_message = HumanMessage(content=f"{context_str}Question: {state.get('question')}")
    
    if not messages:
        return {"messages": [SystemMessage(content=SYSTEM_PROMPT), new_message]}
    else:
        return {"messages": [new_message]}

def call_model(state: InvestigationState) -> dict:
    messages = state["messages"]
    try:
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
    except Exception as e:
        logger.error(f"LLM Error: {e}", exc_info=True)
        # Return a safe message — do NOT expose the raw Python exception to the investigator
        from langchain_core.messages import AIMessage
        return {
            "messages": [AIMessage(content="[UNKNOWN] The reasoning engine is temporarily unavailable. I could not complete this investigation step.")],
            "errors": ["LLM engine error. Details have been logged."]
        }


def should_continue(state: InvestigationState) -> Literal["tools", "__end__"]:
    messages = state["messages"]
    last_message = messages[-1]
    
    tool_calls_count = len([m for m in messages if hasattr(m, 'tool_calls') and m.tool_calls])
    
    # If the LLM makes a tool call, we transition to the "tools" node
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        if any(tc["name"] == "submit_final_response" for tc in last_message.tool_calls):
            return "__end__"
            
        if tool_calls_count > 20:
            logger.warning("Investigation exceeded 20 tool calls. Forcing termination.")
            return "__end__"
        return "tools"
        
    # Otherwise, it has produced a final response
    return "__end__"

workflow = StateGraph(InvestigationState)
workflow.add_node("interpret_query", interpret_query)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "interpret_query")
workflow.add_edge("interpret_query", "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

app_workflow = workflow.compile(checkpointer=checkpointer)

def run_investigation(case_id: str, question: str, request_id: str, thread_id: str = None, context: dict = None) -> dict:
    if not thread_id:
        import uuid
        thread_id = str(uuid.uuid4())
        
    initial_state = {
        "request_id": request_id,
        "case_id": case_id,
        "question": question,
        "context": context or {},
        "errors": []
    }
    
    config = {
        "configurable": {"thread_id": thread_id},
        "recursion_limit": 50
    }
    
    # Run graph with recursion limit
    try:
        result = app_workflow.invoke(initial_state, config)
        last_message = result["messages"][-1]
        
        # Initialize structured output
        raw_content = last_message.content or ""
        structured_response = {
            "answer": sanitize_answer(raw_content) or "[No text returned]",
            "facts": [],
            "observations": [],
            "uncertainties": [],
            "actions": [],
            "trace": {"tools_used": [], "truncated": False}
        }
        
        # Check if the agent called submit_final_response
        called_tool = False
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            for tc in last_message.tool_calls:
                if tc["name"] == "submit_final_response":
                    called_tool = True
                    args = tc["args"]
                    # Override the default answer with the structured one
                    tool_answer = args.get("answer", "")
                    if tool_answer:
                        structured_response["answer"] = sanitize_answer(tool_answer)
                    structured_response["facts"] = args.get("facts", [])
                    structured_response["observations"] = args.get("observations", [])
                    structured_response["uncertainties"] = args.get("uncertainties", [])
                    structured_response["actions"] = args.get("actions", [])
                    break

        # Safety Fallback: Qwen sometimes outputs raw JSON text instead of a tool call
        if not called_tool and (raw_content.strip().startswith("{") or "```json" in raw_content):
            try:
                start = raw_content.find('{')
                end = raw_content.rfind('}')
                if start != -1 and end != -1:
                    import json
                    json_str = raw_content[start:end+1]
                    parsed = json.loads(json_str)
                    if "answer" in parsed:
                        structured_response["answer"] = sanitize_answer(parsed.get("answer", ""))
                        structured_response["facts"] = parsed.get("facts", [])
                        structured_response["observations"] = parsed.get("observations", [])
                        structured_response["uncertainties"] = parsed.get("uncertainties", [])
                        structured_response["actions"] = parsed.get("actions", [])
            except Exception as e:
                logger.warning(f"Failed to parse fallback JSON from LLM: {e}")
        
        # Add safety fallback
        if not structured_response["answer"] and hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            structured_response["answer"] = "[INCOMPLETE] The investigation reached its safety limit before a final answer could be generated."
        
        # Extract trace metadata
        trace_tools = []
        for msg in result["messages"]:
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tc in msg.tool_calls:
                    if tc["name"] != "submit_final_response":
                        trace_tools.append({
                            "tool": tc['name'],
                            "arguments": tc['args']
                        })
        structured_response["trace"]["tools_used"] = trace_tools
        
        return {
            "request_id": request_id,
            "thread_id": thread_id,
            **structured_response,
            "errors": result.get("errors", [])
        }
    except Exception as e:
        logger.error("run_investigation fatal error (request_id=%s): %s", request_id, e, exc_info=True)
        return {
            "request_id": request_id,
            "thread_id": thread_id,
            "answer": "The investigation encountered a technical issue. Please try again or contact your system administrator.",
            "trace": [],
            "errors": ["A technical error occurred. Details have been logged."]
        }

