from pages.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.heading_locator = page.locator("h1")

    def is_displayed(self):
        return self.heading_locator.is_visible()

    def get_heading(self):
        return self.get_text(self.heading_locator)   # inherited from BasePage

    def get_nav_links(self):
        links = self.page.locator("a").all()
        return [
            link.text_content().strip()
            for link in links
            if link.text_content().strip()   # skip blank anchor tags
        ]

    def logout(self):
        self.page.get_by_text("Log out", exact=True).click()

    def get_current_url(self):
        return self.page.url