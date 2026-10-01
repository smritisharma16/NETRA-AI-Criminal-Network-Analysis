package com.example.CrimeAi.dto;

import java.time.ZonedDateTime;
import java.util.UUID;

public class EvidenceResponse {
    private String evidenceId;
    private String caseId;
    private String title;
    private String evidenceType;
    private String fileHash;
    private UUID collectedBy;
    private ZonedDateTime collectedAt;
    private String transactionId;

    public String getEvidenceId() { return evidenceId; }
    public void setEvidenceId(String evidenceId) { this.evidenceId = evidenceId; }
    public String getCaseId() { return caseId; }
    public void setCaseId(String caseId) { this.caseId = caseId; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getEvidenceType() { return evidenceType; }
    public void setEvidenceType(String evidenceType) { this.evidenceType = evidenceType; }
    public String getFileHash() { return fileHash; }
    public void setFileHash(String fileHash) { this.fileHash = fileHash; }
    public UUID getCollectedBy() { return collectedBy; }
    public void setCollectedBy(UUID collectedBy) { this.collectedBy = collectedBy; }
    public ZonedDateTime getCollectedAt() { return collectedAt; }
    public void setCollectedAt(ZonedDateTime collectedAt) { this.collectedAt = collectedAt; }
    public String getTransactionId() { return transactionId; }
    public void setTransactionId(String transactionId) { this.transactionId = transactionId; }
}
