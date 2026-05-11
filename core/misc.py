from datetime import datetime
from asyncio import get_running_loop
from concurrent.futures import ThreadPoolExecutor
import os
import ffmpeg

def curTime() -> str:
    now = datetime.now()
    return str(now.strftime("%I:%M:%S %p"))

async def convertAsync(filePath : str, outputFileType : str = ".ogg") -> str:
    def convert() -> str:
        out = filePath.split(".")

        assert len(out) > 1
        assert outputFileType.startswith(".")

        outFilePath = out[0] + outputFileType

        sound = ffmpeg.input(filePath)

        ffmpeg.output(sound.audio, outFilePath).run(quiet=True)

        os.remove(filePath)
        return outFilePath

    with ThreadPoolExecutor(1) as exe:
        _loop = get_running_loop()
        content = await _loop.run_in_executor(exe, convert)
    return content

def clamp(num, mini, maxi):
    return max(mini, min(num, maxi))
