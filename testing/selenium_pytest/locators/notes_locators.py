from selenium.webdriver.common.by import By

class NotesLocators:
    # Trigger Create Note
    OPEN_NOTE_FORM_BTN = (By.ID, "btn-create-note")
    
    # Form Inputs (Inside Modal)
    NOTE_TITLE_INPUT = (By.XPATH, "//div[contains(@class, 'modal')]//label[span[text()='Tiêu đề']]//input")
    NOTE_DATE_INPUT = (By.XPATH, "//div[contains(@class, 'modal')]//label[span[text()='Ngày']]//input")
    NOTE_CONTENT_TEXTAREA = (By.XPATH, "//div[contains(@class, 'modal')]//label[span[text()='Nội dung']]//textarea")
    NOTE_COLOR_BUTTON = (By.CSS_SELECTOR, ".color-picker button")
    
    # Controls
    SUBMIT_BTN = (By.CSS_SELECTOR, ".modal-actions button.solid-button")
    CANCEL_BTN = (By.CSS_SELECTOR, ".modal-actions button.secondary-button")
    FORM_ERROR_MSG = (By.CLASS_NAME, "form-error")
    
    # Note Cards in Daily Agenda
    AGENDA_NOTE_CARD = (By.CSS_SELECTOR, ".agenda-card.agenda-note")
    NOTE_TITLE = (By.XPATH, ".//h4")
    NOTE_CONTENT = (By.XPATH, ".//p")
    
    # Inline actions inside Note Card
    EDIT_NOTE_BTN = (By.XPATH, ".//div[contains(@class, 'item-actions')]/button[1]")
    DELETE_NOTE_BTN = (By.XPATH, ".//div[contains(@class, 'item-actions')]/button[2]")
