package com.example.appointments.repository;

import com.example.appointments.domain.CalendarNote;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

public interface CalendarNoteRepository extends JpaRepository<CalendarNote, Long> {
    List<CalendarNote> findAllByOwnerUsernameAndNoteDateBetweenOrderByNoteDateAsc(
            String username, LocalDate from, LocalDate to);

    Optional<CalendarNote> findByIdAndOwnerUsername(Long id, String username);
}

