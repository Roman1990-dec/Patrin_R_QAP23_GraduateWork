import time

import allure

from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage


@allure.feature("Регистрация")
class TestRegistration:
    @allure.story("Успешная регистрация")
    @allure.title("Регистрация нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Проверяет, что новый пользователь может зарегистрироваться и автоматически войти"
    )
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
    @allure.description(
        "Проверяет, что при попытке зарегистрироваться с существующим email появляется ошибка"
    )
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
    @allure.description(
        "Проверяет, что при несовпадении пароля и подтверждения появляется ошибка"
    )
    def test_registration_password_mismatch(self, page, base_url):
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
        assert "password" in error.lower() or "match" in error.lower(), \
            f"Ожидалась ошибка о несовпадении паролей, получено: {error}"

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с пустыми обязательными полями")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Проверяет, что при отправке формы без email, пароля и подтверждения появляются ошибки валидации"
    )
    def test_registration_empty_fields(self, page, base_url):
        """Кейс №9: Регистрация с пустыми обязательными полями."""
        register_page = RegistrationPage(page, base_url)
        register_page.open()

        # Оставляем все поля пустыми, нажимаем Register
        register_page.click(register_page.REGISTER_BUTTON)

        # Получаем все ошибки (серверные + клиентские)
        errors = register_page.get_all_error_messages()

        # Ожидаем, что хотя бы одна ошибка содержит "required" или "Email"
        assert len(errors) > 0, "Ошибки не найдены"
        # Проверяем, что есть сообщение о required для Email или пароля
        expected_phrases = ["required", "Email"]
        found = any(any(phrase in err for phrase in expected_phrases) for err in errors)
        assert found, f"Ожидались ошибки валидации, получено: {errors}"