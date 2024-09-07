from playwright.async_api import async_playwright 
from asyncio import sleep, run
from core.sha import getSha256
import base64
import os

PATH = "temp"
async def Stable_XL(prompt : str, negPrompt : str = None, debug : bool = False) -> list[str]:
    async with async_playwright() as p:
        driver = await p.firefox.launch(headless=not debug)
        page = await driver.new_page()
        await page.goto("https://google-sdxl.hf.space/")
        await page.get_by_placeholder("Enter your prompt").fill(prompt)
        if negPrompt:
            await page.get_by_role("button", name="Advanced settings ▼").click()
            await page.get_by_placeholder("Enter a negative prompt").fill(negPrompt)
        await page.get_by_role("button", name="Generate").click()

        _cc = 0

        while await page.get_by_label("Thumbnail 1 of").is_hidden():
            await sleep(1)
            _cc += 1
            if _cc >= 120:
                raise Exception("Timed out")
            if await page.get_by_text("Error").first.is_visible():
                raise Exception("Please try again with a different prompt\nRemember, it's Google. No Naughty words!")

        imgs = await page.query_selector_all('img')

        b64 = []
        for found in imgs:
            link = await found.get_attribute('src')
            if link.startswith("data"):
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


if __name__ == '__main__':
    test = run(Stable_XL("ass", debug=True))
    print(test)
