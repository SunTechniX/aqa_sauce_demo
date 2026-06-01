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

    @allure.title("TC_TOUCH_003")
    @pytest.mark.test
    @pytest.mark.parametrize("mobile", [("chromium", "Pixel 5")],
                             indirect=True)
    def test_mobile_touch_003(self, mobile):
        login_page = LoginPage(mobile)
        login_page.open()
        login_page.fill_username("user")
        # inputmode = "numeric"

    @allure.title("TC_TOUCH_004")
    @pytest.mark.test
    @pytest.mark.parametrize("mobile", [("chromium", "Pixel 5", False)],
                             indirect=True)
    def test_mobile_touch_004(self, login_mobile):
        inv = InventoryPage(login_mobile)
        #w inv.swipe_screen()
        inv.page.mouse.wheel(0, 300)
        # inv.swipe_down(".inventory_list")
        # inv.swipe_down(".inventory_container")
        # inv.swipe_element(".inventory_container", direction="down")
        #login_mobile.pause()
        login_mobile.wait_for_timeout(2_000)
