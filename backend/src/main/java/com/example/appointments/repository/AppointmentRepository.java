package com.example.appointments.repository;

import com.example.appointments.domain.Appointment;
import com.example.appointments.domain.AppointmentStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDateTime;
import java.util.Collection;
import java.util.List;

public interface AppointmentRepository extends JpaRepository<Appointment, Long> {
    @Query("""
            select a from Appointment a
            left join fetch a.contact
            left join fetch a.organizer
            left join fetch a.guest
            left join fetch a.service
            where a.startTime >= :from and a.startTime < :to
              and (a.organizer.username = :username or a.contact.username = :username)
              and (:status is null or a.status = :status)
            order by a.startTime asc
            """)
    List<Appointment> findSchedule(
            @Param("from") LocalDateTime from,
            @Param("to") LocalDateTime to,
            @Param("username") String username,
            @Param("status") AppointmentStatus status
    );

    @Query("""
            select count(a) > 0 from Appointment a
            where a.status not in :ignoredStatuses
              and a.startTime < :endTime
              and a.endTime > :startTime
            """)
    boolean existsOverlapping(
            @Param("startTime") LocalDateTime startTime,
            @Param("endTime") LocalDateTime endTime,
            @Param("ignoredStatuses") Collection<AppointmentStatus> ignoredStatuses
    );

    @Query("""
            select count(a) > 0 from Appointment a
            where a.id <> :appointmentId
              and a.status not in :ignoredStatuses
              and a.startTime < :endTime
              and a.endTime > :startTime
            """)
    boolean existsOverlappingExcluding(
            @Param("appointmentId") Long appointmentId,
            @Param("startTime") LocalDateTime startTime,
            @Param("endTime") LocalDateTime endTime,
            @Param("ignoredStatuses") Collection<AppointmentStatus> ignoredStatuses
    );

    @Query("""
            select a from Appointment a
            left join fetch a.contact
            left join fetch a.organizer
            left join fetch a.guest
            left join fetch a.service
            where a.contact.username = :username
              and a.invitationStatus = com.example.appointments.domain.InvitationStatus.PENDING
              and a.startTime >= :now
            order by a.startTime asc
            """)
    List<Appointment> findPendingInvitations(
            @Param("username") String username,
            @Param("now") LocalDateTime now
    );
}
