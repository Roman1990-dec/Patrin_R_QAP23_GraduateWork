import pytest
import allure
from pages.login_page import LoginPage
from pages.password_recovery_page import PasswordRecoveryPage

@allure.feature("Восстановление пароля")
class TestPasswordRecovery:

    @allure.story("Ссылка 'Forgot password?'")
    @allure.title("Кейс 1: Проверка ссылки, перехода и ошибки при пустом email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_forgot_password_link_and_empty_email(self, page, base_url):
        """Кейс 1: Проверка, что ссылка 'Forgot password?' ведёт на страницу восстановления,
        и при пустом email появляется ошибка 'Enter your email'."""
        # 1. Открываем страницу логина
        login_page = LoginPage(page, base_url)
        login_page.open()

        # 2. Проверяем, что ссылка "Forgot password?" видна
        assert login_page.is_visible(".forgot-password a"), "Ссылка 'Forgot password?' не видна"

        # 3. Кликаем по ссылке и переходим на страницу восстановления
        recovery_page = login_page.click_forgot_password()

        # 4. Проверяем, что мы на странице /passwordrecovery
        assert "/passwordrecovery" in page.url, "Переход на страницу восстановления не выполнен"

        # 5. Нажимаем Recover, не заполняя email
        recovery_page.click(recovery_page.RECOVER_BUTTON)

        # 6. Проверяем, что появилась ошибка валидации
        error_text = recovery_page.get_validation_error()
        assert "Enter your email" in error_text, f"Ожидалась ошибка 'Enter your email', получено: {error_text}"

    @allure.story("Восстановление с существующим email")
    @allure.title("Кейс 2: Успешное восстановление с существующим email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_password_recovery_existing_email(self, page, base_url):
        """Кейс 2: Ввод существующего email -> получение сообщения об отправке инструкций."""
        # 1. Переходим напрямую на страницу восстановления
        recovery_page = PasswordRecoveryPage(page, base_url)
        recovery_page.open()

        # 2. Вводим существующий email (rptest@mail.com) и нажимаем Recover
        recovery_page.recover_password("rptest@mail.com")

        # 3. Проверяем сообщение об успехе
        result_text = recovery_page.get_result_message()
        assert "Email with instructions has been sent to you" in result_text, \
            f"Ожидалось сообщение об отправке, получено: {result_text}"

    @allure.story("Восстановление с несуществующим email")
    @allure.title("Кейс 3: Восстановление с несуществующим email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_password_recovery_nonexistent_email(self, page, base_url):
        """Кейс 3: Ввод несуществующего email -> получение сообщения 'Email not found'."""
        recovery_page = PasswordRecoveryPage(page, base_url)
        recovery_page.open()

        # Вводим несуществующий email
        recovery_page.recover_password("nonexistent@example.com")

        # Проверяем сообщение об ошибке
        result_text = recovery_page.get_result_message()
        assert "Email not found" in result_text, \
            f"Ожидалось сообщение 'Email not found', получено: {result_text}"