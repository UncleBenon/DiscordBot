from playwright.async_api import async_playwright 
from asyncio import sleep, get_running_loop
from concurrent.futures import ThreadPoolExecutor
from core.sha import getSha256
import requests
import os

PATH = 'temp'
async def voiceSynthFunction(prompt : str, debug = False) -> str:
    async with async_playwright() as p:
        driver = await p.firefox.launch(headless=not debug)
        page = await driver.new_page()
        await page.goto("https://fishaudio-fish-speech-1.hf.space/?__theme=light")

        if await page.get_by_text("Your space is in error").is_visible():
            raise Exception("Space is having errors, not the bot's fault")

        await page.get_by_placeholder("Put your text here.").fill(prompt)

        await page.get_by_text("Text Normalization (ZH)").click()
        await page.get_by_text("Load / Unload ASR model for").click()

        await page.get_by_role("button", name="🎧 Generate").click()

        found = page.get_by_label("Download")
        _cc = 0
        _errorforce = 0
        while not await found.is_visible():
            await sleep(1)
            _cc += 1
            if _cc >= 120:
                raise Exception("timed out")
            if await page.get_by_text("Error").first.is_visible():
                if _errorforce > 4:
                    raise Exception("Error!")
                await page.get_by_role("button", name="🎧 Generate").click()
                _errorforce += 1
                _cc = 0

        links = await page.locator('a').all()
        for out in links[::-1]:
            _out = await out.get_attribute("href")
            if _out.lower().endswith(".wav"):
                link = _out
                break

    with ThreadPoolExecutor(1) as exe:
        _loop = get_running_loop()
        content = await _loop.run_in_executor(exe, requests.get, link)

    filename = f"{getSha256(content)}.wav"
    fullPath = os.path.join(PATH, filename)
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    with open(fullPath,"wb") as f:
        f.write(content.content)
    return fullPath