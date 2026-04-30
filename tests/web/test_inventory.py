import allure
import pytest

from pages.inventory_page import InventoryPage

@allure.epic("SauceDemo")
@allure.parent_suite("SauceDemo")
@allure.feature("Страница товаров")
@allure.suite("Страница товаров")
class TestInventory:

    @allure.title("Инвентори 01")
    def test_inv_001(self, login):
        inv_page = InventoryPage(login)
        inv_page.check_items_count()
