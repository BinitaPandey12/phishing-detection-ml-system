package com.secureshield.phishing_backend.scan.service.impl;

import com.secureshield.backend.model.*;
import com.secureshield.phishing_backend.scan.domain.Scan;
import com.secureshield.phishing_backend.scan.flask.FlaskClient;
import com.secureshield.phishing_backend.scan.flask.FlaskPredictionResponse;
import com.secureshield.phishing_backend.scan.mapper.ScanMapper;
import com.secureshield.phishing_backend.scan.persistence.entity.ScanEntity;
import com.secureshield.phishing_backend.scan.report.CsvReportGenerator;
import com.secureshield.phishing_backend.scan.repository.JpaScanRepository;
import com.secureshield.phishing_backend.scan.user.entity.UserEntity;
import com.secureshield.phishing_backend.scan.user.repository.JpaUserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AnonymousAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class ScanServiceImpl implements ScanService {

    private final JpaUserRepository userRepository;
    private final CsvReportGenerator csvReportGenerator;
    private final FlaskClient flaskClient;
    private final JpaScanRepository scanRepository;
    private final ScanMapper scanMapper;


    @Override
    public ScanResponse scan(ScanRequest request) {


        FlaskPredictionResponse flaskResponse =
                flaskClient.predict(request.getUrl());


        Scan scan =
                scanMapper.fromFlaskResponse(
                        flaskResponse,
                        request.getUrl()
                );


        scan.setReference(generateReference());

        scan.setScannedAt(
                OffsetDateTime.now()
        );


        Authentication authentication =
                SecurityContextHolder
                        .getContext()
                        .getAuthentication();


        // Logged in user
        if (authentication != null
                && authentication.isAuthenticated()
                && !(authentication instanceof AnonymousAuthenticationToken)) {


            String email = authentication.getName();


            UserEntity user =
                    userRepository.findByEmail(email)
                            .orElseThrow();


            ScanEntity entity =
                    scanMapper.toEntity(scan);


            entity.setUser(user);


            ScanEntity saved =
                    scanRepository.save(entity);


            return scanMapper.toScanResponse(
                    scanMapper.toDomain(saved)
            );
        }


        // Guest user
        return scanMapper.toScanResponse(scan);
    }


    @Override
    public ScanReportResponse getScanReport(String reference) {

        ScanEntity entity =
                scanRepository.findByReference(reference)
                        .orElseThrow();

        return scanMapper.toScanReportResponse(
                scanMapper.toDomain(entity));

    }

    private String generateReference() {

        return "SCAN-" + UUID.randomUUID();

    }

    @Override
    public ScanHistoryResponse getScanHistory(String email) {

        List<ScanHistoryItem> scans = scanRepository.findByUserEmail(email)
                .stream()
                .map(scanMapper::toDomain)
                .map(scanMapper::toScanHistoryItem)
                .toList();

        ScanHistoryResponse response = new ScanHistoryResponse();
        response.setScans(scans);

        return response;
    }

    @Override
    public void deleteScan(String reference) {

        ScanEntity entity = scanRepository.findByReference(reference)
                .orElseThrow(() -> new RuntimeException("Scan not found"));

        scanRepository.delete(entity);
    }

    @Override
    public byte[] downloadScanReport(String reference) {

        ScanEntity entity = scanRepository.findByReference(reference)
                .orElseThrow(() -> new RuntimeException("Scan not found"));

        Scan scan = scanMapper.toDomain(entity);

        return csvReportGenerator.generate(scan);
    }


}
