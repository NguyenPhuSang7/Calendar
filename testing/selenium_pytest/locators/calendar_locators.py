from selenium.webdriver.common.by import By

class CalendarLocators:
    # Month / Toolbar Navigation
    PREV_MONTH_BTN = (By.XPATH, "//div[contains(@class, 'date-navigation')]/button[1]")
    NEXT_MONTH_BTN = (By.XPATH, "//div[contains(@class, 'date-navigation')]/button[3]")
    MONTH_HEADER = (By.CSS_SELECTOR, ".calendar-toolbar h2")
    TODAY_BTN = (By.CLASS_NAME, "today-button")
    
    # Calendar Layout Grid
    CALENDAR_GRID = (By.CLASS_NAME, "calendar-grid")
    CALENDAR_DAY_CELL = (By.CLASS_NAME, "calendar-day")
    DAY_NUMBER_SPN = (By.CLASS_NAME, "day-number")
    
    # Mini elements inside cells
    CALENDAR_MINI_EVENT = (By.CLASS_NAME, "mini-event")
    
    # UI Elements for Breakpoint Checks
    SIDEBAR_CONTAINER = (By.CLASS_NAME, "sidebar")
    SIDEBAR_BACKDROP = (By.CLASS_NAME, "sidebar-backdrop")
    MOBILE_HAMBURGER_BTN = (By.CSS_SELECTOR, "button.menu-button")
    MAIN_CONTENT = (By.CLASS_NAME, "main-content")
    
    # Views/Tabs triggers in sidebar
    MENU_CALENDAR = (By.ID, "menu-calendar")
    MENU_APPOINTMENTS = (By.ID, "menu-appointments")
    MENU_NOTES = (By.ID, "menu-notes")
    MENU_CONTACTS = (By.ID, "menu-contacts")
