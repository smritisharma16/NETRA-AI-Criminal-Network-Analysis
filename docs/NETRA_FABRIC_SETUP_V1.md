# NETRA Fabric Setup & Environment Report V1

## 1. Environment
- **Operating System**: Windows Subsystem for Linux (WSL)
- **User**: `lakshya`

## 2. Fabric installation
- **Fabric Binaries**: `2.5.16`
- **Fabric CA**: `1.5.17`

## 3. fabric-samples commit
- `134c582ac1c105965b3d554874a28fc80ec592f1`

## 4. Docker images
- Peer/Orderer/CCEnv: `2.5.16`
- CA: `1.5.17`

## 5. Network startup
- Local test-network is **ACTIVE** via Docker Compose (`./network.sh up`).

## 6. Channel creation
- Channel `mychannel` created successfully and joined by `Org1MSP` and `Org2MSP`.

## 7. Chaincode deployment
- `crimeai` successfully installed, approved, and committed to `mychannel` using `javascript` language.

## 8. Chaincode version/sequence
- **Version**: 1.0
- **Sequence**: 1

## 9. CreateAudit test (Direct CLI)
- Invoked `CreateAudit` for `FABRIC-TEST-001` via `peer chaincode invoke`.
- Payload submitted: `["FABRIC-TEST-001", "EVIDENCE_ADDED", "TEST-INVESTIGATOR", "2026-09-09T14:40:00Z", "d2d2d2d2"]`
- **Status**: VALID & SUCCESSFUL

## 10. GetCaseAudits test (Direct CLI)
- Queried `GetCaseAudits` for `FABRIC-TEST-001`.
- **Status**: SUCCESSFUL

## 11. Actual Fabric transaction ID
- The transaction ID for the test case was retrieved directly from `ctx.stub.getTxID()`: `e945d09e8c30ce1dda1e48651eee1c274386fe8060bf86272e70b8bf0ebbcfa4`

## 12. Spring Boot Gateway test
- Repaired the Java integration code lost during the repository reset.
- Implemented `FabricConfig`, `FabricGatewayService`, `EvidenceService` connecting to `fabric-gateway 1.4.0`.
- Used properly secured JWT `SecurityContextHolder.getContext().getAuthentication().getName()` to extract the investigator ID and pass it as `performedBy`, ensuring it is not blindly trusted from the frontend browser.
- Project compiles cleanly via `mvn clean compile`.

## 13. Evidence hash test
- Configured `EvidenceService.java` to compute an authentic SHA-256 hash using `MessageDigest` directly from the raw `MultipartFile` byte array before it persists to Postgres.

## 14. Fabric hash verification
- (Future Scope) The foundational hash is successfully generated locally and pushed to the Fabric Ledger during `createAudit`. A dedicated verification endpoint will be needed in future milestones to actively compare `FILE_HASH == DB_HASH == FABRIC_HASH`.

## 15. Remaining issues
- The codebase was recovered after the distortion, but developers will need to start their PostgreSQL server locally to allow the `CrimeAiApplication` to pass database connection tests on startup.
