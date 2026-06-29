from pages.base_page import BasePage


class BooksPage(BasePage):
    def open_computing_book(self):
        # Ждём появления сетки товаров
        self.page.wait_for_selector(".product-grid", state="visible", timeout=10000)

        # Используем точный селектор, скопированный из браузера
        exact_selector = "body > div.master-wrapper-page > div.master-wrapper-content > div.master-wrapper-main > div.center-2 > div.page.category-page > div.page-body > div.product-grid > div:nth-child(1) > div > div.details > h2 > a"

        # Ждём, пока элемент станет видимым
        self.page.wait_for_selector(exact_selector, state="visible", timeout=15000)

        # Кликаем по нему (Playwright автоматически прокрутит, если нужно)
        self.page.locator(exact_selector).click()

        # Ждём загрузки страницы товара
        self.page.wait_for_selector(
            ".button-1.add-to-cart-button", state="visible", timeout=10000
        )

        from pages.product_page import ProductPage

        return ProductPage(self.page, self.base_url)
