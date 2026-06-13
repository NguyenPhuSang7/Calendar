package com.example.appointments.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record GuestContactRequest(
        @NotBlank @Size(max = 120) String fullName,
        @Email @Size(max = 180) String email,
        @Size(max = 30) String phone
) {
}
