package com.example.appointments.dto;

import com.example.appointments.domain.ServiceOffering;
import java.math.BigDecimal;

public record ServiceResponse(Long id, String name, Integer durationMinutes, BigDecimal price) {
    public static ServiceResponse from(ServiceOffering service) {
        return new ServiceResponse(service.getId(), service.getName(), service.getDurationMinutes(), service.getPrice());
    }
}

