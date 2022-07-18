import asyncio

from playwright.async_api import async_playwright
import Price


async def price(Server, Subserver):
    async with async_playwright() as playwright:
        price_gold = await Price.price_server(playwright, Server, Subserver)
    return price_gold
