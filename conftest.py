import pytest
from playwright.sync_api import sync_playwright

from config.base import URL_BASE


@pytest.fixture
def page():
    with sync_playwright() as drv:
        browser = drv.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        page.set_default_timeout(3_000)
        yield page
        browser.close()
