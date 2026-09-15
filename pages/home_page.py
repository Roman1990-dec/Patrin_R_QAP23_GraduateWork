from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.top_menu = page.locator(".top-menu")
        self.logo = page.locator(".header-logo a img")
        self.register_link = page.locator("a.ico-register")
        self.login_link = page.locator("a.ico-login")
        self.cart_link = page.locator("#topcartlink a.ico-cart")
        self.wishlist_link = page.locator(".header-links a.ico-wishlist")
        self.search_input = page.locator("#small-searchterms")
        self.search_button = page.locator("input[value='Search']")
        self.digital_downloads_link = page.locator(
            ".top-menu a[href='/digital-downloads']"
        )
        self.page_title = page.locator(".page-title h1")
        self.search_results = page.locator(".product-item")
        self.search_no_results = page.locator(".result")
        self.newsletter_email = page.locator("#newsletter-email")
        self.newsletter_subscribe = page.locator("input[value='Subscribe']")
        self.poll_title = page.locator("text=Do you like nopCommerce?")
        self.poll_vote_button = page.locator("input[value='Vote']")
        self.poll_vote_error = page.locator(".poll-vote-error")
        self.featured_products = page.locator(".product-item")
        self.popular_tags = page.locator(".tags a")
        self.view_all_tags_link = page.locator(".view-all a")
        self.digital_tag_link = page.locator("a[href='/producttag/16/digital']")
        self.footer = page.locator(".footer")

    def open(self, url: str = "") -> "HomePage":
        if url:
            return super().open(url)
        super().open("/")
        self.wait_visible(self.top_menu)
        return self

    def go_to_digital_downloads(self):
        self.click(self.digital_downloads_link)
        self.wait_visible(self.page_title)
        from pages.digital_downloads_page import DigitalDownloadsPage

        return DigitalDownloadsPage(self.page, self.base_url)

    def click_top_menu_link_by_href(self, href: str) -> "HomePage":
        self.click(self.page.locator(f".top-menu a[href='{href}']"))
        return self

    def click_footer_link_by_text(self, text: str) -> "HomePage":
        self.click(self.footer.locator(f"a:has-text('{text}')"))
        return self

    def wait_for_url(self, url: str, timeout: int = 10000) -> "HomePage":
        self.page.wait_for_url(url, timeout=timeout)
        return self

    def is_logo_visible(self) -> bool:
        return self.is_visible(self.logo)

    def is_register_link_visible(self) -> bool:
        return self.is_visible(self.register_link)

    def click_register_link(self) -> "HomePage":
        self.click(self.register_link)
        return self

    def is_login_link_visible(self) -> bool:
        return self.is_visible(self.login_link)

    def click_login_link(self) -> "HomePage":
        self.click(self.login_link)
        return self

    def is_cart_link_visible(self) -> bool:
        return self.is_visible(self.cart_link)

    def click_cart_link(self) -> "HomePage":
        self.click(self.cart_link)
        return self

    def is_wishlist_link_visible(self) -> bool:
        return self.is_visible(self.wishlist_link)

    def click_wishlist_link(self) -> "HomePage":
        self.click(self.wishlist_link)
        return self

    def is_search_field_visible(self) -> bool:
        return self.is_visible(self.search_input) and self.is_visible(
            self.search_button
        )

    def search(self, query: str) -> "HomePage":
        self.fill(self.search_input, query)
        self.click(self.search_button)
        return self

    def get_search_results_count(self) -> int:
        return self.search_results.count()

    def get_search_message(self) -> str:
        return self.get_text(self.search_no_results)

    def is_newsletter_visible(self) -> bool:
        return self.is_visible(self.newsletter_email) and self.is_visible(
            self.newsletter_subscribe
        )

    def get_poll_question(self) -> str:
        return self.get_text(self.poll_title)

    def is_poll_radio_visible(self, answer_id: str) -> bool:
        return self.is_visible(self.page.locator(f"#{answer_id}"))

    def get_poll_label_text(self, answer_id: str) -> str:
        return self.get_text(self.page.locator(f"label[for='{answer_id}']"))

    def is_poll_vote_visible(self) -> bool:
        return self.is_visible(self.poll_vote_button)

    def select_poll_answer(self, answer_id: str) -> "HomePage":
        self.click(self.page.locator(f"#{answer_id}"))
        return self

    def vote(self) -> "HomePage":
        self.click(self.poll_vote_button)
        return self

    def get_vote_error(self) -> str:
        return self.get_text(self.poll_vote_error)

    def get_featured_products_count(self) -> int:
        return self.featured_products.count()

    def get_popular_tags_count(self) -> int:
        return self.popular_tags.count()

    def click_view_all_tags(self) -> "HomePage":
        self.click(self.view_all_tags_link)
        return self

    def click_digital_tag(self) -> "HomePage":
        self.click(self.digital_tag_link)
        return self

    def is_digital_tag_visible(self) -> bool:
        return self.is_visible(self.digital_tag_link)
