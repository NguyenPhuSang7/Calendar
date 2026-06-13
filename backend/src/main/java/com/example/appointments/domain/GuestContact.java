package com.example.appointments.domain;

import jakarta.persistence.*;

@Entity
@Table(name = "guest_contacts")
public class GuestContact {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "owner_id", nullable = false)
    private AppUser owner;

    @Column(nullable = false, length = 120)
    private String fullName;

    @Column(length = 180)
    private String email;

    @Column(length = 30)
    private String phone;

    protected GuestContact() {
    }

    public GuestContact(AppUser owner, String fullName, String email, String phone) {
        this.owner = owner;
        this.fullName = fullName;
        this.email = email;
        this.phone = phone;
    }

    public Long getId() { return id; }
    public AppUser getOwner() { return owner; }
    public String getFullName() { return fullName; }
    public String getEmail() { return email; }
    public String getPhone() { return phone; }
}
