from pages.base_page import BasePage

class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.url="https://practicetestautomation.com/practice-test-login/"

        #Define Locators of this page in __init__()
        self.username_field = page.locator("#username")
        self.password_field = page.locator("#password")
        self.login_button = page.locator("#submit")

    def open(self):
        self.navigate(self.url)

    def login(self, username, password):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()

    def get_error_msg(self):
        error = self.page.locator("#error")
        return self.get_text(error)
    
    def is_login_successfull(self):
        return "logged-in-successfully" in self.page.url

    def get_errors_as_list(self):
        errors_list = self.page.locator("#error").all()
        return [ 
            err.text_content().strip()
            for err in errors_list 
            if len(err.text_content().strip())>0
        ]

    