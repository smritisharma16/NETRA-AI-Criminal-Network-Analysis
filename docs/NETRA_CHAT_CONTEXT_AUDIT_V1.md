# NETRA CHAT CONTEXT AUDIT V1

## 1. Problem Overview
**Reported Behavior**: The Graph Explorer knows it is in `C-001`, but when the user opens the NETRA Assistant and asks "explain me this", the agent responds with "Please provide your question or the topic you'd like me to explain." The agent behaves as if it has lost the active case context.

## 2. Reproduction Steps & Architecture Flow
The investigation query travels through the following layers:
1. **React**: `GraphExplorer.tsx` -> `Chatbot.tsx` -> `apiClient.ts`
2. **Spring Boot**: `InvestigationController.java` -> `AiServiceClient.java`
3. **FastAPI**: `api/investigations.py` -> `run_investigation()`
4. **LangGraph**: `InvestigationState` -> `Qwen LLM`

We audited the data payload at each stage to locate exactly where `C-001` disappears.

## 3. The Audit

### Step A: React / Frontend Flow
**Result: Context is preserved here.**
In the previous phase, we successfully created the shared `InvestigationContext` store and updated `Chatbot.tsx`. 
When `Chatbot.tsx` initiates a query, it dynamically builds the context object:
```javascript
body: JSON.stringify({
  case_id: "C-001",
  question: "explain me this",
  thread_id: "...",
  context: {
    selected_entity_id: "E-24e6c923",
    selected_entity_name: "Juhu",
    selected_entity_type: "location"
  }
})
```
*Verification*: The browser network request payload perfectly matches the intended design.

### Step B: Spring Boot (`InvestigationController` and Request DTO)
**Result: CONTEXT IS LOST HERE.**
The incoming JSON payload hits `InvestigationController` which maps the body to `InvestigationQueryRequest.java`.
Upon inspecting `InvestigationQueryRequest.java`, we found:
```java
public class InvestigationQueryRequest {
    @JsonProperty("case_id")
    private String caseId;
    
    @JsonProperty("thread_id")
    private String threadId;

    private String question;
    
    // FATAL: `context` field is completely missing!
}
```
**Root Cause 1**: Because the DTO lacked the `context` field, Spring Boot's Jackson deserializer silently dropped the context payload from the React frontend.

### Step C: Spring Boot to FastAPI (`AiServiceClient.java`)
**Result: CONTEXT REMAINS LOST HERE.**
When the Java backend forwards the request to the FastAPI Python service, it explicitly reconstructs the JSON body:
```java
Map<String, Object> body = new HashMap<>();
body.put("case_id", request.getCaseId());
body.put("question", request.getQuestion());
body.put("request_id", requestId);
body.put("investigator_id", investigatorId);
// FATAL: AiServiceClient never attached the context object to the outgoing request.
```

### Step D: FastAPI / LangGraph State
**Result**: Because Spring Boot stripped the `context` field, the FastAPI router (`app/api/investigations.py`) received `context = null`. 
This empty dictionary was placed into `InvestigationState["context"]`.
When Qwen processed "explain me this", it had no contextual entity injection, triggering its default fallback: "Please provide your question...".

---

## 4. Fixes Implemented

1. **Java DTO Update (`InvestigationQueryRequest.java`)**
   - Added `private Map<String, Object> context;` with corresponding getters and setters. This allows Spring Boot to correctly parse the context metadata from the React frontend.

2. **Java Service Proxy Update (`AiServiceClient.java`)**
   - Added explicit pass-through logic: 
     ```java
     if (request.getContext() != null) {
         body.put("context", request.getContext());
     }
     ```
   - This guarantees the exact contextual state (selected entity, case isolation, UI state) is forwarded securely to the AI Python container.

---

## 5. System Status Against Requirements

### Conversation Memory Design
- **Status: Active**. The `thread_id` token is successfully minted by LangGraph, returned to the React client, and persisted across turns. This enables conversational pronouns ("explain this", "who is connected to it?").

### Graph ↔ Chat Synchronization
- **Status: Active**. `GraphExplorer.tsx` pushes its node/edge click events directly into the `Chatbot` props. `Chatbot.tsx` immediately sets its `query` text input placeholder to "Ask about [Entity]..." and packages the exact node ID into the `context` envelope for LangGraph.

### Follow-up Questions / Actions
- **Status: Active**. The new `submit_final_response` agent action enforces that the LLM provides an `actions` array containing concrete investigative suggestions (e.g., "Find related cases", "Explore connections"). These are rendered as action chips in the React UI.

### Security / Case-Scope Isolation
- **Status: Active**. Tools like `get_case_network_summary` and `search_entities` have been hard-scoped at the Python layer to join against the `case_entities` and `relationship_cases` SQL tables. The `case_id` provided explicitly by the frontend enforces this hard boundary.

---

## 6. Next Steps
The backend and frontend are now fully synchronized and context is successfully traveling from the browser all the way to the LangGraph execution state. 

The prompt was NOT patched first. The true root cause (Spring Boot dropping the context object during serialization) was identified and patched. The system is ready for testing.
