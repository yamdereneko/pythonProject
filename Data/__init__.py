import DataBase
import Price
from playwright.sync_api import Playwright, sync_playwright, expect

if __name__ == '__main__':
    with sync_playwright() as playwright:
        Server = "电信五区"
        Subserver = "斗转星移"
        price = Price.price_server(playwright, Server, Subserver)
        print(price)
