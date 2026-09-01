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

    @allure.story("Навигация")
    @allure.title("Переход в раздел Digital downloads")
    @allure.severity(allure.severity_level.NORMAL)
    def test_digital_downloads_navigation(self):
        assert "/digital-downloads" in self.downloads_page.page.url, (
            "URL не соответствует ожидаемому"
        )

    @allure.story("Страница списка")
    @allure.title("Проверка заголовка страницы")
    @allure.severity(allure.severity_level.NORMAL)
    def test_digital_downloads_page_title(self):
        title = self.downloads_page.get_page_title()
        assert "Digital downloads" in title, (
            f"Заголовок не соответствует, получено: {title}"
        )

    @allure.story("Страница списка")
    @allure.title("Проверка наличия выпадающего списка сортировки")
    @allure.severity(allure.severity_level.MINOR)
    def test_digital_downloads_sort_by_visible(self):
        assert self.downloads_page.is_sort_by_visible(), "Список сортировки не виден"

    @allure.story("Страница списка")
    @allure.title("Проверка наличия выпадающего списка отображения")
    @allure.severity(allure.severity_level.MINOR)
    def test_digital_downloads_display_visible(self):
        assert self.downloads_page.is_display_visible(), "Список отображения не виден"

    @allure.story("Страница списка")
    @allure.title("Проверка наличия переключателя вида 'Grid'")
    @allure.severity(allure.severity_level.MINOR)
    def test_digital_downloads_view_as_grid_visible(self):
        assert self.downloads_page.is_view_as_grid_visible(), (
            "Переключатель 'View as Grid' не виден"
        )

    @allure.story("Страница списка")
    @allure.title("Проверка, что на странице есть товары")
    @allure.severity(allure.severity_level.NORMAL)
    def test_digital_downloads_has_products(self):
        count = self.downloads_page.get_product_count()
        assert count > 0, "На странице нет товаров"

    @allure.story("Карточка товара")
    @allure.title("Открытие карточки '3rd Album'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_product_page_3rd_album_navigation(self):
        product_page = self.downloads_page.open_product_by_href("/album-3")
        assert "/album-3" in product_page.page.url, "Не удалось открыть карточку товара"

    @allure.story("Карточка товара")
    @allure.title("Проверка названия товара")
    @allure.severity(allure.severity_level.NORMAL)
    def test_product_name(self):
        product_page = self.downloads_page.open_product_by_href("/album-3")
        name = product_page.get_product_name()
        assert "3rd Album" in name, f"Название не соответствует, получено: {name}"

    @allure.story("Карточка товара")
    @allure.title("Проверка цены товара")
    @allure.severity(allure.severity_level.NORMAL)
    def test_product_price(self):
        product_page = self.downloads_page.open_product_by_href("/album-3")
        price = product_page.get_product_price()
        assert "1.00" in price, f"Цена не соответствует, получено: {price}"

    @allure.story("Карточка товара")
    @allure.title("Проверка наличия кнопки 'Add to cart'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_product_add_to_cart_visible(self):
        product_page = self.downloads_page.open_product_by_href("/album-3")
        assert product_page.is_add_to_cart_visible(), "Кнопка 'Add to cart' не видна"

    @allure.story("Карточка товара")
    @allure.title("Проверка наличия поля Qty")
    @allure.severity(allure.severity_level.MINOR)
    def test_product_qty_visible(self):
        product_page = self.downloads_page.open_product_by_href("/album-3")
        assert product_page.is_qty_visible(), "Поле Qty не видно"

    @allure.story("Карточка товара")
    @allure.title("Проверка ссылки на отзывы")
    @allure.severity(allure.severity_level.MINOR)
    def test_product_reviews_link_visible(self):
        product_page = self.downloads_page.open_product_by_href("/album-3")
        reviews = product_page.get_reviews_text()
        assert "review" in reviews.lower(), "Ссылка на отзывы не найдена"
