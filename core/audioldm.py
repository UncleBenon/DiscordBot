from playwright.async_api import async_playwright 
from asyncio import sleep, get_running_loop
from concurrent.futures import ThreadPoolExecutor
from core.sha import getSha256
from random import randrange
import requests
import os

STABLE_AUDIO_PATH = 'temp'
async def stableaudioLDM(prompt : str, neg : str = None, debug = False) -> str:
    async with async_playwright() as p:
        driver = await p.firefox.launch(headless=not debug)
        page = await driver.new_page()
        await page.goto("https://haoheliu-audioldm-48k-text-to-hifiaudio-generation.hf.space")
        while await page.get_by_text("Preparing Space").is_visible():
            await sleep(10)
            await page.goto("https://haoheliu-audioldm-48k-text-to-hifiaudio-generation.hf.space")
        if await page.get_by_text("Your space is in error").is_visible():
            raise Exception("Space is having errors, not the bot's fault")
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
            if _cc >= 600:
                raise Exception("timed out")
            if await page.get_by_text("Error").first.is_visible():
                raise Exception("Error!")

        link = await page.get_by_test_id("Output-player").get_attribute("src")

    with ThreadPoolExecutor(1) as exe:
        _loop = get_running_loop()
        content = await _loop.run_in_executor(exe, requests.get, link)

    filename = f"{getSha256(content)}.mp4"
    fullPath = os.path.join(STABLE_AUDIO_PATH, filename)
    if not os.path.exists(STABLE_AUDIO_PATH):
        os.mkdir(STABLE_AUDIO_PATH)
    with open(fullPath,"wb") as f:
        f.write(content.content)
    return fullPath
