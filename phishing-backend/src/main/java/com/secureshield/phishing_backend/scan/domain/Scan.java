package com.secureshield.phishing_backend.scan.domain;


import lombok.Data;

import java.time.LocalDateTime;
import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;

@Data
public class Scan {

    private UUID id;
    private String reference;
    private String url;
    private String prediction;
    private String conclusion;
    private String formattedExplanation;
    private List<String> phishingReasons;
    private List<String> legitimateReasons;
    private OffsetDateTime scannedAt;
}



