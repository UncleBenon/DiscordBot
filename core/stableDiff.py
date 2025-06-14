from playwright.async_api import async_playwright 
from asyncio import sleep, get_running_loop
from concurrent.futures import ThreadPoolExecutor
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
            if _cc >= 600:
                raise Exception("timed out")
            if await page.get_by_text("Error").first.is_visible():
                raise Exception("Error!")
        imgs = await page.query_selector_all('img')
        files = []
        for found in imgs:
            link = await found.get_attribute('src')
            if link.endswith(".jpg"):
                with ThreadPoolExecutor(1) as exe:
                    _loop = get_running_loop()
                    content = await _loop.run_in_executor(exe, requests.get, link)
                files.append(content)
        out = []
        for img in files:
            filename = f"{getSha256(img)}.png"
            fullPath = os.path.join(PATH, filename)
            if not os.path.exists(PATH):
                os.mkdir(PATH)
            with open(fullPath,"wb") as f:
                f.write(img.content)
                out.append(fullPath)
        return out
