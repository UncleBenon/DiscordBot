from concurrent.futures import ThreadPoolExecutor
from playwright.async_api import async_playwright
from requests import get
from hashlib import sha256
from asyncio import sleep, get_running_loop
import os

URL = "https://hidream-ai-hidream-o1-image-dev-2604.hf.space/"
DIR_PATH = "temp"


async def dreamSmallMasterFunc(prompt: str, DEBUG=False):
    _PROMPT_REFINE = "body > div:nth-child(1) > div.gradio-container.gradio-container-6-14-0.svelte-99kmwu > div > div.wrap.svelte-zxu34v > main > div > div.row.svelte-7xavid.unequal-height > div:nth-child(1) > div > div:nth-child(3) > label > span"
    _PROMPT = "body > div:nth-child(1) > div.gradio-container.gradio-container-6-14-0.svelte-99kmwu > div > div.wrap.svelte-zxu34v > main > div > div.row.svelte-7xavid.unequal-height > div:nth-child(1) > div > div:nth-child(1) > label > div > textarea"
    _GENERATE = "body > div:nth-child(1) > div.gradio-container.gradio-container-6-14-0.svelte-99kmwu > div > div.wrap.svelte-zxu34v > main > div > div.row.svelte-7xavid.unequal-height > div:nth-child(1) > button"
    _IMAGE = "body > div:nth-child(1) > div.gradio-container.gradio-container-6-14-0.svelte-99kmwu > div > div.wrap.svelte-zxu34v > main > div > div.row.svelte-7xavid.unequal-height > div:nth-child(2) > div > div.image-container.svelte-12vrxzd > button > div > img"

    async with async_playwright() as p:
        driver = await p.firefox.launch(headless=not DEBUG)
        page = await driver.new_page()
        await page.goto(URL)

        _timeout = 0
        while (
            await page.get_by_text("Preparing Space").is_visible()
            or await page.get_by_text("Internal Error").is_visible()
        ):
            if _timeout >= 6:
                raise Exception("timed out")
            await page.goto(URL)
            await sleep(10)
            _timeout += 1

        if await page.get_by_text("Your space is in error").is_visible():
            raise Exception("Space is having errors, not the bot's fault")

        await page.locator(_PROMPT_REFINE).click()
        await sleep(1)
        await page.locator(_PROMPT).fill(prompt)
        await sleep(1)
        await page.locator(_GENERATE).click()

        _cc = 0
        _error = 0
        while not await page.locator(_IMAGE).is_visible():
            await sleep(1)
            _cc += 1
            if _cc >= 600:
                raise Exception("timed out")
            if await page.get_by_text("Error").first.is_visible():
                if _error >= 30:
                    raise Exception("Error!")
                _cc = 0
                _error += 1
                await sleep(1)
                await page.locator(_GENERATE).click()

        link = await page.locator(_IMAGE).get_attribute("src")

    with ThreadPoolExecutor(1) as exe:
        _loop = get_running_loop()
        file = await _loop.run_in_executor(exe, get, link)

    if file.status_code != 200:
        raise Exception(
            f"Something went wrong, Download link returning {file.status_code}"
        )
    file = file.content
    filename = f"{sha256(file).hexdigest()}.webp"
    if not os.path.exists(DIR_PATH):
        os.mkdir(DIR_PATH)
    fullPath = os.path.join(DIR_PATH, filename)
    with open(fullPath, "wb") as f:
        f.write(file)

    return fullPath
