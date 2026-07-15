from selenium.webdriver.common.by import By

class ContactsLocators:
    # Sidebar Tab trigger
    CONTACTS_TAB_BTN = (By.ID, "menu-contacts")
    
    # Guest Creation Trigger
    OPEN_GUEST_FORM_BTN = (By.ID, "btn-create-guest")
    REFRESH_CONTACTS_BTN = (By.CSS_SELECTOR, "button.refresh-button")
    
    # Search System Users form & field
    SEARCH_FORM = (By.CLASS_NAME, "contact-search-form")
    SEARCH_INPUT = (By.CSS_SELECTOR, ".contact-search-form input")
    SEARCH_FORM_ERROR = (By.CLASS_NAME, "form-error")
    
    # Search Results
    SEARCH_RESULT_CARD = (By.CSS_SELECTOR, ".user-search-results .customer-card")
    SEARCH_RESULT_NAME = (By.XPATH, ".//div[contains(@class, 'customer-info')]/h3")
    ADD_FRIEND_BTN = (By.CSS_SELECTOR, "button.friend-button")
    RELATIONSHIP_LABEL = (By.CSS_SELECTOR, ".relationship-label")
    
    # Incoming Friend Requests Box
    FRIEND_REQUEST_BOX = (By.CLASS_NAME, "friend-request-box")
    FRIEND_REQUEST_ITEM = (By.CLASS_NAME, "friend-request-item")
    REQUESTER_NAME = (By.XPATH, ".//strong")
    ACCEPT_REQUEST_BTN = (By.CSS_SELECTOR, ".friend-request-item button.accept")
    DECLINE_REQUEST_BTN = (By.CSS_SELECTOR, ".friend-request-item button.decline")
    
    # Guest Creation Form Inputs
    GUEST_NAME_INPUT = (By.XPATH, "//div[contains(@class, 'modal')]//label[span[text()='Họ và tên']]//input")
    GUEST_EMAIL_INPUT = (By.XPATH, "//div[contains(@class, 'modal')]//label[span[text()='Email']]//input")
    GUEST_PHONE_INPUT = (By.XPATH, "//div[contains(@class, 'modal')]//label[span[text()='Số điện thoại']]//input")
    SUBMIT_GUEST_BTN = (By.CSS_SELECTOR, ".modal-actions button.solid-button")
    
    # My Contacts Grid
    CONTACTS_GRID = (By.CLASS_NAME, "customer-grid")
    CONTACT_CARD = (By.CSS_SELECTOR, ".customer-grid .customer-card")
    CONTACT_CARD_NAME = (By.XPATH, ".//div[contains(@class, 'customer-info')]/h3")
    GUEST_BADGE = (By.CLASS_NAME, "guest-badge")
