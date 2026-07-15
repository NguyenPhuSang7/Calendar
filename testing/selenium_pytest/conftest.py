import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# Import page objects (we'll create these files next)
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.calendar_page import CalendarPage
from pages.appointment_page import AppointmentPage
from pages.notes_page import NotesPage
from pages.contacts_page import ContactsPage


def pytest_addoption(parser):
    """Command-line options for running tests."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser type: chrome or firefox",
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="http://localhost:3000",
        help="Base URL of the application under test",
    )


@pytest.fixture(scope="session")
def base_url(request):
    """Retrieve base_url command-line option."""
    return request.config.getoption("--base-url")


@pytest.fixture(scope="function")
def driver(request):
    """Initialize and quit WebDriver instance for each test function."""
    browser_type = request.config.getoption("--browser").lower()
    
    if browser_type == "chrome":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # Headless option can be toggled if needed
        # chrome_options.add_argument("--headless=new")
        
        service = ChromeService(ChromeDriverManager().install())
        web_driver = webdriver.Chrome(service=service, options=chrome_options)
        
    elif browser_type == "firefox":
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")
        # firefox_options.add_argument("-headless")
        
        service = FirefoxService(GeckoDriverManager().install())
        web_driver = webdriver.Firefox(service=service, options=firefox_options)
        
    else:
        raise ValueError(f"Unsupported browser: {browser_type}")

    # Set standard resolution explicitly
    web_driver.set_window_size(1920, 1080)
    
    yield web_driver
    
    web_driver.quit()


# --- Page Object Fixtures ---

@pytest.fixture
def login_page(driver, base_url):
    """Fixture to instantiate Login Page."""
    return LoginPage(driver, base_url)


@pytest.fixture
def register_page(driver, base_url):
    """Fixture to instantiate Register Page."""
    return RegisterPage(driver, base_url)


@pytest.fixture
def calendar_page(driver, base_url):
    """Fixture to instantiate Calendar Page."""
    return CalendarPage(driver, base_url)


@pytest.fixture
def appointment_page(driver, base_url):
    """Fixture to instantiate Appointment Page."""
    return AppointmentPage(driver, base_url)


@pytest.fixture
def notes_page(driver, base_url):
    """Fixture to instantiate Notes Page."""
    return NotesPage(driver, base_url)


@pytest.fixture
def contacts_page(driver, base_url):
    """Fixture to instantiate Contacts Page."""
    return ContactsPage(driver, base_url)


# --- Helper Fixtures ---

@pytest.fixture
def logged_in_session(driver, login_page, register_page):
    """Pre-authenticates a session to skip login for other modules."""
    login_page.navigate()
    if login_page.is_logged_in():
        login_page.logout()
        
    # Attempt to register standard test user
    register_page.register("Test User", "testuser@example.com", "", "testuser", "Password123!")
    
    # If not logged in (e.g. user already exists), log in directly
    if not login_page.is_logged_in():
        login_page.login("testuser", "Password123!")
        
    login_page.wait_for_dashboard_load()
    assert login_page.is_logged_in(), "Failed to pre-authenticate for test session"
    return driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save screenshot of browser state on test failure."""
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        try:
            if "driver" in item.fixturenames:
                driver = item.funcargs["driver"]
                import os
                screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
                driver.save_screenshot(screenshot_path)
                print(f"\n[QA FAILURE HOOK] Saved screenshot to: {screenshot_path}")
        except Exception as e:
            print(f"\n[QA FAILURE HOOK] Failed to save screenshot: {e}")
