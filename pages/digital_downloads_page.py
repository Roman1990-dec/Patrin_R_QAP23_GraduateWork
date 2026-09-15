from playwright.sync_api import Page

from pages.base_page import BasePage


class DigitalDownloadsPage(BasePage):
    """Page Object для страницы категории Digital downloads."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.page_title = page.locator(".page-title h1")
        self.sort_by_dropdown = page.locator("#products-orderby")
        self.display_dropdown = page.locator("#products-pagesize")
        self.view_mode_dropdown = page.locator("#products-viewmode")
        self.product_items = page.locator(".product-item")

    def open(self, url: str = "") -> "DigitalDownloadsPage":
        if url:
            return super().open(url)
        return super().open("/digital-downloads")

    def get_page_title(self) -> str:
        return self.get_text(self.page_title)

    def is_sort_by_visible(self) -> bool:
        return self.is_visible(self.sort_by_dropdown)

    def is_display_visible(self) -> bool:
        return self.is_visible(self.display_dropdown)

    def is_view_as_grid_visible(self) -> bool:
        return self.is_visible(self.view_mode_dropdown)

    def get_product_count(self) -> int:
        return self.product_items.count()

    def get_first_product_name(self) -> str:
        return self.get_text(self.product_items.first.locator(".product-title a"))

    def select_sort_by_name(self) -> "DigitalDownloadsPage":
        self.sort_by_dropdown.select_option(label="Name: A to Z")
        self.page.wait_for_load_state("networkidle")
        return self

    def select_sort_by_price_low_to_high(self) -> "DigitalDownloadsPage":
        self.sort_by_dropdown.select_option(label="Price: Low to High")
        self.page.wait_for_load_state("networkidle")
        return self

    def select_display_4(self) -> "DigitalDownloadsPage":
        self.display_dropdown.select_option(label="4")
        self.page.wait_for_load_state("networkidle")
        return self

    def select_view_as_list(self) -> "DigitalDownloadsPage":
        self.view_mode_dropdown.select_option(label="List")
        self.page.wait_for_load_state("networkidle")
        return self

    def open_product_by_href(self, href: str):
        product_link = self.page.locator(f".product-title a[href='{href}']")
        self.click(product_link)
        self.page.wait_for_load_state("networkidle")
        from pages.product_page import ProductPage

        return ProductPage(self.page, self.base_url)
