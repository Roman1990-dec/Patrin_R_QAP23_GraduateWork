from pages.base_page import BasePage

class ProductPage(BasePage):
    # Более точный CSS-селектор для кнопки "Add to cart" на странице товара
    ADD_TO_CART_BUTTON = ".button-1.add-to-cart-button"

    def add_to_cart(self):
        """Нажимает кнопку добавления в корзину."""
        self.click(self.ADD_TO_CART_BUTTON)
        # Даём время на обновление счётчика корзины
        self.page.wait_for_timeout(1000)
        return self
    