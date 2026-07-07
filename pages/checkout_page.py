from pages.base_page import BasePage

class CheckoutPage(BasePage):
    # --- Локаторы для шага Billing Address ---
    FIRST_NAME = "#BillingNewAddress_FirstName"
    LAST_NAME = "#BillingNewAddress_LastName"
    EMAIL = "#BillingNewAddress_Email"
    CITY = "#BillingNewAddress_City"
    ADDRESS = "#BillingNewAddress_Address1"
    ZIP = "#BillingNewAddress_ZipPostalCode"
    PHONE = "#BillingNewAddress_PhoneNumber"
    CONTINUE_BILLING = "input[onclick='Billing.save()']"

    # --- Локаторы для шага Shipping Method ---
    SHIPPING_METHOD_GROUND = "#shippingoption_0"   # или другой вариант
    CONTINUE_SHIPPING = "input[onclick='ShippingMethod.save()']"

    # --- Локаторы для шага Payment Method ---
    PAYMENT_METHOD_CHECK = "#paymentmethod_0"      # Check/Money Order
    CONTINUE_PAYMENT = "input[onclick='PaymentMethod.save()']"

    # --- Локаторы для шага Confirm Order ---
    CONFIRM_ORDER = "input[value='Confirm']"
    SUCCESS_MESSAGE = ".title"
    ORDER_NUMBER = ".order-number strong"

    # --- Локатор для кнопки "Checkout as Guest" (только для гостя) ---
    GUEST_CHECKOUT_BUTTON = "button.checkout-as-guest-button"

    def fill_billing_address(self, first_name, last_name, email, city, address, zip_code, phone):
        """Заполняет форму адреса и нажимает Continue."""
        self.fill(self.FIRST_NAME, first_name)
        self.fill(self.LAST_NAME, last_name)
        self.fill(self.EMAIL, email)
        self.fill(self.CITY, city)
        self.fill(self.ADDRESS, address)
        self.fill(self.ZIP, zip_code)
        self.fill(self.PHONE, phone)
        self.click(self.CONTINUE_BILLING)
        # Ждём, пока загрузится следующий шаг (появление кнопки Continue для доставки)
        self.page.wait_for_selector(self.CONTINUE_SHIPPING, state="visible", timeout=10000)
        return self

    def select_shipping_method(self, method_index=0):
        """Выбирает способ доставки (по умолчанию первый) и нажимает Continue."""
        # Выбираем радио-кнопку с указанным индексом (0 - первый способ)
        shipping_radio = f"#shippingoption_{method_index}"
        self.click(shipping_radio)
        self.click(self.CONTINUE_SHIPPING)
        self.page.wait_for_selector(self.CONTINUE_PAYMENT, state="visible", timeout=10000)
        return self

    def select_payment_method(self, method_index=0):
        """Выбирает способ оплаты (по умолчанию первый) и нажимает Continue."""
        payment_radio = f"#paymentmethod_{method_index}"
        self.click(payment_radio)
        self.click(self.CONTINUE_PAYMENT)
        # На следующем шаге Payment Information может быть кнопка Continue, но для Check/Money Order её нет, сразу идёт Confirm
        # Поэтому ждём появления кнопки Confirm
        self.page.wait_for_selector(self.CONFIRM_ORDER, state="visible", timeout=10000)
        return self

    def confirm_order(self):
        """Нажимает кнопку подтверждения заказа."""
        self.click(self.CONFIRM_ORDER)
        # Ждём появления сообщения об успехе
        self.page.wait_for_selector(self.SUCCESS_MESSAGE, state="visible", timeout=15000)
        return self

    def get_success_message(self) -> str:
        """Возвращает текст сообщения об успешном оформлении."""
        return self.page.locator(self.SUCCESS_MESSAGE).text_content()

    def get_order_number(self) -> str:
        """Возвращает номер заказа."""
        return self.page.locator(self.ORDER_NUMBER).text_content()

    def checkout_as_guest(self):
        """Нажимает кнопку 'Checkout as Guest' (используется в гостевом сценарии)."""
        self.click(self.GUEST_CHECKOUT_BUTTON)
        # Ждём появления формы адреса
        self.page.wait_for_selector(self.FIRST_NAME, state="visible", timeout=10000)
        return self