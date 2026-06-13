package com.example.appointments.service;

import com.example.appointments.domain.AppUser;
import com.example.appointments.domain.CalendarNote;
import com.example.appointments.dto.CalendarNoteRequest;
import com.example.appointments.dto.CalendarNoteResponse;
import com.example.appointments.exception.NotFoundException;
import com.example.appointments.repository.AppUserRepository;
import com.example.appointments.repository.CalendarNoteRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;

@Service
@Transactional(readOnly = true)
public class CalendarNoteService {
    private final CalendarNoteRepository noteRepository;
    private final AppUserRepository userRepository;

    public CalendarNoteService(CalendarNoteRepository noteRepository, AppUserRepository userRepository) {
        this.noteRepository = noteRepository;
        this.userRepository = userRepository;
    }

    public List<CalendarNoteResponse> findRange(String username, LocalDate from, LocalDate to) {
        return noteRepository.findAllByOwnerUsernameAndNoteDateBetweenOrderByNoteDateAsc(username, from, to)
                .stream().map(CalendarNoteResponse::from).toList();
    }

    @Transactional
    public CalendarNoteResponse create(String username, CalendarNoteRequest request) {
        AppUser owner = userRepository.findByUsername(username)
                .orElseThrow(() -> new NotFoundException("Không tìm thấy người dùng"));
        CalendarNote note = new CalendarNote(
                owner, request.title(), request.content(), request.noteDate(), request.color());
        return CalendarNoteResponse.from(noteRepository.save(note));
    }

    @Transactional
    public CalendarNoteResponse update(String username, Long id, CalendarNoteRequest request) {
        CalendarNote note = ownedNote(username, id);
        note.update(request.title(), request.content(), request.noteDate(), request.color());
        return CalendarNoteResponse.from(note);
    }

    @Transactional
    public void delete(String username, Long id) {
        noteRepository.delete(ownedNote(username, id));
    }

    private CalendarNote ownedNote(String username, Long id) {
        return noteRepository.findByIdAndOwnerUsername(id, username)
                .orElseThrow(() -> new NotFoundException("Không tìm thấy ghi chú"));
    }
}

