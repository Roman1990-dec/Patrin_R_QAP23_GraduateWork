from playwright.sync_api import Page


class BasePage:
    """Базовый класс для всех Page Object'ов."""

    def __init__(self, page: Page, base_url : str = "https://demowebshop.tricentis.com"):
        self.page = page
        self.base_url = base_url

    def open(self, url: str = ""):
        """Открывает полный URL, склеивая base_url + url."""
        full_url = self.base_url + url
        self.page.goto(full_url)
        return self

    def click(self, selector: str):
        """Клик по элементу с автоматическим ожиданием."""
        self.page.locator(selector).click()
        return self

    def fill(self, selector: str, text: str):
        """Очистить поле и ввести текст."""
        locator = self.page.locator(selector)
        locator.clear()
        locator.fill(text)
        return self

    def get_text(self, selector: str) -> str:
        """Возвращает текстовое содержимое элемента."""
        return self.page.locator(selector).text_content()

    def is_visible(self, selector: str) -> bool:
        """Проверяет, видим ли элемент на странице."""
        return self.page.locator(selector).is_visible()
