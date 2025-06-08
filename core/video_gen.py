from concurrent.futures import ThreadPoolExecutor
from playwright.async_api import async_playwright
from requests import get
from hashlib import sha256
from asyncio import sleep, get_running_loop
import os

URL = "https://vchitect-lavie.hf.space/"
DIR_PATH = "temp"

async def vgMasterFunction(prompt : str, DEBUG = False):
    _input = "#prompt-in > label > textarea"
    _generateButton = "#component-13"
    _output = "#video-output > div.wrap.svelte-euo1cw > div.mirror-wrap.svelte-euo1cw > video"

    async with async_playwright() as p:
        driver = await p.firefox.launch(headless = not DEBUG)
        page = await driver.new_page()
        await page.goto(URL)

        if await page.get_by_text("Your space is in error").is_visible():
            raise Exception("Space is having errors, not the bot's fault")

        while await page.get_by_text("Preparing Space").is_visible() or await page.get_by_text("Internal Error").is_visible():
            await sleep(10)
            await page.goto(URL)

        await sleep(1)
        await page.locator(_input).fill(prompt)
        await page.locator(_generateButton).click()

        _cc = 0
        _error = 0
        while not await page.locator(_output).is_visible():
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
                await page.locator(_generateButton).click()

        link = await page.locator(_output).get_attribute("src")


    with ThreadPoolExecutor(1) as exe:
        _loop = get_running_loop()
        file = await _loop.run_in_executor(exe, get, link)


    if file.status_code != 200:
        raise Exception(f"Something went wrong, Download link returning {file.status_code}")

    file = file.content
    filename = f"{sha256(file).hexdigest()}.mp4"
    if not os.path.exists(DIR_PATH):
        os.mkdir(DIR_PATH)
    fullPath = os.path.join(DIR_PATH, filename)
    with open(fullPath, 'wb') as f:
        f.write(file)

    return fullPath
