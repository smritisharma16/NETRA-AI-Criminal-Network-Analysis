import sys

with open(r"d:\NETRA\SIH2026\ai-service\app\agent\workflow.py", "r", encoding="utf-8") as f:
    content = f.read()

fallback_code = """
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
"""

old_code = """
        # Check if the agent called submit_final_response
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            for tc in last_message.tool_calls:
                if tc["name"] == "submit_final_response":
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
"""

if old_code.strip() in content:
    content = content.replace(old_code.strip(), fallback_code.strip())
    with open(r"d:\NETRA\SIH2026\ai-service\app\agent\workflow.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Added fallback logic to workflow.py")
else:
    print("Could not find old code block to replace.")

