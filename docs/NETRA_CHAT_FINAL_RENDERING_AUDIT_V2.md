# NETRA CHAT FINAL RENDERING AUDIT V2

## 1. Reproduction & Root Cause
**Reported Behavior**: The chat UI continued to display internal action metadata, such as:
```text
Suggested Actions:
Trace financial links
Prompt: "..."
Type: EVIDENCE
Target ID: E-24e6c923
is_recommended: true
```
**Root Cause**: The LLM (Qwen) was outputting its thought process and action parameters directly into the conversational text body (generating markdown bullet points for the action schema). Because the backend fallback/extraction logic appended or accepted this plain text when it parsed the `submit_final_response` tool, the raw schema bled through the `answer` string directly into the React UI. Furthermore, the frontend `Chatbot.tsx` had a line explicitly rendering the internal `prompt` string onto the card UI, instead of a human-readable description.

## 2. Where Metadata Leaked
- **Backend `answer` string**: Qwen dumped its markdown serialization of the actions array into the prose block.
- **Frontend `ActionCards`**: React intentionally rendered `Ask: "{action.prompt}"` as a subtitle on recommended action cards.

## 3. Strict Architecture Fixes

### A. Strict LLM Instructions (Agent Boundary)
Added a `# STRICT UI SEPARATION (CRITICAL)` block to `prompts.py`:
- Explicitly mandates that the `answer` parameter MUST ONLY contain human-readable conversational prose.
- Strictly bans including "Suggested Actions", "Prompts", "Target IDs", or "Types" in the text response.

### B. Defensive Backend Sanitization (Response Adapter)
Enhanced `sanitize_answer` in `workflow.py` to strip out structural metadata leaks:
- Added regex matching to catch and remove `(?i)\**Suggested Actions:?.*` and `(?im)^.*(Target ID:|Type:|Prompt:|is_recommended:).*$\n?`.
- This ensures the API payload object is perfectly normalized before leaving FastAPI.

### C. UI Component Isolation (React)
- Updated `ActionItem` in `Chatbot.tsx` to distinguish between the internal `prompt` (the executable query) and a new `description` field (the human-readable subtext).
- Completely removed the rendering of the `prompt` string.
- Hidden variables (`target_id`, `type`, `prompt`, `is_recommended`) now solely dictate React internal logic (onClick handlers, SVG icon mapping, and component ordering) and are completely invisible in the DOM.

### D. Entity-ID Routing 
The `SYSTEM_PROMPT` enforces strict routing:
- Canonical IDs (`E-336f5a12`) must use `get_entity(entity_id)`.
- Human names (`Juhu`) must use `search_entities(query)`.
- Prevents the agent from producing "No identities found" errors when misusing string search.

## 4. Tests
- Created an automated regression test skeleton (`tests/test_chat_ui_leakage.js`) using Puppeteer to scan output strings for `<tool_call>`, `Target ID:`, `Type:`, and `Prompt:` leakages.
