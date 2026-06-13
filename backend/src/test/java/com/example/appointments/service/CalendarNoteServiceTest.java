package com.example.appointments.service;

import com.example.appointments.domain.AppUser;
import com.example.appointments.dto.CalendarNoteRequest;
import com.example.appointments.repository.AppUserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
@Transactional
class CalendarNoteServiceTest {
    @Autowired CalendarNoteService noteService;
    @Autowired AppUserRepository userRepository;
    @Autowired PasswordEncoder passwordEncoder;

    private String username;

    @BeforeEach
    void setUp() {
        username = "noteuser" + System.nanoTime();
        AppUser user = new AppUser("Note User", username + "@example.com", null);
        user.setCredentials(username, passwordEncoder.encode("NoteUser@123"));
        userRepository.save(user);
    }

    @Test
    void createsUpdatesAndDeletesOwnNote() {
        LocalDate date = LocalDate.now().plusDays(2);
        var created = noteService.create(username,
                new CalendarNoteRequest("Việc cần làm", "Gọi khách hàng", date, "yellow"));
        var updated = noteService.update(username, created.id(),
                new CalendarNoteRequest("Đã cập nhật", "Chuẩn bị hồ sơ", date, "blue"));

        assertThat(updated.title()).isEqualTo("Đã cập nhật");
        assertThat(noteService.findRange(username, date, date)).hasSize(1);

        noteService.delete(username, created.id());
        assertThat(noteService.findRange(username, date, date)).isEmpty();
    }
}
