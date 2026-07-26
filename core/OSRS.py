from playwright.async_api import async_playwright 

async def getBondPriceOSRS(debug : bool = False) -> tuple[str,str]:
    async with async_playwright() as p:
        driver = await p.firefox.launch(headless=not debug)
        page = await driver.new_page()
        await page.goto("https://prices.runescape.wiki/osrs/item/13190")
        buyPrice = await page.locator("#root > div > main > div > div.item-info-container > div.item-info-row > div.item-info-prices > div:nth-child(1) > div:nth-child(2) > span").inner_text()
        sellPrice = await page.locator("#root > div > main > div > div.item-info-container > div.item-info-row > div.item-info-prices > div:nth-child(2) > div:nth-child(2) > span").inner_text()
        return (sellPrice, buyPrice)
