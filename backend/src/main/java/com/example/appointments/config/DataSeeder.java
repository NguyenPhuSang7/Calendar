package com.example.appointments.config;

import com.example.appointments.domain.AppUser;
import com.example.appointments.repository.AppUserRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.List;

@Configuration
public class DataSeeder {
    @Bean
    CommandLineRunner seedData(AppUserRepository userRepository,
                               PasswordEncoder passwordEncoder) {
        return args -> {
            if (userRepository.count() == 0) {
                userRepository.saveAll(List.of(
                        account("Nguyễn Minh Anh", "minhanh@example.com", "0901234567",
                                "minhanh", "MinhAnh@123", passwordEncoder),
                        account("Trần Hoàng Nam", "hoangnam@example.com", "0912345678",
                                "hoangnam", "HoangNam@123", passwordEncoder),
                        account("Lê Thảo Vy", "thaovy@example.com", "0987654321",
                                "thaovy", "ThaoVy@123", passwordEncoder),
                        account("Phạm Gia Hân", "giahan@example.com", "0934567890",
                                "giahan", "GiaHan@123", passwordEncoder)
                ));
            } else {
                ensureCredentials(userRepository, "minhanh@example.com", "minhanh", "MinhAnh@123", passwordEncoder);
                ensureCredentials(userRepository, "hoangnam@example.com", "hoangnam", "HoangNam@123", passwordEncoder);
                ensureCredentials(userRepository, "thaovy@example.com", "thaovy", "ThaoVy@123", passwordEncoder);
                ensureCredentials(userRepository, "giahan@example.com", "giahan", "GiaHan@123", passwordEncoder);
            }
        };
    }

    private AppUser account(String fullName, String email, String phone, String username,
                            String password, PasswordEncoder passwordEncoder) {
        AppUser user = new AppUser(fullName, email, phone);
        user.setCredentials(username, passwordEncoder.encode(password));
        return user;
    }

    private void ensureCredentials(AppUserRepository userRepository, String email, String username,
                                   String password, PasswordEncoder passwordEncoder) {
        userRepository.findByEmail(email).ifPresent(user -> {
            if (user.getUsername() == null || user.getPasswordHash() == null) {
                user.setCredentials(username, passwordEncoder.encode(password));
                userRepository.save(user);
            }
        });
    }
}
