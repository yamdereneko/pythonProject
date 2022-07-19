import asyncio
import sys
import time

from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright


async def role_server(playwright, school):
    try:
        # 开启浏览器，默认设置浏览器引擎为chromium。
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(5000)
        # 进入网站去获取各个门派总号数
        await page.goto("https://jx3.seasunwbl.com/buyer?t=role")
        await page.locator("text=更多筛选条件").click()
        await page.locator("text=" + school).first.click()
        await page.wait_for_timeout(200)
        await page.locator("[aria-label=\"icon\\: search\"] svg").click()
        await page.wait_for_timeout(200)

        dict_role = {}

        # 查询成男号的数量
        if await page.locator("text=" + school).first.text_content() != "七秀坊":
            size = '成男'
            Total = await searchBodySize(page, school, size)
            dict_role[school+size] = Total
            print(dict_role)
        else:
            print("七秀没有男妹妹哟")

        # 查询成女号的数量
        if await page.locator("text=" + school).first.text_content() != "少林寺":
            size = '成女'
            Total = await searchBodySize(page, school, size)
            dict_role[school+size] = Total
        else:
            print("少林寺没有女妹妹哟")

        # 查询萝莉号数量
        if await page.locator("text=" + school).first.text_content() != "少林寺":
            size = '萝莉'
            Total = await searchBodySize(page, school, size)
            dict_role[school+size] = Total
        else:
            print("少林寺没有女妹妹哟")

        # 查询正太号数量
        size = '正太'
        Total = await searchBodySize(page, school, size)
        dict_role[school+size] = Total

        await context.close()
        await browser.close()
        print(dict_role)
        return dict_role
    except Exception as e:
        print("门派获取失败")
        print(e)


async def searchBodySize(page, school, size):
    await page.locator("text=" + size).click()
    await page.wait_for_timeout(1000)
    await page.locator("text=查询").click()
    await page.wait_for_timeout(1000)
    if not await page.locator("//*[@id='app']/div/div[3]/div/div[3]/div[4]/ul/li[9]").is_visible(timeout=2000):
        print("没有这个选项")
        sys.exit(1)
    await page.wait_for_timeout(1000)
    size_count = await page.locator("//*[@id='app']/div/div[3]/div/div[3]/div[4]/ul/li[9]").text_content()
    await page.wait_for_timeout(500)
    await page.locator("//*[@id='app']/div/div[3]/div/div[3]/div[4]/ul/li[9]").click()
    await page.wait_for_timeout(500)
    rows = await page.locator("div.app-web-components-role-item-styles-index-m__roleItem--1R4F8").all_text_contents()
    sizeCount = (int(size_count) - 1) * 10 + len(rows)
    await page.wait_for_timeout(200)
    await page.locator("text=" + size).click()
    return sizeCount


async def role(school):
    async with async_playwright() as playwright:
        role_choose = await role_server(playwright, school)
    return role_choose


asyncio.run(role("纯阳"))
# asyncio.run(role("七秀坊"))
# asyncio.run(role("少林寺"))
