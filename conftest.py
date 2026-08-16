import allure
import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="function")
def page():
    """Создаёт новую страницу браузера для каждого теста"""
    with sync_playwright() as p:
        # Запускаем браузер (headless=False, чтобы видеть браузер при отладке)
        browser = p.chromium.launch(headless=False)
        # Создаёт новый контекст браузера — изолированную среду с собственными куками, локальным хранилищем, сессиями
        context = browser.new_context()
        # Открывает новую вкладку (страницу) внутри этого контекста
        page = context.new_page()
        # возвращает объект page в тест, но при этом функция не завершается — она «замораживается» и ждёт, пока тест завершится
        yield page
        # После теста закрываем контекст и браузер, чтобы освободить ресурсы (память, процессы)
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