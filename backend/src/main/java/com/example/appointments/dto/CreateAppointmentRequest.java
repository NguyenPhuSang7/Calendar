package com.example.appointments.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.time.LocalDateTime;

public record CreateAppointmentRequest(
        @NotBlank @Size(max = 160) String title,
        Long contactId,
        Long guestId,
        @NotNull LocalDateTime startTime,
        @NotNull LocalDateTime endTime,
        @Size(max = 500) String note
) {
    public CreateAppointmentRequest(String title, Long contactId, LocalDateTime startTime,
                                    LocalDateTime endTime, String note) {
        this(title, contactId, null, startTime, endTime, note);
    }
}
