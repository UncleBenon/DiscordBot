from playwright.async_api import async_playwright 
from asyncio import sleep, run
from core.CORE import curTime
import base64
import os

DALLE_PATH = 'DALLE_IMAGES'
async def dalle(prompt, debug = False) -> list[str]:
    async with async_playwright() as p:
        driver = await p.firefox.launch(headless=not debug)
        page = await driver.new_page()
        await page.goto("https://dalle-mini-dalle-mini.static.hf.space/index.html")
        await page.get_by_label("Enter your prompt").fill(str(prompt))
        await page.get_by_role("button", name="Run").click()

        _cc = 0
        while not await page.locator("#gallery div").nth(1).is_visible():
            await sleep(1)
            _cc += 1
            if _cc >= 120:
                raise Exception("Timed out")

        imgs = await page.locator(".gallery-item").all()

        b64 = []
        for found in imgs:
            link = await found.locator('img').get_attribute("src")
            b64.append(
                base64.b64decode(
                    link.split(',')[1]
                )
            )

        out = []
        for i, img in enumerate(b64):
            filename = f"{curTime()}-{i}.png"
            fullPath = os.path.join(DALLE_PATH, filename)
            if not os.path.exists(DALLE_PATH):
                os.mkdir(DALLE_PATH)
            with open(fullPath,"wb") as f:
                f.write(img)
                out.append(fullPath)
        return out

if __name__ == "__main__":
    run(dalle("abdul akir zimbabwae"))
