from pages.base_page import BasePage
from locators.contacts_locators import ContactsLocators
from selenium.webdriver.common.by import By

class ContactsPage(BasePage):
    locators = ContactsLocators

    def navigate(self):
        """Navigate to Contacts view."""
        self.navigate_via_sidebar("menu-contacts")

    def search_user(self, query):
        """Input name, phone, or email and search."""
        self.enter_text(ContactsLocators.SEARCH_INPUT, query)
        # Click search button to trigger React onSubmit synthetic event handler
        search_btn = (By.CSS_SELECTOR, ".contact-search-form button")
        self.click_element(search_btn)

    def is_search_result_found(self, username):
        """Check if target user is displayed in search results."""
        if not self.is_element_visible(ContactsLocators.SEARCH_RESULT_CARD, timeout=3):
            return False
        results = self.driver.find_elements(*ContactsLocators.SEARCH_RESULT_CARD)
        for res in results:
            try:
                if username in res.text:
                    return True
            except Exception:
                continue
        return False

    def send_friend_request(self, username):
        """Send friend request to search result."""
        self.wait_for_element_visible(ContactsLocators.SEARCH_RESULT_CARD, timeout=5)
        results = self.driver.find_elements(*ContactsLocators.SEARCH_RESULT_CARD)
        for res in results:
            try:
                if username in res.text:
                    add_btn = res.find_element(*ContactsLocators.ADD_FRIEND_BTN)
                    add_btn.click()
                    return True
            except Exception:
                continue
        return False

    def get_friend_request_status(self, username):
        """Get the relationship status text for the user card."""
        results = self.driver.find_elements(*ContactsLocators.SEARCH_RESULT_CARD)
        for res in results:
            try:
                if username in res.text:
                    # It could be the button with text "Kết bạn" or the label relationship-label
                    # Let's check both
                    labels = res.find_elements(*ContactsLocators.RELATIONSHIP_LABEL)
                    if len(labels) > 0:
                        return labels[0].text
                    btns = res.find_elements(*ContactsLocators.ADD_FRIEND_BTN)
                    if len(btns) > 0:
                        return btns[0].text
            except Exception:
                continue
        return ""

    def accept_friend_request(self, requester_name):
        """Accept friend request from a user in the pending list."""
        if not self.is_element_visible(ContactsLocators.FRIEND_REQUEST_BOX, timeout=3):
            return False
        items = self.driver.find_elements(*ContactsLocators.FRIEND_REQUEST_ITEM)
        for item in items:
            name_el = item.find_element(*ContactsLocators.REQUESTER_NAME)
            if requester_name in name_el.text:
                accept_btn = item.find_element(*ContactsLocators.ACCEPT_REQUEST_BTN)
                accept_btn.click()
                return True
        return False

    def decline_friend_request(self, requester_name):
        """Decline friend request from a user in the pending list."""
        if not self.is_element_visible(ContactsLocators.FRIEND_REQUEST_BOX, timeout=3):
            return False
        items = self.driver.find_elements(*ContactsLocators.FRIEND_REQUEST_ITEM)
        for item in items:
            name_el = item.find_element(*ContactsLocators.REQUESTER_NAME)
            if requester_name in name_el.text:
                decline_btn = item.find_element(*ContactsLocators.DECLINE_REQUEST_BTN)
                decline_btn.click()
                return True
        return False

    def create_guest_contact(self, name, email="", phone=""):
        """Flow to create a private guest contact."""
        self.click_element(ContactsLocators.OPEN_GUEST_FORM_BTN)
        self.enter_text(ContactsLocators.GUEST_NAME_INPUT, name)
        if email:
            self.enter_text(ContactsLocators.GUEST_EMAIL_INPUT, email)
        if phone:
            self.enter_text(ContactsLocators.GUEST_PHONE_INPUT, phone)
        self.click_element(ContactsLocators.SUBMIT_GUEST_BTN)

    def is_guest_contact_visible(self, guest_name):
        """Verify presence of guest contact in the owner's list."""
        if not self.is_element_visible(ContactsLocators.CONTACT_CARD, timeout=3):
            return False
        guests = self.driver.find_elements(*ContactsLocators.CONTACT_CARD)
        for guest in guests:
            try:
                name_text = guest.find_element(*ContactsLocators.CONTACT_CARD_NAME).text
                # It must be a Guest, so it should also contain guest-badge
                badges = guest.find_elements(*ContactsLocators.GUEST_BADGE)
                if guest_name in name_text and len(badges) > 0:
                    return True
            except Exception:
                continue
        return False

    def get_search_error_message(self):
        """Get validation error text from search card."""
        return self.get_element_text(ContactsLocators.SEARCH_FORM_ERROR)

    def wait_for_friend_request_status(self, username, expected_status, timeout=5):
        """Wait until friendship status matches expected_status."""
        from selenium.webdriver.support.ui import WebDriverWait
        def check_status(driver):
            results = driver.find_elements(*ContactsLocators.SEARCH_RESULT_CARD)
            for res in results:
                try:
                    if username in res.text:
                        labels = res.find_elements(*ContactsLocators.RELATIONSHIP_LABEL)
                        if len(labels) > 0 and expected_status.lower() in labels[0].text.lower():
                            return True
                        btns = res.find_elements(*ContactsLocators.ADD_FRIEND_BTN)
                        if len(btns) > 0 and expected_status.lower() in btns[0].text.lower():
                            return True
                except Exception:
                    continue
            return False
        WebDriverWait(self.driver, timeout).until(check_status)
