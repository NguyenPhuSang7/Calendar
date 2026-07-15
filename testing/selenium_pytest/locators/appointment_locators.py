from selenium.webdriver.common.by import By

class AppointmentLocators:
    # Trigger Create Form
    OPEN_CREATE_FORM_BTN = (By.ID, "btn-create-appointment")
    
    # Form Inputs (Inside Modal)
    TITLE_INPUT = (By.XPATH, "//div[contains(@class, 'modal')]//label[span[text()='Tiêu đề']]//input")
    CONTACT_SELECT = (By.XPATH, "//div[contains(@class, 'modal')]//label[contains(span/text(), 'Người liên hệ')]//select")
    DATE_INPUT = (By.XPATH, "//div[contains(@class, 'modal')]//label[span[text()='Ngày']]//input")
    START_TIME_INPUT = (By.XPATH, "//div[contains(@class, 'modal')]//label[span[text()='Bắt đầu']]//input")
    END_TIME_INPUT = (By.XPATH, "//div[contains(@class, 'modal')]//label[span[text()='Kết thúc']]//input")
    NOTE_TEXTAREA = (By.XPATH, "//div[contains(@class, 'modal')]//label[span[text()='Ghi chú']]//textarea")
    
    # Modal Form Controls
    SUBMIT_BTN = (By.CSS_SELECTOR, ".modal-actions button.solid-button")
    CANCEL_BTN = (By.CSS_SELECTOR, ".modal-actions button.secondary-button")
    
    # Validation / Exception Displays
    FORM_ERROR_MSG = (By.CLASS_NAME, "form-error")
    
    # Agenda Appointment Cards (rendered in Daily Panel / Right Panel)
    AGENDA_APPOINTMENT_CARD = (By.CSS_SELECTOR, ".agenda-card.agenda-appointment")
    APPOINTMENT_TITLE = (By.XPATH, ".//h4")
    INVITATION_STATUS_BADGE = (By.CLASS_NAME, "status-badge")
    
    # Inline Card Actions
    EDIT_BTN = (By.XPATH, ".//div[contains(@class, 'item-actions')]/button[1]")
    DELETE_BTN = (By.XPATH, ".//div[contains(@class, 'item-actions')]/button[2]")
    
    # Invitation Box (Notification container at the top of dashboard)
    INVITATION_BOX_CONTAINER = (By.CLASS_NAME, "invitation-box")
    INVITATION_ITEM = (By.CLASS_NAME, "invitation-item")
    ACCEPT_INVITATION_BTN = (By.CSS_SELECTOR, ".invitation-item button.accept")
    DECLINE_INVITATION_BTN = (By.CSS_SELECTOR, ".invitation-item button.decline")
