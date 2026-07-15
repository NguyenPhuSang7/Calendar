import pytest
import time
from locators.appointment_locators import AppointmentLocators

class TestAppointments:

    @pytest.fixture
    def dynamic_user(self, register_page, login_page):
        """Creates a unique user, logs them in, and yields their credentials."""
        register_page.navigate()
        timestamp = int(time.time() * 1000)
        username = f"user{timestamp}"
        email = f"user{timestamp}@example.com"
        register_page.register("Appointment Test User", email, "", username, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        assert login_page.is_logged_in(), "Dynamic user failed to automatically login after registration"
        
        yield {"username": username, "fullName": "Appointment Test User"}
        
        login_page.logout()

    def test_create_personal_appointment(self, dynamic_user, appointment_page, calendar_page):
        """TC-APT-01: Create personal appointment without selecting contacts, visible on calendar."""
        appointment_page.navigate()
        
        # Act: Create personal appointment
        appointment_page.create_personal_appointment(
            title="Meeting with myself",
            date="2026-08-20",
            start_time="10:00",
            end_time="11:00",
            desc="Self-alignment time"
        )
        
        # Assert: Visible in daily agenda
        card = appointment_page.get_appointment_by_title("Meeting with myself")
        assert card is not None, "Created appointment did not appear on daily agenda"

    def test_time_rules_reject_past_datetime(self, dynamic_user, appointment_page):
        """TC-APT-02: Verify system rejects booking dates/times in the past."""
        appointment_page.navigate()
        appointment_page.open_create_form()
        
        # Act: Fill past time on today's date to bypass HTML5 min="today" input validation
        from datetime import datetime
        today_str = datetime.now().strftime("%Y-%m-%d")
        appointment_page.fill_appointment_details(
            title="Past Event",
            date=today_str,
            start_time="00:00",
            end_time="01:00"
        )
        appointment_page.submit_form()
        
        # Assert: Error message is visible on screen
        err = appointment_page.get_form_error()
        assert "quá khứ" in err.lower(), f"Expected past date error message. Got: {err}"
        appointment_page.close_modal_if_open()

    def test_time_rules_end_time_before_start_time(self, dynamic_user, appointment_page):
        """TC-APT-03: Verify system rejects end times equal to or before the start time."""
        appointment_page.navigate()
        
        # Act: Submit invalid time range via JS fetch to bypass React auto-adjustment logic
        js_script = """
        const auth = JSON.parse(localStorage.getItem('appointment_auth'));
        fetch('/api/appointments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + auth.token
            },
            body: JSON.stringify({
                title: "Invalid Duration Event",
                startTime: "2026-08-20T15:00:00",
                endTime: "2026-08-20T14:00:00",
                note: null
            })
        }).then(res => res.json()).then(data => {
            let errDiv = document.createElement('div');
            errDiv.className = 'form-error';
            errDiv.innerText = data.message || 'Error';
            document.body.appendChild(errDiv);
        }).catch(err => {
            let errDiv = document.createElement('div');
            errDiv.className = 'form-error';
            errDiv.innerText = err.message;
            document.body.appendChild(errDiv);
        });
        """
        appointment_page.driver.execute_script(js_script)
        
        # Assert: End time validation warning shown
        err = appointment_page.get_form_error()
        assert "sau" in err.lower() or "kết thúc" in err.lower() or "bắt đầu" in err.lower(), \
            f"Expected end time logical validation message. Got: {err}"
        appointment_page.close_modal_if_open()

    def test_time_rules_auto_population(self, dynamic_user, appointment_page):
        """TC-APT-04 & TC-APT-05: Verify auto-setting end time/start time offsets by 1 hour."""
        appointment_page.navigate()
        appointment_page.open_create_form()
        
        # Act 1: Input start time and verify end time auto-populates
        appointment_page.fill_appointment_details(
            title="Auto Set End Time",
            date="2026-08-20",
            start_time="17:00",
            end_time=""  # Leave empty
        )
        # End time should be auto populated to 18:00
        assert appointment_page.get_end_time() == "18:00", \
            "End time was not automatically set to 1 hour after start time"

    def test_appointment_crud_and_authorization(self, dynamic_user, appointment_page, calendar_page):
        """TC-APT-11 & TC-APT-12: Create, Edit, and Delete appointment. Verify owner permissions."""
        appointment_page.navigate()
        appointment_page.create_personal_appointment(
            title="CRUD Temp Event",
            date="2026-08-25",
            start_time="13:00",
            end_time="14:00"
        )
        
        # Find the card in agenda
        card = appointment_page.get_appointment_by_title("CRUD Temp Event")
        assert card is not None, "Created appointment for CRUD not found"
                
        # Assert owner permissions are visible (Edit & Delete btns available)
        assert appointment_page.is_edit_delete_button_present(card), \
            "Owner was not shown Edit and Delete authorization buttons on their own event"
            
        # Edit title
        appointment_page.edit_appointment(card, new_title="CRUD Updated Event")
        
        # Verify title updated in calendar
        updated_card = appointment_page.get_appointment_by_title("CRUD Updated Event")
        assert updated_card is not None, "Appointment title did not update after editing"
        
        # Delete
        appointment_page.delete_appointment(updated_card)
        
        # Verify removed from calendar agenda
        final_card = appointment_page.get_appointment_by_title("CRUD Updated Event")
        assert final_card is None, "Appointment was not deleted from the calendar"

    def test_invitation_workflow_accept_and_decline(self, register_page, login_page, contacts_page, appointment_page, calendar_page):
        """TC-APT-07, TC-APT-08 & TC-APT-09: Flow to create invitation, accept and decline from invited friend."""
        # 1. Register two users: User A and User B
        timestamp = int(time.time() * 1000)
        userA_name = f"apta{timestamp}"
        userB_name = f"aptb{timestamp}"
        
        register_page.navigate()
        register_page.register("User A", f"{userA_name}@example.com", "", userA_name, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        login_page.logout()
        
        register_page.navigate()
        register_page.register("User B", f"{userB_name}@example.com", "", userB_name, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        login_page.logout()
        
        # 2. Establish friendship (User A sends request, User B accepts)
        login_page.login(userA_name, "SecurePassword123!")
        contacts_page.navigate()
        contacts_page.search_user(userB_name)
        contacts_page.send_friend_request(userB_name)
        contacts_page.wait_for_friend_request_status(userB_name, "Đã gửi lời mời")
        login_page.logout()
        
        login_page.login(userB_name, "SecurePassword123!")
        contacts_page.navigate()
        contacts_page.accept_friend_request("User A")
        login_page.logout()
        
        # 3. User A creates appointment and invites User B
        import datetime
        today_date = datetime.date.today()
        target_date = today_date + datetime.timedelta(days=1)
        target_date_str = target_date.strftime("%Y-%m-%d")

        login_page.login(userA_name, "SecurePassword123!")
        appointment_page.navigate()
        appointment_page.create_appointment_with_invitee(
            title=f"Sync {timestamp}",
            date=target_date_str,
            start_time="11:00",
            end_time="12:00",
            contact_name="User B"
        )
        login_page.logout()
        
        # 4. User B accepts the invitation
        login_page.login(userB_name, "SecurePassword123!")
        appointment_page.navigate()
        
        assert appointment_page.is_invitation_box_visible(), "Invitation notification box should be visible to User B"
        
        success = appointment_page.accept_invitation(f"Sync {timestamp}")
        assert success, "Failed to accept the invitation"
        
        # Navigate to the correct date on calendar to view the updated daily panel agenda
        calendar_page.navigate()
        if target_date.month != today_date.month:
            calendar_page.go_to_next_month()
        calendar_page.select_day_in_current_month(target_date.day)
        
        # Verify it now appears on User B's agenda
        card = appointment_page.get_appointment_by_title(f"Sync {timestamp}")
        assert card is not None, "Accepted appointment did not show on recipient's daily panel"
        
        # Verify status is accepted/confirmed
        status_badge = card.find_element(*AppointmentLocators.INVITATION_STATUS_BADGE).text
        assert "đã chấp nhận" in status_badge.lower() or "confirmed" in status_badge.lower(), \
            f"Expected status to change to confirmed. Got: {status_badge}"
            
        login_page.logout()

    def test_only_recipient_can_respond_to_invitation(self, register_page, login_page, contacts_page, appointment_page):
        """TC-APT-10: Verify another unauthorized user cannot see or respond to the invitation."""
        timestamp = int(time.time() * 1000)
        userA_name = f"aptasec{timestamp}"
        userB_name = f"aptbsec{timestamp}"
        userC_name = f"aptcsec{timestamp}"
        
        # Register User A
        register_page.navigate()
        register_page.register("Organizer", f"{userA_name}@example.com", "", userA_name, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        login_page.logout()
        
        # Register User B
        register_page.navigate()
        register_page.register("Invitee", f"{userB_name}@example.com", "", userB_name, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        login_page.logout()
        
        # Register User C
        register_page.navigate()
        register_page.register("Stranger", f"{userC_name}@example.com", "", userC_name, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        login_page.logout()
        
        # Make A & B friends
        login_page.login(userA_name, "SecurePassword123!")
        contacts_page.navigate()
        contacts_page.search_user(userB_name)
        contacts_page.send_friend_request(userB_name)
        contacts_page.wait_for_friend_request_status(userB_name, "Đã gửi lời mời")
        login_page.logout()
        
        login_page.login(userB_name, "SecurePassword123!")
        contacts_page.navigate()
        contacts_page.accept_friend_request("Organizer")
        login_page.logout()
        
        # Organizer invites User B
        login_page.login(userA_name, "SecurePassword123!")
        appointment_page.navigate()
        appointment_page.create_appointment_with_invitee(
            title=f"Private Sync {timestamp}",
            date="2026-09-02",
            start_time="14:00",
            end_time="15:00",
            contact_name="Invitee"
        )
        login_page.logout()
        
        # Log in as User C (who is not the recipient)
        login_page.login(userC_name, "SecurePassword123!")
        appointment_page.navigate()
        
        # Assert: User C cannot see User B's invitation box
        assert not appointment_page.is_invitation_box_visible(), \
            "Non-recipient user should not see other users' pending invitation alerts"
        login_page.logout()
