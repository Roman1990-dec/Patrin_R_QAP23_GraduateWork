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
        assert self.home_page.is_visible("#topcartlink a.ico-cart"), (
            "Ссылка Shopping cart не видна"
        )

    @allure.story("Хедер")
    @allure.title("Проверка ссылки 'Wishlist'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_header_wishlist_link_visible(self):
        assert self.home_page.is_visible(".header-links a.ico-wishlist"), (
            "Ссылка Wishlist не видна"
        )

    @allure.story("Хедер")
    @allure.title("Проверка поля поиска и кнопки Search")
    @allure.severity(allure.severity_level.NORMAL)
    def test_header_search_field_visible(self):
        assert self.home_page.is_visible("#small-searchterms"), "Поле поиска не видно"
        assert self.home_page.is_visible("input[value='Search']"), (
            "Кнопка Search не видна"
        )

    @allure.story("Навигация")
    @allure.title("Переход по пунктам верхнего меню")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "link_text, expected_path",
        [
            ("Books", "/books"),
            ("Computers", "/computers"),
            ("Electronics", "/electronics"),
            ("Apparel & Shoes", "/apparel-shoes"),
            ("Digital downloads", "/digital-downloads"),
            ("Jewelry", "/jewelry"),
            ("Gift Cards", "/gift-cards"),
        ],
    )
    def test_top_menu_navigation(self, link_text, expected_path):
        """Кейс №13: Проверка перехода по пунктам верхнего меню."""
        link_selector = f".top-menu a[href='{expected_path}']"
        self.home_page.click(link_selector)
        self.home_page.page.wait_for_url(
            f"{self.home_page.base_url}{expected_path}", timeout=5000
        )
        assert expected_path in self.home_page.page.url, (
            f"Ожидался путь {expected_path}, текущий URL: {self.home_page.page.url}"
        )

    @allure.story("Поиск")
    @allure.title("Поиск существующего товара")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_existing_product(self):
        """Кейс №14: Поиск товара 'computer'."""
        search_input = "#small-searchterms"
        search_button = "input[value='Search']"
        self.home_page.fill(search_input, "computer")
        self.home_page.click(search_button)
        # Ждём появления результатов
        self.home_page.page.wait_for_selector(
            ".product-item", state="visible", timeout=5000
        )
        # Проверяем, что есть хотя бы один товар
        items = self.home_page.page.locator(".product-item").count()
        assert items > 0, "Результаты поиска не найдены"

    @allure.story("Поиск")
    @allure.title("Поиск несуществующего товара")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_nonexistent_product(self):
        """Кейс №15: Поиск товара 'nonexistent'."""
        search_input = "#small-searchterms"
        search_button = "input[value='Search']"
        self.home_page.fill(search_input, "nonexistent")
        self.home_page.click(search_button)
        # Ожидаем сообщение об отсутствии результатов
        self.home_page.page.wait_for_selector(".result", state="visible", timeout=5000)
        result_text = self.home_page.page.locator(".result").text_content()
        assert (
            "No products were found" in result_text
            or "No products found" in result_text
        ), f"Неожиданное сообщение: {result_text}"

    @allure.story("Блоки на главной")
    @allure.title("Проверка блока Newsletter")
    @allure.severity(allure.severity_level.MINOR)
    def test_newsletter_block_visible(self):
        """Кейс №16: Проверка видимости поля email и кнопки Subscribe."""
        assert self.home_page.is_visible("#newsletter-email"), "Поле email не видно"
        assert self.home_page.is_visible("input[value='Subscribe']"), (
            "Кнопка Subscribe не видна"
        )

    @allure.story("Блоки на главной")
    @allure.title("Проверка блока Community Poll")
    @allure.severity(allure.severity_level.NORMAL)
    def test_community_poll_visible(self):
        """Кейс №17: Проверка наличия вопроса, всех радиокнопок и их текстов."""
        # 1. Проверяем текст вопроса (ищем по тексту, так как селектор может отличаться)
        question_text = self.home_page.page.locator(
            "text=Do you like nopCommerce?"
        ).text_content()
        assert (
            question_text is not None and "Do you like nopCommerce?" in question_text
        ), "Вопрос не отображается или неверный"

        # 2. Проверяем видимость каждой радиокнопки и её текста
        expected_options = ["Excellent", "Good", "Poor", "Very bad"]
        for i, option_text in enumerate(expected_options, start=1):
            radio_selector = f"#pollanswers-{i}"
            label_selector = f"label[for='pollanswers-{i}']"

            # Проверяем, что радио-кнопка видна
            assert self.home_page.is_visible(radio_selector), (
                f"Радиокнопка для '{option_text}' не видна"
            )

            # Проверяем, что подпись к кнопке содержит ожидаемый текст
            label_text = self.home_page.page.locator(label_selector).text_content()
            assert option_text in label_text, (
                f"Ожидался текст '{option_text}', получено '{label_text}'"
            )

        # 3. Проверяем, что кнопка Vote видна
        assert self.home_page.is_visible("input[value='Vote']"), "Кнопка Vote не видна"

    @allure.story("Блоки на главной")
    @allure.title("Голосование без авторизации показывает ошибку")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "option_id, option_text",
        [
            ("pollanswers-1", "Excellent"),
            ("pollanswers-2", "Good"),
            ("pollanswers-3", "Poor"),
            ("pollanswers-4", "Very bad"),
        ],
    )
    def test_community_poll_vote_without_login(self, option_id, option_text):
        """Кейс №21: Проверка, что голосование без логина показывает сообщение 'Only registered users can vote'."""
        # Открываем главную страницу (без логина)
        self.home_page.open()

        # Выбираем радиокнопку
        self.home_page.click(f"#{option_id}")
        # Нажимаем кнопку Vote
        self.home_page.click("input[value='Vote']")

        # Ожидаем появления сообщения об ошибке и проверяем его текст
        error_locator = "text=Only registered users can vote"
        self.home_page.page.wait_for_selector(
            error_locator, state="visible", timeout=5000
        )
        error_text = self.home_page.page.locator(error_locator).text_content()
        assert "Only registered users can vote" in error_text, (
            f"Неверное сообщение: {error_text}"
        )

    @allure.story("Блоки на главной")
    @allure.title("Проверка блока Featured Products")
    @allure.severity(allure.severity_level.NORMAL)
    def test_featured_products_visible(self):
        """Кейс №18: Проверка, что в блоке Featured Products есть товары."""
        items = self.home_page.page.locator(".product-item").count()
        assert items > 0, "В блоке Featured Products нет товаров"

    @allure.story("Блоки на главной")
    @allure.title("Проверка блока Popular Tags")
    @allure.severity(allure.severity_level.MINOR)
    def test_popular_tags_visible(self):
        """Кейс №19: Проверка, что теги отображаются."""
        tags = self.home_page.page.locator("a[href^='/producttag/']").count()
        assert tags > 0, "Теги не найдены"

    @allure.story("Блоки на главной")
    @allure.title("Проверка ссылки 'View all' в блоке Popular Tags")
    @allure.severity(allure.severity_level.NORMAL)
    def test_popular_tags_view_all_link(self):
        """Кейс №22: Проверка, что ссылка 'View all' ведёт на /producttag/all."""
        # Находим ссылку "View all" внутри блока .view-all
        view_all_link = ".view-all a"
        # Проверяем, что ссылка видна
        assert self.home_page.is_visible(view_all_link), "Ссылка 'View all' не видна"
        # Кликаем по ссылке
        self.home_page.click(view_all_link)
        # Ожидаем перехода на страницу со всеми тегами
        expected_path = "/producttag/all"
        self.home_page.page.wait_for_url(
            f"{self.home_page.base_url}{expected_path}", timeout=10000
        )
        assert expected_path in self.home_page.page.url, (
            f"Ожидался путь {expected_path}, текущий URL: {self.home_page.page.url}"
        )

    @allure.story("Блоки на главной")
    @allure.title("Проверка наличия тега 'digital' и перехода по нему")
    @allure.severity(allure.severity_level.NORMAL)
    def test_popular_tags_digital_tag(self):
        """Кейс №23: Проверка, что тег 'digital' присутствует и ведёт на /producttag/16/digital."""
        # Ожидаем появления блока с тегами
        self.home_page.page.wait_for_selector(".tags", state="visible", timeout=5000)

        # 1. Проверяем, что тег "digital" присутствует в списке
        digital_tag_selector = "a[href='/producttag/16/digital']"
        assert self.home_page.is_visible(digital_tag_selector), (
            "Тег 'digital' не найден в списке"
        )

        # 2. Кликаем по тегу "digital"
        self.home_page.click(digital_tag_selector)

        # 3. Ожидаем перехода на страницу тега
        expected_path = "/producttag/16/digital"
        self.home_page.page.wait_for_url(
            f"{self.home_page.base_url}{expected_path}", timeout=10000
        )
        assert expected_path in self.home_page.page.url, (
            f"Ожидался путь {expected_path}, текущий URL: {self.home_page.page.url}"
        )

        # 4. Проверяем, что на странице отображаются товары, связанные с тегом "digital"
        # (на основе вашего скриншота — там должны быть товары)
        self.home_page.page.wait_for_selector(
            ".product-item", state="visible", timeout=5000
        )
        items = self.home_page.page.locator(".product-item").count()
        assert items > 0, "На странице тега 'digital' не найдено товаров"

    @allure.story("Нижний колонтитул")
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
        """Кейс №20: Проверка перехода по ссылкам в нижнем колонтитуле."""
        # Ищем ссылку в футере (обычно она находится внутри div.footer или внизу страницы)
        link_selector = f".footer a:has-text('{link_text}')"
        self.home_page.click(link_selector)
        self.home_page.page.wait_for_url(
            f"{self.home_page.base_url}{expected_path}", timeout=5000
        )
        assert expected_path in self.home_page.page.url, (
            f"Ожидался путь {expected_path}, текущий URL: {self.home_page.page.url}"
        )
