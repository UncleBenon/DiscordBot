from playwright.async_api import async_playwright 
from asyncio import sleep, get_running_loop
from core.misc import convertAsync
from concurrent.futures import ThreadPoolExecutor
from core.sha import getSha256
import requests
import os

PATH = 'temp'
VOICES = [
    "alba",
    "marius",
    "javert",
    "jean",
    "fantine",
    "cosette",
    "eponine",
    "azelma"
]

async def voiceSynth2Function(prompt: str, voice: int = 0, temp: float = 1.5, debug:bool = False) -> str:
    async with async_playwright() as p:
        driver = await p.firefox.launch(headless=not debug)
        page = await driver.new_page()
        await page.goto("https://xlnk-tts.hf.space/")

        if await page.get_by_text("Your space is in error").is_visible():
            raise Exception("Space is having errors, not the bot's fault")
        if await page.get_by_text("502 Bad Gateway").is_visible():
            raise Exception("Page is giving a 502, it's dead jim.")
        while await page.get_by_text("Preparing Space").is_visible():
            await page.goto("https://xlnk-tts.hf.space/")
            await sleep(10)

        await sleep(3)

        await page.locator("#text-input > label > div > textarea").fill(prompt)
        await sleep(1)
        await page.locator("body > div:nth-child(1) > div.gradio-container.gradio-container-6-3-0.svelte-99kmwu > main > div.wrap.svelte-zxu34v > div > div > div.row.svelte-7xavid.unequal-height > div:nth-child(1) > div.block.svelte-1plpy97.padded.auto-margin > button > span:nth-child(1)").click()
        await sleep(1)
        await page.locator("body > div:nth-child(1) > div.gradio-container.gradio-container-6-3-0.svelte-99kmwu > main > div.wrap.svelte-zxu34v > div > div > div.row.svelte-7xavid.unequal-height > div:nth-child(1) > div.block.svelte-1plpy97.padded.auto-margin > div:nth-child(3) > div > div:nth-child(1) > div > div:nth-child(1) > div.wrap.svelte-8epfm4 > div.head.svelte-8epfm4 > div > input").fill(str(temp))
        await sleep(1)

        if voice > 7: 
            voice = 0

        if voice > 0:
            await page.locator("#voice-select > div.svelte-1xfsv4t.container > div > div.wrap-inner.svelte-1xfsv4t > div > input").fill(VOICES[voice])
            await sleep(1)
            await page.locator("#voice-select > div.svelte-1xfsv4t.container > div > div.wrap-inner.svelte-1xfsv4t > div > input").press("Enter")
            await sleep(1)

        await sleep(1)
        await page.locator("body > div:nth-child(1) > div.gradio-container.gradio-container-6-3-0.svelte-99kmwu > main > div.wrap.svelte-zxu34v > div > div > div.row.svelte-7xavid.unequal-height > div:nth-child(1) > div.row.svelte-7xavid.unequal-height > button.lg.primary.svelte-xzq5jh").press("Enter")

        _cc = 0
        _errorforce = 0
        found = page.get_by_label("Download")
        while not await found.is_visible():
            await sleep(1)
            _cc += 1
            if _cc >= 900:
                raise Exception("timed out")
            if await page.get_by_text("Error").first.is_visible() and not await page.locator("body > div:nth-child(1) > div.gradio-container.gradio-container-6-3-0.svelte-99kmwu > main > div.wrap.svelte-zxu34v > div > div > div.row.svelte-7xavid.unequal-height > div:nth-child(1) > div.row.svelte-7xavid.unequal-height > button.lg.stop.svelte-xzq5jh").is_visible():
                if _errorforce >= 10:
                    raise Exception("Error!")
                await page.locator("body > div:nth-child(1) > div.gradio-container.gradio-container-6-3-0.svelte-99kmwu > main > div.wrap.svelte-zxu34v > div > div > div.row.svelte-7xavid.unequal-height > div:nth-child(1) > div.row.svelte-7xavid.unequal-height > button.lg.primary.svelte-xzq5jh").press("Enter")
                _errorforce += 1
                _cc = 0
            if await page.get_by_text("no audio").is_visible():
                raise Exception("no audio generated")
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
