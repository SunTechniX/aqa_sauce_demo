import allure
from playwright.sync_api import expect

from config.products import BACKPACK, COLOR_RED
from pages.inventory_item_page import InvItemPage


class InventoryPage(InvItemPage):

    def __init__(self, page):
        super().__init__(page)
        self.title = self.page.locator(".title")
        # Находим карточку товара по тексту внутри
        self.backpack_item_list = self.page.locator(".inventory_item")
        self.backpack_item = self.backpack_item_list.filter(has_text=BACKPACK)
        self.backpack_name = self.backpack_item.page.get_by_text(BACKPACK)
        self.backpack_price = self.backpack_item.locator(".inventory_item_price")
        self.backpack_btn = self.backpack_item.get_by_role("button")
        # следующие варианты тоже рабочие:
        #[w] self.backpack_price = self.page.locator(f".inventory_item:has-text('{BACKPACK}') .inventory_item_price")
        #[w] self.backpack_btn = self.backpack_item.locator("//button[contains(@class, 'btn_inventory')]")
        #[w] self.backpack_btn = self.backpack_item.locator(".btn_inventory")  # [contains(@class, 'btn_inventory')]

    @allure.step("Нажать на карточке на заголовок")
    def click_on_cart_title(self):
        self.backpack_name.click()

    @allure.step("Проверка: есть заголовок '{title_text}'")
    def have_title(self, title_text: str):
        expect(self.title).to_be_visible()
        expect(self.title).to_have_text(title_text)
        return True

    @allure.step("Проверить: количество карточек равно {expect_value}")
    def check_items_count(self, expect_value: int = 6):
        cnt = len(self.backpack_item_list.all())
        assert cnt == expect_value, \
            f"Количество карточек ожидалось:   {expect_value}\n" \
            f"Количество карточек на странице: {cnt}"
