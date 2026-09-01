from pages.base_page import BasePage


class ProductPage(BasePage):
    PRODUCT_NAME = ".product-name h1"
    PRODUCT_PRICE = ".product-price"
    ADD_TO_CART_BUTTON = ".button-1.add-to-cart-button"
    QTY_INPUT = "input.qty-input"
    ADD_TO_WISHLIST_BUTTON = "input[value='Add to wishlist']"
    ADD_TO_COMPARE_BUTTON = "input[value='Add to compare list']"
    REVIEWS_LINK = ".product-review-links a:has-text('Add your review')"

    def get_product_name(self) -> str:
        return self.get_text(self.PRODUCT_NAME)

    def get_product_price(self) -> str:
        return self.get_text(self.PRODUCT_PRICE)

    def is_add_to_cart_visible(self) -> bool:
        try:
            self.page.wait_for_selector(
                self.ADD_TO_CART_BUTTON, state="visible", timeout=5000
            )
            return True
        except TimeoutError:
            return False

    def is_qty_visible(self) -> bool:
        try:
            self.page.wait_for_selector(self.QTY_INPUT, state="visible", timeout=5000)
            return True
        except TimeoutError:
            return False

    def is_add_to_wishlist_visible(self) -> bool:
        try:
            self.page.wait_for_selector(
                self.ADD_TO_WISHLIST_BUTTON, state="visible", timeout=5000
            )
            return True
        except TimeoutError:
            return False

    def is_add_to_compare_visible(self) -> bool:
        try:
            self.page.wait_for_selector(
                self.ADD_TO_COMPARE_BUTTON, state="visible", timeout=5000
            )
            return True
        except TimeoutError:
            return False

    def get_reviews_text(self) -> str:
        return self.get_text(self.REVIEWS_LINK)

    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)
        self.page.wait_for_timeout(1000)
        return self
