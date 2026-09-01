from pages.base_page import BasePage


class DigitalDownloadsPage(BasePage):
    # Локаторы
    PAGE_TITLE = ".page-title h1"
    SORT_BY_DROPDOWN = "#products-orderby"
    DISPLAY_DROPDOWN = "#products-pagesize"
    VIEW_AS_GRID = "#products-viewmode"
    PRODUCT_ITEMS = ".product-item"

    def open(self, url: str = ""):
        """Открывает страницу Digital downloads напрямую или переданный url."""
        if url:
            return super().open(url)
        return super().open("/digital-downloads")

    def get_page_title(self) -> str:
        return self.get_text(self.PAGE_TITLE)

    def is_sort_by_visible(self) -> bool:
        return self.is_visible(self.SORT_BY_DROPDOWN)

    def is_display_visible(self) -> bool:
        return self.is_visible(self.DISPLAY_DROPDOWN)

    def is_view_as_grid_visible(self) -> bool:
        return self.is_visible(self.VIEW_AS_GRID)

    def get_product_count(self) -> int:
        return self.page.locator(self.PRODUCT_ITEMS).count()

    def open_product_by_href(self, href: str):
        """Открывает товар по его href (например, '/album-3'), кликая по текстовой ссылке."""
        # Ищем ссылку внутри .product-title, чтобы избежать ссылки на картинку
        self.click(f".product-title a[href='{href}']")
        self.page.wait_for_load_state("networkidle")
        from pages.product_page import ProductPage

        return ProductPage(self.page, self.base_url)
