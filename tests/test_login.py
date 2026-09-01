import allure

from pages.login_page import LoginPage


@allure.feature("Авторизация")
class TestLogin:
    @allure.story("Успешный вход")
    @allure.title("Вход с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Проверяет, что пользователь может войти с корректными email и паролем"
    )
    def test_successful_login(self, page, base_url):
        """Тест проверяет успешный вход с валидными данными"""
        login_page = LoginPage(page, base_url)
        login_page.open().login("rptest@mail.com", "123456!")
        page.wait_for_timeout(3000)
        assert login_page.is_logged_in() is True, "Пользователь не авторизован"
        assert login_page.is_account_correct("rptest@mail.com"), (
            "Email не совпадает или не виден"
        )

    @allure.story("Негативные сценарии")
    @allure.title("Вход с неверным паролем")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Проверяет, что при неверном пароле появляется сообщение об ошибке"
    )
    def test_invalid_password(self, page, base_url):
        """Тест проверяет, что при неверном пароле появляется сообщение об ошибке"""
        login_page = LoginPage(page, base_url)
        login_page.open().login("rptest@mail.com", "wrong_password")
        error_text = login_page.get_error_message()
        assert "The credentials provided are incorrect" in error_text, (
            "Сообщение об ошибке не соответствует ожидаемому"
        )
