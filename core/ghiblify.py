from playwright.async_api import async_playwright
from hashlib import sha256
from requests import get
from asyncio import sleep
from core.removebg import downloadImage
import os

PATH = "temp"
URL = "https://abidlabs-easyghibli.hf.space/"

async def ghiblifyFunction(inp: str, DEBUG=False):
    _uploadButton = "#component-4 > div.image-container.svelte-1hdlew6 > div.upload-container.svelte-1hdlew6.reduced-height > button"
    _generateButton = "#component-5"
    _img = "#component-7 > div.image-container.svelte-zxsjoa > button > div > img"

    _, inp = await downloadImage(inp)

    async with async_playwright() as p:
        driver = await p.firefox.launch(headless=not DEBUG)
        page = await driver.new_page()
        await page.goto(URL)

        if await page.get_by_text("Your space is in error").is_visible():
            raise Exception("Space is having errors, not the bot's fault")

        await sleep(1)

        async with page.expect_file_chooser() as f:
            await page.locator(_uploadButton).click()
            _upload = await f.value
            await _upload.set_files(inp)

        await sleep(3)
        await page.locator(_generateButton).click()

        _cc = 0
        _errorforce = 0
        while not await page.locator(_img).is_visible():
            await sleep(1)
            _cc += 1
            if _cc >= 600:
                raise Exception("timed out")
            if await page.get_by_text("Error").first.is_visible():
                if _errorforce >= 10:
                    raise Exception("Error!")
                await page.locator(_generateButton).click()
                _errorforce += 1
                _cc = 0

        atr = await page.locator(_img).get_attribute('src')
        if atr.startswith(URL):
            out = atr

    file = get(out)
    if file.status_code != 200:
        raise Exception(f"Something went wrong, Download link returning {file.status_code}")
    file = file.content
    filename = f"{sha256(file).hexdigest()}.webp"
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    fullPath = os.path.join(PATH, filename)
    with open(fullPath, 'wb') as f:
        f.write(file)

    return fullPath
