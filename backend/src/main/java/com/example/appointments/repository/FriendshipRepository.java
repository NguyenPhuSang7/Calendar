package com.example.appointments.repository;

import com.example.appointments.domain.Friendship;
import com.example.appointments.domain.FriendshipStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface FriendshipRepository extends JpaRepository<Friendship, Long> {
    @Query("""
            select f from Friendship f
            where (f.requester.id = :first and f.recipient.id = :second)
               or (f.requester.id = :second and f.recipient.id = :first)
            """)
    Optional<Friendship> findBetween(@Param("first") Long first, @Param("second") Long second);

    @Query("""
            select f from Friendship f
            join fetch f.requester
            where f.recipient.username = :username and f.status = :status
            order by f.createdAt desc
            """)
    List<Friendship> findIncoming(@Param("username") String username,
                                  @Param("status") FriendshipStatus status);

    @Query("""
            select f from Friendship f
            join fetch f.requester
            join fetch f.recipient
            where (f.requester.username = :username or f.recipient.username = :username)
              and f.status = :status
            """)
    List<Friendship> findForUser(@Param("username") String username,
                                 @Param("status") FriendshipStatus status);
}
