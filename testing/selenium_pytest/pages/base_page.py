from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By

class BasePage:
    def __init__(self, driver, base_url="http://localhost:3000"):
        self.driver = driver
        self.base_url = base_url
        self.timeout = 10

    def navigate_to(self, path=""):
        """Navigates to the specified path appended to the base URL."""
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        self.driver.get(url)

    def navigate_via_sidebar(self, button_id):
        """Navigate to a view by clicking its sidebar button, handling mobile hamburger toggle if necessary."""
        # Ensure we are logged in / on the app shell
        app_shell_locator = (By.CLASS_NAME, "app-shell")
        try:
            self.wait_for_element_visible(app_shell_locator, timeout=5)
        except TimeoutException:
            self.navigate_to("/")
            self.wait_for_element_visible(app_shell_locator, timeout=5)
            
        # If mobile hamburger button is visible and sidebar is hidden, click hamburger first
        hamburger_btn = (By.CSS_SELECTOR, "button.menu-button")
        sidebar = (By.CLASS_NAME, "sidebar")
        if self.is_element_visible(hamburger_btn, timeout=1):
            sidebar_el = self.driver.find_element(*sidebar)
            classes = sidebar_el.get_attribute("class") or ""
            # If sidebar is not open (does not contain is-open class)
            if "is-open" not in classes:
                self.click_element(hamburger_btn)
                # Wait for sidebar to open (transition of classes)
                WebDriverWait(self.driver, 3).until(
                    lambda d: "is-open" in sidebar_el.get_attribute("class")
                )
                
        # Now click the sidebar button
        btn_locator = (By.ID, button_id)
        self.click_element(btn_locator)

    def wait_for_element_visible(self, locator, timeout=None):
        """Wait until an element is visible on the DOM."""
        t = timeout or self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait until an element is clickable (visible and enabled)."""
        t = timeout or self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_element_invisible(self, locator, timeout=None):
        """Wait until an element is invisible or removed from DOM."""
        t = timeout or self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.invisibility_of_element_located(locator)
        )

    def click_element(self, locator, timeout=None):
        """Find an element, wait for it to be clickable, and click it. Falls back to JS click if intercepted."""
        element = self.wait_for_element_clickable(locator, timeout)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def enter_text(self, locator, text, clear_first=True, timeout=None):
        """Find an input, wait for visibility, and set its value using React-compatible JS setters."""
        element = self.wait_for_element_visible(locator, timeout)
        js_script = """
        var el = arguments[0];
        var val = arguments[1];
        var proto = el.tagName === 'TEXTAREA' ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
        var setter = Object.getOwnPropertyDescriptor(proto, 'value').set;
        setter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        """
        self.driver.execute_script(js_script, element, text)

    def close_modal_if_open(self):
        """Close any open modal by clicking Cancel or pressing Escape key."""
        modal_backdrop = (By.CLASS_NAME, "modal-backdrop")
        if self.is_element_present(modal_backdrop):
            cancel_btn = (By.CSS_SELECTOR, ".modal-actions button.secondary-button")
            if self.is_element_visible(cancel_btn, timeout=1):
                try:
                    btn = self.driver.find_element(*cancel_btn)
                    self.driver.execute_script("arguments[0].click();", btn)
                    self.wait_for_element_invisible(modal_backdrop, timeout=3)
                    return
                except Exception:
                    pass
            # Fallback: Send ESC key to close
            from selenium.webdriver.common.keys import Keys
            try:
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                self.wait_for_element_invisible(modal_backdrop, timeout=3)
            except Exception:
                pass

    def get_element_text(self, locator, timeout=None):
        """Retrieve the text of an element."""
        element = self.wait_for_element_visible(locator, timeout)
        return element.text

    def is_element_visible(self, locator, timeout=2):
        """Check if an element is visible, with a short timeout to prevent long hangs."""
        try:
            self.wait_for_element_visible(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_present(self, locator):
        """Check if an element exists in the DOM, regardless of visibility."""
        elements = self.driver.find_elements(*locator)
        return len(elements) > 0

    def resize_window(self, width, height=800):
        """Resize browser window to test responsive layouts."""
        self.driver.set_window_size(width, height)

    def verify_elements_no_overlap(self, locator_a, locator_b):
        """Verify that two elements are not overlapping vertically or horizontally.
        Returns True if they do not overlap, False if they do.
        """
        elem_a = self.wait_for_element_visible(locator_a)
        elem_b = self.wait_for_element_visible(locator_b)
        
        rect_a = elem_a.rect
        rect_b = elem_b.rect
        
        # Check coordinates: rect structure is {'x': val, 'y': val, 'width': val, 'height': val}
        overlap_x = not (rect_a['x'] + rect_a['width'] <= rect_b['x'] or rect_b['x'] + rect_b['width'] <= rect_a['x'])
        overlap_y = not (rect_a['y'] + rect_a['height'] <= rect_b['y'] or rect_b['y'] + rect_b['height'] <= rect_a['y'])
        
        # Elements overlap only if they overlap on both X and Y axes
        return not (overlap_x and overlap_y)

    def wait_for_dashboard_load(self, timeout=5):
        """Wait until the app-shell dashboard is loaded."""
        self.wait_for_element_visible((By.CLASS_NAME, "app-shell"), timeout)
