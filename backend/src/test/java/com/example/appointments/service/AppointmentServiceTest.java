package com.example.appointments.service;

import com.example.appointments.domain.AppUser;
import com.example.appointments.domain.AppointmentStatus;
import com.example.appointments.domain.InvitationStatus;
import com.example.appointments.domain.Friendship;
import com.example.appointments.domain.FriendshipStatus;
import com.example.appointments.dto.CreateAppointmentRequest;
import com.example.appointments.dto.GuestContactRequest;
import com.example.appointments.dto.UpdateAppointmentRequest;
import com.example.appointments.exception.BusinessException;
import com.example.appointments.repository.AppUserRepository;
import com.example.appointments.repository.FriendshipRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.ZoneId;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

@SpringBootTest
@Transactional
class AppointmentServiceTest {
    @Autowired
    private AppointmentService appointmentService;
    @Autowired
    private AppUserRepository userRepository;
    @Autowired
    private FriendshipRepository friendshipRepository;
    @Autowired
    private ContactService contactService;
    private AppUser user;
    private LocalDateTime startTime;

    @BeforeEach
    void setUp() {
        user = userRepository.save(new AppUser("Test User", "test-" + System.nanoTime() + "@example.com", "0900000000"));
        user.setCredentials("testuser" + System.nanoTime(), "unused");
        startTime = LocalDate.now().plusDays(1).atTime(9, 0);
    }

    @Test
    void createsCalendarEventWithExplicitEndTime() {
        var result = appointmentService.create(user.getUsername(), new CreateAppointmentRequest(
                "Họp dự án", user.getId(), startTime, startTime.plusHours(1), "Ghi chú"));

        assertThat(result.endTime()).isEqualTo(startTime.plusHours(1));
        assertThat(result.title()).isEqualTo("Họp dự án");
        assertThat(result.contactName()).isEqualTo("Test User");
        assertThat(result.status()).isEqualTo(AppointmentStatus.PENDING);
    }

    @Test
    void allowsEventWithoutContact() {
        var result = appointmentService.create(user.getUsername(), new CreateAppointmentRequest(
                "Việc cá nhân", null, startTime, startTime.plusMinutes(30), null));

        assertThat(result.contactId()).isNull();
    }

    @Test
    void allowsOverlappingCalendarEvents() {
        appointmentService.create(user.getUsername(), new CreateAppointmentRequest(
                "Sự kiện một", null, startTime, startTime.plusHours(1), null));

        var overlapping = appointmentService.create(user.getUsername(), new CreateAppointmentRequest(
                "Sự kiện hai", null, startTime.plusMinutes(30), startTime.plusHours(2), null));

        assertThat(overlapping.id()).isNotNull();
    }

    @Test
    void rejectsEndTimeBeforeStartTime() {
        assertThatThrownBy(() -> appointmentService.create(user.getUsername(), new CreateAppointmentRequest(
                "Sai thời gian", null, startTime, startTime.minusMinutes(1), null)))
                .isInstanceOf(BusinessException.class)
                .hasMessageContaining("kết thúc");
    }

    @Test
    void rejectsAppointmentInThePast() {
        LocalDateTime past = LocalDateTime.now(ZoneId.of("Asia/Ho_Chi_Minh")).minusMinutes(1);

        assertThatThrownBy(() -> appointmentService.create(user.getUsername(), new CreateAppointmentRequest(
                "Cuộc hẹn quá khứ", null, past, past.plusMinutes(30), null)))
                .isInstanceOf(BusinessException.class)
                .hasMessageContaining("quá khứ");
    }

    @Test
    void updatesAppointmentDateAndTime() {
        var created = appointmentService.create(user.getUsername(),
                new CreateAppointmentRequest("Họp", user.getId(), startTime, startTime.plusHours(1), null));
        var updatedTime = startTime.plusDays(1).plusHours(2);

        var updated = appointmentService.update(created.id(),
                new UpdateAppointmentRequest(
                        "Họp đã đổi", user.getId(), updatedTime, updatedTime.plusMinutes(45), "Đã đổi lịch"));

        assertThat(updated.startTime()).isEqualTo(updatedTime);
        assertThat(updated.title()).isEqualTo("Họp đã đổi");
        assertThat(updated.note()).isEqualTo("Đã đổi lịch");
    }

    @Test
    void deletesAppointment() {
        var created = appointmentService.create(user.getUsername(),
                new CreateAppointmentRequest("Họp", null, startTime, startTime.plusHours(1), null));

        appointmentService.delete(created.id());

        assertThat(appointmentService.getSchedule(user.getUsername(), startTime.toLocalDate(), null)).isEmpty();
    }

    @Test
    void contactCanAcceptInvitation() {
        AppUser organizer = new AppUser("Organizer", "organizer-" + System.nanoTime() + "@example.com", null);
        organizer.setCredentials("organizer" + System.nanoTime(), "unused");
        userRepository.save(organizer);
        Friendship friendship = new Friendship(organizer, user);
        friendship.respond(FriendshipStatus.ACCEPTED);
        friendshipRepository.save(friendship);
        var created = appointmentService.create(organizer.getUsername(),
                new CreateAppointmentRequest("Họp xác nhận", user.getId(), startTime, startTime.plusHours(1), null));

        assertThat(created.invitationStatus()).isEqualTo(InvitationStatus.PENDING);
        assertThat(appointmentService.getPendingInvitations(user.getUsername())).hasSize(1);

        var accepted = appointmentService.respondToInvitation(
                user.getUsername(), created.id(), InvitationStatus.ACCEPTED);

        assertThat(accepted.invitationStatus()).isEqualTo(InvitationStatus.ACCEPTED);
        assertThat(appointmentService.getPendingInvitations(user.getUsername())).isEmpty();
    }

    @Test
    void eventWithoutContactHasNoInvitationStatus() {
        var created = appointmentService.create(user.getUsername(),
                new CreateAppointmentRequest("Việc riêng", null, startTime, startTime.plusHours(1), null));

        assertThat(created.invitationStatus()).isNull();
    }

    @Test
    void guestAppointmentIsAutomaticallyAccepted() {
        var guest = contactService.createGuest(user.getUsername(),
                new GuestContactRequest("Guest Test", "guest@example.com", "0911111111"));

        var created = appointmentService.create(user.getUsername(),
                new CreateAppointmentRequest(
                        "Lịch với guest", null, guest.id(),
                        startTime, startTime.plusHours(1), null));

        assertThat(created.contactType()).isEqualTo("GUEST");
        assertThat(created.guestId()).isEqualTo(guest.id());
        assertThat(created.invitationStatus()).isEqualTo(InvitationStatus.ACCEPTED);
    }
}
