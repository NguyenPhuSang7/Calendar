from pages.base_page import BasePage
from locators.notes_locators import NotesLocators
from selenium.webdriver.common.by import By

class NotesPage(BasePage):
    def navigate(self):
        """Navigate to Calendar view (where notes are managed)."""
        self.navigate_via_sidebar("menu-calendar")

    def open_create_note_form(self):
        """Click to open Note Form."""
        self.click_element(NotesLocators.OPEN_NOTE_FORM_BTN)

    def fill_note_details(self, title, content, date, color=None):
        """Populate the note fields."""
        self.enter_text(NotesLocators.NOTE_TITLE_INPUT, title)
        if date:
            self.enter_text(NotesLocators.NOTE_DATE_INPUT, date)
        self.enter_text(NotesLocators.NOTE_CONTENT_TEXTAREA, content)
        
        # Select color button if provided
        if color:
            color_selector = f".color-picker button.{color}"
            # Locate within color-picker
            btn = self.driver.find_element(By.CSS_SELECTOR, color_selector)
            btn.click()

    def submit_note(self, wait_for_close=False):
        """Submit the note form."""
        self.click_element(NotesLocators.SUBMIT_BTN)
        if wait_for_close:
            from selenium.webdriver.common.by import By
            self.wait_for_element_invisible((By.CLASS_NAME, "modal-backdrop"), timeout=5)

    def create_note(self, title, content, date, color=None):
        """Full create-note flow."""
        self.open_create_note_form()
        self.fill_note_details(title, content, date, color)
        self.submit_note(wait_for_close=True)

    def edit_note(self, note_element, new_title, new_content):
        """Edit an existing note card."""
        edit_btn = note_element.find_element(*NotesLocators.EDIT_NOTE_BTN)
        self.driver.execute_script("arguments[0].click();", edit_btn)
        
        self.enter_text(NotesLocators.NOTE_TITLE_INPUT, new_title)
        self.enter_text(NotesLocators.NOTE_CONTENT_TEXTAREA, new_content)
        self.submit_note(wait_for_close=True)

    def delete_note(self, note_element):
        """Delete an existing note card and confirm alert."""
        delete_btn = note_element.find_element(*NotesLocators.DELETE_NOTE_BTN)
        delete_btn.click()
        
        # Handle the native JavaScript window.confirm prompt
        alert = self.driver.switch_to.alert
        alert.accept()

    def get_all_notes(self):
        """Return list of note cards present on screen."""
        return self.driver.find_elements(*NotesLocators.AGENDA_NOTE_CARD)

    def does_note_exist(self, title):
        """Return True if a note card with the specified title is found."""
        return self.get_note_by_title(title) is not None

    def get_note_by_title(self, title):
        """Find note card by exact title."""
        notes = self.get_all_notes()
        for note in notes:
            try:
                card_title = note.find_element(*NotesLocators.NOTE_TITLE).text
                if title in card_title:
                    return note
            except Exception:
                continue
        return None

    def wait_for_note_to_disappear(self, title, timeout=5):
        """Wait until note with title disappears from screen."""
        from selenium.webdriver.support.ui import WebDriverWait
        WebDriverWait(self.driver, timeout).until(
            lambda d: self.get_note_by_title(title) is None
        )
