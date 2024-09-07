from playwright.async_api import async_playwright
from asyncio import sleep, run
from datetime import datetime
import requests
import os

FB_AUDIO_PATH = "FB_AUDIO"
async def FBAudio(prompt: str, debug=False) -> list[str]:
    def curTime() -> str:
        now = datetime.now()
        return str(now.strftime("%d-%m-%y %I-%M-%S %p"))

    async with async_playwright() as p:
        driver = await p.firefox.launch(headless=not debug)
        page = await driver.new_page()
        await page.goto("https://facebook-musicgen.hf.space")

        if await page.get_by_text("Your space is in error").is_visible():
            raise Exception("Space is having errors, not the bot's fault")
        while await page.get_by_text("Preparing Space").is_visible():
            await sleep(10)
            await page.goto("https://facebook-musicgen.hf.space")

        await page.get_by_test_id("textbox").fill(prompt)
        await page.get_by_role("button", name="Generate").click()

        found = page.locator("video")
        _cc = 0
        while not await found.is_visible():
            await sleep(1)
            _cc += 1
            if _cc >= 120:
                raise Exception("timed out")

        link = await found.get_attribute("src")

    content = requests.get(link)
    filename = f"{curTime()}.mp4"
    fullPath = os.path.join(FB_AUDIO_PATH, filename)
    if not os.path.exists(FB_AUDIO_PATH):
        os.mkdir(FB_AUDIO_PATH)
    with open(fullPath,"wb") as f:
        f.write(content.content)
    return fullPath

if __name__ == '__main__':
    test = run(FBAudio("Epic synth music with farts", debug=True))
    print(test)
    os.remove(test)
