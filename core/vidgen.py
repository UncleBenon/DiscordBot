from concurrent.futures import ThreadPoolExecutor
from playwright.async_api import async_playwright
from requests import get
from hashlib import sha256
from asyncio import sleep, get_running_loop
import os

URL = "https://bestwishysh-magictime.hf.space/"
DIR_PATH = "temp"


async def vidGenMasterFunc(prompt: str, neg: str = None, gen: int = 0, DEBUG=False):
    _prompt = "#component-10 > label > textarea"
    _neg = "#component-11 > label > textarea"
    _output = "#component-24 > div.wrap.svelte-lcpz3o > div:nth-child(1) > video"
    _gen = "#component-21"

    async with async_playwright() as p:
        driver = await p.firefox.launch(headless=not DEBUG)
        page = await driver.new_page()
        await page.goto(URL)

        if await page.get_by_text("Your space is in error").is_visible():
            raise Exception("Space is having errors, not the bot's fault")

        await sleep(1)

        await page.locator(_prompt).press_sequentially(prompt)
        if neg:
            await page.locator(_neg).press_sequentially(", " + neg)

        if int(gen) > 0:
            _loc = "#component-8 > label > div > div.wrap-inner.svelte-tq78c3 > div > input"
            await page.locator(_loc).click()
            await sleep(1)
            for _ in range(int(gen) + 1):
                await page.locator(_loc).press("ArrowDown")
                await sleep(1)
            await page.locator(_loc).press("Enter")

        await page.locator(_gen).click()

        _cc = 0
        _error = 0
        while not await page.locator(_output).is_visible():
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
                await page.locator(_gen).click()

        link = await page.locator(_output).get_attribute("src")

    with ThreadPoolExecutor(1) as exe:
        _loop = get_running_loop()
        file = await _loop.run_in_executor(exe, get, link)

    if file.status_code != 200:
        raise Exception(
            f"Something went wrong, Download link returning {file.status_code}"
        )

    file = file.content
    filename = f"{sha256(file).hexdigest()}.mp4"
    if not os.path.exists(DIR_PATH):
        os.mkdir(DIR_PATH)
    fullPath = os.path.join(DIR_PATH, filename)
    with open(fullPath, "wb") as f:
        f.write(file)

    return fullPath
