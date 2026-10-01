package com.example.CrimeAi.service;

import com.example.CrimeAi.dto.EvidenceResponse;
import com.example.CrimeAi.entity.Evidence;
import com.example.CrimeAi.entity.User;
import com.example.CrimeAi.fabric.FabricGatewayService;
import com.example.CrimeAi.repository.EvidenceRepository;
import com.example.CrimeAi.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.Authentication;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.MessageDigest;
import java.time.ZonedDateTime;
import java.util.UUID;

@Service
public class EvidenceService {

    private final EvidenceRepository evidenceRepository;
    private final UserRepository userRepository;
    private final FabricGatewayService fabricGatewayService;
    private final Path storageLocation = Paths.get("evidence-storage");

    public EvidenceService(EvidenceRepository evidenceRepository, UserRepository userRepository, FabricGatewayService fabricGatewayService) {
        this.evidenceRepository = evidenceRepository;
        this.userRepository = userRepository;
        this.fabricGatewayService = fabricGatewayService;
        try {
            Files.createDirectories(storageLocation);
        } catch (IOException e) {
            throw new RuntimeException("Could not create storage directory", e);
        }
    }

    public EvidenceResponse uploadEvidence(String caseId, MultipartFile file) throws Exception {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        String username = (auth != null) ? auth.getName() : "SYSTEM";
        
        UUID collectedBy = null;
        if (!"SYSTEM".equals(username)) {
            User user = userRepository.findByUsername(username).orElse(null);
            if (user != null) {
                collectedBy = user.getUserId();
            }
        }

        byte[] bytes = file.getBytes();
        String hash = calculateSha256(bytes);

        Evidence evidence = new Evidence();
        evidence.setEvidenceId(UUID.randomUUID().toString());
        evidence.setCaseId(caseId);
        evidence.setTitle(file.getOriginalFilename());
        evidence.setEvidenceType(file.getContentType() != null ? file.getContentType() : "application/octet-stream");
        evidence.setFileHash(hash); // The table is 64 length, so raw hex hash.
        evidence.setCollectedBy(collectedBy);
        
        Path destination = storageLocation.resolve(System.currentTimeMillis() + "_" + file.getOriginalFilename());
        Files.write(destination, bytes);
        evidence.setStorageUri(destination.toString());

        Evidence saved = evidenceRepository.save(evidence);

        String transactionId = fabricGatewayService.createAudit(
                saved.getCaseId(),
                "EVIDENCE_ADDED",
                username, // Store username on fabric for readability
                saved.getCreatedAt().toString(),
                saved.getFileHash()
        );

        saved.setFabricTransactionId(transactionId);
        saved = evidenceRepository.save(saved);

        EvidenceResponse res = new EvidenceResponse();
        res.setEvidenceId(saved.getEvidenceId());
        res.setCaseId(saved.getCaseId());
        res.setTitle(saved.getTitle());
        res.setEvidenceType(saved.getEvidenceType());
        res.setFileHash(saved.getFileHash());
        res.setCollectedBy(saved.getCollectedBy());
        res.setCollectedAt(saved.getCollectedAt());
        res.setTransactionId(transactionId);
        
        return res;
    }

    private String calculateSha256(byte[] data) throws Exception {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        byte[] hash = md.digest(data);
        StringBuilder hexString = new StringBuilder(2 * hash.length);
        for (byte b : hash) {
            String hex = Integer.toHexString(0xff & b);
            if(hex.length() == 1) {
                hexString.append('0');
            }
            hexString.append(hex);
        }
        return hexString.toString();
    }
}
