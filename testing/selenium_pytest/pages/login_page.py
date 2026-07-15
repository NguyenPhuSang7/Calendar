from pages.base_page import BasePage
from locators.auth_locators import AuthLocators

class LoginPage(BasePage):
    def navigate(self):
        """Navigate to the main page (which displays login card if unauthenticated)."""
        self.navigate_to("/")

    def switch_to_login(self):
        """Click on the 'Đăng nhập' tab."""
        self.click_element(AuthLocators.LOGIN_TAB_BTN)

    def switch_to_register(self):
        """Click on the 'Đăng ký' tab."""
        self.click_element(AuthLocators.REGISTER_TAB_BTN)

    def login(self, username, password):
        """Perform login action with given credentials."""
        self.switch_to_login()
        self.enter_text(AuthLocators.USERNAME_INPUT, username)
        self.enter_text(AuthLocators.PASSWORD_INPUT, password)
        self.click_element(AuthLocators.SUBMIT_BUTTON)

    def is_logged_in(self):
        """Check if user has logged in successfully by verifying logout button visibility."""
        return self.is_element_visible(AuthLocators.LOGOUT_BUTTON, timeout=3)

    def get_error_message(self):
        """Retrieve unified form error message text."""
        return self.get_element_text(AuthLocators.FORM_ERROR_MSG)

    def logout(self):
        """Perform logout action."""
        self.close_modal_if_open()
        if self.is_logged_in():
            self.click_element(AuthLocators.LOGOUT_BUTTON)
            # Wait until login card is visible again
            self.wait_for_element_visible(AuthLocators.SUBMIT_BUTTON)
