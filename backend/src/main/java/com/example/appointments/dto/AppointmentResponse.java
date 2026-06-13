package com.example.appointments.dto;

import com.example.appointments.domain.Appointment;
import com.example.appointments.domain.AppointmentStatus;
import com.example.appointments.domain.InvitationStatus;
import java.time.LocalDateTime;

public record AppointmentResponse(
        Long id,
        String title,
        Long organizerId,
        String organizerName,
        Long contactId,
        Long guestId,
        String contactType,
        String contactName,
        String contactPhone,
        LocalDateTime startTime,
        LocalDateTime endTime,
        AppointmentStatus status,
        InvitationStatus invitationStatus,
        String note
) {
    public static AppointmentResponse from(Appointment appointment) {
        return new AppointmentResponse(
                appointment.getId(),
                appointment.getTitle(),
                appointment.getOrganizer() == null ? null : appointment.getOrganizer().getId(),
                appointment.getOrganizer() == null ? null : appointment.getOrganizer().getFullName(),
                appointment.getContact() == null ? null : appointment.getContact().getId(),
                appointment.getGuest() == null ? null : appointment.getGuest().getId(),
                appointment.getGuest() != null ? "GUEST" : appointment.getContact() != null ? "USER" : null,
                appointment.getGuest() != null ? appointment.getGuest().getFullName()
                        : appointment.getContact() == null ? null : appointment.getContact().getFullName(),
                appointment.getGuest() != null ? appointment.getGuest().getPhone()
                        : appointment.getContact() == null ? null : appointment.getContact().getPhone(),
                appointment.getStartTime(),
                appointment.getEndTime(),
                appointment.getStatus(),
                appointment.getInvitationStatus(),
                appointment.getNote()
        );
    }
}
