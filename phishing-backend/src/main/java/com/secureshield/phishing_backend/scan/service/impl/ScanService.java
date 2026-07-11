package com.secureshield.phishing_backend.scan.service.impl;

import com.secureshield.backend.model.ScanHistoryResponse;
import com.secureshield.backend.model.ScanReportResponse;
import com.secureshield.backend.model.ScanRequest;
import com.secureshield.backend.model.ScanResponse;

public interface ScanService {

    ScanResponse scan(ScanRequest request);

    ScanReportResponse getScanReport(String reference);

    ScanHistoryResponse getScanHistory(String email);

    void deleteScan(String reference);

    byte[] downloadScanReport(String reference);
}
