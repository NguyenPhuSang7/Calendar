package com.example.appointments.controller;

import com.example.appointments.dto.CalendarNoteRequest;
import com.example.appointments.dto.CalendarNoteResponse;
import com.example.appointments.service.CalendarNoteService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;

@RestController
@RequestMapping("/api/notes")
@Tag(name = "Calendar Notes", description = "Ghi chú cá nhân trên lịch")
public class CalendarNoteController {
    private final CalendarNoteService noteService;

    public CalendarNoteController(CalendarNoteService noteService) {
        this.noteService = noteService;
    }

    @GetMapping
    @Operation(summary = "Lấy ghi chú cá nhân trong khoảng ngày")
    public List<CalendarNoteResponse> findRange(
            Authentication authentication,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate from,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate to) {
        return noteService.findRange(authentication.getName(), from, to);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public CalendarNoteResponse create(Authentication authentication,
                                       @Valid @RequestBody CalendarNoteRequest request) {
        return noteService.create(authentication.getName(), request);
    }

    @PutMapping("/{id}")
    public CalendarNoteResponse update(Authentication authentication, @PathVariable Long id,
                                       @Valid @RequestBody CalendarNoteRequest request) {
        return noteService.update(authentication.getName(), id, request);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(Authentication authentication, @PathVariable Long id) {
        noteService.delete(authentication.getName(), id);
    }
}
