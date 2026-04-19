import os
import logging
from playwright.sync_api import Page, Locator, expect

#Set up module-level logger- evry subclass inherits this 
logger = logging.getLogger(__name__)

class BasePage:
    """Base class for all page objects. Never instantiate directly."""

    def __init__(self, page:Page) -> None:
        self.page = page
        self.timeout = 10_000 # 10 seconds default

#---Navigation--------------------------
    def navigate(self, url: str) -> None:
        logger.info(f"Navigating to: {url}")
        self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()
    
    def get_url(self) -> str:
        return self.page.url
    
    def reload(self) -> None:
        self.page.reload()
    
#---Element helpers--------------------- 
    def get_text(self, locator: Locator) -> str:
        """Return stripped text content of an element"""
        return (locator.text_content() or "").strip()  
    
    def get_all_texts(self, locator: Locator) -> list[str]:
        """Return list of non-empty text strings for all matches"""
        return [t.strip() for t in locator.all_text_contents() if t.strip()]

    def is_visible(self, locator: Locator) -> bool:
        return locator.is_visible()
    
    def wait_for_visible(self, locator: Locator, timeout: int=10_000) -> None:
        locator.wait_for(state="visible", timeout=timeout)

    def wait_for_hidden(self, locator: Locator, timeout: int=10_000) -> None:
        locator.wait_for(state="hidden", timeout=timeout)

# ---Assertions (wrap expect for reuse)--------------
    def assert_visible(self, locator: Locator, msg: str="") -> None:
        expect(locator).to_be_visible()

    def assert_text(self, locator: Locator, text:str) -> None:
        expect(locator).to_have_text(text)

    def assert_url_contains(self, fragment: str) -> None:
        expect(self.page).to_have_url(f"**{fragment}**")

# ---Screenshots------------------------
    def screenshot(self, name: str, folder: str="screenshots") -> str:
        os.makedirs(folder, exist_ok=True) #creates folder automatically if it doesn't exist
        path = f"{folder}/{name}.png"
        self.page.screenshot(path=path, full_page=True)
        logger.info(f"Screenshot: {path}")
        return path
# ---Scroll------------------------------
    def scroll_to_bottom(self) -> None:
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_into_view(self, locator: Locator) -> None:
        locator.scroll_into_view_if_needed()