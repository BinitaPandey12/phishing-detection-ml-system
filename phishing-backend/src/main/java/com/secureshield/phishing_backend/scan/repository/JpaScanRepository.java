package com.secureshield.phishing_backend.scan.repository;

import com.secureshield.phishing_backend.scan.persistence.entity.ScanEntity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;
import java.util.UUID;

public interface JpaScanRepository extends JpaRepository<ScanEntity, UUID> {

    Optional<ScanEntity> findByReference(String reference);
}
