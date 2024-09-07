from playwright.async_api import async_playwright 
from asyncio import sleep, run

async def StableLM(prompt : str, DEBUG : bool = False) -> str:
    async with async_playwright() as p:
        driver = await p.firefox.launch(headless = not DEBUG)
        page = await driver.new_page()
        await page.goto("https://stabilityai-stablelm-2-chat.hf.space/")
        await page.get_by_placeholder("input").fill(prompt)
        await page.get_by_role("button", name="Submit").click()
        await sleep(1)

        if await page.get_by_text("error").is_visible():
            await page.goto("https://stabilityai-stable-code-instruct-3b.hf.space")
            await page.get_by_placeholder("input").fill(prompt)
            await page.get_by_role("button", name="Submit").click()
            await sleep(1)

        stop = page.get_by_role("button", name="Stop").first
        _cc = 0
        while await stop.is_visible():
            await sleep(1)
            _cc += 1
            if _cc >= 120:
                raise Exception("Timed out")

        await sleep(1)
        out = await page.get_by_label("bot's message:").get_attribute("aria-label")
        out = out.strip("bot's message: ")

        return out.split('\n') if len(out) >= 2000 else out


if __name__ == "__main__":
    test = run(
        StableLM(
            "write me an expansion idea for Final Fantasy XIV involving potatos"
        )
    )
    if isinstance(test, list):
        for line in test:
            print(line)
