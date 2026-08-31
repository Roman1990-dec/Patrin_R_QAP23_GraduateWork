import os
import allure
import pytest
from playwright.sync_api import Page, sync_playwright


@pytest.fixture(scope="function")
def page():
    # Проверяем переменную окружения HEADLESS (по умолчанию False)
    headless = os.environ.get("HEADLESS", "false").lower() == "true"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.fixture(scope="session")
def base_url():
    return "https://demowebshop.tricentis.com"

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Делает скриншот, если тест упал, и прикрепляет его к Allure-отчёту."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        # Получаем фикстуру page из теста
        page = item.funcargs.get("page")
        if page and isinstance(page, Page):
            screenshot = page.screenshot(full_page=True)
            allure.attach(
                screenshot,
                name="Скриншот при падении",
                attachment_type=allure.attachment_type.PNG
            )