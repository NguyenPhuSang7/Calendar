package com.example.appointments.service;

import com.example.appointments.domain.*;
import com.example.appointments.dto.*;
import com.example.appointments.exception.BusinessException;
import com.example.appointments.exception.NotFoundException;
import com.example.appointments.repository.AppUserRepository;
import com.example.appointments.repository.FriendshipRepository;
import com.example.appointments.repository.GuestContactRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

@Service
@Transactional(readOnly = true)
public class ContactService {
    private final AppUserRepository userRepository;
    private final GuestContactRepository guestRepository;
    private final FriendshipRepository friendshipRepository;

    public ContactService(AppUserRepository userRepository,
                          GuestContactRepository guestRepository,
                          FriendshipRepository friendshipRepository) {
        this.userRepository = userRepository;
        this.guestRepository = guestRepository;
        this.friendshipRepository = friendshipRepository;
    }

    public List<ContactResponse> contacts(String username) {
        List<ContactResponse> contacts = new ArrayList<>();
        friendshipRepository.findForUser(username, FriendshipStatus.ACCEPTED).stream()
                .map(friendship -> username.equals(friendship.getRequester().getUsername())
                        ? friendship.getRecipient() : friendship.getRequester())
                .map(ContactResponse::user)
                .forEach(contacts::add);
        guestRepository.findByOwnerUsernameOrderByFullNameAsc(username).stream()
                .map(ContactResponse::guest)
                .forEach(contacts::add);
        return contacts.stream()
                .sorted((left, right) -> left.fullName().compareToIgnoreCase(right.fullName()))
                .toList();
    }

    public List<UserSearchResponse> searchUsers(String username, String query) {
        if (query == null || query.trim().length() < 2) {
            return List.of();
        }
        AppUser current = requireUser(username);
        String normalized = query.trim().toLowerCase(Locale.ROOT);
        return userRepository.findAll().stream()
                .filter(user -> !user.getId().equals(current.getId()))
                .filter(user -> contains(user.getFullName(), normalized)
                        || contains(user.getEmail(), normalized)
                        || contains(user.getPhone(), normalized))
                .limit(20)
                .map(user -> UserSearchResponse.from(user, relationshipStatus(current, user)))
                .toList();
    }

    public List<FriendRequestResponse> incomingRequests(String username) {
        return friendshipRepository.findIncoming(username, FriendshipStatus.PENDING).stream()
                .map(FriendRequestResponse::from)
                .toList();
    }

    @Transactional
    public ContactResponse createGuest(String username, GuestContactRequest request) {
        AppUser owner = requireUser(username);
        GuestContact guest = new GuestContact(
                owner, request.fullName().trim(), trimToNull(request.email()), trimToNull(request.phone()));
        return ContactResponse.guest(guestRepository.save(guest));
    }

    @Transactional
    public void sendFriendRequest(String username, Long recipientId) {
        AppUser requester = requireUser(username);
        AppUser recipient = userRepository.findById(recipientId)
                .orElseThrow(() -> new NotFoundException("Không tìm thấy người dùng"));
        if (requester.getId().equals(recipient.getId())) {
            throw new BusinessException("Không thể gửi lời mời kết bạn cho chính mình");
        }
        var existing = friendshipRepository.findBetween(requester.getId(), recipient.getId());
        if (existing.isPresent()) {
            Friendship friendship = existing.get();
            if (friendship.getStatus() == FriendshipStatus.ACCEPTED) {
                throw new BusinessException("Hai người đã là bạn bè");
            }
            if (friendship.getStatus() == FriendshipStatus.PENDING) {
                throw new BusinessException("Lời mời kết bạn đang chờ phản hồi");
            }
            friendshipRepository.delete(friendship);
        }
        friendshipRepository.save(new Friendship(requester, recipient));
    }

    @Transactional
    public void respondToFriendRequest(String username, Long requestId, FriendshipStatus response) {
        if (response != FriendshipStatus.ACCEPTED && response != FriendshipStatus.DECLINED) {
            throw new BusinessException("Phản hồi lời mời kết bạn không hợp lệ");
        }
        Friendship friendship = friendshipRepository.findById(requestId)
                .orElseThrow(() -> new NotFoundException("Không tìm thấy lời mời kết bạn"));
        if (!username.equals(friendship.getRecipient().getUsername())) {
            throw new BusinessException("Chỉ người nhận mới có thể phản hồi lời mời");
        }
        if (friendship.getStatus() != FriendshipStatus.PENDING) {
            throw new BusinessException("Lời mời kết bạn đã được phản hồi");
        }
        friendship.respond(response);
    }

    private String relationshipStatus(AppUser current, AppUser other) {
        return friendshipRepository.findBetween(current.getId(), other.getId())
                .map(friendship -> {
                    if (friendship.getStatus() == FriendshipStatus.ACCEPTED) return "FRIEND";
                    if (friendship.getStatus() == FriendshipStatus.PENDING) {
                        return current.getId().equals(friendship.getRequester().getId())
                                ? "REQUEST_SENT" : "REQUEST_RECEIVED";
                    }
                    return "NONE";
                })
                .orElse("NONE");
    }

    private AppUser requireUser(String username) {
        return userRepository.findByUsername(username)
                .orElseThrow(() -> new NotFoundException("Không tìm thấy người dùng"));
    }

    private boolean contains(String value, String query) {
        return value != null && value.toLowerCase(Locale.ROOT).contains(query);
    }

    private String trimToNull(String value) {
        return value == null || value.isBlank() ? null : value.trim();
    }
}
