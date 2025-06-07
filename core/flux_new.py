from playwright.async_api import async_playwright
from requests import get
from hashlib import sha256
from asyncio import sleep
from random import choice
import os

url = "https://nihalgazi-flux-pro-unlimited.hf.space/"
servers = [
    "Azure Lite Supercomputer Server",
    "Artemis GPU Super cluster",
    "NebulaDrive Tensor Server",
    "PixelNet NPU Server",
    "Google US Server",
]

DIR_PATH = "temp"
async def fluxMasterFunction(prompt : str, DEBUG = False):
    async with async_playwright() as p:
        _textArea = "#component-2 > label > div > textarea"
        _button = "#component-8"
        _img = "#component-9 > div.image-container.svelte-dpdy90 > button > div > img"
        _servers = "#component-7 > div.svelte-1hfxrpf.container > div > div.wrap-inner.svelte-1hfxrpf > div > input"

        driver = await p.firefox.launch(headless = not DEBUG)
        page = await driver.new_page()
        await page.goto(url)

        while await page.get_by_text("Preparing Space").is_visible() or await page.get_by_text("Internal Error").is_visible():
            await sleep(10)
            await page.goto(url)

        if await page.get_by_text("Your space is in error").is_visible():
            raise Exception("Space is having errors, not the bot's fault")

        await sleep(1)
        await page.locator(_textArea).fill(prompt)
        await page.locator(_servers).click()
        await page.get_by_label(choice(servers[:-1])).click()
        await sleep(1)
        await page.locator(_button).click()

        _cc = 0
        _error = 0
        _serverCount = 0
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
                await page.locator(_servers).click()
                await page.get_by_label(servers[_serverCount]).click()
                await sleep(1)
                await page.locator(_button).click()
                _serverCount += 1
                if _serverCount > 4:
                    _serverCount = 0

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
