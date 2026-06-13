package com.example.appointments.dto;

public record AuthResponse(
        String token,
        String tokenType,
        long expiresInSeconds,
        Long userId,
        String username,
        String fullName
) {
}

