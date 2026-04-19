from playwright.sync_api import sync_playwright
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage

def run_scenario_a(login, dashboard):
    print("-----Scenario A: Valid login-------")
    login.open()
    login.login("student", "Password123")

    assert dashboard.is_displayed(), "Dashboard not visible after login!"
    print(f"  Heading : {dashboard.get_heading()}")
    print(f"  Nav links: {dashboard.get_nav_links()}")
    print(f"  URL     : {dashboard.get_current_url()}")

    dashboard.take_screenshot("scenario_a_dashboard")
    dashboard.logout()

    assert "practice-test-login" in login.page.url, "Logout did not redirect!"
    print("  [PASS] Logged out successfully")


def run_scenario_b(login):
    print("\n--- Scenario B: Wrong username ---")
    login.open()
    login.login("wronguser", "Password123")

    errors = login.get_errors_as_list()
    assert len(errors) > 0, "Expected errors but got none!"

    for msg in errors:
        print(f"  Error: '{msg}'")

    login.take_screenshot("scenario_b_wrong_user")
    print("  [PASS] Error messages captured correctly")


def run_scenario_c(login):
    print("\n--- Scenario C: Empty fields ---")
    login.open()
    login.login("", "")   # submit with no input

    errors = login.get_errors_as_list()
    print(f"  Errors found: {len(errors)}")
    for msg in errors:
        print(f"  Error: '{msg}'")

    login.take_screenshot("scenario_c_empty_fields")
    print("  [PASS] Empty field errors captured")


def main():
    with sync_playwright() as p:
        browser   = p.chromium.launch(headless=False)
        page      = browser.new_page()
        login     = LoginPage(page)
        dashboard = DashboardPage(page)   # same page object, different view
        run_scenario_a(login, dashboard)
        run_scenario_b(login)
        run_scenario_c(login)

        #--- Test 1: valid login 
        # login.open()
        # login.login("student","Password123")

        # if login.is_login_successfull():
        #     print("[PASS] Login successfully!")
        # else: 
        #     print("[FAIL] Login did not succeed")

        #------Invalid Login-----
        # login.open()
        # login.login("student", "wrongpassword")

        # if not login.is_login_successfull():
        #     error = login.get_error_msg()
        #     print(f"[PASS] Got expected error: {error}")
        #     login.take_screenshot("login_failed")
        # else:
        #     print("[FAIL] Should have failed but didn't")

        browser.close()
        
if __name__ == "__main__":
    main()
