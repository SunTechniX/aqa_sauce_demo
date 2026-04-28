from playwright.sync_api import expect
import pytest
from config.base import URL_BASE_ROOT
from config.users import USER1_NAME, USERS_PASSWORD
from pages.inventory_item_page import InvItemPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class TestCheckout:

    @pytest.mark.parametrize("page",
                             [(False, "chrome")],
                             indirect=True)
    def test_check_001(self, page):
        login_page = LoginPage(page)
        # Шаг 1 Открыть сайт
        login_page.open()
        expect(page).to_have_url(URL_BASE_ROOT)
        # Шаг 2	Ввести логин
        login_page.fill_username(USER1_NAME)
        login_page.check_field_username(USER1_NAME)
        # Шаг 3	Ввести пароль
        login_page.fill_password(USERS_PASSWORD)
        login_page.check_field_password(USERS_PASSWORD)
        # Шаг 4	Нажать Login
        login_page.click_btn_login()
        login_page.expect_to_have_url("/inventory.html")
        # Шаг 5	Найти товар "Sauce Labs Backpack"
        inventory_page = InventoryPage(page)
        inventory_page.check_backpack_visible()
        # Шаг 6	Сохранить цену товара
        price1 = inventory_page.get_backpack_price()
        inventory_page.check_is_price()
        print(f"'{price1}'")
        # Шаг 7	Нажать "Add to cart" для товара
        # inventory_page.click_btn_add_to_cart()

        inventory_page.click_on_cart_btn()
        print(inventory_page.get_btn_name_on_cart())
        inventory_page.check_color_card_button()
        inventory_page.check_color_on_ring_card()
        inventory_page.check_count_on_ring_card("1")

        # inventory_page.click_on_cart_btn()
        # print(inventory_page.get_btn_name_on_cart())
        # inventory_page.check_color_card_button(COLOR_BLACK)

        # Переход в item
        inventory_page.click_on_cart_title()

        # Проверки карточки в одном item
        inv_item_page = InvItemPage(page)
        inv_item_page.check_backpack_visible()

        # Сохранить цену товара
        price2 = inv_item_page.get_backpack_price()
        inv_item_page.check_is_price()
        print(f"'{price2}'")
        # print(inventory_page.get_btn_name_on_cart())
        inv_item_page.check_color_card_button()
        inv_item_page.check_color_on_ring_card()
        inv_item_page.check_count_on_ring_card("1")
        page.wait_for_timeout(2)
