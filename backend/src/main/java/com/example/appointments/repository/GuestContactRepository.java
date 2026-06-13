package com.example.appointments.repository;

import com.example.appointments.domain.GuestContact;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface GuestContactRepository extends JpaRepository<GuestContact, Long> {
    List<GuestContact> findByOwnerUsernameOrderByFullNameAsc(String username);
    Optional<GuestContact> findByIdAndOwnerUsername(Long id, String username);
}
