from asyncio import run
from core.CORE import stableDiff, stableAudio, stableMusic
from core.SDXL_Google import Stable_XL
from core.dalle import dalle
from core.vidgen import sdVidGenFunction
from core.removebg import RemoveBackGroundFunction
from core.WoW import getWoWTokenPrice
from core.OSRS import getBondPriceOSRS
from core.budgetGPT import StableLM

def runTests(debug : bool = False):
    from os import remove
    try:
        test = run(getWoWTokenPrice(debug))
        print("WoW Token price passed")
    except Exception:
        print("WoW Token price failed")
    try:
        test = run(getBondPriceOSRS(debug))
        print("Runescape Bond price passed")
    except Exception:
        print("Runescape Bond price failed")
    try:
        test = run(stableDiff("Clarence Thomas", debug=debug))
        for t in test:
            remove(t)
        print("stable diff passed")
    except Exception:
        print("stable diff failed")
    try:
        test = run(stableAudio("Clarence Thomas", debug=debug))
        remove(test)
        print("stable audio passed")
    except Exception:
        print("stable audio failed")
    try:
        test = run(stableMusic("Clarence Thomas", debug=debug))
        remove(test)
        print("stable music passed")
    except Exception:
        print("stable music failed")
    try:
        test = run(Stable_XL("Clarence Thomas", debug=debug))
        for t in test:
            remove(t)
        print("stable diff XL passed")
    except Exception:
        print("stable diff XL failed")
    try:
        test = run(dalle("Clarence Thomas", debug=debug))
        for t in test:
            remove(t)
        print("dalle passed")
    except Exception:
        print("dalle failed")
    try:
        test = run(sdVidGenFunction("Clarence Thomas", DEBUG=debug))
        remove(test)
        print("VidGen passed")
    except Exception:
        print("VidGen failed")
    try:
        test = run(RemoveBackGroundFunction(inp="https://data2.nssmag.com/images/galleries/22874/wojak-nss-magazine-1.jpg", DEBUG=debug))
        remove(test)
        print("Remove BG passed")
    except Exception:
        print("Remove BG failed")
    try:
        test = run(StableLM("how do i punish a dog", DEBUG=debug))
        print("GPT passed")
    except Exception:
        print("GPT failed")

if __name__ == "__main__":
    runTests(True)
