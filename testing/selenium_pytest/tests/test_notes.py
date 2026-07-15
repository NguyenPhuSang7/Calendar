import pytest
import time

class TestNotes:

    @pytest.fixture
    def userA(self, register_page, login_page):
        """Register User A and log in."""
        register_page.navigate()
        timestamp = int(time.time() * 1000)
        username = f"notea{timestamp}"
        email = f"notea{timestamp}@example.com"
        register_page.register("User A", email, "", username, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        assert login_page.is_logged_in(), "User A failed to automatically login after registration"
        yield {"username": username, "fullName": "User A"}
        login_page.logout()

    @pytest.fixture
    def userB(self, register_page, login_page):
        """Register User B and log in."""
        register_page.navigate()
        timestamp = int(time.time() * 1000) + 1
        username = f"noteb{timestamp}"
        email = f"noteb{timestamp}@example.com"
        register_page.register("User B", email, "", username, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        assert login_page.is_logged_in(), "User B failed to automatically login after registration"
        yield {"username": username, "fullName": "User B"}
        login_page.logout()

    def test_create_note_in_past(self, userA, notes_page):
        """TC-NOTE-01: Verify note creation in the past is permitted (no block on past dates)."""
        notes_page.navigate()
        
        # Act: Create a note dated in the past (e.g. 2020-01-01)
        notes_page.create_note(
            title="Past Reflection Note",
            content="Writing notes for past dates should succeed",
            date="2020-01-01"
        )
        
        # Assert: Creation succeeds and note is rendered on screen
        assert notes_page.does_note_exist("Past Reflection Note"), \
            "Note in the past was not successfully created"

    def test_edit_and_delete_note(self, userA, notes_page):
        """TC-NOTE-02 & TC-NOTE-03: Verify editing and deleting of notes works correctly."""
        notes_page.navigate()
        notes_page.create_note(
            title="Note to Modify",
            content="Original content",
            date="2026-08-20"
        )
        
        # Find note element
        note_el = notes_page.get_note_by_title("Note to Modify")
        assert note_el is not None, "Created note not found for editing"
        
        # Act: Edit note
        notes_page.edit_note(note_el, new_title="Note Has Modified", new_content="Updated content")
        
        # Assert updated on UI
        assert notes_page.does_note_exist("Note Has Modified"), "Edited note title not reflected on UI"
        assert not notes_page.does_note_exist("Note to Modify"), "Original note title should no longer exist"
        
        # Act: Delete note
        updated_note_el = notes_page.get_note_by_title("Note Has Modified")
        notes_page.delete_note(updated_note_el)
        
        # Wait for note to disappear from UI
        notes_page.wait_for_note_to_disappear("Note Has Modified")
        
        # Assert removed from view
        assert not notes_page.does_note_exist("Note Has Modified"), "Deleted note is still visible on screen"

    def test_note_owner_isolation(self, register_page, login_page, notes_page):
        """TC-NOTE-04: Verify note isolation (User A notes are not visible to User B)."""
        timestamp = int(time.time() * 1000)
        userA_name = f"diarya{timestamp}"
        userB_name = f"diaryb{timestamp}"
        
        # Step 1: User A creates a private note
        register_page.navigate()
        register_page.register("Diary A", f"{userA_name}@example.com", "", userA_name, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        notes_page.navigate()
        notes_page.create_note(
            title=f"User A Private Diary {timestamp}",
            content="Secrets of User A",
            date="2026-08-20"
        )
        login_page.logout()
        
        # Step 2: User B logs in and verifies they cannot see the note
        register_page.navigate()
        register_page.register("Diary B", f"{userB_name}@example.com", "", userB_name, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        notes_page.navigate()
        
        # Assert: Note is not rendered for User B
        assert not notes_page.does_note_exist(f"User A Private Diary {timestamp}"), \
            "Security Breach: User B can view User A's private note!"
        login_page.logout()
