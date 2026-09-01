from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object для страницы авторизации (/login)"""

    EMAIL_INPUT = "#Email"
    PASSWORD_INPUT = "#Password"
    LOGIN_BUTTON = "input[value='Log in']"
    ERROR_MESSAGE = ".validation-summary-errors li"
    LOGOUT_LINK = "a.ico-logout"
    ACCOUNT_LINK = "div.header-links a.account"

    def login(self, email: str, password: str):
        """Заполняет форму и нажимает кнопку входа"""
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def get_error_message(self) -> str:
        """Возвращает текст ошибки, если она появилась"""
        return self.get_text(self.ERROR_MESSAGE)

    def is_logged_in(self) -> bool:
        """Проверяет, видна ли ссылка 'Log out'"""
        return self.is_visible(self.LOGOUT_LINK)

    def get_account_email(self) -> str:
        """ "Возвращает текст ссылки на аккаунт (email)"""
        return self.get_text(self.ACCOUNT_LINK)

    def is_account_correct(self, expected_email: str) -> bool:
        """ "Проверяет, видна ли ссылка аккаунта с корректным текстом (email)"""
        try:
            self.page.wait_for_selector(
                self.ACCOUNT_LINK, state="visible", timeout=3000
            )
            actual_email = self.get_account_email()
            return actual_email == expected_email
        except TimeoutError:
            return False

    def open(self, url: str = ""):
        """Открывает страницу логина (или переданный url, если указан)"""
        if url:
            return super().open(url)
        return super().open("/login")

    def click_forgot_password(self):
        """Кликает по ссылке 'Forgot password?' и возвращает объект PasswordRecoveryPage."""
        self.click(".forgot-password a")
        from pages.password_recovery_page import PasswordRecoveryPage

        return PasswordRecoveryPage(self.page, self.base_url)
