from playwright.async_api import async_playwright
from hashlib import sha256
from requests import get
from asyncio import sleep, get_running_loop
from concurrent.futures import ThreadPoolExecutor
import os
import re

RMBG_PATH = "temp"
async def RemoveBackGroundFunction(inp : str, DEBUG = False) -> str:
    # Makes the folder if it doesn't exist.
    if not os.path.exists(RMBG_PATH):
        os.mkdir(RMBG_PATH)

    _, inp = await downloadImage(inp)

    async with async_playwright() as p:
        driver = await p.firefox.launch(headless = not DEBUG)
        page = await driver.new_page()
        await page.goto("https://not-lain-locally-compatible-bg-removal.hf.space")

        if await page.get_by_text("Your space is in error").is_visible():
            raise Exception("Space is having errors, not the bot's fault")

        _inp = page.get_by_role("button", name="Drop Image Here - or - Click")
        async with page.expect_file_chooser() as f:
            await _inp.click()
            _upload = await f.value
            await _upload.set_files(inp)

        _cc = 0
        while await page.locator("div").filter(has_text=re.compile(r"^0$")).is_visible():
            await sleep(1)
            _cc += 1
            if _cc >= 120:
                raise Exception("Timed Out")
            if await page.get_by_text("Error").first.is_visible():
                raise Exception("Error!")

        await page.get_by_role("button", name="Submit").click()
        
        if await page.get_by_text("Error").is_visible():
            raise Exception("Error")

        link = page.get_by_role("link", name="⇣")
        _cc = 0
        while not await link.is_visible():
            await sleep(1)
            _cc += 1
            if _cc >= 120:
                raise Exception("Timed Out")
            if await page.get_by_text("Error").first.is_visible():
                breakpoint()
                raise Exception("Error!")

        img = await link.get_attribute("href")

    file, fullPath = await downloadImage(img)
    os.remove(inp)
    return fullPath

async def downloadImage(url) -> str:
    with ThreadPoolExecutor(1) as exe:
        _loop = get_running_loop()
        inpt = await _loop.run_in_executor(exe, get, url)
    if inpt.status_code != 200:
        raise Exception(f"Dead link {url}")
    file = inpt.content
    filename = f"{sha256(file).hexdigest()}.png"
    fullPath = os.path.join(RMBG_PATH, filename)
    with open(fullPath, 'wb') as f:
        f.write(file)
    return file, fullPath

if __name__ == "__main__":
    from asyncio import run
    test = run(RemoveBackGroundFunction("https://cdn.discordapp.com/attachments/1048600881593061416/1283688331435053066/image.png?ex=66e3e76b&is=66e295eb&hm=423002909247e1f0383de4cc7a144395715a04077e939e236d68df617dd79d2b&", True))
    print(test)
