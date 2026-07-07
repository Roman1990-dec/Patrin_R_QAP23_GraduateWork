import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

class TestCheckout:

    def test_checkout_as_authenticated_user(self, page, base_url):
        # 1. Авторизация
        login_page = LoginPage(page, base_url)
        login_page.open().login("rptest@mail.com", "123456!")
        page.wait_for_url("https://demowebshop.tricentis.com/", timeout=5000)
        assert login_page.is_logged_in()

        # 2. Добавление товара
        home_page = HomePage(page, base_url)
        home_page.open()
        books_page = home_page.go_to_books_category()
        product_page = books_page.open_computing_book()
        product_page.add_to_cart()

        # 3. Переход в корзину, согласие с условиями и переход к оформлению
        cart_page = CartPage(page, base_url)
        cart_page.open()
        cart_page.agree_to_terms()          # <-- добавили
        checkout_page = cart_page.proceed_to_checkout()

        # 4. Заполнение адреса
        checkout_page.fill_billing_address(
            first_name="Roman",
            last_name="Patrin",
            email="rptest@mail.com",
            city="New York",
            address="123 Main St",
            zip_code="10001",
            phone="1234567890"
        )

        # 5. Выбор доставки и оплаты
        checkout_page.select_shipping_method(0)
        checkout_page.select_payment_method(0)

        # 6. Подтверждение
        checkout_page.confirm_order()

        # 7. Проверка
        success_msg = checkout_page.get_success_message()
        assert "Your order has been successfully processed!" in success_msg
        order_number = checkout_page.get_order_number()
        assert order_number != ""

    def test_checkout_as_guest(self, page, base_url):
        # 1. Добавление товара без логина
        home_page = HomePage(page, base_url)
        home_page.open()
        books_page = home_page.go_to_books_category()
        product_page = books_page.open_computing_book()
        product_page.add_to_cart()

        # 2. Переход в корзину, согласие и оформление
        cart_page = CartPage(page, base_url)
        cart_page.open()
        cart_page.agree_to_terms()          # <-- добавили
        checkout_page = cart_page.proceed_to_checkout()

        # 3. Нажатие "Checkout as Guest"
        checkout_page.checkout_as_guest()

        # 4. Заполнение адреса
        checkout_page.fill_billing_address(
            first_name="Guest",
            last_name="User",
            email="guest@example.com",
            city="Los Angeles",
            address="456 Oak Ave",
            zip_code="90210",
            phone="9876543210"
        )

        # 5. Выбор доставки и оплаты
        checkout_page.select_shipping_method(0)
        checkout_page.select_payment_method(0)

        # 6. Подтверждение
        checkout_page.confirm_order()

        # 7. Проверка
        success_msg = checkout_page.get_success_message()
        assert "Your order has been successfully processed!" in success_msg