package com.secureshield.phishing_backend.scan.mapper;

import com.secureshield.backend.model.ScanHistoryItem;
import com.secureshield.backend.model.ScanReportResponse;
import com.secureshield.backend.model.ScanResponse;
import com.secureshield.phishing_backend.scan.domain.Scan;
import com.secureshield.phishing_backend.scan.flask.FlaskPredictionResponse;
import com.secureshield.phishing_backend.scan.persistence.entity.ScanEntity;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface ScanMapper {

    @Mapping(target = "id", ignore = true)
    ScanEntity toEntity(Scan scan);

    Scan toDomain(ScanEntity entity);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "scannedAt", ignore = true)
    Scan fromFlaskResponse(FlaskPredictionResponse response, String url);

    ScanHistoryItem toScanHistoryItem(Scan scan);


    ScanResponse toScanResponse(Scan scan);

    ScanReportResponse toScanReportResponse(Scan scan);
}
