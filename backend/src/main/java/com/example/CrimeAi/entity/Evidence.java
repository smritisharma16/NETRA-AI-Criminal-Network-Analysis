package com.example.CrimeAi.entity;

import jakarta.persistence.*;
import java.time.ZonedDateTime;
import java.util.UUID;

@Entity
@Table(name = "evidence")
public class Evidence {

    @Id
    @Column(name = "evidence_id", length = 100)
    private String evidenceId;

    @Column(name = "case_id", length = 50)
    private String caseId;

    @Column(name = "evidence_type", nullable = false, length = 100)
    private String evidenceType;

    @Column(name = "title", length = 255)
    private String title;

    @Column(name = "storage_uri", nullable = false, length = 500)
    private String storageUri;

    @Column(name = "file_hash", nullable = false, length = 64)
    private String fileHash;

    @Column(name = "hash_algorithm", length = 50)
    private String hashAlgorithm = "SHA-256";

    @Column(name = "source", length = 255)
    private String source;

    @Column(name = "collected_at")
    private ZonedDateTime collectedAt;

    @Column(name = "collected_by")
    private UUID collectedBy;

    @Column(name = "sealed")
    private Boolean sealed = false;

    @Column(name = "fabric_transaction_id", length = 255)
    private String fabricTransactionId;

    @Column(name = "created_at", nullable = false, updatable = false)
    private ZonedDateTime createdAt;

    // We can omit source_record_id and provenance_status if we don't map them explicitly, or we can map them as strings.
    // provenance_status is a postgres ENUM. It's safer to not map it or map it using @Enumerated if we need to set it.
    // Since it has a default 'VERIFIED' in the DB, omitting it is fine for basic inserts, but hibernate might complain.
    // If hibernate validates it, we should add it. Wait, the error was "missing column [id]", so hibernate checks what's in the Entity.
    // If the entity has fewer properties than the table, that's fine for validation.
    
    @PrePersist
    public void prePersist() {
        if (createdAt == null) {
            createdAt = ZonedDateTime.now();
        }
        if (collectedAt == null) {
            collectedAt = ZonedDateTime.now();
        }
    }

    public String getEvidenceId() { return evidenceId; }
    public void setEvidenceId(String evidenceId) { this.evidenceId = evidenceId; }
    public String getCaseId() { return caseId; }
    public void setCaseId(String caseId) { this.caseId = caseId; }
    public String getEvidenceType() { return evidenceType; }
    public void setEvidenceType(String evidenceType) { this.evidenceType = evidenceType; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getStorageUri() { return storageUri; }
    public void setStorageUri(String storageUri) { this.storageUri = storageUri; }
    public String getFileHash() { return fileHash; }
    public void setFileHash(String fileHash) { this.fileHash = fileHash; }
    public String getHashAlgorithm() { return hashAlgorithm; }
    public void setHashAlgorithm(String hashAlgorithm) { this.hashAlgorithm = hashAlgorithm; }
    public String getSource() { return source; }
    public void setSource(String source) { this.source = source; }
    public ZonedDateTime getCollectedAt() { return collectedAt; }
    public void setCollectedAt(ZonedDateTime collectedAt) { this.collectedAt = collectedAt; }
    public UUID getCollectedBy() { return collectedBy; }
    public void setCollectedBy(UUID collectedBy) { this.collectedBy = collectedBy; }
    public Boolean getSealed() { return sealed; }
    public void setSealed(Boolean sealed) { this.sealed = sealed; }
    public String getFabricTransactionId() { return fabricTransactionId; }
    public void setFabricTransactionId(String fabricTransactionId) { this.fabricTransactionId = fabricTransactionId; }
    public ZonedDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(ZonedDateTime createdAt) { this.createdAt = createdAt; }
}
