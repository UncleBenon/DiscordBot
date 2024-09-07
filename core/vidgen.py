from playwright.async_api import async_playwright
from hashlib import sha256
from requests import get
from asyncio import (run, sleep)
import os

RMBG_PATH = "temp"
async def sdVidGenFunction(prompt : str, DEBUG = False):
    # Makes the folder if it doesn't exist.
    if not os.path.exists(RMBG_PATH):
        os.mkdir(RMBG_PATH)

    async with async_playwright() as p:
        driver = await p.firefox.launch(headless = not DEBUG)
        page = await driver.new_page()
        await page.goto("https://ali-vilab-modelscope-text-to-video-synthesis.hf.space")

        # if the page is having errors raise this:
        if await page.get_by_text("Your space is in error").is_visible():
            raise Exception("Space is having errors, not the bot's fault")
            
        await page.get_by_test_id("textbox").fill(prompt)
        await page.get_by_role("button", name="Generate video").click()

        found = page.locator("video")
        _cc = 0
        while not await found.is_visible():
            await sleep(1)
            _cc += 1
            if _cc >= 120:
                raise Exception("Timed Out")
            if await page.get_by_text("Error").first.is_visible():
                raise Exception("Error!")

        link = await found.get_attribute("src")

    # Download and Save the image.
    file = get(link)
    if file.status_code != 200:
        raise Exception(f"Something went wrong, Download link returning {file.status_code}")
    file = file.content
    filename = f"{sha256(file).hexdigest()}.mp4"
    fullPath = os.path.join(RMBG_PATH, filename)
    with open(fullPath, 'wb') as f:
        f.write(file)

    return fullPath

if __name__ == "__main__":
    test = run(
        sdVidGenFunction("Boris Johnson running", True)
    )

    print(test)
