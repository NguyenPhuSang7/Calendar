from pages.base_page import BasePage
from locators.auth_locators import AuthLocators

class RegisterPage(BasePage):
    def navigate(self):
        """Navigate to the main page."""
        self.navigate_to("/")

    def register(self, fullname, email, phone, username, password):
        """Switch to register tab, fill registration form and submit."""
        # Click Đăng ký tab first
        self.click_element(AuthLocators.REGISTER_TAB_BTN)
        
        self.enter_text(AuthLocators.REG_FULLNAME_INPUT, fullname)
        self.enter_text(AuthLocators.REG_EMAIL_INPUT, email)
        if phone:
            self.enter_text(AuthLocators.REG_PHONE_INPUT, phone)
        self.enter_text(AuthLocators.USERNAME_INPUT, username)
        self.enter_text(AuthLocators.PASSWORD_INPUT, password)
        self.click_element(AuthLocators.SUBMIT_BUTTON)

    def get_error_message(self):
        """Retrieve unified form error message (server-side duplicate or pattern errors)."""
        return self.get_element_text(AuthLocators.FORM_ERROR_MSG)

    def get_username_field_validation_message(self):
        """Retrieve the HTML5 native validation message from username input (e.g. for pattern format blocking)."""
        el = self.wait_for_element_visible(AuthLocators.USERNAME_INPUT)
        return el.get_attribute("validationMessage")
        
    def get_password_field_validation_message(self):
        """Retrieve the HTML5 native validation message from password input."""
        el = self.wait_for_element_visible(AuthLocators.PASSWORD_INPUT)
        return el.get_attribute("validationMessage")
