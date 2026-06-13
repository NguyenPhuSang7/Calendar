package com.example.appointments.dto;

import com.example.appointments.domain.CalendarNote;

import java.time.LocalDate;

public record CalendarNoteResponse(
        Long id,
        String title,
        String content,
        LocalDate noteDate,
        String color
) {
    public static CalendarNoteResponse from(CalendarNote note) {
        return new CalendarNoteResponse(
                note.getId(), note.getTitle(), note.getContent(), note.getNoteDate(), note.getColor());
    }
}

