from pages.base_page import BasePage
from locators.calendar_locators import CalendarLocators
from locators.appointment_locators import AppointmentLocators
from selenium.webdriver.common.by import By

class CalendarPage(BasePage):
    def navigate(self):
        """Navigate to Calendar view."""
        self.navigate_via_sidebar("menu-calendar")

    def get_current_month_year(self):
        """Get text of the current month-year header."""
        return self.get_element_text(CalendarLocators.MONTH_HEADER)

    def go_to_next_month(self):
        """Click next month button."""
        self.click_element(CalendarLocators.NEXT_MONTH_BTN)

    def go_to_prev_month(self):
        """Click previous month button."""
        self.click_element(CalendarLocators.PREV_MONTH_BTN)

    def is_calendar_grid_visible(self):
        """Check if calendar grid is rendered."""
        return self.is_element_visible(CalendarLocators.CALENDAR_GRID)

    def get_appointment_elements(self):
        """Find and return all appointment elements in the active daily agenda panel."""
        return self.driver.find_elements(*AppointmentLocators.AGENDA_APPOINTMENT_CARD)

    def is_sidebar_hidden(self):
        """Check if sidebar is hidden/collapsed based on screen width and class names."""
        if not self.is_element_present(CalendarLocators.SIDEBAR_CONTAINER):
            return True
        width = self.driver.execute_script("return window.innerWidth;")
        if width <= 760:
            sidebar = self.driver.find_element(*CalendarLocators.SIDEBAR_CONTAINER)
            classes = sidebar.get_attribute("class") or ""
            return "is-open" not in classes
        else:
            # On desktop it's always visible
            return False

    def is_hamburger_menu_visible(self):
        """Check if mobile hamburger toggle button is displayed."""
        return self.is_element_visible(CalendarLocators.MOBILE_HAMBURGER_BTN, timeout=2)

    def check_layout_overlap(self):
        """Verify navigation hamburger button does not overlap the topbar title header."""
        title_header = (By.CSS_SELECTOR, "header.topbar h1")
        if not self.is_element_visible(title_header):
            return True
        return self.verify_elements_no_overlap(
            CalendarLocators.MOBILE_HAMBURGER_BTN,
            title_header
        )

    def select_day_in_current_month(self, day_number):
        """Click on the calendar day cell with the specified day number."""
        cells = self.driver.find_elements(*CalendarLocators.CALENDAR_DAY_CELL)
        for cell in cells:
            try:
                classes = cell.get_attribute("class") or ""
                if "outside" in classes:
                    continue
                day_num_el = cell.find_element(*CalendarLocators.DAY_NUMBER_SPN)
                if int(day_num_el.text.strip()) == int(day_number):
                    cell.click()
                    return True
            except Exception:
                continue
        return False
