from pages.base_page import BasePage
from locators.appointment_locators import AppointmentLocators
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

class AppointmentPage(BasePage):
    def navigate(self):
        """Navigate to Calendar view."""
        self.navigate_via_sidebar("menu-calendar")

    def open_create_form(self):
        """Click the button to open the appointment form modal."""
        # Wait for loading mask to disappear (from functional_tests.robot)
        # Note: we check if calendar loading is visible, and wait for it to disappear
        self.click_element(AppointmentLocators.OPEN_CREATE_FORM_BTN)

    def fill_appointment_details(self, title, date, start_time, end_time, desc=""):
        """Populate the appointment fields without submitting."""
        self.enter_text(AppointmentLocators.TITLE_INPUT, title)
        
        # Select contact if specified, handled by separate method
        
        # Set date (on React it's input type="date")
        if date:
            self.enter_text(AppointmentLocators.DATE_INPUT, date)
            
        if start_time:
            self.enter_text(AppointmentLocators.START_TIME_INPUT, start_time)
            
        # End time might be auto-set, or we input it
        if end_time:
            self.enter_text(AppointmentLocators.END_TIME_INPUT, end_time)
            
        if desc:
            self.enter_text(AppointmentLocators.NOTE_TEXTAREA, desc)

    def select_invitee_contact(self, contact_name):
        """Select a friend/contact from the invitee dropdown menu."""
        select_element = self.wait_for_element_visible(AppointmentLocators.CONTACT_SELECT)
        select = Select(select_element)
        select.select_by_visible_text(contact_name)

    def submit_form(self, wait_for_close=False):
        """Click submit button on the form."""
        self.click_element(AppointmentLocators.SUBMIT_BTN)
        if wait_for_close:
            self.wait_for_element_invisible((By.CLASS_NAME, "modal-backdrop"), timeout=5)

    def create_personal_appointment(self, title, date, start_time, end_time, desc=""):
        """Flow to create a personal appointment."""
        self.open_create_form()
        self.fill_appointment_details(title, date, start_time, end_time, desc)
        self.submit_form(wait_for_close=True)

    def create_appointment_with_invitee(self, title, date, start_time, end_time, contact_name, desc=""):
        """Flow to create an invitation appointment."""
        self.open_create_form()
        self.fill_appointment_details(title, date, start_time, end_time, desc)
        self.select_invitee_contact(contact_name)
        self.submit_form(wait_for_close=True)

    def edit_appointment(self, appointment_card_element, new_title, new_start_time=None, new_end_time=None):
        """Trigger edit form from an active agenda card and apply changes."""
        # Find the inline edit pencil button inside the specific card
        edit_btn = appointment_card_element.find_element(*AppointmentLocators.EDIT_BTN)
        self.driver.execute_script("arguments[0].click();", edit_btn)
        
        self.enter_text(AppointmentLocators.TITLE_INPUT, new_title)
        if new_start_time:
            self.enter_text(AppointmentLocators.START_TIME_INPUT, new_start_time)
        if new_end_time:
            self.enter_text(AppointmentLocators.END_TIME_INPUT, new_end_time)
        self.submit_form(wait_for_close=True)

    def delete_appointment(self, appointment_card_element):
        """Trigger deletion from card and confirm native browser alert."""
        delete_btn = appointment_card_element.find_element(*AppointmentLocators.DELETE_BTN)
        delete_btn.click()
        
        # Handle the native JavaScript window.confirm prompt
        alert = self.driver.switch_to.alert
        alert.accept()

    def get_start_time(self):
        """Get current value of start time input."""
        element = self.wait_for_element_visible(AppointmentLocators.START_TIME_INPUT)
        return element.get_attribute("value")

    def get_end_time(self):
        """Get current value of end time input."""
        element = self.wait_for_element_visible(AppointmentLocators.END_TIME_INPUT)
        return element.get_attribute("value")

    def get_form_error(self):
        """Get text of validation warning within modal."""
        return self.get_element_text(AppointmentLocators.FORM_ERROR_MSG)

    def is_invitation_box_visible(self):
        """Check if invitation alert panel is on screen."""
        return self.is_element_visible(AppointmentLocators.INVITATION_BOX_CONTAINER, timeout=3)

    def accept_invitation(self, title):
        """Accept a specific pending invitation from the notification panel."""
        items = self.driver.find_elements(*AppointmentLocators.INVITATION_ITEM)
        for item in items:
            if title in item.text:
                accept_btn = item.find_element(*AppointmentLocators.ACCEPT_INVITATION_BTN)
                accept_btn.click()
                return True
        return False

    def decline_invitation(self, title):
        """Decline a specific pending invitation from the notification panel."""
        items = self.driver.find_elements(*AppointmentLocators.INVITATION_ITEM)
        for item in items:
            if title in item.text:
                decline_btn = item.find_element(*AppointmentLocators.DECLINE_INVITATION_BTN)
                decline_btn.click()
                return True
        return False

    def is_edit_delete_button_present(self, card_element):
        """Check if Edit/Delete actions are visible inside the card."""
        edit_elements = card_element.find_elements(*AppointmentLocators.EDIT_BTN)
        delete_elements = card_element.find_elements(*AppointmentLocators.DELETE_BTN)
        return len(edit_elements) > 0 and len(delete_elements) > 0

    def get_appointment_by_title(self, title):
        """Find appointment card in daily agenda list by title."""
        cards = self.driver.find_elements(*AppointmentLocators.AGENDA_APPOINTMENT_CARD)
        for card in cards:
            try:
                card_title = card.find_element(*AppointmentLocators.APPOINTMENT_TITLE).text
                if title in card_title:
                    return card
            except Exception:
                continue
        return None
