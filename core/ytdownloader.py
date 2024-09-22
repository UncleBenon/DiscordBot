from asyncio import get_running_loop
from concurrent.futures import ThreadPoolExecutor
from pytubefix import YouTube
import os
from time import time
from hashlib import sha256

PATH = "temp"
async def downloadYoutubeVideoAsync(url:str):
    def downloadYouTubeVideo(url:str):
        if not url.startswith("http"):
            raise Exception("that's not a valid link.")

        # some string magic to get it working
        url = url.split("&")

        url = fr"{url[0]}"

        # lmao
        yt = YouTube(url)

        # check if the vid is shorter than 5m
        if yt.length >= 300:
            raise Exception("Video above 5m, bit long no?")

        try:
            ys = yt.streams.get_highest_resolution()
        except Exception:
            downloadYouTubeVideo(url)

        if ys.filesize_mb >= 25:
            raise Exception("File size too big, sorry bro. (above 25mb)")

        if not os.path.exists(PATH):
            os.mkdir(PATH)

        sha = sha256(url.encode())
        sha.update(str(time()).encode())
        _filename = sha.hexdigest() + ".mp4"

        ys.download(PATH, _filename)

        return os.path.join(PATH, _filename)

    with ThreadPoolExecutor(1) as exe:
        _loop = get_running_loop()
        content = await _loop.run_in_executor(exe, downloadYouTubeVideo, url)

    return content

if __name__ == "__main__":
    from asyncio import run
    url = "https://www.youtube.com/watch?v=Y6JnYnA9Tzo&pp=ygUUd29vc2ggaGFwcHkgYmlydGhkYXk%3D"
    test = run(downloadYoutubeVideoAsync(url))
    print(test)
    os.remove(test)
