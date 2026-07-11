package com.secureshield.phishing_backend.scan.report.impl;

import com.secureshield.phishing_backend.scan.domain.Scan;
import com.secureshield.phishing_backend.scan.report.CsvReportGenerator;
import org.springframework.stereotype.Component;

import java.nio.charset.StandardCharsets;

@Component
public class CsvReportGeneratorImpl implements CsvReportGenerator {

    @Override
    public byte[] generate(Scan scan) {

        StringBuilder csv = new StringBuilder();

        csv.append("Field,Value\n");
        csv.append("Reference,")
                .append(scan.getReference())
                .append("\n");
        csv.append("URL,")
                .append(scan.getUrl())
                .append("\n");
        csv.append("Prediction,")
                .append(scan.getPrediction())
                .append("\n");

        csv.append("\n");
        csv.append("Phishing Reasons\n");
        csv.append("Number,Reason\n");
        int i = 1;
        for (String reason : scan.getPhishingReasons()) {
            csv.append(i++)
                    .append(",\"")
                    .append(reason)
                    .append("\"\n");
        }

        csv.append("\n");
        csv.append("Legitimate Reasons\n");
        csv.append("Number,Reason\n");

        i = 1;
        for (String reason : scan.getLegitimateReasons()) {
            csv.append(i++)
                    .append(",\"")
                    .append(reason)
                    .append("\"\n");
        }

        csv.append("\n");
        csv.append("Conclusion,\"")
                .append(scan.getConclusion())
                .append("\"\n");
        csv.append("Scanned At,")
                .append(scan.getScannedAt())
                .append("\n\n");

        return csv.toString().getBytes(StandardCharsets.UTF_8);
    }
}