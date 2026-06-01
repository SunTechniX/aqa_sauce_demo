from playwright.sync_api import expect

from config.products import COLOR_RED
from pages.base_page import BasePage


class CommonPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.ring_card_count = self.page.locator(".shopping_cart_badge")
        self.app_logo = self.page.locator(".app_logo")

    def check_color_on_ring_card(self, value: str = COLOR_RED):
        expect(self.ring_card_count).to_have_css("background-color", value)

    def check_count_on_ring_card(self, value: str = "1"):
        expect(self.ring_card_count).to_have_text(value)
