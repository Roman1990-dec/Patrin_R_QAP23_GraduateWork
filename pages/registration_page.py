from pages.base_page import BasePage


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
    ERROR_SELECTORS = [  # <-- добавьте эту строку
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
        for selector in self.ERROR_SELECTORS:
            try:
                self.page.wait_for_selector(selector, state="visible", timeout=2000)
                return self.page.locator(selector).first.text_content()
            except TimeoutError:
                continue
        raise Exception("No error message found on the page")

    def get_all_error_messages(self) -> list:
        """
        Возвращает список всех видимых сообщений об ошибках на странице.
        Ищет в нескольких возможных контейнерах.
        """
        # Ждём, пока появится хотя бы одно сообщение об ошибке (любое)
        try:
            # Пробуем стандартный блок nopCommerce
            self.page.wait_for_selector(
                ".validation-summary-errors", state="visible", timeout=5000
            )
            error_items = self.page.locator(".validation-summary-errors li").all()
            return [item.text_content() for item in error_items]
        except TimeoutError:
            # Если не нашлось, пробуем другой селектор (например, для клиентской валидации)
            try:
                self.page.wait_for_selector(
                    ".field-validation-error", state="visible", timeout=2000
                )
                error_items = self.page.locator(".field-validation-error").all()
                return [item.text_content() for item in error_items]
            except TimeoutError:
                # Если ничего не найдено, пробуем собрать все элементы с классом 'error'
                try:
                    error_elements = self.page.locator(".error").all()
                    if error_elements:
                        return [
                            el.text_content()
                            for el in error_elements
                            if el.is_visible()
                        ]
                except TimeoutError:
                    pass
                return []

    def get_email_exists_error(self) -> str:
        return self.get_text(".message-error li")
