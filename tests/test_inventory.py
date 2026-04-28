import allure
import pytest

from pages.inventory_page import InventoryPage


class TestInventory:

    def test_inv_001(self, login):
        inv_page = InventoryPage(login)
        inv_page.check_items_count()
