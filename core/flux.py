from concurrent.futures import ThreadPoolExecutor
from playwright.async_api import async_playwright
from requests import get
from hashlib import sha256
from asyncio import sleep, get_running_loop
import os

URL = "https://agents-mcp-hackathon-ai-marketing-content-creator.hf.space/"
DIR_PATH = "temp"

async def fluxMasterFunction(prompt : str, DEBUG = False):
    _promptInput = "#component-27 > label > div > textarea"
    _genButton = "#component-49"
    _image = "#component-37 > div.image-container.svelte-zxsjoa > button > div > img"
    async with async_playwright() as p:
        driver = await p.firefox.launch(headless = not DEBUG)
        page = await driver.new_page()
        await page.goto(URL)

        while await page.get_by_text("Preparing Space").is_visible() or await page.get_by_text("Internal Error").is_visible():
            await sleep(10)
            await page.goto(URL)

        if await page.get_by_text("Your space is in error").is_visible():
            raise Exception("Space is having errors, not the bot's fault")

        await page.locator("#component-24-button").click()
        await sleep(1)
        await page.locator(_promptInput).fill(prompt)
        await page.locator(_genButton).click()

        _cc = 0
        _error = 0
        while not await page.locator(_image).is_visible():
            await sleep(1)
            _cc += 1
            if _cc >= 600:
                raise Exception("timed out")
            if await page.get_by_text("Error").first.is_visible():
                if _error >= 10:
                    raise Exception("Error!")
                _cc = 0
                _error += 1
                await sleep(1)
                await page.locator(_genButton).click()

        link = await page.locator(_image).get_attribute("src")

    with ThreadPoolExecutor(1) as exe:
        _loop = get_running_loop()
        file = await _loop.run_in_executor(exe, get, link)

    if file.status_code != 200:
        raise Exception(f"Something went wrong, Download link returning {file.status_code}")
    file = file.content
    filename = f"{sha256(file).hexdigest()}.webp"
    if not os.path.exists(DIR_PATH):
        os.mkdir(DIR_PATH)
    fullPath = os.path.join(DIR_PATH, filename)
    with open(fullPath, 'wb') as f:
        f.write(file)

    return fullPath
