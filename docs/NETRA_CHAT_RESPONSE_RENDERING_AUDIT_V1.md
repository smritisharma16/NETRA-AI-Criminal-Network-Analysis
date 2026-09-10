# NETRA CHAT RESPONSE RENDERING AUDIT V1

## 1. Problem Overview
**Reported Behavior**: The Chat UI was rendering internal response structures, unparsed HTML/XML-like content (e.g. `<tool_call>`), and text concatenated with Material Icon names (e.g., `analyticsWhy It Matters`, `device_hubExplore relationships`). The output was overly repetitive, duplicating facts, observations, and tool calls.

## 2. Root Cause Analysis
We performed a full trace of the response pipeline from Qwen to the React UI:
1. **Tool Output & XML Bleed**: Because Qwen uses `<tool_call>` wrappers to invoke `submit_final_response`, these internal XML wrappers were occasionally leaking into the conversational `content` payload.
2. **Duplication**: The LangGraph state was merging the `last_message.content` (which sometimes contained a raw text answer AND an unparsed XML block) with the structured payload extracted from the `submit_final_response` tool arguments.
3. **UI Icon Bleed**: The React frontend used `<span className="material-symbols-outlined">analytics</span> Why It Matters`. In certain environments, this text simply concatenated into `analyticsWhy It Matters` because the fallback font failed or the semantic HTML lacked ARIA isolation.
4. **Entity Resolution Tool Mismatch**: The prompt did not specify the difference between canonical entity ID lookup (`get_entity`) and string search (`search_entities`), leading to LLM lookup failures (e.g., "E-336f5a12" was sent into the string search engine).

## 3. Architecture & Rendering Fixes Implemented

### Backend (FastAPI / LangGraph)
1. **Regex Sanitization Layer**: Introduced `sanitize_answer(text)` in `workflow.py`. It aggressively strips `<tool_call>...</tool_call>` and `<function=...>` XML tags from the final text payload before returning it to the user.
2. **Single-Pass Extraction**: `workflow.py` now explicitly overrides any default `content` text if `submit_final_response` was invoked. It isolates the JSON payload and ignores the unparsed reasoning trace.
3. **Routing Precision**: The `SYSTEM_PROMPT` in `prompts.py` was updated with a `CRITICAL DISTINCTION` block. It instructs the agent to route canonical IDs (e.g., `E-123`) strictly to `get_entity`, and human names (e.g., `Juhu`) strictly to `search_entities`.

### Frontend (React)
1. **Removed Material Icon Text**: All `<span className="material-symbols-outlined">` references in `Chatbot.tsx` were replaced with native SVG components from `lucide-react` (e.g., `<BarChart3 />`, `<CheckCircle2 />`, `<LinkIcon />`). This completely eliminates the risk of text bleeding like `analyticsWhy It Matters`.
2. **Action Card Isolation**: Action buttons are now beautifully rendered with their semantic labels and independent SVG icons.
3. **Investigation Details Drawer**: The internal LangGraph trace (tools used, truncation flag) is nested cleanly inside a collapsible `▸ Investigation Details` panel. It is no longer dumped into the main investigator chat stream.

## 4. Final Response Contract Validation
The API response schema remains strictly separated into 3 tiers:
- **Semantic Answer**: `answer`, `facts`, `observations`, `uncertainties`
- **Context Metadata**: `case_id`, `selected_entity_id`, etc.
- **Investigator Actions**: Executable `actions` containing human-readable `label` and a natural language `prompt`.

No HTML or XML is sent by the backend. The frontend handles 100% of the UI rendering through safe, typed React components.
