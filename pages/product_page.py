from playwright.sync_api import Page

from pages.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.product_name = page.locator(".product-name h1")
        self.product_price = page.locator(".product-price")
        self.add_to_cart_button = page.locator(".button-1.add-to-cart-button")
        self.qty_input = page.locator("input.qty-input")
        self.add_to_wishlist_button = page.locator("input[value='Add to wishlist']")
        self.add_to_compare_button = page.locator("input[value='Add to compare list']")
        self.reviews_link = page.locator(
            ".product-review-links a:has-text('Add your review')"
        )
        self.added_to_cart_notification = page.locator(".bar-notification")

    def get_product_name(self) -> str:
        return self.get_text(self.product_name)

    def get_product_price(self) -> str:
        return self.get_text(self.product_price)

    def is_add_to_cart_visible(self) -> bool:
        return self.is_visible(self.add_to_cart_button, timeout=5000)

    def is_qty_visible(self) -> bool:
        return self.is_visible(self.qty_input, timeout=5000)

    def is_add_to_wishlist_visible(self) -> bool:
        return self.is_visible(self.add_to_wishlist_button, timeout=5000)

    def is_add_to_compare_visible(self) -> bool:
        return self.is_visible(self.add_to_compare_button, timeout=5000)

    def get_reviews_text(self) -> str:
        return self.get_text(self.reviews_link)

    def add_to_cart(self) -> "ProductPage":
        self.click(self.add_to_cart_button)
        self.wait_visible(self.added_to_cart_notification)
        return self
