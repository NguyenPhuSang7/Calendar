package com.example.appointments.service;

import com.example.appointments.domain.AppUser;
import com.example.appointments.dto.AuthResponse;
import com.example.appointments.dto.LoginRequest;
import com.example.appointments.dto.RegisterRequest;
import com.example.appointments.exception.BusinessException;
import com.example.appointments.exception.UnauthorizedException;
import com.example.appointments.repository.AppUserRepository;
import com.example.appointments.security.JwtService;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class AuthService {
    private final AppUserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    public AuthService(AppUserRepository userRepository, PasswordEncoder passwordEncoder, JwtService jwtService) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtService = jwtService;
    }

    @Transactional(readOnly = true)
    public AuthResponse login(LoginRequest request) {
        AppUser user = userRepository.findByUsername(request.username())
                .orElseThrow(() -> new UnauthorizedException("Username hoặc mật khẩu không đúng"));
        if (user.getPasswordHash() == null || !passwordEncoder.matches(request.password(), user.getPasswordHash())) {
            throw new UnauthorizedException("Username hoặc mật khẩu không đúng");
        }
        return responseFor(user);
    }

    @Transactional
    public AuthResponse register(RegisterRequest request) {
        return responseFor(createUserAccount(request));
    }

    private AppUser createUserAccount(RegisterRequest request) {
        if (userRepository.existsByUsername(request.username())) {
            throw new BusinessException("Username đã tồn tại");
        }
        if (userRepository.existsByEmail(request.email())) {
            throw new BusinessException("Email đã tồn tại");
        }

        AppUser user = new AppUser(request.fullName(), request.email(), request.phone());
        user.setCredentials(request.username(), passwordEncoder.encode(request.password()));
        return userRepository.save(user);
    }

    private AuthResponse responseFor(AppUser user) {
        return new AuthResponse(
                jwtService.generateToken(user),
                "Bearer",
                jwtService.getExpirationSeconds(),
                user.getId(),
                user.getUsername(),
                user.getFullName()
        );
    }
}
