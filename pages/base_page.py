import os
from playwright.sync_api import Page

class BasePage:
    def __init__(self, page:Page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url)

    def get_title(self):
        return self.page.title()
    
    def take_screenshot(self, name):
        os.makedirs("screenshots", exist_ok=True) #creates folder automatically if it doesn't exist
        self.page.screenshot(path=f"screenshots/{name}.png")
        print(f"Screenhot saved: screenshots/{name}.png")

    def get_text(self,locator):
        return locator.text_content().strip()   