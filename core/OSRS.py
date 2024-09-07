from playwright.async_api import async_playwright 

async def getBondPriceOSRS(debug : bool = False) -> tuple[str,str]:
    async with async_playwright() as p:
        driver = await p.firefox.launch(headless=not debug)
        page = await driver.new_page()
        await page.goto("https://prices.runescape.wiki/osrs/item/13190")
        buyPrice = await page.get_by_role("heading", name="Buy price icon Buy price:").text_content()
        sellPrice = await page.get_by_role("heading", name="Sell price icon Sell price:").text_content()
        buyPrice = buyPrice.strip('?').strip(" Buy price: ").strip(" coins")
        sellPrice = sellPrice.strip('?').strip(" Sell price: ").strip(" coins")
        return (sellPrice, buyPrice)
