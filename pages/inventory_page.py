from playwright.sync_api import expect

from config.products import BACKPACK
from pages.base_page import BasePage


class InventoryPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        # Находим карточку товара по тексту внутри
        self.backpack_item = self.page \
            .locator(".inventory_item").filter(has_text=BACKPACK)
        self.backpack_name = self.backpack_item.page.get_by_text(BACKPACK)
        self.backpack_price = self.backpack_item.locator(".inventory_item_price")
        self.backpack_btn = self.backpack_item.get_by_role("button")

        # следующие варианты тоже рабочие:
        #[w] self.backpack_price = self.page.locator(f".inventory_item:has-text('{BACKPACK}') .inventory_item_price")
        #[w] self.backpack_btn = self.backpack_item.locator("//button[contains(@class, 'btn_inventory')]")
        #[w] self.backpack_btn = self.backpack_item.locator(".btn_inventory")  # [contains(@class, 'btn_inventory')]

    def check_backpack_visible(self):
        expect(self.backpack_name).to_be_visible()

    def get_backpack_price(self) -> str:
        return self.backpack_price.text_content()

    def check_is_price(self):
        assert self.get_backpack_price().startswith("$")

    def click_btn_add_to_cart(self):
        self.backpack_btn.click()
