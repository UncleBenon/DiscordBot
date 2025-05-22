from playwright.async_api import async_playwright 
from asyncio import sleep, get_running_loop
from concurrent.futures import ThreadPoolExecutor
from core.sha import getSha256
from random import choice
from core.misc import convertAsync
import requests
import os

PATH = 'temp'

voices = [
    "Unconditional",
    "Announcer",
    "Speaker 0 (en)",
    "Speaker 1 (en)",
    "Speaker 2 (en)",
    "Speaker 3 (en)",
    "Speaker 4 (en)",
    "Speaker 5 (en)",
    "Speaker 6 (en)",
    "Speaker 7 (en)",
    "Speaker 8 (en)",
    "Speaker 9 (en)",
    "Speaker 0 (de)",
    "Speaker 1 (de)",
    "Speaker 2 (de)",
    "Speaker 3 (de)",
    "Speaker 4 (de)",
    "Speaker 5 (de)",
    "Speaker 6 (de)",
    "Speaker 7 (de)",
    "Speaker 8 (de)",
    "Speaker 9 (de)",
    "Speaker 0 (es)",
    "Speaker 1 (es)",
    "Speaker 2 (es)",
    "Speaker 3 (es)",
    "Speaker 4 (es)",
    "Speaker 5 (es)",
    "Speaker 6 (es)",
    "Speaker 7 (es)",
    "Speaker 8 (es)",
    "Speaker 9 (es)",
    "Speaker 0 (fr)",
    "Speaker 1 (fr)",
    "Speaker 2 (fr)",
    "Speaker 3 (fr)",
    "Speaker 4 (fr)",
    "Speaker 5 (fr)",
    "Speaker 6 (fr)",
    "Speaker 7 (fr)",
    "Speaker 8 (fr)",
    "Speaker 9 (fr)",
    "Speaker 0 (hi)",
    "Speaker 1 (hi)",
    "Speaker 2 (hi)",
    "Speaker 3 (hi)",
    "Speaker 4 (hi)",
    "Speaker 5 (hi)",
    "Speaker 6 (hi)",
    "Speaker 7 (hi)",
    "Speaker 8 (hi)",
    "Speaker 9 (hi)",
    "Speaker 0 (it)",
    "Speaker 1 (it)",
    "Speaker 2 (it)",
    "Speaker 3 (it)",
    "Speaker 4 (it)",
    "Speaker 5 (it)",
    "Speaker 6 (it)",
    "Speaker 7 (it)",
    "Speaker 8 (it)",
    "Speaker 9 (it)",
    "Speaker 0 (ja)",
    "Speaker 1 (ja)",
    "Speaker 2 (ja)",
    "Speaker 3 (ja)",
    "Speaker 4 (ja)",
    "Speaker 5 (ja)",
    "Speaker 6 (ja)",
    "Speaker 7 (ja)",
    "Speaker 8 (ja)",
    "Speaker 9 (ja)",
    "Speaker 0 (ja)",
    "Speaker 1 (ko)",
    "Speaker 2 (ko)",
    "Speaker 3 (ko)",
    "Speaker 4 (ko)",
    "Speaker 5 (ko)",
    "Speaker 6 (ko)",
    "Speaker 7 (ko)",
    "Speaker 8 (ko)",
    "Speaker 9 (ko)",
    "Speaker 0 (pl)",
    "Speaker 1 (pl)",
    "Speaker 2 (pl)",
    "Speaker 3 (pl)",
    "Speaker 4 (pl)",
    "Speaker 5 (pl)",
    "Speaker 6 (pl)",
    "Speaker 7 (pl)",
    "Speaker 8 (pl)",
    "Speaker 9 (pl)",
    "Speaker 0 (pt)",
    "Speaker 1 (pt)",
    "Speaker 2 (pt)",
    "Speaker 3 (pt)",
    "Speaker 4 (pt)",
    "Speaker 5 (pt)",
    "Speaker 6 (pt)",
    "Speaker 7 (pt)",
    "Speaker 8 (pt)",
    "Speaker 9 (pt)",
    "Speaker 0 (ru)",
    "Speaker 1 (ru)",
    "Speaker 2 (ru)",
    "Speaker 3 (ru)",
    "Speaker 4 (ru)",
    "Speaker 5 (ru)",
    "Speaker 6 (ru)",
    "Speaker 7 (ru)",
    "Speaker 8 (ru)",
    "Speaker 9 (ru)",
    "Speaker 0 (tr)",
    "Speaker 1 (tr)",
    "Speaker 2 (tr)",
    "Speaker 3 (tr)",
    "Speaker 4 (tr)",
    "Speaker 5 (tr)",
    "Speaker 6 (tr)",
    "Speaker 7 (tr)",
    "Speaker 8 (tr)",
    "Speaker 9 (tr)",
    "Speaker 0 (zh)",
    "Speaker 1 (zh)",
    "Speaker 2 (zh)",
    "Speaker 3 (zh)",
    "Speaker 4 (zh)",
    "Speaker 5 (zh)",
    "Speaker 6 (zh)",
    "Speaker 7 (zh)",
    "Speaker 8 (zh)",
    "Speaker 9 (zh)",
]

async def barkVoiceSynthFunc(prompt : str, debug = False) -> str:
    async with async_playwright() as p:
        driver = await p.firefox.launch(headless=not debug)
        page = await driver.new_page()
        await page.goto("https://suno-bark.hf.space/")

        await sleep(1)
        voice = choice(voices)

        inputPrompt = page.locator("#input_text > label > textarea")
        await inputPrompt.fill(prompt)

        speaker = page.locator("#speaker_option > label > div > div.wrap-inner.svelte-1ythexu")
        await speaker.click()
        await page.get_by_text(voice).first.click()

        await page.locator("#component-7").click()

        _cc = 0
        while not await page.locator("audio").is_visible():
            if await page.get_by_text("Error").first.is_visible():
                raise Exception("Error")
            if _cc >= 600:
                raise Exception("Timed Out")
            await sleep(1)
            _cc += 1

        link = await page.locator("audio").get_attribute("src")

    with ThreadPoolExecutor(1) as exe:
        _loop = get_running_loop()
        content = await _loop.run_in_executor(exe, requests.get, link)

    filename = f"{getSha256(content)}.wav"
    fullPath = os.path.join(PATH, filename)
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    with open(fullPath,"wb") as f:
        f.write(content.content)

    fullPath = await convertAsync(fullPath)

    return (fullPath, voice)
