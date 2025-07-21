from concurrent.futures import ThreadPoolExecutor
from playwright.async_api import async_playwright
from requests import get
from hashlib import sha256
from asyncio import sleep, get_running_loop
import os

URL = "https://hidream-ai-hidream-i1-dev.hf.space/"
DIR_PATH = "temp"

async def dreamMasterFunc(prompt : str, res : int, DEBUG = False):
    _seed = "#component-9 > label > input"
    _promptInput = "#component-6 > label > div > textarea"
    _genButton = "#component-12"
    _image = "#component-19 > div.image-container.svelte-w225pd > button > div > img"

    async with async_playwright() as p:
        driver = await p.firefox.launch(headless = not DEBUG)
        page = await driver.new_page()
        await page.goto(URL)

        while await page.get_by_text("Preparing Space").is_visible() or await page.get_by_text("Internal Error").is_visible():
            await sleep(10)
            await page.goto(URL)

        if await page.get_by_text("Your space is in error").is_visible():
            raise Exception("Space is having errors, not the bot's fault")

        await page.locator(_seed).fill("-1")

        match res:
            case 0: # 1:1
                await page.locator("#component-8 > div.wrap.svelte-1kzox3m > label:nth-child(1)").click()
            case 1: # 3:4
                await page.locator("#component-8 > div.wrap.svelte-1kzox3m > label:nth-child(2)").click()
            case 3: # 9:16
                await page.locator("#component-8 > div.wrap.svelte-1kzox3m > label:nth-child(4)").click()
            case 4: # 16:9
                await page.locator("#component-8 > div.wrap.svelte-1kzox3m > label:nth-child(5)").click()
            case _:
                pass

        await sleep(1)
        await page.locator(_promptInput).fill(prompt)
        await sleep(1)
        await page.locator(_genButton).click()

        _cc = 0
        _error = 0
        while not await page.locator(_image).is_visible():
            await sleep(1)
            _cc += 1
            if _cc >= 300:
                raise Exception("timed out")
            if await page.get_by_text("Error").first.is_visible():
                if _error >= 30:
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
