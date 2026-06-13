package com.example.appointments.dto;

import com.example.appointments.domain.AppUser;
import com.example.appointments.domain.GuestContact;

public record ContactResponse(
        Long id,
        String type,
        String fullName,
        String email,
        String phone,
        String username
) {
    public static ContactResponse user(AppUser user) {
        return new ContactResponse(
                user.getId(), "USER", user.getFullName(), user.getEmail(), user.getPhone(), user.getUsername());
    }

    public static ContactResponse guest(GuestContact guest) {
        return new ContactResponse(
                guest.getId(), "GUEST", guest.getFullName(), guest.getEmail(), guest.getPhone(), null);
    }
}
