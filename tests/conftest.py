import os
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

#---1. Environment config-----------------------------
#Sets the base for page.goto("/login") to work
@pytest.fixture(scope="session")
def base_url():
    #Read from env var - easy to switch environments
    return os.getenv("BASE_URL", "https://practicetestautomation.com")

#---2. Context defaults-applies to every test-----------------------
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return{
        **browser_context_args,
        "viewport":{"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "locale": "en-US",
        "timezone_id": "Asia/Kolkata"
    }

#---3. Global timeouts-run before every test--------------------
@pytest.fixture(autouse=True)
def configure_timeouts(page:Page):
    page.set_default_timeout(10000) #Wait up to 10 seconds before failing
    page.set_default_navigation_timeout(30000) #Wait up to 30 seconds for page to load
    yield

#---4. Page object fixtures--------------------
@pytest.fixture
def login_page(page: Page, base_url):
    lp = LoginPage(page)
    lp.open()
    return lp

@pytest.fixture
def dashboard_page(page:Page):
    return DashboardPage(page)

#---5. Pre-authenticated fixture--------------------
@pytest.fixture(scope="session")
def auth_state_file(browser):
    """Login once per session, store auth cookies for whole session"""
    os.makedirs("auth", exist_ok=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://practicetestautomation.com/practice-test-login/")
    page.locator("#username").fill("student")
    page.locator("#password").fill("Password123")
    page.locator("#submit").click()
    page.wait_for_url("**/logged-in-successfully/**")
    context.storage_state(path="auth/state.json")  #save cookies+localStorage
    context.close()
    yield "auth/state.json"
    #cleanup: os.remove("auth/state.json")

@pytest.fixture
def authenticated_page(browser, auth_state_file):
    """Every test using this fixture starts already logged in"""
    context = browser.new_context(storage_state=auth_state_file) #injects saved cookies
    page = context.new_page()
    yield page
    context.close()

    # Mobile emulation
@pytest.fixture
def mobile_page(playwright, browser):
    device = playwright.devices["iPhone 13"]
    context = browser.new_context(**device)
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def recorded_page(browser):
    context = browser.new_context(
        record_video_dir="videos/",
        record_video_size={"width": 1280, "height":720}
    )
    page = context.new_page()
    yield page
    context.close() # video saved on context.close()
