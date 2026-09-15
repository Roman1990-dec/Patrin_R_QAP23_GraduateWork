import allure
import pytest

from pages.home_page import HomePage


@allure.feature("Главная страница")
class TestHomePage:
    @pytest.fixture(autouse=True)
    def setup(self, page, base_url):
        self.home_page = HomePage(page, base_url)
        self.home_page.open()

    @allure.story("Хедер")
    @allure.title("Проверка видимости логотипа")
    @allure.severity(allure.severity_level.MINOR)
    def test_logo_visible(self):
        assert self.home_page.is_logo_visible(), "Логотип не виден"

    @allure.story("Хедер")
    @allure.title("Проверка видимости элементов хедера")
    @allure.severity(allure.severity_level.NORMAL)
    def test_header_elements_visible(self):
        assert self.home_page.is_register_link_visible(), "Ссылка Register не видна"
        assert self.home_page.is_login_link_visible(), "Ссылка Log in не видна"
        assert self.home_page.is_cart_link_visible(), "Ссылка Shopping cart не видна"
        assert self.home_page.is_wishlist_link_visible(), "Ссылка Wishlist не видна"
        assert self.home_page.is_search_field_visible(), (
            "Поле поиска или кнопка Search не видны"
        )

    @allure.story("Навигация")
    @allure.title("Переход по ссылке 'Register'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_register_link_navigates(self):
        self.home_page.click_register_link()
        self.home_page.wait_for_url(f"{self.home_page.base_url}/register")
        assert "/register" in self.home_page.get_current_url(), (
            f"Ожидался /register, текущий: {self.home_page.get_current_url()}"
        )

    @allure.story("Навигация")
    @allure.title("Переход по ссылке 'Log in'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_link_navigates(self):
        self.home_page.click_login_link()
        self.home_page.wait_for_url(f"{self.home_page.base_url}/login")
        assert "/login" in self.home_page.get_current_url(), (
            f"Ожидался /login, текущий: {self.home_page.get_current_url()}"
        )

    @allure.story("Навигация")
    @allure.title("Переход по ссылке 'Shopping cart'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cart_link_navigates(self):
        self.home_page.click_cart_link()
        self.home_page.wait_for_url(f"{self.home_page.base_url}/cart")
        assert "/cart" in self.home_page.get_current_url(), (
            f"Ожидался /cart, текущий: {self.home_page.get_current_url()}"
        )

    @allure.story("Навигация")
    @allure.title("Переход по ссылке 'Wishlist'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_wishlist_link_navigates(self):
        self.home_page.click_wishlist_link()
        self.home_page.wait_for_url(f"{self.home_page.base_url}/wishlist")
        assert "/wishlist" in self.home_page.get_current_url(), (
            f"Ожидался /wishlist, текущий: {self.home_page.get_current_url()}"
        )

    @allure.story("Навигация")
    @allure.title("Переход по пунктам верхнего меню")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "expected_path",
        [
            "/books",
            "/computers",
            "/electronics",
            "/apparel-shoes",
            "/digital-downloads",
            "/jewelry",
            "/gift-cards",
        ],
    )
    def test_top_menu_navigation(self, expected_path):
        self.home_page.click_top_menu_link_by_href(expected_path)
        self.home_page.wait_for_url(f"{self.home_page.base_url}{expected_path}")
        assert expected_path in self.home_page.get_current_url(), (
            f"Ожидался путь {expected_path}, текущий URL: {self.home_page.get_current_url()}"
        )

    @allure.story("Навигация")
    @allure.title("Переход по ссылкам в нижнем колонтитуле")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "link_text, expected_path",
        [
            ("Sitemap", "/sitemap"),
            ("About Us", "/about-us"),
            ("Contact Us", "/contactus"),
            ("Privacy Notice", "/privacy-policy"),
            ("Conditions of Use", "/conditions-of-use"),
        ],
    )
    def test_footer_links_navigation(self, link_text, expected_path):
        self.home_page.click_footer_link_by_text(link_text)
        self.home_page.wait_for_url(f"{self.home_page.base_url}{expected_path}")
        assert expected_path in self.home_page.get_current_url(), (
            f"Ожидался путь {expected_path}, текущий URL: {self.home_page.get_current_url()}"
        )

    @allure.story("Поиск")
    @allure.title("Поиск существующего товара")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_existing_product(self):
        self.home_page.search("computer")
        assert self.home_page.get_search_results_count() > 0, (
            "Результаты поиска не найдены"
        )

    @allure.story("Поиск")
    @allure.title("Поиск несуществующего товара")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_nonexistent_product(self):
        self.home_page.search("nonexistent")
        message = self.home_page.get_search_message()
        assert "No products" in message, f"Неожиданное сообщение: {message}"

    @allure.story("Блоки на главной")
    @allure.title("Проверка блоков Newsletter, Featured Products, Popular Tags")
    @allure.severity(allure.severity_level.MINOR)
    def test_home_blocks_visible(self):
        assert self.home_page.is_newsletter_visible(), "Блок Newsletter не виден"
        assert self.home_page.get_featured_products_count() > 0, (
            "Нет товаров в Featured Products"
        )
        assert self.home_page.get_popular_tags_count() > 0, "Нет тегов в Popular Tags"

    @allure.story("Community Poll")
    @allure.title("Проверка отображения блока Community Poll")
    @allure.severity(allure.severity_level.NORMAL)
    def test_community_poll_visible(self):
        assert "Do you like nopCommerce" in self.home_page.get_poll_question(), (
            "Неверный вопрос в блоке опроса"
        )
        expected_options = ["Excellent", "Good", "Poor", "Very bad"]
        for i, option_text in enumerate(expected_options, start=1):
            answer_id = f"pollanswers-{i}"
            assert self.home_page.is_poll_radio_visible(answer_id), (
                f"Радиокнопка для '{option_text}' не видна"
            )
            label_text = self.home_page.get_poll_label_text(answer_id)
            assert option_text in label_text, (
                f"Ожидался текст '{option_text}', получено '{label_text}'"
            )
        assert self.home_page.is_poll_vote_visible(), "Кнопка Vote не видна"

    @allure.story("Community Poll")
    @allure.title("Голосование без авторизации показывает ошибку")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "option_id",
        ["pollanswers-1", "pollanswers-2", "pollanswers-3", "pollanswers-4"],
    )
    def test_community_poll_vote_without_login(self, option_id):
        self.home_page.select_poll_answer(option_id)
        self.home_page.vote()
        error = self.home_page.get_vote_error()
        assert "Only registered users can vote" in error, f"Неверное сообщение: {error}"

    @allure.story("Popular Tags")
    @allure.title("Переход по ссылке 'View all'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_popular_tags_view_all_link(self):
        self.home_page.click_view_all_tags()
        self.home_page.wait_for_url(f"{self.home_page.base_url}/producttag/all")
        assert "/producttag/all" in self.home_page.get_current_url(), (
            f"Ожидался путь /producttag/all, текущий: {self.home_page.get_current_url()}"
        )

    @allure.story("Popular Tags")
    @allure.title("Переход по тегу 'digital'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_popular_tags_digital_tag(self):
        assert self.home_page.is_digital_tag_visible(), "Тег 'digital' не виден"
        self.home_page.click_digital_tag()
        self.home_page.wait_for_url(f"{self.home_page.base_url}/producttag/16/digital")
        assert "/producttag/16/digital" in self.home_page.get_current_url(), (
            f"Ожидался путь /producttag/16/digital, текущий: {self.home_page.get_current_url()}"
        )
        assert self.home_page.get_search_results_count() > 0, (
            "На странице тега 'digital' не найдено товаров"
        )
