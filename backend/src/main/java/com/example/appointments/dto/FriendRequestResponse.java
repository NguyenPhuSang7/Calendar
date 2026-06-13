package com.example.appointments.dto;

import com.example.appointments.domain.Friendship;

public record FriendRequestResponse(
        Long id,
        Long requesterId,
        String requesterName,
        String requesterUsername
) {
    public static FriendRequestResponse from(Friendship friendship) {
        return new FriendRequestResponse(
                friendship.getId(),
                friendship.getRequester().getId(),
                friendship.getRequester().getFullName(),
                friendship.getRequester().getUsername()
        );
    }
}
