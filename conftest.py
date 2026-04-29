import allure
import pytest
from playwright.sync_api import sync_playwright

from config.users import USER1_NAME, USERS_PASSWORD
from pages.login_page import LoginPage


HEAD_FLAG = True


def pytest_addoption(parser):
    parser.addoption(
        "--bro", action="store", default="chrome",
        help="use --bro: chrome, firefox, safari"
    )


@pytest.fixture
def page(request):
    browser_ = "_X_"
    if hasattr(request, "param"):
        browser_ = "chrome"
        if isinstance(request.param, tuple):
            headless_ = request.param[0]
            if len(request.param) > 1:
                browser_ = request.param[1]
        else:
            headless_ = request.param
    else:
        headless_ = True  # HEAD_FLAG
    with (sync_playwright() as drv):
        bro_name = request.config.getoption("--bro")
        if browser_ == "chrome":
            drv_bro = drv.chromium
        elif browser_ == "firefox":
            drv_bro = drv.firefox
        elif browser_ == "safari" or browser_ == "webkit":
            drv_bro = drv.webkit
        else:
            if bro_name == "chrome" or bro_name == "chromium":
                drv_bro = drv.chromium
            elif bro_name == "firefox":
                drv_bro = drv.firefox
            elif bro_name == "safari":
                drv_bro = drv.webkit
            else:
                drv_bro = drv.chromium

        print(f"{browser_=} {bro_name=}")
        browser = drv_bro.launch(headless=headless_, slow_mo=500)
        page = browser.new_page()
        page.set_default_timeout(4_000)  # 1_100
        yield page
        browser.close()


@allure.title("Логин в магазин: '{USER1_NAME}' / 'USERS_PASSWORD'")
@pytest.fixture(params=[(USER1_NAME, USERS_PASSWORD)])
def login(request, page):
    username, password = request.param
    login_page = LoginPage(page)
    login_page.open()
    login_page.login_procedure(username, password)
    yield login_page.page


@pytest.fixture
def mobile(request):
    browser_ = "chrome"
    device_id = "Pixel 4"
    if hasattr(request, "param") and  isinstance(request.param, tuple):
        if len(request.param) == 2:
            browser_, device_id = request.param

    with (sync_playwright() as drv):
        # print("\n".join(list(drv.devices.keys())))
        drv_bro = getattr(drv, browser_)
        browser = drv_bro.launch(headless=HEAD_FLAG, slow_mo=500)
        print(drv.devices[device_id])
        context = browser.new_context(**drv.devices[device_id])
        mobile_ = context.new_page()
        mobile_.set_default_timeout(5_000)  # 1_100
        yield mobile_
        browser.close()


@pytest.fixture
def page_at():
    with (sync_playwright() as drv):
        drv_bro = drv.chromium
        browser = drv_bro.launch(headless=HEAD_FLAG, slow_mo=500)
        page_ = browser.new_page()
        page_.set_default_timeout(4_000)  # 1_100
        yield page_
        browser.close()


# @pytest.hookimpl(tryfirst=True, wrapper=True)
# def pytest_runtest_makereport(item, call):
#     rep = yield
#     node = rep.nodeid.replace("::", "_").replace(".", "_")
#     file_path = f"screenshot_{node}.png"
#     if rep.when == "call" and rep.failed:
#         page_ = item.funcargs.get("page")
#         page_.screenshot(path=file_path)
#
#         with open(file_path, "rb") as f:
#             allure.attach(
#                 f.read(),
#                 name=f"Кадр при падении '{item.name}'",
#                 attachment_type=allure.attachment_type.PNG
#             )
#     return rep
