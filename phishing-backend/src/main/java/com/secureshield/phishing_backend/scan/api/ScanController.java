package com.secureshield.phishing_backend.scan.api;

import com.secureshield.backend.api.ApiUtil;
import com.secureshield.backend.api.ScansApi;
import com.secureshield.backend.model.ScanHistoryResponse;
import com.secureshield.backend.model.ScanReportResponse;
import com.secureshield.backend.model.ScanRequest;
import com.secureshield.backend.model.ScanResponse;
import com.secureshield.phishing_backend.scan.service.impl.ScanService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.enums.ParameterIn;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequiredArgsConstructor
public class ScanController implements ScansApi {

    private final ScanService scanService;

    @Override
    public ResponseEntity<String> deleteScan(String reference) {
        scanService.deleteScan(reference);
        return ResponseEntity.ok("Scan deleted successfully.");
    }


    @Override
    public ResponseEntity<ScanReportResponse> getScanByReference(String reference) {
        ScanReportResponse response = scanService.getScanReport(reference);

        return ResponseEntity.ok(response);
    }

    @Override
    public ResponseEntity<ScanHistoryResponse> getScanHistory() {
        ScanHistoryResponse response = scanService.getScanHistory();
        return ResponseEntity.ok(response);
    }

    @Override
    public ResponseEntity<ScanResponse> scanUrl(@Valid @RequestBody ScanRequest scanRequest) {
        ScanResponse response = scanService.scan(scanRequest);

        return ResponseEntity.ok(response);
    }


    @Operation(
            summary = "Download scan report",
            description = "Downloads the scan report as a CSV file."
    )
    @GetMapping("/scans/{reference}/report")
    public ResponseEntity<byte[]> downloadReport(
            @PathVariable String reference) {

        byte[] csv = scanService.downloadScanReport(reference);

        String filename = "scan_" + reference + ".csv";

        return ResponseEntity.ok()
                .header(
                        HttpHeaders.CONTENT_DISPOSITION,
                        "attachment; filename=\"" + filename + "\"")
                .contentType(MediaType.parseMediaType("text/csv"))
                .body(csv);
    }

}


