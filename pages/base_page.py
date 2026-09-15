from playwright.sync_api import Locator, Page, TimeoutError


class BasePage:
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page, base_url: str = "https://demowebshop.tricentis.com"):
        self.page = page
        self.base_url = base_url

    def open(self, url: str = ""):
        self.page.goto(self.base_url + url)
        return self

    def wait_visible(self, locator: Locator, timeout: int | None = None) -> Locator:
        locator.wait_for(state="visible", timeout=timeout or self.DEFAULT_TIMEOUT)
        return locator

    def is_visible(self, locator: Locator, timeout: int = 3000) -> bool:
        try:
            locator.wait_for(state="visible", timeout=timeout)
            return True
        except TimeoutError:
            return False

    def click(self, locator: Locator) -> "BasePage":
        self.wait_visible(locator)
        locator.click()
        return self

    def fill(self, locator: Locator, text: str) -> "BasePage":
        self.wait_visible(locator)
        locator.clear()
        locator.fill(text)
        return self

    def get_text(self, locator: Locator) -> str:
        self.wait_visible(locator)
        return locator.text_content() or ""

    def get_current_url(self) -> str:
        return self.page.url
