from concurrent.futures import ThreadPoolExecutor
from playwright.async_api import async_playwright
from hashlib import sha256
from requests import get
from asyncio import sleep, get_running_loop
from core.removebg import downloadImage
from random import randint
import os

PATH = "temp"
URL = "https://diffusers-unofficial-sdxl-turbo-i2i-t2i.hf.space/"

async def stable_xl_function(prompt: str, image: str = None, DEBUG: bool = False) -> list[str]:
    _del_reminder = False
    _prompt = "#component-5 > label > textarea"
    _upload_button = "#component-9 > div.image-container.svelte-rrgd5g > div > button"
    _options = "#component-12 > button"
    _seed_inp = "#component-15 > div.wrap.svelte-pc1gm4 > div > input"
    _generate_button = "#component-6"
    _generated_image = "#component-11 > button > div > img"

    if image:
        if image.startswith("http"):
            _, inp = await downloadImage(image)
            _del_reminder = True
        else:
            inp = image

    async with async_playwright() as p:
        driver = await p.firefox.launch(headless=not DEBUG)
        page = await driver.new_page()
        await page.goto(URL)

        if await page.get_by_text("Your space is in error").is_visible():
            raise Exception("Space is having errors, not the bot's fault")

        await sleep(1)
        await page.click(_options) # open options

        if image: # if an image is supplied use that for image to image
            async with page.expect_file_chooser() as f:
                await page.locator(_upload_button).click()
                _upload = await f.value
                await _upload.set_files(inp)

        await sleep(1)

        await page.fill(_prompt, prompt) # set prompt

        out = []
        for _ in range(4):
            await page.fill(_seed_inp, gen_seed()) # set seed
            await page.click(_generate_button) # generate image
            await sleep(10)

            link = await page.locator(_generated_image).get_attribute("src")

            with ThreadPoolExecutor(1) as exe:
                _loop = get_running_loop()
                try:
                    file = await _loop.run_in_executor(exe, get, link)
                except Exception as e:
                    print(e)
                    continue
            if file.status_code != 200:
                continue
            file = file.content
            filename = f"{sha256(file).hexdigest()}.webp"
            if not os.path.exists(PATH):
                os.mkdir(PATH)
            fullPath = os.path.join(PATH, filename)
            with open(fullPath, 'wb') as f:
                f.write(file)
            out.append(fullPath)

    if _del_reminder:
        os.remove(inp)

    return out

def gen_seed() -> str:
    return str(randint(0, 12013012031030))
