import asyncio

from playwright.async_api import async_playwright
import Price
import Role


async def price(Server, Subserver):
    async with async_playwright() as playwright:
        price_gold = await Price.price_server(playwright, Server, Subserver)
    return price_gold


async def role(school):
    async with async_playwright() as playwright:
        role_choose = await Role.role_server(playwright,school)
    return role_choose
role = asyncio.run(role("蓬莱"))
print(role)