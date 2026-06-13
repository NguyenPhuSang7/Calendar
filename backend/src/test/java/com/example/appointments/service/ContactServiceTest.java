package com.example.appointments.service;

import com.example.appointments.domain.AppUser;
import com.example.appointments.domain.FriendshipStatus;
import com.example.appointments.dto.GuestContactRequest;
import com.example.appointments.repository.AppUserRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
@Transactional
class ContactServiceTest {
    @Autowired ContactService contactService;
    @Autowired AppUserRepository userRepository;

    @Test
    void friendAppearsOnlyAfterRequestIsAccepted() {
        AppUser first = user("First User");
        AppUser second = user("Second User");

        contactService.sendFriendRequest(first.getUsername(), second.getId());
        assertThat(contactService.contacts(first.getUsername())).isEmpty();

        var request = contactService.incomingRequests(second.getUsername()).get(0);
        contactService.respondToFriendRequest(
                second.getUsername(), request.id(), FriendshipStatus.ACCEPTED);

        assertThat(contactService.contacts(first.getUsername()))
                .extracting("username")
                .containsExactly(second.getUsername());
        assertThat(contactService.contacts(second.getUsername()))
                .extracting("username")
                .containsExactly(first.getUsername());
    }

    @Test
    void guestIsVisibleOnlyToItsOwner() {
        AppUser owner = user("Guest Owner");
        AppUser other = user("Other User");

        contactService.createGuest(owner.getUsername(),
                new GuestContactRequest("Private Guest", null, "0900000000"));

        assertThat(contactService.contacts(owner.getUsername()))
                .extracting("type")
                .containsExactly("GUEST");
        assertThat(contactService.contacts(other.getUsername())).isEmpty();
    }

    private AppUser user(String name) {
        String suffix = Long.toString(System.nanoTime());
        AppUser user = new AppUser(name, suffix + "@example.com", null);
        user.setCredentials("user" + suffix, "unused");
        return userRepository.save(user);
    }
}
