package com.example.appointments.dto;

import com.example.appointments.domain.AppointmentStatus;
import jakarta.validation.constraints.NotNull;

public record UpdateAppointmentStatusRequest(@NotNull AppointmentStatus status) {
}

