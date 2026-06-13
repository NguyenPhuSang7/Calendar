package com.example.appointments.domain;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "appointments", indexes = {
        @Index(name = "idx_appointment_start_time", columnList = "startTime"),
        @Index(name = "idx_appointment_contact", columnList = "user_id")
})
public class Appointment {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private AppUser contact;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "organizer_id")
    private AppUser organizer;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "guest_id")
    private GuestContact guest;

    // Kept only so existing database rows remain readable after removing services.
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "service_id", insertable = false, updatable = false)
    private ServiceOffering service;

    @Column(length = 160)
    private String title;

    @Column(nullable = false)
    private LocalDateTime startTime;

    @Column(nullable = false)
    private LocalDateTime endTime;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private AppointmentStatus status = AppointmentStatus.PENDING;

    @Enumerated(EnumType.STRING)
    @Column(length = 20)
    private InvitationStatus invitationStatus;

    @Column(length = 500)
    private String note;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    protected Appointment() {
    }

    public Appointment(String title, AppUser organizer, AppUser contact, GuestContact guest, LocalDateTime startTime,
                       LocalDateTime endTime, String note) {
        this.title = title;
        this.organizer = organizer;
        this.contact = contact;
        this.guest = guest;
        this.startTime = startTime;
        this.endTime = endTime;
        this.note = note;
        refreshInvitationStatus(null);
    }

    @PrePersist
    void prePersist() {
        createdAt = LocalDateTime.now();
    }

    public void updateStatus(AppointmentStatus status) {
        this.status = status;
    }

    public void update(String title, AppUser contact, GuestContact guest, LocalDateTime startTime,
                       LocalDateTime endTime, String note) {
        Long previousContactId = this.contact == null ? null : this.contact.getId();
        this.title = title;
        this.contact = contact;
        this.guest = guest;
        this.startTime = startTime;
        this.endTime = endTime;
        this.note = note;
        refreshInvitationStatus(previousContactId);
    }

    public void respondToInvitation(InvitationStatus response) {
        this.invitationStatus = response;
    }

    private void refreshInvitationStatus(Long previousContactId) {
        if (guest != null) {
            invitationStatus = InvitationStatus.ACCEPTED;
            return;
        }
        Long contactId = contact == null ? null : contact.getId();
        Long organizerId = organizer == null ? null : organizer.getId();
        if (contactId == null || contactId.equals(organizerId)) {
            invitationStatus = null;
        } else if (!contactId.equals(previousContactId)) {
            invitationStatus = InvitationStatus.PENDING;
        }
    }

    public Long getId() { return id; }
    public String getTitle() {
        if (title != null && !title.isBlank()) {
            return title;
        }
        return service != null ? service.getName() : "Cuộc hẹn";
    }
    public AppUser getContact() { return contact; }
    public AppUser getOrganizer() { return organizer; }
    public GuestContact getGuest() { return guest; }
    public ServiceOffering getService() { return service; }
    public LocalDateTime getStartTime() { return startTime; }
    public LocalDateTime getEndTime() { return endTime; }
    public AppointmentStatus getStatus() { return status; }
    public InvitationStatus getInvitationStatus() { return invitationStatus; }
    public String getNote() { return note; }
    public LocalDateTime getCreatedAt() { return createdAt; }
}
