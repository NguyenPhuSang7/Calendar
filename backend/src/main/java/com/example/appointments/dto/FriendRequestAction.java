package com.example.appointments.dto;

import com.example.appointments.domain.FriendshipStatus;
import jakarta.validation.constraints.NotNull;

public record FriendRequestAction(@NotNull FriendshipStatus response) {
}
