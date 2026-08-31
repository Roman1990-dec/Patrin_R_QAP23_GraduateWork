from pages.base_page import BasePage

class HomePage(BasePage):

    NEWSLETTER_EMAIL = "#newsletter-email"
    NEWSLETTER_SUBSCRIBE = "input[value='Subscribe']"
    POLL_RADIO = "#pollanswers-1"  # первый вариант ответа
    POLL_VOTE = "input[value='Vote']"
    FEATURED_PRODUCTS = ".product-item"
    POPULAR_TAGS = ".tag-item"

    def open(self):
        super().open("/")
        self.page.wait_for_selector(".top-menu", state="visible", timeout=3000)
        return self