import pytest
import allure
from pages.home_page import HomePage

@allure.feature("Главная страница")
class TestHomePage:
    @pytest.fixture(autouse=True)
    def setup(self, page, base_url):
        self.home_page = HomePage(page, base_url)
        self.home_page.open()

    @allure.story("Хедер")
    @allure.title("Проверка ссылки 'Register'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_header_register_link_visible(self):
        assert self.home_page.is_visible("a.ico-register"), "Ссылка Register не видна"

    @allure.story("Хедер")
    @allure.title("Проверка ссылки 'Log in'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_header_login_link_visible(self):
        assert self.home_page.is_visible("a.ico-login"), "Ссылка Log in не видна"

    @allure.story("Хедер")
    @allure.title("Проверка ссылки 'Shopping cart'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_header_shopping_cart_link_visible(self):
        # Уточняем: ищем ссылку внутри блока header-links
        assert self.home_page.is_visible("#topcartlink a.ico-cart"), "Ссылка Shopping cart не видна"

    @allure.story("Хедер")
    @allure.title("Проверка ссылки 'Wishlist'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_header_wishlist_link_visible(self):
        assert self.home_page.is_visible(".header-links a.ico-wishlist"), "Ссылка Wishlist не видна"

    @allure.story("Хедер")
    @allure.title("Проверка поля поиска и кнопки Search")
    @allure.severity(allure.severity_level.NORMAL)
    def test_header_search_field_visible(self):
        assert self.home_page.is_visible("#small-searchterms"), "Поле поиска не видно"
        assert self.home_page.is_visible("input[value='Search']"), "Кнопка Search не видна"