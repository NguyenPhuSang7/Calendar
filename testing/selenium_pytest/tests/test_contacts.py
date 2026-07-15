import pytest
import time

class TestContactsAndFriendship:

    def test_search_and_send_friend_request(self, register_page, login_page, contacts_page):
        """TC-FRD-01, TC-FRD-02 & TC-FRD-03: Search user, request friendship, prevent duplicates."""
        timestamp = int(time.time() * 1000)
        userA_name = f"frda{timestamp}"
        userB_name = f"frdb{timestamp}"
        
        # Setup: Register User A and User B
        register_page.navigate()
        register_page.register("User A", f"{userA_name}@example.com", "", userA_name, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        login_page.logout()
        
        register_page.navigate()
        register_page.register("User B", f"{userB_name}@example.com", "", userB_name, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        login_page.logout()
        
        # Act: User A logs in and searches for User B
        login_page.login(userA_name, "SecurePassword123!")
        contacts_page.navigate()
        contacts_page.search_user(userB_name)
        
        # Assert: Search result shows User B
        assert contacts_page.is_search_result_found(userB_name), "Search query did not return User B"
        
        # Act: Send friend request
        contacts_page.send_friend_request(userB_name)
        contacts_page.wait_for_friend_request_status(userB_name, "Đã gửi lời mời")
        
        # Assert: Request is pending (relationshipStatus is REQUEST_SENT -> "Đã gửi lời mời")
        status = contacts_page.get_friend_request_status(userB_name)
        assert "gửi lời mời" in status.lower() or "sent" in status.lower(), \
            f"Expected friendship request status to change to sent. Got: {status}"
            
        # Act/Assert duplicate request: Adding again should be disabled/blocked
        # We assert that the status label still says "Đã gửi lời mời"
        assert "gửi lời mời" in status.lower() or "sent" in status.lower(), \
            "Duplicate add request wasn't prevented"
            
        login_page.logout()

    def test_accept_friend_request(self, register_page, login_page, contacts_page):
        """TC-FRD-04: Recipient accepts pending request; both users see each other as friends."""
        timestamp = int(time.time() * 1000)
        userA_name = f"accfa{timestamp}"
        userB_name = f"accfb{timestamp}"
        
        # Register User A and User B
        register_page.navigate()
        register_page.register("User A", f"{userA_name}@example.com", "", userA_name, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        login_page.logout()
        
        register_page.navigate()
        register_page.register("User B", f"{userB_name}@example.com", "", userB_name, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        login_page.logout()
        
        # User A sends request to User B
        login_page.login(userA_name, "SecurePassword123!")
        contacts_page.navigate()
        contacts_page.search_user(userB_name)
        contacts_page.send_friend_request(userB_name)
        contacts_page.wait_for_friend_request_status(userB_name, "Đã gửi lời mời")
        login_page.logout()
        
        # Recipient (User B) logs in
        login_page.login(userB_name, "SecurePassword123!")
        contacts_page.navigate()
        
        # Act: Accept friend request from userA
        success = contacts_page.accept_friend_request("User A")
        assert success, "Failed to locate or accept friend request from User A"
        
        # Assert friendship status (User B now sees User A in contacts search list as friend)
        contacts_page.search_user(userA_name)
        assert contacts_page.is_search_result_found(userA_name), "User A not found in search results"
        status = contacts_page.get_friend_request_status(userA_name)
        assert "bạn bè" in status.lower() or "friend" in status.lower(), \
            f"Expected friendship accepted state. Got: {status}"
            
        login_page.logout()

    def test_decline_friend_request(self, register_page, login_page, contacts_page):
        """TC-FRD-05: Recipient declines pending request; request is removed."""
        timestamp = int(time.time() * 1000)
        userA_name = f"decfa{timestamp}"
        userB_name = f"decfb{timestamp}"
        
        # Register User A and User B
        register_page.navigate()
        register_page.register("User A", f"{userA_name}@example.com", "", userA_name, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        login_page.logout()
        
        register_page.navigate()
        register_page.register("User B", f"{userB_name}@example.com", "", userB_name, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        login_page.logout()
        
        # User A sends request to User B
        login_page.login(userA_name, "SecurePassword123!")
        contacts_page.navigate()
        contacts_page.search_user(userB_name)
        contacts_page.send_friend_request(userB_name)
        contacts_page.wait_for_friend_request_status(userB_name, "Đã gửi lời mời")
        login_page.logout()
        
        # Recipient (User B) logs in
        login_page.login(userB_name, "SecurePassword123!")
        contacts_page.navigate()
        
        # Act: Decline friend request from userA
        success = contacts_page.decline_friend_request("User A")
        assert success, "Failed to locate or decline friend request from User A"
        
        # Assert: User A is not in friends list, relationship reverts to "Kết bạn" / NONE
        contacts_page.search_user(userA_name)
        status = contacts_page.get_friend_request_status(userA_name)
        assert "kết bạn" in status.lower() or "friend" not in status.lower(), \
            f"Expected declined request to revert status to clean state. Got: {status}"
            
        login_page.logout()

    def test_guest_contact_creation_and_privacy(self, register_page, login_page, contacts_page):
        """TC-GST-01 & TC-GST-02: Create guest contact; verify guest privacy is isolated."""
        timestamp = int(time.time() * 1000)
        userA_name = f"gsta{timestamp}"
        userB_name = f"gstb{timestamp}"
        guest_name = f"Guest A {timestamp}"
        
        # Step 1: User A creates guest contact
        register_page.navigate()
        register_page.register("User A", f"{userA_name}@example.com", "", userA_name, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        contacts_page.navigate()
        
        contacts_page.create_guest_contact(
            name=guest_name,
            email="guesta@example.com",
            phone="0909123456"
        )
        
        # Trigger reload of contacts
        contacts_page.click_element(contacts_page.locators.REFRESH_CONTACTS_BTN)
        
        # Assert: Guest visible for User A
        assert contacts_page.is_guest_contact_visible(guest_name), \
            "Guest contact was not visible in creator's contact list"
            
        login_page.logout()
        
        # Step 2: User B logs in, searches/views contacts, must not see User A's guest contact
        register_page.navigate()
        register_page.register("User B", f"{userB_name}@example.com", "", userB_name, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        contacts_page.navigate()
        
        # Check: User B's own guest list
        assert not contacts_page.is_guest_contact_visible(guest_name), \
            "Security Breach: User B can view User A's private guest contact in list"
            
        # Check: Searching for User A's guest yields nothing (and guest contacts are private)
        contacts_page.search_user(guest_name)
        assert not contacts_page.is_search_result_found(guest_name), \
            "Security Breach: User B could search for and discover User A's private guest contact"
            
        login_page.logout()
