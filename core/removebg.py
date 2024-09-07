from playwright.async_api import async_playwright
from hashlib import sha256
from requests import get
from asyncio import (run, sleep)
import os

RMBG_PATH = "RMBG"
async def RemoveBackGroundFunction(inp : str, DEBUG = False) -> str:
    # Makes the folder if it doesn't exist.
    if not os.path.exists(RMBG_PATH):
        os.mkdir(RMBG_PATH)

    _, inp = await downloadImage(inp)

    async with async_playwright() as p:
        driver = await p.firefox.launch(headless = not DEBUG)
        page = await driver.new_page()
        await page.goto("https://not-lain-locally-compatible-bg-removal.hf.space")

        # if the page is having errors raise this:
        if await page.get_by_text("Your space is in error").is_visible():
            raise Exception("Space is having errors, not the bot's fault")

        # Uploads the image to Gradio
        _inp = page.get_by_role("button", name="Drop Image Here - or - Click")
        async with page.expect_file_chooser() as f:
            await _inp.click()
            _upload = await f.value
            await _upload.set_files(inp)
        await sleep(5)
        await page.get_by_role("button", name="Submit").click()
        
        # General error check
        if await page.get_by_text("Error").is_visible():
            raise Exception("Error")

        # Wait till the link is either visible or when it times out (300 sec)
        link = page.get_by_role("link", name="⇣")
        _cc = 0
        while not await link.is_visible():
            await sleep(1)
            _cc += 1
            if _cc >= 300:
                raise Exception("Timed Out")

        img = await link.get_attribute("href")

    # Download and Save the image.
    file, fullPath = await downloadImage(img)
    os.remove(inp)
    return fullPath

async def downloadImage(url) -> str:
    inpt = get(url)
    if inpt.status_code != 200:
        raise Exception(f"Dead link {url}")
    file = inpt.content
    filename = f"{sha256(file).hexdigest()}.png"
    fullPath = os.path.join(RMBG_PATH, filename)
    with open(fullPath, 'wb') as f:
        f.write(file)
    return file, fullPath

if __name__ == "__main__":
    test = run(RemoveBackGroundFunction("https://media.discordapp.net/attachments/1048600881593061416/1275503857908187156/image.png?ex=66d3f8c9&is=66d2a749&hm=dee4b854ae730254bf074c708e999ee07d938cbb2b5b99db565f5754852e2644", False))
    print(test)
