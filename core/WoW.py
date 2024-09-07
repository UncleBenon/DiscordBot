from playwright.async_api import async_playwright 

async def getWoWTokenPrice(debug : bool = False) -> tuple[str, str, str, str]:
    # https://wowauction.us
    async with async_playwright() as p:
        driver = await p.firefox.launch(headless=not debug)
        page = await driver.new_page()
        await page.goto("https://wowauction.us/token")
        retailNA = await page.get_by_text("US WoW Token Price Current:").inner_text()
        retailEU = await page.get_by_text("EU WoW Token Price Current:").inner_text()

        retailNA = retailNA.splitlines()[2].strip()
        retailEU = retailEU.splitlines()[2].strip()

        await page.goto("https://wowauction.us/classic/token")
        classicNA = await page.get_by_text("US WoW Token Price Current:").inner_text()
        classicEU = await page.get_by_text("EU WoW Token Price Current:").inner_text()

        classicNA = classicNA.splitlines()[2].strip()
        classicEU = classicEU.splitlines()[2].strip()

        return (retailNA, retailEU, classicNA, classicEU)
