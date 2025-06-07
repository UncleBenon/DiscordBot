from playwright.async_api import async_playwright
from requests import get
from hashlib import sha256
from asyncio import sleep
import os

url = "https://nihalgazi-flux-pro-unlimited.hf.space/"

DIR_PATH = "temp"
async def fluxMasterFunction(prompt : str, DEBUG = False):
    async with async_playwright() as p:
        driver = await p.firefox.launch(headless = not DEBUG)
        page = await driver.new_page()
        await page.goto(url)

        while await page.get_by_text("Preparing Space").is_visible():
            await sleep(10)
            await page.goto(url)

        if await page.get_by_text("Your space is in error").is_visible():
            raise Exception("Space is having errors, not the bot's fault")


        await sleep(1)

        await page.get_by_placeholder("Enter a your image prompt").fill(prompt)
        await page.get_by_role("button", name="Generate").click()

        _cc = 0
        _error = 0
        _img = "#component-9 > div.image-container.svelte-dpdy90 > button > div > img"
        while not await page.locator(_img).is_visible():
            await sleep(1)
            _cc += 1
            if _cc >= 600:
                raise Exception("timed out")
            if await page.get_by_text("Error").first.is_visible():
                if _error >= 10:
                    raise Exception("Error!")
                _cc = 0
                _error += 1
                await page.get_by_role("button", name="Generate").click()

        found = await page.query_selector_all('img')

        for img in found:
            atr = await img.get_attribute('src')
            if atr.startswith(url):
                out = atr
                break

    file = get(out)
    if file.status_code != 200:
        raise Exception(f"Something went wrong, Download link returning {file.status_code}")
    file = file.content
    filename = f"{sha256(file).hexdigest()}.webp"
    fullPath = os.path.join(DIR_PATH, filename)
    with open(fullPath, 'wb') as f:
        f.write(file)

    return fullPath

