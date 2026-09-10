package com.example.CrimeAi.controller;

import com.example.CrimeAi.dto.EvidenceResponse;
import com.example.CrimeAi.service.EvidenceService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/evidence")
@CrossOrigin(origins = "http://localhost:5173")
public class EvidenceController {

    private final EvidenceService evidenceService;

    public EvidenceController(EvidenceService evidenceService) {
        this.evidenceService = evidenceService;
    }

    @PostMapping("/upload")
    public ResponseEntity<EvidenceResponse> uploadEvidence(
            @RequestParam("caseId") String caseId,
            @RequestParam("file") MultipartFile file) throws Exception {

        EvidenceResponse response = evidenceService.uploadEvidence(caseId, file);
        return ResponseEntity.ok(response);
    }
}
