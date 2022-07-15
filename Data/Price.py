import time
import traceback
import DataBase
from selenium.webdriver.common.by import By
from playwright.sync_api import Playwright, sync_playwright, expect


def price():
    try:
        driver = DataBase.Datas()
        price_max = []
        base_url = 'https://jx3.seasunwbl.com/buyer'
        driver.get(base_url)

        # 获取服务器金价(万宝楼)
        for i in range(1, len(driver.find_element(by=By.XPATH,
                                                  value="//*[@id='app']/div/div[3]/div/div[2]/div[1]/div[2]/div").text.split(
            "\n")) + 1):
            print(driver.find_element(by=By.XPATH,
                                      value="//*[@id='app']/div/div[3]/div/div[2]/div[1]/div[2]/div/div[" + str(
                                          i) + "]").text)
            driver.find_element(by=By.XPATH,
                                value="//*[@id='app']/div/div[3]/div/div[2]/div[1]/div[2]/div/div[" + str(
                                    i) + "]").click()

            servers = driver.find_element(by=By.XPATH,
                                          value="//*[@id='app']/div/div[3]/div/div[2]/div[2]/div[2]/div").text.split(
                "\n")
            for n in range(1, len(servers) + 1):
                driver.find_element(by=By.XPATH,
                                    value="//*[@id='app']/div/div[3]/div/div[2]/div[2]/div[2]/div/div[" + str(
                                        n) + "]").click()
                time.sleep(0.5)
                price_Total = driver.find_element(by=By.XPATH,
                                                  value="//*[@id='app']/div/div[3]/div/div[3]").text.split(
                    "\n")
                for i in price_Total:
                    if i.find("1元=") != -1:
                        price_max.append(i.split("=")[1].split("金")[0])
                print(servers[n - 1] + " 目前最高金价:" + max(price_max))
                price_max.clear()
            print("**" * 20)
        driver.quit()
    except:
        print(traceback.format_exc())
        print("价格获取失败")


def price_server(playwright, Server, Subserver):
    try:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        # Open new page
        page = context.new_page()
        page.goto("https://jx3.seasunwbl.com/buyer?t=coin")

        page.locator("text=" + Server).click()
        page.locator("text=" + Subserver).click()
        page.wait_for_timeout(500)
        prices = page.locator("//*[@id='app']/div/div[3]/div/div[3]/div[2]/div[4]").text_content()
        price = str(prices).split("=")[1]
        context.close()
        browser.close()
        return price
    except:
        print("价格获取失败")
        return None