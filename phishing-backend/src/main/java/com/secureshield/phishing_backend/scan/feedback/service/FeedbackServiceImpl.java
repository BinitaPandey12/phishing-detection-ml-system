package com.secureshield.phishing_backend.scan.feedback.service;

import com.secureshield.backend.model.FeedbackRequest;
import com.secureshield.backend.model.FeedbackResponse;
import com.secureshield.phishing_backend.scan.feedback.domain.Feedback;
import com.secureshield.phishing_backend.scan.feedback.entity.FeedbackEntity;
import com.secureshield.phishing_backend.scan.feedback.mapper.FeedbackMapper;
import com.secureshield.phishing_backend.scan.feedback.repository.FeedbackRepository;
import com.secureshield.phishing_backend.scan.persistence.entity.ScanEntity;
import com.secureshield.phishing_backend.scan.repository.JpaScanRepository;
import com.secureshield.phishing_backend.scan.user.entity.UserEntity;
import com.secureshield.phishing_backend.scan.user.repository.JpaUserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;


@Service
@RequiredArgsConstructor
public class FeedbackServiceImpl implements FeedbackService {


    private final FeedbackRepository feedbackRepository;
    private final JpaScanRepository scanRepository;
    private final JpaUserRepository userRepository;
    private final FeedbackMapper mapper;


    @Override
    public FeedbackResponse createFeedback(
            FeedbackRequest request,
            UUID userId) {


        UserEntity user = userRepository.findById(userId)
                .orElseThrow(() ->
                        new RuntimeException("User not found"));


        ScanEntity scan = null;


        if (request.getScanId() != null) {
            scan = scanRepository.findById(request.getScanId())
                    .orElseThrow(() ->
                            new RuntimeException("Scan not found"));

            if (!scan.getUser().getId().equals(userId)) {
                throw new RuntimeException("Not your scan");
            }
        }

        FeedbackEntity entity = FeedbackEntity.builder()
                .user(user)
                .scan(scan)
                .message(request.getMessage())
                .createdAt(OffsetDateTime.now())
                .build();

        FeedbackEntity savedEntity =
                feedbackRepository.save(entity);

        Feedback saved =
                mapper.toDomain(savedEntity);

        return mapper.toResponse(saved);
    }


    @Override
    public List<FeedbackResponse> getFeedback(UUID userId) {


        return feedbackRepository.findByUserId(userId)
                .stream()
                .map(mapper::toDomain)
                .map(mapper::toResponse)
                .toList();

    }

}