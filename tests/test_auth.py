import pytest

from config.users import USER1_NAME, USERS_PASSWORD, USER_FAKE_NAME
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class TestAuth:

    def test_auth_001(self, page):
        login_page = LoginPage(page)
        # Шаг 1 Перейти на главную страницу (аутентификация)
        login_page.open()
        # Шаг 2	Ввести имя
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
        assert inventory_page.have_title("Products"), "Заголовок не тот"

    @pytest.mark.parametrize("usename,password",
                             [(USER1_NAME, "wrong_password"),
                              (USER_FAKE_NAME, USERS_PASSWORD)]
                             )
    def test_auth_003_004(self, page, usename, password):
        login_page = LoginPage(page)
        # Шаг 1 Перейти на главную страницу (аутентификация)
        login_page.open()
        # Шаг 2	Ввести имя
        login_page.fill_username(usename)
        login_page.check_field_username(usename)
        # Шаг 3	Ввести пароль
        login_page.fill_password(password)
        login_page.check_field_password(password)
        # Шаг 4	Нажать Login
        login_page.click_btn_login()
        assert login_page.check_error_with_msg, "Что-то пошло не так!"
