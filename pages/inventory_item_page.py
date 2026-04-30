import allure
from playwright.sync_api import expect

from config.products import BACKPACK, COLOR_RED
from pages.common_page import CommonPage


class InvItemPage(CommonPage):

    def __init__(self, page):
        super().__init__(page)
        self.app_logo = self.page.locator(".app_logo2")
        self.backpack_item = self.page \
            .locator(".inventory_details_container").filter(has_text=BACKPACK)
        self.backpack_name = self.backpack_item.page.get_by_text(BACKPACK)
        self.backpack_price = self.backpack_item.locator(".inventory_details_price")
        self.backpack_btn = self.backpack_item.get_by_role("button")

    def get_backpack_price(self) -> str:
        price_ = self.backpack_price.text_content()
        with allure.step(f"Получена цена: {price_}"):
            ...
        return price_  # .replace("$", "")

    @allure.step("Проверка: это цена!")
    def check_is_price(self):
        assert self.get_backpack_price().startswith("$")

    @allure.step("Нажать на карточке на кнопку")
    def click_on_cart_btn(self):
        self.backpack_btn.click()

    @allure.step("Получить название кнопки на карточке")
    def get_btn_name_on_cart(self):
        return self.backpack_btn.text_content()

    @allure.step("Виден рюкзак")
    def check_backpack_visible(self):
        expect(self.backpack_name).to_be_visible()
        expect(self.backpack_price).to_be_visible()
        expect(self.backpack_btn).to_be_visible()

    def check_color_card_button(self, value: str = COLOR_RED):
        # bg_color = self.backpack_btn.evaluate("el => getComputedStyle(el).backgroundColor")
        # styles = self.backpack_btn.evaluate("el => getComputedStyle(el)")
        # print(f"{bg_color=}")
        # print("\n".join([f"{key} = '{value}'" for key, value in styles.items()]))
        expect(self.backpack_btn).to_have_css("color", value)
        expect(self.backpack_btn).to_have_css("border-top-color", value)
        expect(self.backpack_btn).to_have_css("border-bottom-color", value)
        expect(self.backpack_btn).to_have_css("border-left-color", value)
        expect(self.backpack_btn).to_have_css("border-right-color", value)
