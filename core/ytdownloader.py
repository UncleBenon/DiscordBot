from asyncio import get_running_loop
from concurrent.futures import ThreadPoolExecutor
from pytubefix import YouTube
from time import time
from hashlib import sha256
import ffmpeg
import os

PATH = "temp"
async def downloadYoutubeVideoAsync(url:str, start : str = None, end : str = None, fileType : str = None):
    def downloadYouTubeVideo(url:str, start : str = None, end : str = None, fileType : str = None):
        if not url.startswith("http"):
            raise Exception("that's not a valid link.")

        url = url.split("&")

        url = fr"{url[0]}"

        yt = YouTube(url)

        try:
            ys = yt.streams.get_highest_resolution()
        except Exception:
            downloadYouTubeVideo(url)

        if not os.path.exists(PATH):
            os.mkdir(PATH)

        sha = sha256(url.encode())
        sha.update(str(time()).encode())
        _filename = sha.hexdigest() + ".mp4"

        try:
            ys.download(PATH, _filename)
        except Exception:
            downloadYouTubeVideo(url)

        _filePath = os.path.join(PATH, _filename)

        sha.update(str(time()).encode())
        if not fileType:
            _outFilePath = sha.hexdigest() + ".mp4"
        else:
            _outFilePath = sha.hexdigest() + fileType
        _outFilePath = os.path.join(PATH, _outFilePath)

        if start and end:
            (
                ffmpeg
                .input(_filePath, ss=start, to=end)
                .output(_outFilePath)
                .run(quiet=True)
            )
        elif start:
            (
                ffmpeg
                .input(_filePath, ss=start)
                .output(_outFilePath)
                .run(quiet=True)
            )
        elif end:
            (
                ffmpeg
                .input(_filePath, to=end)
                .output(_outFilePath)
                .run(quiet=True)
            )
        elif fileType:
            (
                ffmpeg
                .input(_filePath)
                .output(_outFilePath)
                .run(quiet=True)
            )
        else:
            return _filePath

        os.remove(_filePath)
        return _outFilePath

    with ThreadPoolExecutor(1) as exe:
        _loop = get_running_loop()
        content = await _loop.run_in_executor(exe, downloadYouTubeVideo, url, start, end)

    return content
