import allure
import pytest

from config.base import E_MSG_LOGIN, E_MSG_LOGIN_USERNAME, E_MSG_LOGIN_PASSWORD
from config.users import USER1_NAME, USERS_PASSWORD, USER_FAKE_NAME
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


HEAD_FLAG = True

@allure.epic("SauceDemo")
@allure.parent_suite("SauceDemo")
@allure.feature("Авторизация - Логин по имени и паролю")
@allure.suite("Авторизация - Логин по имени и паролю")
class TestAuth:

    @allure.story("Успешный вход")
    @allure.sub_suite("Успешный вход")
    # @pytest.mark.flaky(reruns=2, rerun_delay=2)
    @allure.title("auth_001 Успешный вход")
    # @pytest.mark.parametrize("page",
    #                          [(HEAD_FLAG, "chrome"),
    #                           (HEAD_FLAG, "safari"),
    #                           (HEAD_FLAG, "firefox")],
    #                          indirect=True)
    def test_auth_001(self, page):
        """ Успешный вход со стандартным пользователем """
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

    @allure.story("Негативные тесты")
    @allure.title("auth_003-008 Вход с неверными данными")
    @pytest.mark.flaky
    @pytest.mark.parametrize(
        "page,username,password,error_msg",
        [(HEAD_FLAG, USER1_NAME, "wrong_password", E_MSG_LOGIN),
         (HEAD_FLAG, USER_FAKE_NAME, USERS_PASSWORD, E_MSG_LOGIN),
         (HEAD_FLAG, "", USERS_PASSWORD, E_MSG_LOGIN_USERNAME),
         (HEAD_FLAG, USER1_NAME, "", E_MSG_LOGIN_PASSWORD),
         (HEAD_FLAG, "admin' OR 1=1", "any", E_MSG_LOGIN),
         (HEAD_FLAG, "' OR '1'='1", "any", E_MSG_LOGIN),
         (HEAD_FLAG, "1 UNION SELECT username, password FROM users", "any",
          E_MSG_LOGIN),
         (HEAD_FLAG, "1 AND (SELECT COUNT(*) FROM users WHERE id=5)=1", "any",
          E_MSG_LOGIN),
         (HEAD_FLAG, "<script>alert(1)</script>", "any", E_MSG_LOGIN)],
        indirect = ["page"]
        )
    def test_auth_003_004_005_006_007_008(self, page, username, password, error_msg):
        """
        Тесты Авторизации:
        003 Вход с неверным паролем
        004 Вход с несуществующим логином
        005 Пустой логин
        006 Пустой пароль

        :param page: фикстура браузера со страницей
        :param username: имя пользователя
        :param password: пароль пользователя
        :param error_msg: сообщение об ошибке
        :return: None
        """
        login_page = LoginPage(page)
        login_page.open()
        login_page.login_procedure(username, password)
        assert login_page.check_error_with_msg(error_msg), "Что-то пошло не так!"


