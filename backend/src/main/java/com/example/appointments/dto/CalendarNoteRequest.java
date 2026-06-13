package com.example.appointments.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

import java.time.LocalDate;

public record CalendarNoteRequest(
        @NotBlank(message = "Tiêu đề không được để trống")
        @Size(max = 120, message = "Tiêu đề tối đa 120 ký tự")
        String title,

        @NotBlank(message = "Nội dung không được để trống")
        @Size(max = 1000, message = "Nội dung tối đa 1000 ký tự")
        String content,

        @NotNull(message = "Ngày ghi chú không được để trống")
        LocalDate noteDate,

        @NotBlank
        @Pattern(regexp = "^(yellow|blue|green|pink)$", message = "Màu ghi chú không hợp lệ")
        String color
) {
}

