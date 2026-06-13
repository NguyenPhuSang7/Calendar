package com.example.appointments.domain;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "friendships", uniqueConstraints = {
        @UniqueConstraint(name = "uk_friendship_pair", columnNames = {"requester_id", "recipient_id"})
})
public class Friendship {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "requester_id", nullable = false)
    private AppUser requester;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "recipient_id", nullable = false)
    private AppUser recipient;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private FriendshipStatus status = FriendshipStatus.PENDING;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    protected Friendship() {
    }

    public Friendship(AppUser requester, AppUser recipient) {
        this.requester = requester;
        this.recipient = recipient;
    }

    @PrePersist
    void prePersist() {
        createdAt = LocalDateTime.now();
    }

    public void respond(FriendshipStatus status) {
        this.status = status;
    }

    public Long getId() { return id; }
    public AppUser getRequester() { return requester; }
    public AppUser getRecipient() { return recipient; }
    public FriendshipStatus getStatus() { return status; }
}
