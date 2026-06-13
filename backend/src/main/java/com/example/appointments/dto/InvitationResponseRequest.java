package com.example.appointments.dto;

import com.example.appointments.domain.InvitationStatus;
import jakarta.validation.constraints.NotNull;

public record InvitationResponseRequest(@NotNull InvitationStatus response) {
}

