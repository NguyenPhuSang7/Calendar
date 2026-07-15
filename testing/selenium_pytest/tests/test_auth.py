import pytest
import time

class TestAuthentication:
    
    def test_valid_registration(self, register_page, login_page):
        """TC-AUTH-01: Verify valid registration creates a new user, redirects, and logs in."""
        register_page.navigate()
        
        # Act: Submit valid details with unique username using timestamp
        timestamp = int(time.time())
        username = f"user{timestamp}"
        email = f"user{timestamp}@example.com"
        
        register_page.register("John Doe", email, "0909123456", username, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        
        # Assert: Successful registration directs to dashboard (logged in status is verified)
        assert login_page.is_logged_in(), "User was not automatically logged in or redirected after registration"

    def test_registration_invalid_username_space(self, register_page):
        """TC-AUTH-02: Verify username containing spaces is blocked by HTML5 client-side constraints."""
        register_page.navigate()
        
        # Act: Try username containing whitespace (which is disallowed by pattern [A-Za-z0-9]+)
        register_page.register("Jane Doe", "jane.doe@example.com", "", "invalid user", "SecurePassword123!")
        
        # Assert: Username input fails HTML5 native constraint validation
        val_msg = register_page.get_username_field_validation_message()
        assert val_msg != "", "Expected HTML5 validation message on username field due to space format violation"

    def test_registration_weak_password(self, register_page):
        """TC-AUTH-03: Verify registration fails when the password does not meet complexity rules."""
        register_page.navigate()
        
        # Act: Try registering with password lacking uppercase/special characters (length > 8 to bypass client-side minlength)
        timestamp = int(time.time())
        register_page.register("Jane Doe", f"weak{timestamp}@example.com", "", f"weakuser{timestamp}", "password123")
        
        # Assert: Validation error banner is displayed
        err_msg = register_page.get_error_message()
        assert "dữ liệu không hợp lệ" in err_msg.lower() or "mật khẩu" in err_msg.lower(), \
            f"Expected validation error on password complexity. Got: {err_msg}"

    def test_registration_duplicate_account(self, register_page, login_page):
        """TC-AUTH-04: Verify registration blocks duplicate email or username with a Conflict error message."""
        register_page.navigate()
        
        # Setup: Pre-register a unique user
        timestamp = int(time.time())
        username = f"dup{timestamp}"
        email = f"dup{timestamp}@example.com"
        register_page.register("Dup User", email, "", username, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        
        # Logout
        login_page.logout()
        
        # Act: Try registering again with the exact same username
        register_page.register("Another Dup User", f"other{timestamp}@example.com", "", username, "SecurePassword123!")
        
        # Assert: Application returns duplicate error banner/alert
        err_msg = register_page.get_error_message()
        assert "tồn tại" in err_msg.lower() or "duplicate" in err_msg.lower(), \
            f"Expected duplicate account error, instead got: {err_msg}"

    def test_login_success_and_failure(self, login_page, register_page):
        """TC-AUTH-05: Verify login works with valid credentials, and fails with invalid credentials."""
        # Setup: Create a user to test login
        register_page.navigate()
        timestamp = int(time.time())
        username = f"login{timestamp}"
        email = f"login{timestamp}@example.com"
        register_page.register("Login User", email, "", username, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        login_page.logout()

        # 1. Test Failed Login
        login_page.navigate()
        login_page.login(username, "WrongPassword!")
        
        assert not login_page.is_logged_in(), "User should not be logged in with incorrect password"
        error_text = login_page.get_error_message()
        assert "không đúng" in error_text.lower() or "unauthorized" in error_text.lower(), \
            f"Expected auth failure warning, but got: {error_text}"
            
        # 2. Test Successful Login
        login_page.login(username, "SecurePassword123!")
        login_page.wait_for_dashboard_load()
        assert login_page.is_logged_in(), "Failed to log in with valid credentials"
