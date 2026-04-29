import allure
from playwright.sync_api import expect
import pytest
from config.base import URL_BASE_ROOT
from config.users import USER1_NAME, USERS_PASSWORD
from pages.inventory_item_page import InvItemPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@allure.epic("SauceDemo mobile")
@allure.parent_suite("SauceDemo mobile")
class TestCheckoutMobile:

    @pytest.mark.parametrize("mobile", [("webkit", "iPhone 11"),
                                        ("chromium", "Pixel 5")], indirect=True)
    def test_check_mobile_001(self, mobile):
        login_page = LoginPage(mobile)
        # Шаг 1 Открыть мобильный сайт
        login_page.open()
        expect(mobile).to_have_url(URL_BASE_ROOT)
        print(mobile.viewport_size)
        assert mobile.viewport_size["width"] < 415, "Размер не тот!"
        # mobile.set_viewport_size({"width": 667, "height": 375})

        # Шаг 2	Ввести логин
        login_page.fill_username(USER1_NAME)
        login_page.check_field_username(USER1_NAME)
        # Шаг 3	Ввести пароль
        login_page.fill_password(USERS_PASSWORD)
        login_page.check_field_password(USERS_PASSWORD)
        # Шаг 4	Нажать Login
        login_page.tap_btn_login()
        login_page.expect_to_have_url("/inventory.html")
        # Шаг 5	Найти товар "Sauce Labs Backpack"
        inventory_page = InventoryPage(mobile)
        inventory_page.check_backpack_visible()
