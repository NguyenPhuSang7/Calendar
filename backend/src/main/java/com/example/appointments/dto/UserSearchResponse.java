package com.example.appointments.dto;

import com.example.appointments.domain.AppUser;

public record UserSearchResponse(
        Long id,
        String fullName,
        String email,
        String phone,
        String username,
        String relationshipStatus
) {
    public static UserSearchResponse from(AppUser user, String relationshipStatus) {
        return new UserSearchResponse(
                user.getId(), user.getFullName(), user.getEmail(), user.getPhone(),
                user.getUsername(), relationshipStatus);
    }
}
