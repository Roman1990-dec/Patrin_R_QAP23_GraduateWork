from pages.base_page import BasePage


class HomePage(BasePage):
    # Локаторы
    NEWSLETTER_EMAIL = "#newsletter-email"
    NEWSLETTER_SUBSCRIBE = "input[value='Subscribe']"
    POLL_RADIO = "#pollanswers-1"
    POLL_VOTE = "input[value='Vote']"
    FEATURED_PRODUCTS = ".product-item"
    POPULAR_TAGS = ".tag-item"

    def open(self):
        super().open("/")
        self.page.wait_for_selector(".top-menu", state="visible", timeout=3000)
        return self

    def go_to_digital_downloads(self):
        """Переход в раздел Digital downloads через верхнее меню."""
        self.click(".top-menu a[href='/digital-downloads']")
        # Ждём загрузки страницы (появление заголовка)
        self.page.wait_for_selector(".page-title h1", state="visible", timeout=10000)
        from pages.digital_downloads_page import DigitalDownloadsPage

        return DigitalDownloadsPage(self.page, self.base_url)
