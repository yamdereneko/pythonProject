from playwright.sync_api import sync_playwright


async def role_server(playwright, school):
    try:
        browser = await playwright.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://jx3.seasunwbl.com/buyer?t=role")
        await page.locator("text=更多筛选条件").click()
        await page.locator("text=" + school).first.click()
        await page.locator("[aria-label=\"icon\\: search\"] svg").click()
        await page.wait_for_timeout(500)
        roles = await page.locator("//*[@id='app']/div/div[3]/div/div[3]/div[4]/ul/li[9]").text_content()
        return roles
    except Exception as e:
        print("门派获取失败")
        print(e)
        return None
