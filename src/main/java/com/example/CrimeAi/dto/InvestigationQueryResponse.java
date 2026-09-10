package com.example.CrimeAi.dto;

import java.util.List;
import java.util.Map;

public class InvestigationQueryResponse {

    private String requestId;

    @com.fasterxml.jackson.annotation.JsonProperty("thread_id")
    private String threadId;

    private String answer;

    // Structured sections from submit_final_response
    private List<Map<String, Object>> facts;
    private List<Map<String, Object>> observations;
    private List<Map<String, Object>> uncertainties;
    private List<Map<String, Object>> actions;

    // Legacy / pass-through fields
    private List<Map<String, Object>> entities;
    private List<Map<String, Object>> relationships;
    private List<Map<String, Object>> findings;
    private List<Map<String, Object>> evidence;

    // trace is now an object: {"tools_used": [...], "truncated": false}
    @com.fasterxml.jackson.annotation.JsonIgnoreProperties(ignoreUnknown = true)
    private Map<String, Object> trace;

    private List<String> errors;

    // Keep old error/message fields for backward compat
    private String error;
    private String message;

    public InvestigationQueryResponse() {}

    public String getThreadId() { return threadId; }
    public void setThreadId(String threadId) { this.threadId = threadId; }

    public String getRequestId() { return requestId; }
    public void setRequestId(String requestId) { this.requestId = requestId; }

    public String getAnswer() { return answer; }
    public void setAnswer(String answer) { this.answer = answer; }

    public List<Map<String, Object>> getFacts() { return facts; }
    public void setFacts(List<Map<String, Object>> facts) { this.facts = facts; }

    public List<Map<String, Object>> getObservations() { return observations; }
    public void setObservations(List<Map<String, Object>> observations) { this.observations = observations; }

    public List<Map<String, Object>> getUncertainties() { return uncertainties; }
    public void setUncertainties(List<Map<String, Object>> uncertainties) { this.uncertainties = uncertainties; }

    public List<Map<String, Object>> getActions() { return actions; }
    public void setActions(List<Map<String, Object>> actions) { this.actions = actions; }

    public List<Map<String, Object>> getEntities() { return entities; }
    public void setEntities(List<Map<String, Object>> entities) { this.entities = entities; }

    public List<Map<String, Object>> getRelationships() { return relationships; }
    public void setRelationships(List<Map<String, Object>> relationships) { this.relationships = relationships; }

    public List<Map<String, Object>> getFindings() { return findings; }
    public void setFindings(List<Map<String, Object>> findings) { this.findings = findings; }

    public List<Map<String, Object>> getEvidence() { return evidence; }
    public void setEvidence(List<Map<String, Object>> evidence) { this.evidence = evidence; }

    public Map<String, Object> getTrace() { return trace; }
    public void setTrace(Map<String, Object> trace) { this.trace = trace; }

    public List<String> getErrors() { return errors; }
    public void setErrors(List<String> errors) { this.errors = errors; }

    public String getError() { return error; }
    public void setError(String error) { this.error = error; }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }
}

