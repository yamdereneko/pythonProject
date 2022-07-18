from playwright.sync_api import sync_playwright


def role_server(playwright, page, school):
    try:
        page.goto("https://jx3.seasunwbl.com/buyer?t=role")
        page.locator("text=更多筛选条件").click()
        page.locator("text=" + school).first.click()
        page.locator("[aria-label=\"icon\\: search\"] svg").click()
        page.wait_for_timeout(500)
        roles = page.locator("//*[@id='app']/div/div[3]/div/div[3]/div[4]/ul/li[9]").text_content()
        return roles
    except Exception as e:
        print("门派获取失败")
        print(e)
        return None
