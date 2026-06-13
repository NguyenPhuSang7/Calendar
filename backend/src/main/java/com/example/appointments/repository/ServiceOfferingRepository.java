package com.example.appointments.repository;

import com.example.appointments.domain.ServiceOffering;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface ServiceOfferingRepository extends JpaRepository<ServiceOffering, Long> {
    List<ServiceOffering> findAllByActiveTrueOrderByNameAsc();
}

