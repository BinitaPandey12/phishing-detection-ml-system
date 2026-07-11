package com.secureshield.phishing_backend.scan.service.impl;

import com.secureshield.backend.model.ScanHistoryResponse;
import com.secureshield.backend.model.ScanReportResponse;
import com.secureshield.backend.model.ScanRequest;
import com.secureshield.backend.model.ScanResponse;

import java.util.UUID;

public interface ScanService {

    ScanResponse scan(ScanRequest request);

    ScanReportResponse getScanReport(String reference);

    ScanHistoryResponse getScanHistory();

    void deleteScan(String reference);

    byte[] downloadScanReport(String reference);
}
