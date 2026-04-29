from playwright.sync_api import sync_playwright, expect


def test_at_auth_color(page_at):
        page_at.goto("https://automationteststore.com/")
        link = page_at.get_by_role("link", name="Login or register")
        print(f"{link.get_attribute("href")}")
        link.click()
        btn_login = page_at.get_by_role("button", name="Login")
        # attr = btn_login.get_attribute("title")
        # btn_login = page_at.evaluate_handle("//button[@title='Login']")
        expect(btn_login).to_have_css("background-color", "rgb(242, 92, 39)") # "rgb(216, 66, 14)")
        btn_login.hover()
        expect(btn_login).to_have_css("background-color", "rgb(216, 66, 14)")

        bg_color = btn_login.evaluate("el => getComputedStyle(el).backgroundColor")
        styles = btn_login.evaluate("el => getComputedStyle(el)")
        print(f"{bg_color=}")
        print("\n".join([f"{key} = '{value}'" for key, value in styles.items()]))

        # attr = btn_login.evaluate(
        #     "btn_login => window.getComputedStyle(btn_login).getPropertyValue('background-color')",
        #     btn_login
        #     )
        # print(f"{attr=}")
        # page.get_by_role("button", name=" Login").click()
