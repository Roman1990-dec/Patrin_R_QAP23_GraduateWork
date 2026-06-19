import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="function")
def page():
    """Фикстура создаёт новую страницу браузера для каждого теста."""
    with sync_playwright() as p:
        # Запускаем браузер (headless=False, чтобы видеть браузер при отладке)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        # После теста закрываем
        context.close()
        browser.close()


@pytest.fixture(scope="session")
def base_url():
    return "https://demowebshop.tricentis.com"
