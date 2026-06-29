from pages.base_page import BasePage

class CartPage(BasePage):
    CART_ITEMS = ".cart-item-row"
    QUANTITY_INPUT = ".qty-input"
    UPDATE_CART_BUTTON = "input[name='updatecart']"
    EMPTY_CART_MESSAGE = ".order-summary-content"

    def open(self):
        """Открывает страницу корзины."""
        return super().open("/cart")

    def get_number_of_items(self) -> int:
        """Возвращает количество товаров в корзине."""
        return self.page.locator(self.CART_ITEMS).count()

    def get_quantity_value(self, item_index: int = 0) -> str:
        """Возвращает значение поля количества для товара с указанным индексом."""
        items = self.page.locator(self.CART_ITEMS)
        return items.nth(item_index).locator(self.QUANTITY_INPUT).input_value()

    def update_quantity(self, quantity: str, item_index: int = 0):
        """Обновляет количество товара."""
        items = self.page.locator(self.CART_ITEMS)
        qty_input = items.nth(item_index).locator(self.QUANTITY_INPUT)
        qty_input.clear()
        qty_input.fill(quantity)
        self.click(self.UPDATE_CART_BUTTON)
        return self

    def is_empty(self) -> bool:
        """Проверяет, пуста ли корзина."""
        text = self.page.locator(self.EMPTY_CART_MESSAGE).text_content()
        return "Your Shopping Cart is empty!" in text