package com.example.appointments.domain;

import jakarta.persistence.*;

@Entity
@Table(name = "app_users", indexes = @Index(name = "idx_user_email", columnList = "email", unique = true))
public class AppUser {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 120)
    private String fullName;

    @Column(nullable = false, unique = true, length = 180)
    private String email;

    @Column(length = 30)
    private String phone;

    @Column(unique = true, length = 50)
    private String username;

    @Column(length = 100)
    private String passwordHash;

    protected AppUser() {
    }

    public AppUser(String fullName, String email, String phone) {
        this.fullName = fullName;
        this.email = email;
        this.phone = phone;
    }

    public void setCredentials(String username, String passwordHash) {
        this.username = username;
        this.passwordHash = passwordHash;
    }

    public Long getId() { return id; }
    public String getFullName() { return fullName; }
    public String getEmail() { return email; }
    public String getPhone() { return phone; }
    public String getUsername() { return username; }
    public String getPasswordHash() { return passwordHash; }
}
