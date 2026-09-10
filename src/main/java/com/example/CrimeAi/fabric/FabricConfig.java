package com.example.CrimeAi.fabric;

import io.grpc.Grpc;
import io.grpc.ManagedChannel;
import io.grpc.TlsChannelCredentials;
import org.hyperledger.fabric.client.CallOption;
import org.hyperledger.fabric.client.Gateway;
import org.hyperledger.fabric.client.identity.Identities;
import org.hyperledger.fabric.client.identity.Identity;
import org.hyperledger.fabric.client.identity.Signer;
import org.hyperledger.fabric.client.identity.Signers;
import org.hyperledger.fabric.client.identity.X509Identity;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.InvalidKeyException;
import java.security.cert.CertificateException;
import java.util.concurrent.TimeUnit;

@Configuration
public class FabricConfig {

    @Value("${fabric.network.path}")
    private String networkPath;

    @Value("${fabric.peer.endpoint}")
    private String peerEndpoint;

    @Value("${fabric.peer.tlsHostname}")
    private String peerTlsHostname;

    @Value("${fabric.msp.id}")
    private String mspId;

    @Value("${fabric.cert.path}")
    private String certPath;

    @Value("${fabric.key.path}")
    private String keyPath;

    @Value("${fabric.tls.cert.path}")
    private String tlsCertPath;

    @Bean
    public Gateway gateway() throws Exception {
        ManagedChannel channel = newGrpcConnection();

        Gateway.Builder builder = Gateway.newInstance()
                .identity(newIdentity())
                .signer(newSigner())
                .connection(channel)
                .evaluateOptions(CallOption.deadlineAfter(5, TimeUnit.SECONDS))
                .endorseOptions(CallOption.deadlineAfter(15, TimeUnit.SECONDS))
                .submitOptions(CallOption.deadlineAfter(5, TimeUnit.SECONDS))
                .commitStatusOptions(CallOption.deadlineAfter(1, TimeUnit.MINUTES));

        return builder.connect();
    }

    private ManagedChannel newGrpcConnection() throws IOException {
        Path tlsCert = Paths.get(networkPath, tlsCertPath);
        TlsChannelCredentials.Builder credentials = TlsChannelCredentials.newBuilder()
                .trustManager(tlsCert.toFile());

        return Grpc.newChannelBuilder(peerEndpoint, credentials.build())
                .overrideAuthority(peerTlsHostname)
                .build();
    }

    private Identity newIdentity() throws IOException, CertificateException {
        Path cert = Paths.get(networkPath, certPath);
        var certificate = Identities.readX509Certificate(Files.newBufferedReader(cert));
        return new X509Identity(mspId, certificate);
    }

    private Signer newSigner() throws IOException, InvalidKeyException {
        Path keyDirPath = Paths.get(networkPath, keyPath);
        Path keyFile = null;
        try (var stream = Files.list(keyDirPath)) {
            keyFile = stream.findFirst().orElseThrow();
        }
        var privateKey = Identities.readPrivateKey(Files.newBufferedReader(keyFile));
        return Signers.newPrivateKeySigner(privateKey);
    }
}
