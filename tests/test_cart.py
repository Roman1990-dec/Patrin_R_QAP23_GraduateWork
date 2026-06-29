import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.cart_page import CartPage

class TestCart:

    def test_add_item_to_cart(self, page, base_url):
        login_page = LoginPage(page, base_url)
        login_page.open().login("rptest@mail.com", "123456!")
        page.wait_for_url("https://demowebshop.tricentis.com/", timeout=5000)
        assert login_page.is_logged_in()

        home_page = HomePage(page, base_url)
        home_page.open()
        books_page = home_page.go_to_books_category()
        product_page = books_page.open_computing_book()
        product_page.add_to_cart()

        cart_page = CartPage(page, base_url)
        cart_page.open()
        assert cart_page.get_number_of_items() == 1, "Товар не добавился"

    def test_update_item_quantity(self, page, base_url):
        login_page = LoginPage(page, base_url)
        login_page.open().login("rptest@mail.com", "123456!")
        page.wait_for_url("https://demowebshop.tricentis.com/", timeout=5000)
        assert login_page.is_logged_in()

        home_page = HomePage(page, base_url)
        home_page.open()   # явно открываем главную перед переходом в Books
        books_page = home_page.go_to_books_category()
        product_page = books_page.open_computing_book()
        product_page.add_to_cart()

        cart_page = CartPage(page, base_url)
        cart_page.open()
        cart_page.update_quantity("3")
        quantity = cart_page.get_quantity_value()
        assert quantity == "3", f"Ожидалось 3, получено {quantity}"