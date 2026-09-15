from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.email_input = page.locator("#Email")
        self.password_input = page.locator("#Password")
        self.login_button = page.locator("input[value='Log in']")
        self.login_link_header = page.locator("a.ico-login")
        self.error_message = page.locator(".validation-summary-errors li")
        self.logout_link = page.locator("a.ico-logout")
        self.account_link = page.locator("div.header-links a.account")
        self.login_form_header = page.locator("h1")
        self.remember_me_checkbox = page.locator("#RememberMe")
        self.forgot_password_link = page.locator(".forgot-password a")

    def login(self, email: str, password: str) -> "LoginPage":
        self.fill(self.email_input, email)
        self.fill(self.password_input, password)
        self.click(self.login_button)
        return self

    def get_error_message(self) -> str:
        return self.get_text(self.error_message)

    def is_logged_in(self) -> bool:
        return self.is_visible(self.logout_link)

    def get_account_email(self) -> str:
        return self.get_text(self.account_link)

    def is_account_correct(self, expected_email: str) -> bool:
        if not self.is_visible(self.account_link):
            return False
        return self.get_account_email() == expected_email

    def open(self, url: str = "") -> "LoginPage":
        if url:
            return super().open(url)
        return super().open("/login")

    def is_forgot_password_link_visible(self) -> bool:
        return self.is_visible(self.forgot_password_link)

    def click_forgot_password(self):
        self.click(self.forgot_password_link)
        from pages.password_recovery_page import PasswordRecoveryPage

        return PasswordRecoveryPage(self.page, self.base_url)

    def submit_empty_form(self) -> "LoginPage":
        self.click(self.login_button)
        return self

    def logout(self) -> "LoginPage":
        self.click(self.logout_link)
        self.wait_visible(self.login_link_header)
        return self

    def is_logout_link_visible(self) -> bool:
        return self.is_visible(self.logout_link)
