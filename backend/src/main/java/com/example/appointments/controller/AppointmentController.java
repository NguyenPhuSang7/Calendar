package com.example.appointments.controller;

import com.example.appointments.domain.AppointmentStatus;
import com.example.appointments.dto.AppointmentResponse;
import com.example.appointments.dto.CreateAppointmentRequest;
import com.example.appointments.dto.UpdateAppointmentStatusRequest;
import com.example.appointments.dto.UpdateAppointmentRequest;
import com.example.appointments.dto.InvitationResponseRequest;
import com.example.appointments.service.AppointmentService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;

@RestController
@RequestMapping("/api/appointments")
@Tag(name = "Appointments", description = "Quản lý lịch hẹn")
public class AppointmentController {
    private final AppointmentService appointmentService;

    public AppointmentController(AppointmentService appointmentService) {
        this.appointmentService = appointmentService;
    }

    @GetMapping
    @Operation(summary = "Lấy lịch hẹn theo ngày và trạng thái")
    public List<AppointmentResponse> getSchedule(
            Authentication authentication,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate date,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate from,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate to,
            @RequestParam(required = false) AppointmentStatus status) {
        if (from != null || to != null) {
            return appointmentService.getRange(authentication.getName(), from, to, status);
        }
        return appointmentService.getSchedule(authentication.getName(), date, status);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    @Operation(summary = "Tạo lịch hẹn mới")
    public AppointmentResponse create(Authentication authentication,
                                      @Valid @RequestBody CreateAppointmentRequest request) {
        return appointmentService.create(authentication.getName(), request);
    }

    @GetMapping("/invitations")
    @Operation(summary = "Lấy lời mời đang chờ người dùng hiện tại xác nhận")
    public List<AppointmentResponse> invitations(Authentication authentication) {
        return appointmentService.getPendingInvitations(authentication.getName());
    }

    @PatchMapping("/{id}/invitation")
    @Operation(summary = "Chấp nhận hoặc từ chối lời mời")
    public AppointmentResponse respondToInvitation(
            Authentication authentication,
            @PathVariable Long id,
            @Valid @RequestBody InvitationResponseRequest request) {
        return appointmentService.respondToInvitation(authentication.getName(), id, request.response());
    }

    @PatchMapping("/{id}/status")
    @Operation(summary = "Cập nhật trạng thái lịch hẹn")
    public AppointmentResponse updateStatus(
            @PathVariable Long id,
            @Valid @RequestBody UpdateAppointmentStatusRequest request) {
        return appointmentService.updateStatus(id, request.status());
    }

    @PutMapping("/{id}")
    @Operation(summary = "Chỉnh sửa lịch hẹn")
    public AppointmentResponse update(@PathVariable Long id,
                                      @Valid @RequestBody UpdateAppointmentRequest request) {
        return appointmentService.update(id, request);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    @Operation(summary = "Xóa lịch hẹn")
    public void delete(@PathVariable Long id) {
        appointmentService.delete(id);
    }
}
