package com.example.appointments.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

public record RegisterRequest(
        @NotBlank(message = "Họ tên không được để trống")
        @Size(max = 120, message = "Họ tên tối đa 120 ký tự")
        String fullName,

        @NotBlank(message = "Email không được để trống")
        @Email(message = "Email không hợp lệ")
        String email,

        @Size(max = 30, message = "Số điện thoại tối đa 30 ký tự")
        String phone,

        @NotBlank(message = "Username không được để trống")
        @Pattern(regexp = "^[A-Za-z0-9]+$",
                message = "Username chỉ được chứa chữ và số, không có khoảng trắng hoặc ký tự đặc biệt")
        @Size(min = 4, max = 50, message = "Username phải từ 4 đến 50 ký tự")
        String username,

        @NotBlank(message = "Mật khẩu không được để trống")
        @Size(min = 8, max = 72, message = "Mật khẩu phải có ít nhất 8 ký tự")
        @Pattern(regexp = "^(?=.*[A-Z])(?=.*[^A-Za-z0-9\\s]).{8,}$",
                message = "Mật khẩu phải có ít nhất 1 chữ hoa và 1 ký tự đặc biệt")
        String password
) {
}

