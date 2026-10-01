package com.example.CrimeAi.fabric;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.hyperledger.fabric.client.Contract;
import org.hyperledger.fabric.client.Gateway;
import org.hyperledger.fabric.client.Network;
import org.springframework.stereotype.Service;

import java.nio.charset.StandardCharsets;

@Service
public class FabricGatewayService {

    private final Gateway gateway;
    private final ObjectMapper objectMapper;

    private static final String CHANNEL_NAME = "mychannel";
    private static final String CHAINCODE_NAME = "crimeai";

    public FabricGatewayService(Gateway gateway) {
        this.gateway = gateway;
        this.objectMapper = new ObjectMapper();
    }

    public String createAudit(String caseId, String action, String performedBy, String timestamp, String dataHash) throws Exception {
        Network network = gateway.getNetwork(CHANNEL_NAME);
        Contract contract = network.getContract(CHAINCODE_NAME);

        byte[] result = contract.submitTransaction("CreateAudit", caseId, action, performedBy, timestamp, dataHash);
        
        String resultString = new String(result, StandardCharsets.UTF_8);
        JsonNode jsonNode = objectMapper.readTree(resultString);
        return jsonNode.get("transactionId").asText();
    }

    public String getCaseAudits(String caseId) throws Exception {
        Network network = gateway.getNetwork(CHANNEL_NAME);
        Contract contract = network.getContract(CHAINCODE_NAME);

        byte[] result = contract.evaluateTransaction("GetCaseAudits", caseId);
        return new String(result, StandardCharsets.UTF_8);
    }
}
