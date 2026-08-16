import pytest
import time
import allure
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage


@allure.feature("Регистрация")
class TestRegistration:

    @allure.story("Успешная регистрация")
    @allure.title("Регистрация нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверяет, что новый пользователь может зарегистрироваться и автоматически войти")
    def test_successful_registration(self, page, base_url):
        """Кейс №6: Успешная регистрация нового пользователя."""
        register_page = RegistrationPage(page, base_url)
        register_page.open()

        # Генерируем уникальный email
        unique_email = f"testuser_{int(time.time())}@example.com"
        password = "Test123!"

        register_page.register(
            first_name="Test", last_name="User", email=unique_email, password=password
        )

        # Проверяем сообщение об успехе
        success_msg = register_page.get_success_message()
        assert "Your registration completed" in success_msg, (
            f"Неожиданное сообщение: {success_msg}"
        )

        # Проверяем, что пользователь автоматически вошёл (появился email и Log out)
        login_page = LoginPage(page, base_url)
        # Можно проверить, что в хедере появился email (используем уже знакомый локатор)
        assert login_page.is_logged_in(), (
            "Пользователь не авторизован после регистрации"
        )
        assert login_page.is_account_correct(unique_email), "Email не совпадает"

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с уже существующим email")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверяет, что при попытке зарегистрироваться с существующим email появляется ошибка")
    def test_registration_existing_email(self, page, base_url):
        """Кейс №7: Регистрация с уже существующим email."""
        register_page = RegistrationPage(page, base_url)
        register_page.open()

        # Используем уже зарегистрированный email (например, rptest@mail.com)
        register_page.register(
            first_name="Test",
            last_name="User",
            email="rptest@mail.com",
            password="Test123!",
        )

        error = register_page.get_email_exists_error()
        assert "The specified email already exists" in error, (
            f"Неожиданная ошибка: {error}"
        )

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с несовпадающими паролями")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверяет, что при несовпадении пароля и подтверждения появляется ошибка")
    def test_registration_password_mismatch(self, page, base_url):
        """Кейс №8: Регистрация с несовпадающими паролями."""
        register_page = RegistrationPage(page, base_url)
        register_page.open()
        register_page.register(
            first_name="Test",
            last_name="User",
            email="temp@example.com",
            password="Test123!",
            confirm_password="WrongPass",
        )
        error = register_page.get_error_message()
        assert "The password and confirmation password do not match" in error, (
            f"Неожиданная ошибка: {error}"
        )

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с пустыми обязательными полями")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверяет, что при отправке формы без email, пароля и подтверждения появляются ошибки валидации")
    def test_registration_empty_fields(self, page, base_url):
        register_page = RegistrationPage(page, base_url)
        register_page.open()
        register_page.fill(register_page.FIRST_NAME, "Test")
        register_page.fill(register_page.LAST_NAME, "User")
        register_page.click(register_page.REGISTER_BUTTON)

        # Даём время для появления ошибок (можно заменить на ожидание)
        page.wait_for_timeout(1000)

        errors = register_page.get_all_error_messages()
        expected_phrases = ["Email is required", "Password is required"]
        for phrase in expected_phrases:
            assert any(phrase in err for err in errors), (
                f"Ожидалась ошибка с фразой '{phrase}', но она не найдена. Получены ошибки: {errors}"
            )
