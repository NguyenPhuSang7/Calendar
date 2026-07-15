from selenium.webdriver.common.by import By

class AuthLocators:
    # Tab triggers
    LOGIN_TAB_BTN = (By.XPATH, "//div[contains(@class, 'auth-tabs')]/button[text()='Đăng nhập']")
    REGISTER_TAB_BTN = (By.XPATH, "//div[contains(@class, 'auth-tabs')]/button[text()='Đăng ký']")
    
    # Text Inputs
    USERNAME_INPUT = (By.XPATH, "//label[.//span[text()='Username']]//input")
    PASSWORD_INPUT = (By.CSS_SELECTOR, ".password-field input")
    
    # Registration Fields
    REG_FULLNAME_INPUT = (By.XPATH, "//label[.//span[text()='Họ và tên']]//input")
    REG_EMAIL_INPUT = (By.XPATH, "//label[.//span[text()='Email']]//input")
    REG_PHONE_INPUT = (By.XPATH, "//label[.//span[text()='Số điện thoại']]//input")
    
    # Buttons
    SUBMIT_BUTTON = (By.CLASS_NAME, "login-button")
    LOGOUT_BUTTON = (By.ID, "menu-logout")
    
    # Unified Form Error Message Display
    FORM_ERROR_MSG = (By.CLASS_NAME, "form-error")
