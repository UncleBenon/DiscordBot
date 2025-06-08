from playwright.async_api import async_playwright
from requests import get
from hashlib import sha256
from asyncio import sleep
import os

URL = "https://vchitect-lavie.hf.space/"

DIR_PATH = "temp"
async def vgMasterFunction(prompt : str, DEBUG = False):
    _input = "#prompt-in > label > textarea"
    _generateButton = "#component-13"
    _output = "#video-output > div.wrap.svelte-euo1cw > div.mirror-wrap.svelte-euo1cw > video"

    async with async_playwright() as p:
        driver = await p.firefox.launch(headless = not DEBUG)
        page = await driver.new_page()
        await page.goto(URL)

        while await page.get_by_text("Preparing Space").is_visible() or await page.get_by_text("Internal Error").is_visible():
            await sleep(10)
            await page.goto(URL)
