from pages.base_page import BasePage

class HomePage(BasePage):
    BOOKS_CATEGORY_LINK = ".top-menu a[href='/books']"

    def open(self):
        super().open("/")
        self.page.wait_for_selector(".top-menu", state="visible", timeout=3000)
        return self

    def go_to_books_category(self):
        self.click(self.BOOKS_CATEGORY_LINK)
        # Ждём полной загрузки страницы (включая динамические элементы)
        self.page.wait_for_load_state("networkidle")
        # Ждём полной загрузки сетки товаров
        self.page.wait_for_selector(".product-grid", state="visible", timeout=3000)
        from pages.books_page import BooksPage
        return BooksPage(self.page, self.base_url)