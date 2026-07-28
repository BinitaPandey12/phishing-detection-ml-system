package com.secureshield.phishing_backend.scan.feedback.mapper;

import com.secureshield.backend.model.FeedbackResponse;
import com.secureshield.phishing_backend.scan.feedback.domain.Feedback;
import com.secureshield.phishing_backend.scan.feedback.entity.FeedbackEntity;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface FeedbackMapper {
    @Mapping(
            target = "reply",
            expression = "java(\"Thank you for your valuable feedback!\")"
    )
    FeedbackResponse toResponse(Feedback feedback);

    Feedback toDomain(FeedbackEntity entity);
}
