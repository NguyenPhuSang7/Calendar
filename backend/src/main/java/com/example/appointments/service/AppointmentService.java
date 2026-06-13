package com.example.appointments.service;

import com.example.appointments.domain.*;
import com.example.appointments.dto.AppointmentResponse;
import com.example.appointments.dto.CreateAppointmentRequest;
import com.example.appointments.dto.UpdateAppointmentRequest;
import com.example.appointments.exception.BusinessException;
import com.example.appointments.exception.NotFoundException;
import com.example.appointments.repository.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.List;

@Service
@Transactional(readOnly = true)
public class AppointmentService {
    private static final ZoneId BUSINESS_ZONE = ZoneId.of("Asia/Ho_Chi_Minh");

    private final AppointmentRepository appointmentRepository;
    private final AppUserRepository userRepository;
    private final GuestContactRepository guestRepository;
    private final FriendshipRepository friendshipRepository;

    public AppointmentService(AppointmentRepository appointmentRepository,
                              AppUserRepository userRepository,
                              GuestContactRepository guestRepository,
                              FriendshipRepository friendshipRepository) {
        this.appointmentRepository = appointmentRepository;
        this.userRepository = userRepository;
        this.guestRepository = guestRepository;
        this.friendshipRepository = friendshipRepository;
    }

    public List<AppointmentResponse> getSchedule(String username, LocalDate date, AppointmentStatus status) {
        LocalDate targetDate = date == null ? LocalDate.now() : date;
        return appointmentRepository
                .findSchedule(targetDate.atStartOfDay(), targetDate.plusDays(1).atStartOfDay(), username, status)
                .stream().map(AppointmentResponse::from).toList();
    }

    public List<AppointmentResponse> getRange(String username, LocalDate from, LocalDate to, AppointmentStatus status) {
        if (from == null || to == null || to.isBefore(from)) {
            throw new BusinessException("Khoảng ngày không hợp lệ");
        }
        return appointmentRepository
                .findSchedule(from.atStartOfDay(), to.plusDays(1).atStartOfDay(), username, status)
                .stream().map(AppointmentResponse::from).toList();
    }

    public List<AppointmentResponse> getPendingInvitations(String username) {
        return appointmentRepository.findPendingInvitations(username, LocalDateTime.now(BUSINESS_ZONE))
                .stream().map(AppointmentResponse::from).toList();
    }

    @Transactional
    public synchronized AppointmentResponse create(String organizerUsername, CreateAppointmentRequest request) {
        AppUser organizer = requireUser(organizerUsername);
        AppUser contact = findContact(organizer, request.contactId());
        GuestContact guest = findGuest(organizerUsername, request.guestId());
        validateSingleContact(contact, guest);
        validateTimeRange(request.startTime(), request.endTime());
        Appointment appointment = new Appointment(
                request.title(), organizer, contact, guest,
                request.startTime(), request.endTime(), request.note());
        return AppointmentResponse.from(appointmentRepository.save(appointment));
    }

    @Transactional
    public AppointmentResponse updateStatus(Long id, AppointmentStatus nextStatus) {
        Appointment appointment = requireAppointment(id);
        validateStatusTransition(appointment.getStatus(), nextStatus);
        appointment.updateStatus(nextStatus);
        return AppointmentResponse.from(appointment);
    }

    @Transactional
    public synchronized AppointmentResponse update(Long id, UpdateAppointmentRequest request) {
        Appointment appointment = requireAppointment(id);
        AppUser organizer = appointment.getOrganizer();
        AppUser contact = findContact(organizer, request.contactId());
        GuestContact guest = findGuest(organizer.getUsername(), request.guestId());
        validateSingleContact(contact, guest);
        validateTimeRange(request.startTime(), request.endTime());
        appointment.update(
                request.title(), contact, guest,
                request.startTime(), request.endTime(), request.note());
        return AppointmentResponse.from(appointment);
    }

    @Transactional
    public void delete(Long id) {
        appointmentRepository.delete(requireAppointment(id));
    }

    @Transactional
    public AppointmentResponse respondToInvitation(String username, Long id, InvitationStatus response) {
        if (response != InvitationStatus.ACCEPTED && response != InvitationStatus.DECLINED) {
            throw new BusinessException("Phản hồi lời mời không hợp lệ");
        }
        Appointment appointment = requireAppointment(id);
        if (appointment.getContact() == null
                || !username.equals(appointment.getContact().getUsername())) {
            throw new BusinessException("Chỉ người được mời mới có thể phản hồi");
        }
        if (appointment.getInvitationStatus() != InvitationStatus.PENDING) {
            throw new BusinessException("Lời mời này đã được phản hồi");
        }
        appointment.respondToInvitation(response);
        return AppointmentResponse.from(appointment);
    }

    private AppUser findContact(AppUser organizer, Long contactId) {
        if (contactId == null) {
            return null;
        }
        AppUser contact = userRepository.findById(contactId)
                .orElseThrow(() -> new NotFoundException("Không tìm thấy người liên hệ"));
        if (!contact.getId().equals(organizer.getId())) {
            boolean acceptedFriend = friendshipRepository.findBetween(organizer.getId(), contact.getId())
                    .filter(friendship -> friendship.getStatus() == FriendshipStatus.ACCEPTED)
                    .isPresent();
            if (!acceptedFriend) {
                throw new BusinessException("Chỉ có thể tạo lịch với người đã kết bạn");
            }
        }
        return contact;
    }

    private GuestContact findGuest(String organizerUsername, Long guestId) {
        if (guestId == null) {
            return null;
        }
        return guestRepository.findByIdAndOwnerUsername(guestId, organizerUsername)
                .orElseThrow(() -> new NotFoundException("Không tìm thấy guest trong danh bạ của bạn"));
    }

    private void validateSingleContact(AppUser contact, GuestContact guest) {
        if (contact != null && guest != null) {
            throw new BusinessException("Chỉ được chọn một người liên hệ hoặc một guest");
        }
    }

    private AppUser requireUser(String username) {
        return userRepository.findByUsername(username)
                .orElseThrow(() -> new NotFoundException("Không tìm thấy người tạo cuộc hẹn"));
    }

    private Appointment requireAppointment(Long id) {
        return appointmentRepository.findById(id)
                .orElseThrow(() -> new NotFoundException("Không tìm thấy lịch hẹn"));
    }

    private void validateTimeRange(LocalDateTime startTime, LocalDateTime endTime) {
        if (startTime.isBefore(LocalDateTime.now(BUSINESS_ZONE))) {
            throw new BusinessException("Không thể tạo hoặc chuyển cuộc hẹn vào thời gian trong quá khứ");
        }
        if (!endTime.isAfter(startTime)) {
            throw new BusinessException("Giờ kết thúc phải sau giờ bắt đầu");
        }
    }

    private void validateStatusTransition(AppointmentStatus current, AppointmentStatus next) {
        if (current == next) return;
        boolean allowed = switch (current) {
            case PENDING -> next == AppointmentStatus.CONFIRMED || next == AppointmentStatus.CANCELLED;
            case CONFIRMED -> next == AppointmentStatus.COMPLETED || next == AppointmentStatus.CANCELLED;
            case COMPLETED, CANCELLED -> false;
        };
        if (!allowed) {
            throw new BusinessException("Không thể chuyển trạng thái từ " + current + " sang " + next);
        }
    }
}
