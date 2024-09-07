from playwright.async_api import async_playwright 
from asyncio import sleep, run
from datetime import datetime
from random import randrange
import requests
import os

def curTime() -> str:
        now = datetime.now()
        return str(now.strftime("%d-%m-%y %I-%M-%S %p"))

STABLE_AUDIO_PATH = 'STABLE_AUDIO_LDM'
async def stableaudioLDM(prompt : str, neg : str = None, debug = False) -> list[str]:
    async with async_playwright() as p:
        driver = await p.firefox.launch(headless=not debug)
        page = await driver.new_page()
        await page.goto("https://haoheliu-audioldm-48k-text-to-hifiaudio-generation.hf.space")
        await page.get_by_text("Click to modify detailed").click()
        await page.get_by_label("Duration (seconds)").fill("15")
        await page.get_by_label("Change this value (").fill(f"{randrange(0,99999999)}")
        await page.get_by_test_id("textbox").fill(prompt)

        if neg:
            await page.get_by_label("Negative prompt Enter a").fill(neg)

        await page.get_by_role("button", name="Submit").click()

        found = page.get_by_test_id("Output-player")
        _cc = 0
        while not await found.is_visible():
            await sleep(1)
            _cc += 1
            if _cc >= 90:
                raise Exception("timed out")

        link = await page.get_by_test_id("Output-player").get_attribute("src")

    content = requests.get(link)
    filename = f"{curTime()}.mp4"
    fullPath = os.path.join(STABLE_AUDIO_PATH, filename)
    if not os.path.exists(STABLE_AUDIO_PATH):
        os.mkdir(STABLE_AUDIO_PATH)
    with open(fullPath,"wb") as f:
        f.write(content.content)
    return fullPath

if __name__ == '__main__':
    test = run(stableaudioLDM("Racism+500"))
    print(test)
