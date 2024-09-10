from playwright.async_api import async_playwright 
from asyncio import sleep, get_running_loop
from concurrent.futures import ThreadPoolExecutor
from random import randrange
import base64
import os
import requests
from core.sha import getSha256

PATH = "temp"
async def stableDiff(prompt : str, neg : str = None, debug : bool = False) -> list[str]:
    async with async_playwright() as p:
        driver = await p.firefox.launch(headless=not debug)
        page = await driver.new_page()
        await page.goto("https://stabilityai-stable-diffusion.hf.space/")
        await page.get_by_placeholder("Enter your prompt").fill(prompt)
        if neg:
            await page.get_by_placeholder("Enter a negative prompt").fill(neg)
        await page.get_by_role("button", name="Generate image").click()
        _cc = 0
        imgs = page.locator("#gallery").get_by_role("button")
        while not await imgs.first.is_visible():
            await sleep(1)
            _cc += 1
            if _cc >= 120:
                raise Exception("timed out")
            if await page.get_by_text("Error").first.is_visible():
                raise Exception("Error!")
        imgs = await page.query_selector_all('img')
        b64 = []
        for found in imgs:
            link = await found.get_attribute('src')
            if link.endswith(".svg"):
                continue
            b64.append(
                base64.b64decode(
                    link.split(',')[1]
                )
            )
        out = []
        for img in b64:
            filename = f"{getSha256(img)}.png"
            fullPath = os.path.join(PATH, filename)
            if not os.path.exists(PATH):
                os.mkdir(PATH)
            with open(fullPath,"wb") as f:
                f.write(img)
                out.append(fullPath)
        return out

async def stableAudio(prompt : str, neg : str = None, debug = False) -> str:
    async with async_playwright() as p:
        driver = await p.firefox.launch(headless=not debug)
        page = await driver.new_page()
        await page.goto("https://haoheliu-audioldm-text-to-audio-generation.hf.space/")
        if await page.get_by_text("Your space is in error").is_visible():
            raise Exception("Space is having errors, not the bot's fault")
        while await page.get_by_text("Preparing Space").is_visible():
            await sleep(10)
            await page.goto("https://haoheliu-audioldm-text-to-audio-generation.hf.space/")
        await page.get_by_role("button", name="Click to modify detailed").click()
        await page.get_by_label("number input for Duration (").fill("")
        await page.get_by_label("number input for Duration (").fill("10")
        await page.get_by_label("Seed").fill(f"{randrange(0,99999999)}")
        await page.get_by_label("Input text Your text is").fill(prompt)

        if neg:
            await page.get_by_label("Negative prompt Enter a").fill(neg)

        await page.get_by_role("button", name="Submit").click()

        found = page.get_by_test_id("Output-player")
        _cc = 0
        while not await found.is_visible():
            await sleep(1)
            _cc += 1
            if _cc >= 120:
                raise Exception("timed out")
            if await page.get_by_text("Error").first.is_visible():
                raise Exception("Error!")

        link = await page.get_by_test_id("Output-player").get_attribute("src")

    with ThreadPoolExecutor(1) as exe:
        _loop = get_running_loop()
        content = await _loop.run_in_executor(exe, requests.get, link)

    filename = f"{getSha256(content)}.mp4"
    fullPath = os.path.join(PATH, filename)
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    with open(fullPath,"wb") as f:
        f.write(content.content)
    return fullPath

async def stableMusic(prompt : str, neg : str = None, debug = False) -> str:
    async with async_playwright() as p:
        driver = await p.firefox.launch(headless=not debug)
        page = await driver.new_page()
        await page.goto("https://haoheliu-audioldm2-text2audio-text2music.hf.space")
        if await page.get_by_text("Your space is in error").is_visible():
            raise Exception("Space is having errors, not the bot's fault")
        while await page.get_by_text("Preparing Space").is_visible():
            await sleep(10)
            await page.goto("https://haoheliu-audioldm2-text2audio-text2music.hf.space")
        await page.get_by_label("Input text Your text is").fill(prompt)
        if neg:
            await page.get_by_label("Negative prompt Enter a").fill(neg)
        await page.get_by_text("Click to modify detailed configurations ▼").click()
        await page.get_by_label("Seed Change this value (any").fill(f"{randrange(0,99999999)}")
        await page.locator("#component-9").get_by_test_id("number-input").fill(str(15))
        await page.get_by_role("button", name="Submit").click()
        _cc = 0
        while not await page.get_by_test_id("Output-player").is_visible():
            await sleep(1)
            _cc +=1
            if _cc >= 120:
                raise Exception("timed out")
            if await page.get_by_text("Error").first.is_visible():
                raise Exception("Error!")
        link = await page.get_by_test_id("Output-player").get_attribute("src")

    with ThreadPoolExecutor(1) as exe:
        _loop = get_running_loop()
        content = await _loop.run_in_executor(exe, requests.get, link)

    filename = f"{getSha256(content)}.mp4"
    fullPath = os.path.join(PATH, filename)
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    with open(fullPath,"wb") as f:
        f.write(content.content)
    return fullPath
