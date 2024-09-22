from asyncio import get_running_loop
from concurrent.futures import ThreadPoolExecutor
from pytubefix import YouTube
from time import time
from hashlib import sha256
import ffmpeg
import os

PATH = "temp"
async def downloadYoutubeVideoAsync(url:str, crop : bool = False, start : str = None, end : str = None):
    def downloadYouTubeVideo(url:str, crop : bool = False, start : str = None, end : str = None):
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

        _filePath = os.path.join(PATH, _filename)

        if not crop:
            return _filePath
        else:
            sha.update(time().encode())
            _outFilePath = sha.hexdigest() + ".mp4"
            _outFilePath = os.path.join(PATH, _outFilePath)
            (
                ffmpeg
                .input(_filePath)
                .output(_outFilePath)
                .run(quiet=True)
            )
            os.remove(_filePath)
            return _outFilePath

    with ThreadPoolExecutor(1) as exe:
        _loop = get_running_loop()
        content = await _loop.run_in_executor(exe, downloadYouTubeVideo, url, crop, start, end)

    return content

if __name__ == "__main__":
    from asyncio import run
    url = "https://www.youtube.com/watch?v=Y6JnYnA9Tzo&pp=ygUUd29vc2ggaGFwcHkgYmlydGhkYXk%3D"
    test = run(downloadYoutubeVideoAsync(url))
    print(test)
    os.remove(test)
