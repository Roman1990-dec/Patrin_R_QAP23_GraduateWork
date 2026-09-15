import allure
import pytest

from pages.login_page import LoginPage
from pages.password_recovery_page import PasswordRecoveryPage


@allure.feature("Восстановление пароля")
class TestPasswordRecovery:
    @allure.story("Ссылка 'Forgot password?'")
    @allure.title("Проверка ссылки, перехода и ошибки при пустом email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_forgot_password_link_and_empty_email(self, page, base_url):
        login_page = LoginPage(page, base_url)
        login_page.open()

        assert login_page.is_forgot_password_link_visible(), (
            "Ссылка 'Forgot password?' не видна"
        )

        recovery_page = login_page.click_forgot_password()
        assert "/passwordrecovery" in recovery_page.get_current_url(), (
            "Переход на страницу восстановления не выполнен"
        )

        recovery_page.submit_empty_form()
        error_text = recovery_page.get_validation_error()
        assert "Enter your email" in error_text, (
            f"Ожидалась ошибка 'Enter your email', получено: {error_text}"
        )

    @allure.story("Восстановление пароля по email")
    @allure.title("Проверка сообщений для существующего и несуществующего email")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        ("email", "expected_message"),
        [
            ("rptest@mail.com", "Email with instructions has been sent to you"),
            ("nonexistent@example.com", "Email not found"),
        ],
    )
    def test_password_recovery(self, page, base_url, email, expected_message):
        recovery_page = PasswordRecoveryPage(page, base_url)
        recovery_page.open()
        recovery_page.recover_password(email)

        result_text = recovery_page.get_result_message()
        assert expected_message in result_text, (
            f"Ожидалось сообщение '{expected_message}', получено: {result_text}"
        )
