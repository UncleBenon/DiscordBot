from datetime import datetime
from asyncio import get_running_loop
from concurrent.futures import ThreadPoolExecutor
import os
import ffmpeg
import random

def curTime() -> str:
    now = datetime.now()
    return str(now.strftime("%I:%M:%S %p"))

async def convertAsync(filePath : str, outputFileType : str = ".mp4") -> str:
    def convert() -> str:
        out = filePath.split(".")

        assert len(out) > 1
        assert outputFileType.startswith(".")

        outFilePath = out[0] + outputFileType

        imgs = []
        for (dirPath, _, fileNames) in os.walk("core/ffmpegimgs/"):
            for file in fileNames:
                imgs.append(dirPath + file)

        img = ffmpeg.input(random.choice(imgs), loop=1)
        sound = ffmpeg.input(filePath)

        ffmpeg.output(img.video, sound.audio, outFilePath, shortest=None).run(quiet=True)

        os.remove(filePath)
        return outFilePath

    with ThreadPoolExecutor(1) as exe:
        _loop = get_running_loop()
        content = await _loop.run_in_executor(exe, convert)
    return content
