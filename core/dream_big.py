from concurrent.futures import ThreadPoolExecutor
from playwright.async_api import async_playwright
from requests import get
from hashlib import sha256
from asyncio import sleep, get_running_loop
import os

URL = "https://hidream-ai-hidream-o1-image.hf.space/"
DIR_PATH = "temp"

RES = ["1:1", "4:3", "3:4", "16:9", "9:16", "3:2", "2:3", "21:9", "9:21", "9:7", "7:9"]


async def dreamBigMasterFunc(
    prompt: str, negPrompt: str = None, res: int = 0, DEBUG=False
):
    _PROMPT_REFINE = "#component-10 > label > input"
    _RATIO = "#component-7 > div.svelte-1hfxrpf.container > div.wrap.svelte-1hfxrpf > div.wrap-inner.svelte-1hfxrpf > div > input"
    _PROMPT = "#component-5 > label > div > textarea"
    _NEG_PROMPT = "#component-6 > label > div > textarea"
    _GENERATE = "#component-15"
    _IMAGE = "#component-19 > div.image-container.svelte-w225pd > button > div > img"

    if res < 0 or res > 10:
        res = 0

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
        if res > 0:
            await page.locator(_RATIO).click()
            await sleep(0.5)
            await page.locator(_RATIO).press("Control+A")
            await sleep(0.5)
            await page.locator(_RATIO).press("Backspace")
            await sleep(0.5)
            await page.locator(_RATIO).press_sequentially(RES[res])
            await sleep(0.5)
            await page.locator(_RATIO).press("Enter")
            await sleep(0.5)
        if negPrompt:
            await page.locator(_NEG_PROMPT).fill(negPrompt)
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
