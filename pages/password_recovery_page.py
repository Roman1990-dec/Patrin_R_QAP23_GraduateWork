from playwright.sync_api import Page

from pages.base_page import BasePage


class PasswordRecoveryPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.email_input = page.locator("#Email")
        self.recover_button = page.locator("input[value='Recover']")
        self.result_message = page.locator(".result")
        self.validation_error = page.locator(".field-validation-error")

    def open(self, url: str = "") -> "PasswordRecoveryPage":
        if url:
            return super().open(url)
        return super().open("/passwordrecovery")

    def recover_password(self, email: str) -> "PasswordRecoveryPage":
        self.fill(self.email_input, email)
        self.click(self.recover_button)
        return self

    def submit_empty_form(self) -> "PasswordRecoveryPage":
        self.click(self.recover_button)
        return self

    def get_result_message(self) -> str:
        return self.get_text(self.result_message)

    def get_validation_error(self) -> str:
        return self.get_text(self.validation_error)
