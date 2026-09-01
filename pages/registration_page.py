from pages.base_page import BasePage
from playwright._impl._errors import TimeoutError

class RegistrationPage(BasePage):
    GENDER_MALE = "#gender-male"
    GENDER_FEMALE = "#gender-female"
    FIRST_NAME = "#FirstName"
    LAST_NAME = "#LastName"
    EMAIL = "#Email"
    PASSWORD = "#Password"
    CONFIRM_PASSWORD = "#ConfirmPassword"
    REGISTER_BUTTON = "#register-button"

    SUCCESS_MESSAGE = ".result"
    # Для серверных ошибок (если они всё же появятся)
    ERROR_SELECTORS = [
        ".validation-summary-errors li",
        ".field-validation-error",
        ".message-error li",
    ]

    def open(self, url: str = ""):
        if url:
            return super().open(url)
        return super().open("/register")

    def register(self, first_name, last_name, email, password, confirm_password=None):
        if confirm_password is None:
            confirm_password = password
        self.fill(self.FIRST_NAME, first_name)
        self.fill(self.LAST_NAME, last_name)
        self.fill(self.EMAIL, email)
        self.fill(self.PASSWORD, password)
        self.fill(self.CONFIRM_PASSWORD, confirm_password)
        self.click(self.REGISTER_BUTTON)
        return self

    def get_success_message(self) -> str:
        return self.get_text(self.SUCCESS_MESSAGE)

    def get_error_message(self) -> str:
        # 1. Сначала ищем серверные ошибки
        for selector in self.ERROR_SELECTORS:
            try:
                self.page.wait_for_selector(selector, state="visible", timeout=3000)
                return self.page.locator(selector).first.text_content()
            except TimeoutError:
                continue

        # 2. Если серверных нет, ищем подсвеченные поля (клиентская валидация)
        try:
            self.page.wait_for_selector(".input-validation-error", state="visible", timeout=2000)
            error_input = self.page.locator(".input-validation-error").first
            # Пытаемся получить сообщение браузера
            msg = error_input.get_attribute("validationMessage")
            if msg and msg.strip():
                return msg
            # Если сообщения нет, возвращаем общий текст
            return "Validation error (field is invalid)"
        except TimeoutError:
            pass

        raise Exception("No error message found on the page")

    def get_all_error_messages(self) -> list:
        errors = []

        # 1. Серверные ошибки
        try:
            self.page.wait_for_selector(".validation-summary-errors", state="visible", timeout=3000)
            error_items = self.page.locator(".validation-summary-errors li").all()
            errors.extend([item.text_content() for item in error_items])
        except TimeoutError:
            pass

        # 2. Клиентские ошибки (подсвеченные поля)
        try:
            self.page.wait_for_selector(".input-validation-error", state="visible", timeout=2000)
            error_inputs = self.page.locator(".input-validation-error").all()
            for inp in error_inputs:
                msg = inp.get_attribute("validationMessage")
                if msg and msg.strip():
                    errors.append(msg)
                else:
                    # Добавляем информацию о поле
                    field_name = inp.get_attribute("name") or inp.get_attribute("id") or "unknown"
                    errors.append(f"Field '{field_name}' is invalid")
        except TimeoutError:
            pass

        # 3. Дополнительно field-validation-error (если есть)
        try:
            self.page.wait_for_selector(".field-validation-error", state="visible", timeout=2000)
            items = self.page.locator(".field-validation-error").all()
            errors.extend([item.text_content() for item in items])
        except TimeoutError:
            pass

        return errors

    def get_email_exists_error(self) -> str:
        return self.get_text(".message-error li")