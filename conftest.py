import pytest
from playwright.sync_api import sync_playwright

from config.base import URL_BASE


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
        headless_ = False
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
