The frontend now fully supports the "executable prompt" format. When you click an action card, the exact string in `action.prompt` is dispatched natively into the chat.
- Python tools have been updated: `submit_final_response` now takes `prompt` and `is_recommended` keys for action items.
- The `SYSTEM_PROMPT` enforces strict adherence to the conversational loop guidelines you provided.
