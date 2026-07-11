package com.secureshield.phishing_backend.scan.service.impl;

import com.secureshield.backend.model.*;
import com.secureshield.phishing_backend.scan.domain.Scan;
import com.secureshield.phishing_backend.scan.flask.FlaskClient;
import com.secureshield.phishing_backend.scan.flask.FlaskPredictionResponse;
import com.secureshield.phishing_backend.scan.mapper.ScanMapper;
import com.secureshield.phishing_backend.scan.persistence.entity.ScanEntity;
import com.secureshield.phishing_backend.scan.report.CsvReportGenerator;
import com.secureshield.phishing_backend.scan.repository.JpaScanRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class ScanServiceImpl implements ScanService {

    private final CsvReportGenerator csvReportGenerator;
    private final FlaskClient flaskClient;
    private final JpaScanRepository scanRepository;
    private final ScanMapper scanMapper;

    @Override
    public ScanResponse scan(ScanRequest request) {

        FlaskPredictionResponse flaskResponse =
                flaskClient.predict(request.getUrl());
        System.out.println("Prediction: " + flaskResponse.getPrediction());
        System.out.println("Conclusion: " + flaskResponse.getConclusion());
        System.out.println("Formatted Explanation: " + flaskResponse.getFormattedExplanation());
        System.out.println("Phishing Reasons: " + flaskResponse.getPhishingReasons());
        System.out.println("Legitimate Reasons: " + flaskResponse.getLegitimateReasons());

        Scan scan = scanMapper.fromFlaskResponse(
                        flaskResponse,
                        request.getUrl());

        scan.setReference(generateReference());

        scan.setScannedAt(OffsetDateTime.now());

        ScanEntity saved =
                scanRepository.save(
                        scanMapper.toEntity(scan));

        return scanMapper.toScanResponse(
                scanMapper.toDomain(saved));

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
    public ScanHistoryResponse getScanHistory() {

        List<ScanHistoryItem> scans = scanRepository.findAll()
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
