import allure
import pytest

from pages.home_page import HomePage


@allure.feature("Раздел Digital Downloads")
class TestDigitalDownloads:
    @pytest.fixture(autouse=True)
    def setup(self, page, base_url):
        self.home_page = HomePage(page, base_url)
        self.home_page.open()
        self.downloads_page = self.home_page.go_to_digital_downloads()

    @allure.story("Страница категории")
    @allure.title("Проверка загрузки страницы Digital downloads")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Проверяет, что страница категории Digital downloads корректно "
        "загружается: правильный URL, заголовок, элементы управления списком, "
        "наличие товаров."
    )
    def test_digital_downloads_page_loaded(self):
        assert "/digital-downloads" in self.downloads_page.get_current_url(), (
            f"URL не соответствует ожидаемому: {self.downloads_page.get_current_url()}"
        )
        assert "Digital downloads" in self.downloads_page.get_page_title(), (
            "Заголовок страницы не соответствует ожидаемому"
        )
        assert self.downloads_page.is_sort_by_visible(), "Список сортировки не виден"
        assert self.downloads_page.is_display_visible(), "Список отображения не виден"
        assert self.downloads_page.is_view_as_grid_visible(), (
            "Переключатель вида отображения не виден"
        )
        assert self.downloads_page.get_product_count() > 0, "На странице нет товаров"

    @allure.story("Карточка товара")
    @allure.title("Проверка карточки товара '3rd Album'")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Проверяет, что карточка товара '3rd Album' открывается корректно "
        "и содержит ожидаемые данные: название, цену, кнопку 'Add to cart', "
        "поле ввода количества."
    )
    def test_3rd_album_product_card(self):
        product_page = self.downloads_page.open_product_by_href("/album-3")

        assert "/album-3" in product_page.get_current_url(), (
            f"Не удалось открыть карточку товара: {product_page.get_current_url()}"
        )
        assert "3rd Album" in product_page.get_product_name(), (
            f"Название товара не соответствует: {product_page.get_product_name()}"
        )
        assert "1.00" in product_page.get_product_price(), (
            f"Цена товара не соответствует: {product_page.get_product_price()}"
        )
        assert product_page.is_add_to_cart_visible(), "Кнопка 'Add to cart' не видна"
        assert product_page.is_qty_visible(), "Поле Qty не видно"

    @allure.story("Карточка товара")
    @allure.title("Проверка ссылки на отзывы в карточке товара")
    @allure.severity(allure.severity_level.MINOR)
    def test_3rd_album_reviews_link_visible(self):
        product_page = self.downloads_page.open_product_by_href("/album-3")
        reviews = product_page.get_reviews_text()
        assert "review" in reviews.lower(), "Ссылка на отзывы не найдена"

    @allure.story("Страница категории")
    @allure.title("Сортировка товаров по имени (A to Z)")
    @allure.severity(allure.severity_level.MINOR)
    def test_sort_by_name(self):
        self.downloads_page.select_sort_by_name()
        first_name = self.downloads_page.get_first_product_name()
        assert "3rd Album" in first_name, (
            f"После сортировки первым должен быть '3rd Album', получено: {first_name}"
        )

    @allure.story("Страница категории")
    @allure.title("Сортировка товаров по цене (возрастание)")
    @allure.severity(allure.severity_level.MINOR)
    def test_sort_by_price_low_to_high(self):
        self.downloads_page.select_sort_by_price_low_to_high()
        first_name = self.downloads_page.get_first_product_name()
        assert first_name, "После сортировки не удалось получить имя первого товара"

    @allure.story("Страница категории")
    @allure.title("Изменение количества отображаемых товаров на 4")
    @allure.severity(allure.severity_level.MINOR)
    def test_display_4_products(self):
        self.downloads_page.select_display_4()
        assert self.downloads_page.get_product_count() <= 4, (
            f"Ожидалось не более 4 товаров, получено: {self.downloads_page.get_product_count()}"
        )

    @allure.story("Страница категории")
    @allure.title("Переключение вида отображения на список")
    @allure.severity(allure.severity_level.MINOR)
    def test_view_as_list(self):
        self.downloads_page.select_view_as_list()
        assert self.downloads_page.get_product_count() > 0, (
            "После переключения на вид 'список' товары не отображаются"
        )
        assert "viewmode=list" in self.downloads_page.get_current_url(), (
            f"URL не содержит 'viewmode=list': {self.downloads_page.get_current_url()}"
        )
