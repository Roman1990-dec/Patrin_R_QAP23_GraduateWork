import allure

from pages.login_page import LoginPage


@allure.feature("Авторизация")
class TestLogin:
    @allure.story("Успешный вход")
    @allure.title("Вход с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Проверяет, что пользователь может войти с корректными email и паролем: "
        "происходит редирект на главную, отображается email и ссылка 'Log out'."
    )
    def test_successful_login(self, page, base_url):
        login_page = LoginPage(page, base_url)
        login_page.open().login("rptest@mail.com", "123456!")

        assert login_page.is_logged_in(), "Ссылка 'Log out' не отображается"
        assert login_page.is_account_correct("rptest@mail.com"), (
            "Email авторизованного пользователя не совпадает"
        )
        assert login_page.get_current_url() == f"{base_url}/", (
            f"Ожидался редирект на главную, текущий URL: {login_page.get_current_url()}"
        )

    @allure.story("Негативные сценарии")
    @allure.title("Вход с неверным паролем")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Проверяет, что при неверном пароле появляется сообщение об ошибке, "
        "пользователь не авторизован и остаётся на странице логина."
    )
    def test_invalid_password(self, page, base_url):
        login_page = LoginPage(page, base_url)
        login_page.open().login("rptest@mail.com", "wrong_password")

        error_text = login_page.get_error_message()
        assert "The credentials provided are incorrect" in error_text, (
            f"Сообщение об ошибке не соответствует ожидаемому: {error_text}"
        )
        assert not login_page.is_logged_in(), (
            "Пользователь авторизован, хотя пароль неверный"
        )
        assert "/login" in login_page.get_current_url(), (
            f"Пользователь должен остаться на /login, текущий URL: {login_page.get_current_url()}"
        )

    @allure.story("Негативные сценарии")
    @allure.title("Вход с пустыми полями")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_empty_fields(self, page, base_url):
        login_page = LoginPage(page, base_url)
        login_page.open()
        login_page.submit_empty_form()

        assert not login_page.is_logged_in(), "Пользователь авторизован без данных"
        assert "/login" in login_page.get_current_url(), (
            "Пользователь не остался на /login"
        )

    @allure.story("Негативные сценарии")
    @allure.title("Вход с несуществующим email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_nonexistent_email(self, page, base_url):
        login_page = LoginPage(page, base_url)
        login_page.open().login("nonexistent_user_999@example.com", "SomePassword123!")

        error = login_page.get_error_message()
        assert "No customer account found" in error, (
            f"Ожидалось сообщение 'No customer account found', получено: {error}"
        )

    @allure.story("Выход из системы")
    @allure.title("Выход после успешного входа")
    @allure.severity(allure.severity_level.NORMAL)
    def test_logout_after_login(self, page, base_url):
        login_page = LoginPage(page, base_url)
        login_page.open().login("rptest@mail.com", "123456!")
        assert login_page.is_logged_in(), "Не удалось войти для проверки logout"

        login_page.logout()
        assert not login_page.is_logout_link_visible(), (
            "Ссылка 'Log out' всё ещё видна после выхода"
        )
