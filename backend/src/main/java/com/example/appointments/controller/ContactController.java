package com.example.appointments.controller;

import com.example.appointments.dto.*;
import com.example.appointments.service.ContactService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api")
public class ContactController {
    private final ContactService contactService;

    public ContactController(ContactService contactService) {
        this.contactService = contactService;
    }

    @GetMapping("/contacts")
    public List<ContactResponse> contacts(Authentication authentication) {
        return contactService.contacts(authentication.getName());
    }

    @PostMapping("/guests")
    @ResponseStatus(HttpStatus.CREATED)
    public ContactResponse createGuest(Authentication authentication,
                                       @Valid @RequestBody GuestContactRequest request) {
        return contactService.createGuest(authentication.getName(), request);
    }

    @GetMapping("/users/search")
    public List<UserSearchResponse> searchUsers(Authentication authentication,
                                                @RequestParam String q) {
        return contactService.searchUsers(authentication.getName(), q);
    }

    @GetMapping("/friend-requests")
    public List<FriendRequestResponse> friendRequests(Authentication authentication) {
        return contactService.incomingRequests(authentication.getName());
    }

    @PostMapping("/friend-requests/{recipientId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void sendFriendRequest(Authentication authentication, @PathVariable Long recipientId) {
        contactService.sendFriendRequest(authentication.getName(), recipientId);
    }

    @PatchMapping("/friend-requests/{requestId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void respondToFriendRequest(Authentication authentication,
                                       @PathVariable Long requestId,
                                       @Valid @RequestBody FriendRequestAction action) {
        contactService.respondToFriendRequest(authentication.getName(), requestId, action.response());
    }
}
