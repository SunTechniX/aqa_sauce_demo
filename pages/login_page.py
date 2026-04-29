import allure
from playwright.sync_api import expect

from config.base import E_MSG_LOGIN
from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page_):
        super().__init__(page_)
        self.field_username = self.page.locator("#user-name")
        self.field_password = self.page.locator("#password")
        # self.btn_login = self.page.locator("[data-test='login-button']")
        # self.btn_login = self.page.get_by_test_id("login-button")
        self.btn_login = self.page.get_by_role("button", name="Login")
        self.error = self.page.locator(".error-message-container")

    @allure.step("Ввести имя пользователя: '{username}'")
    def fill_username(self, username):
        self.field_username.fill(username)

    @allure.step("Ввести пароль: '{password}'")
    def fill_password(self, password):
        self.field_password.fill(password)

    @allure.step("Нажать кнопку 'Login'")
    def click_btn_login(self):
        self.btn_login.click()

    @allure.step("Тап по кнопке 'Login'")
    def tap_btn_login(self):
        self.btn_login.tap()

    @allure.step("Проверить, что в поле 'Пользователь' есть текст: '{username}'")
    def check_field_username(self, username):
        expect(self.field_username).to_have_value(username)

    @allure.step("Проверить, что в поле 'Пароль' есть текст: '{password}'")
    def check_field_password(self, password):
        expect(self.field_password).to_have_value(password)

    @allure.step("Процедура логина user: '{username}', password: '{password}'")
    def login_procedure(self, username, password):
        self.fill_username(username)
        self.fill_password(password)
        self.click_btn_login()

    @allure.step("Проверить: отображается ошибка '{error_msg}'")
    def check_error_with_msg(self, error_msg=E_MSG_LOGIN):
        # expect(self.error).to_have_element(".error-message")
        expect(self.error).to_be_visible()
        expect(self.error).to_have_text(error_msg)
        return True
