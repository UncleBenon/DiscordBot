from playwright.async_api import async_playwright 
from asyncio import sleep, get_running_loop
from concurrent.futures import ThreadPoolExecutor
from core.sha import getSha256
from core.misc import convertAsync
import requests
import os

PATH = 'temp'
async def voiceSynthFunction(prompt : str, debug = False) -> str:
    async with async_playwright() as p:
        driver = await p.firefox.launch(headless=not debug)
        page = await driver.new_page()
        await page.goto("https://fishaudio-fish-speech-1.hf.space")

        if await page.get_by_text("Your space is in error").is_visible():
            raise Exception("Space is having errors, not the bot's fault")

        if await page.get_by_text("502 Bad Gateway").is_visible():
            raise Exception("Page is giving a 502, it's dead jim.")

        while await page.get_by_text("Preparing Space").is_visible():
            await sleep(10)
            await page.goto("https://fishaudio-fish-speech-1.hf.space")

        #await page.goto("https://fishaudio-fish-speech-1.hf.space/?__theme=light")
        await page.goto("https://fishaudio-openaudio-s1-mini.hf.space/?__theme=dark")

        await sleep(3)

        await page.locator("#component-9 > div.wrap.svelte-1kajgn1 > div.head.svelte-1kajgn1 > div > input").fill("500")

        await page.get_by_placeholder("Put your text here.").fill(prompt)

        await sleep(1)

        await page.get_by_role("button", name="🎧 Generate").click()

        found = page.get_by_label("Download")
        _cc = 0
        _errorforce = 0
        while not await found.is_visible():
            await sleep(1)
            _cc += 1
            if _cc >= 600:
                raise Exception("timed out")
            if await page.get_by_text("Error").first.is_visible():
                if _errorforce >= 10:
                    raise Exception("Error!")
                await page.get_by_role("button", name="🎧 Generate").click()
                _errorforce += 1
                _cc = 0
            if await page.get_by_text("no audio").is_visible():
                raise Exception("no audio generated, dunno why lmao")
            if await page.get_by_text("CUDA error: device-side assert triggered CUDA kernel errors").is_visible():
                raise Exception("CUDA kernel errors")
            if await page.get_by_text("CUDA out of memory.").is_visible():
                raise Exception("CUDA out of memory")

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

    fullPath = await convertAsync(fullPath)

    return fullPath
