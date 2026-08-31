from pages.base_page import BasePage

class PasswordRecoveryPage(BasePage):
    # Локаторы
    EMAIL_INPUT = "#Email"
    RECOVER_BUTTON = "input[value='Recover']"
    RESULT_MESSAGE = ".result"
    VALIDATION_ERROR = ".field-validation-error"  # сообщение "Enter your email"

    def open(self):
        """Открывает страницу восстановления пароля напрямую."""
        return super().open("/passwordrecovery")

    def recover_password(self, email: str):
        """Заполняет email и нажимает Recover."""
        self.fill(self.EMAIL_INPUT, email)
        self.click(self.RECOVER_BUTTON)
        return self

    def get_result_message(self) -> str:
        """Возвращает текст сообщения после отправки формы."""
        return self.get_text(self.RESULT_MESSAGE)

    def get_validation_error(self) -> str:
        """Возвращает текст ошибки валидации (например, 'Enter your email')."""
        return self.get_text(self.VALIDATION_ERROR)