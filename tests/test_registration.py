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
        "Проверяет, что новый пользователь может зарегистрироваться "
        "и автоматически войти в систему."
    )
    def test_successful_registration(self, page, base_url):
        register_page = RegistrationPage(page, base_url)
        register_page.open()

        unique_email = f"testuser_{int(time.time())}@example.com"
        password = "Test123!"

        register_page.register(
            first_name="Test",
            last_name="User",
            email=unique_email,
            password=password,
        )

        success_msg = register_page.get_success_message()
        assert "Your registration completed" in success_msg, (
            f"Неожиданное сообщение: {success_msg}"
        )

        login_page = LoginPage(page, base_url)
        assert login_page.is_logged_in(), (
            "Пользователь не авторизован после регистрации"
        )
        assert login_page.is_account_correct(unique_email), "Email не совпадает"

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с уже существующим email")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Проверяет, что при попытке зарегистрироваться с существующим email "
        "появляется сообщение об ошибке."
    )
    def test_registration_existing_email(self, page, base_url):
        register_page = RegistrationPage(page, base_url)
        register_page.open()

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
        "Проверяет, что при несовпадении пароля и подтверждения появляется ошибка."
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
        assert "password" in error.lower() or "match" in error.lower(), (
            f"Ожидалась ошибка о несовпадении паролей, получено: {error}"
        )

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с пустыми обязательными полями")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Проверяет, что при отправке пустой формы появляются ошибки валидации "
        "для обязательных полей."
    )
    def test_registration_empty_fields(self, page, base_url):
        register_page = RegistrationPage(page, base_url)
        register_page.open()

        register_page.submit_empty_form()

        errors = register_page.get_all_error_messages()
        assert len(errors) > 0, "Ошибки не найдены"

        expected_phrases = ["required", "Email"]
        found = any(any(phrase in err for phrase in expected_phrases) for err in errors)
        assert found, f"Ожидались ошибки валидации, получено: {errors}"

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с коротким паролем")
    @allure.severity(allure.severity_level.NORMAL)
    def test_registration_short_password(self, page, base_url):
        register_page = RegistrationPage(page, base_url)
        register_page.open()

        register_page.register(
            first_name="Test",
            last_name="User",
            email="short_pwd@example.com",
            password="123",
            confirm_password="123",
        )

        errors = register_page.get_all_error_messages()
        assert any(
            "6 characters" in err or "length" in err.lower() for err in errors
        ), f"Ожидалась ошибка о минимальной длине пароля, получено: {errors}"

    @allure.story("Негативные сценарии")
    @allure.title("Регистрация с некорректным email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_registration_invalid_email(self, page, base_url):
        register_page = RegistrationPage(page, base_url)
        register_page.open()

        register_page.register(
            first_name="Test",
            last_name="User",
            email="not-an-email",
            password="Test123!",
        )

        errors = register_page.get_all_error_messages()
        assert any("email" in err.lower() for err in errors), (
            f"Ожидалась ошибка о некорректном email, получено: {errors}"
        )

    @allure.story("Успешная регистрация")
    @allure.title("Регистрация с выбором пола Female")
    @allure.severity(allure.severity_level.NORMAL)
    def test_registration_with_female_gender(self, page, base_url):
        register_page = RegistrationPage(page, base_url)
        register_page.open()
        register_page.select_female_gender()

        unique_email = f"female_{int(time.time())}@example.com"
        register_page.register(
            first_name="Anna",
            last_name="Test",
            email=unique_email,
            password="Test123!",
        )

        success = register_page.get_success_message()
        assert "Your registration completed" in success, (
            f"Регистрация не завершилась: {success}"
        )
