from concurrent.futures import ThreadPoolExecutor
from asyncio import get_running_loop
from hashlib import sha256
from requests import get
from functools import partial
import os

DIR_PATH = "temp"

async def downloadTwitterVideoFunction(URL):
    if not URL.startswith("https://x.com/"):
        raise Exception("Invalid Link.")

    URL = URL.replace("x.com", "api.vxtwitter.com")

    page = get(URL)

    if page.status_code != 200:
        raise Exception(f"Page failed to load. {page.status_code}")

    content = page.text
    content = content.split("mediaURLs")[1][4:]
    mediaUrl = content.split('"')[0]
    if len(mediaUrl) < 1:
        raise Exception("File not found.")

    fileType = mediaUrl.split(".")[-1]
    with ThreadPoolExecutor(1) as exe:
        _loop = get_running_loop()
        file = await _loop.run_in_executor(exe, partial(get, mediaUrl, stream=True))

    if file.status_code != 200:
        raise Exception("File failed to download.")

    file = file.content
    filename = f"{sha256(file).hexdigest()}.{fileType}"
    if not os.path.exists(DIR_PATH):
        os.mkdir(DIR_PATH)
    fullPath = os.path.join(DIR_PATH, filename)
    with open(fullPath, 'wb') as f:
        f.write(file)

    return fullPath
