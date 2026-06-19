from pages.base_page import BasePage

class LoginPage(BasePage):
    """Page Object для страницы авторизации (/login)."""

    EMAIL_INPUT = "#Email"
    PASSWORD_INPUT = "#Password"
    LOGIN_BUTTON = "input[value='Log in']"
    ERROR_MESSAGE = ".validation-summary-errors li"
    LOGOUT_LINK = "a.ico-logout"

    def login(self, email: str, password: str):
        """Заполняет форму и нажимает кнопку входа."""
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def get_error_message(self) -> str:
        """Возвращает текст ошибки, если она появилась."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_logged_in(self) -> bool:
        """Проверяет, видна ли ссылка 'Log out'."""
        return self.is_visible(self.LOGOUT_LINK)

    def open(self):
        """Открывает страницу логина."""
        return super().open("/login")