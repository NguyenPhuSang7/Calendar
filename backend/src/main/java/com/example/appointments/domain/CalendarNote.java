package com.example.appointments.domain;

import jakarta.persistence.*;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = "calendar_notes", indexes = {
        @Index(name = "idx_calendar_note_date", columnList = "noteDate"),
        @Index(name = "idx_calendar_note_owner", columnList = "owner_id")
})
public class CalendarNote {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "owner_id", nullable = false)
    private AppUser owner;

    @Column(nullable = false, length = 120)
    private String title;

    @Column(nullable = false, length = 1000)
    private String content;

    @Column(nullable = false)
    private LocalDate noteDate;

    @Column(nullable = false, length = 20)
    private String color;

    @Column(nullable = false)
    private LocalDateTime createdAt;

    protected CalendarNote() {
    }

    public CalendarNote(AppUser owner, String title, String content, LocalDate noteDate, String color) {
        this.owner = owner;
        this.title = title;
        this.content = content;
        this.noteDate = noteDate;
        this.color = color;
    }

    @PrePersist
    void prePersist() {
        createdAt = LocalDateTime.now();
    }

    public void update(String title, String content, LocalDate noteDate, String color) {
        this.title = title;
        this.content = content;
        this.noteDate = noteDate;
        this.color = color;
    }

    public Long getId() { return id; }
    public AppUser getOwner() { return owner; }
    public String getTitle() { return title; }
    public String getContent() { return content; }
    public LocalDate getNoteDate() { return noteDate; }
    public String getColor() { return color; }
}

