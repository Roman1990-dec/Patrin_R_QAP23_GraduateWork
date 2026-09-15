from playwright.sync_api import Page

from pages.base_page import BasePage


class RegistrationPage(BasePage):

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.gender_male = page.locator("#gender-male")
        self.gender_female = page.locator("#gender-female")
        self.first_name_input = page.locator("#FirstName")
        self.last_name_input = page.locator("#LastName")
        self.email_input = page.locator("#Email")
        self.password_input = page.locator("#Password")
        self.confirm_password_input = page.locator("#ConfirmPassword")
        self.register_button = page.locator("#register-button")
        self.success_message = page.locator(".result")
        # Локаторы для сообщений об ошибках
        self.validation_summary_items = page.locator(".validation-summary-errors li")
        self.field_validation_errors = page.locator(".field-validation-error")
        self.message_errors = page.locator(".message-error li")

    def open(self, url: str = "") -> "RegistrationPage":
        if url:
            return super().open(url)
        return super().open("/register")

    def register(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        confirm_password: str | None = None,
    ) -> "RegistrationPage":
        if confirm_password is None:
            confirm_password = password
        self.fill(self.first_name_input, first_name)
        self.fill(self.last_name_input, last_name)
        self.fill(self.email_input, email)
        self.fill(self.password_input, password)
        self.fill(self.confirm_password_input, confirm_password)
        self.click(self.register_button)
        return self

    def submit_empty_form(self) -> "RegistrationPage":
        self.click(self.register_button)
        return self

    def get_success_message(self) -> str:
        return self.get_text(self.success_message)

    def get_error_message(self) -> str:
        for item in self.validation_summary_items.all():
            if item.is_visible():
                return item.text_content() or ""
        for item in self.field_validation_errors.all():
            if item.is_visible():
                return item.text_content() or ""
        for item in self.message_errors.all():
            if item.is_visible():
                return item.text_content() or ""
        raise AssertionError("No error message found on the page")

    def get_all_error_messages(self) -> list[str]:
        errors: list[str] = []
        for item in self.validation_summary_items.all():
            if item.is_visible():
                errors.append(item.text_content() or "")
        for item in self.field_validation_errors.all():
            if item.is_visible():
                errors.append(item.text_content() or "")
        for item in self.message_errors.all():
            if item.is_visible():
                errors.append(item.text_content() or "")
        return errors

    def get_email_exists_error(self) -> str:
        for item in self.message_errors.all():
            if item.is_visible():
                return item.text_content() or ""
        raise AssertionError("Email error not found")

    def select_female_gender(self) -> "RegistrationPage":
        self.click(self.gender_female)
        return self
