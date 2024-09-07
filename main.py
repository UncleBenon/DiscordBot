from core.CORE import stableDiff, stableAudio, stableMusic
from core.SDXL_Google import Stable_XL
from core.dalle import dalle
from core.vidgen import sdVidGenFunction
from core.removebg import RemoveBackGroundFunction
from core.WoW import getWoWTokenPrice
from core.OSRS import getBondPriceOSRS
from core.budgetGPT import StableLM
from core.sha import getSha256
from discord.ext import commands
from datetime import datetime
from asyncio import sleep
from os import remove
import discord
import random

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

def curTime() -> str:
    now = datetime.now()
    return str(now.strftime("%I:%M:%S %p"))

DEBUG_CHANNEL = None
BOT_CHANNEL = None
@bot.listen()
async def on_ready() -> None:
    global DEBUG_CHANNEL, BOT_CHANNEL
    name = str(bot.user).split("#")[0]
    print(f'{curTime()}', f'{name} Online',f'Ping: {int(bot.latency * 1000)}ms', sep="  -  ")
    DEBUG_CHANNEL = bot.get_channel(1048564475659288666)
    BOT_CHANNEL = bot.get_channel(1048600881593061416)
    await DEBUG_CHANNEL.send("----------------------------------------------------------------------")
    await DEBUG_CHANNEL.send(f'{name} Online!\t-\tPing: {int(bot.latency * 1000)}ms')
    with open("inc/vidya.txt") as f:
        vidya = f.readlines()
        await bot.change_presence(status=discord.Status.dnd,activity=discord.Game(random.choice(vidya)))

@bot.listen()
async def on_resumed() -> None:
    with open("inc/vidya.txt") as f:
        vidya = f.readlines()
        await bot.change_presence(status=discord.Status.dnd,activity=discord.Game(random.choice(vidya)))

async def CheckChannel(c : commands.Context) -> None:
    if c.channel == BOT_CHANNEL:
        return True
    else:
        m = await BOT_CHANNEL.send(c.message.author.mention + " Use bot commands in the bot channel!")
        await c.message.delete()
        await m.delete(delay=10)
        return False

STABLE_QUEUE = []
@bot.command(aliases=['sd'])
async def StableDiff(ctx : commands.Context) -> None:
    if not await CheckChannel(ctx):
        return

    global STABLE_QUEUE

    prompt = ctx.message.content.split(' ')
    prompt = prompt[1:]

    if len(prompt) < 1:
        ctx.reply("Need a prompt buddy!")
        return

    stored_prompt = getSha256(prompt)
    STABLE_QUEUE.append(stored_prompt)
    await DEBUG_CHANNEL.send(f"{curTime()}  -  {ctx.author} used the stable diffusion command")
    print(f"{curTime()}  -  {ctx.author} used the stable diffusion command")
    await ctx.message.add_reaction("⏳")

    while len(STABLE_QUEUE) > 1: 
        if stored_prompt == STABLE_QUEUE[0]:
            break
        await sleep(1)

    _prompt = ''
    _neg = ''
    _addNeg = False
    for word in prompt:
        if word.lower() == '!neg':
            _addNeg = True
            continue
        if _addNeg:
            _neg += f'{word} '
        else:
            _prompt += f'{word} '

    try:
        out = await stableDiff(_prompt, _neg)
    except Exception as e:
        STABLE_QUEUE.pop(0)
        await ctx.reply(e)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        return

    async with ctx.typing():
        files: list[discord.File] = []
        for file in out:
            with open(file, "rb") as f:
                files.append(
                    discord.File(f, filename="image.png")
                )
        await ctx.reply(f"# Stable Diff: {_prompt}",files=files)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        for f in out:
            remove(f)
        STABLE_QUEUE.pop(0)

STABLE_QUEUE_XL = []
@bot.command(aliases=['sdx'])
async def StableDiffXL(ctx : commands.Context) -> None:
    if not await CheckChannel(ctx):
        return

    global STABLE_QUEUE_XL

    prompt = ctx.message.content.split(' ')
    prompt = prompt[1:]

    if len(prompt) < 1:
        ctx.reply("Need a prompt buddy!")
        return

    stored_prompt = getSha256(prompt)
    STABLE_QUEUE_XL.append(stored_prompt)
    await DEBUG_CHANNEL.send(f"{curTime()}  -  {ctx.author} used the stable XL command")
    print(f"{curTime()}  -  {ctx.author} used the stable XL command")
    await ctx.message.add_reaction("⏳")

    while len(STABLE_QUEUE_XL) > 1: 
        if stored_prompt == STABLE_QUEUE_XL[0]:
            break
        await sleep(1)

    _prompt = ''
    _neg = ''
    _addNeg = False
    for word in prompt:
        if word.lower() == '!neg':
            _addNeg = True
            continue
        if _addNeg:
            _neg += f'{word} '
        else:
            _prompt += f'{word} '

    try:
        out = await Stable_XL(_prompt, _neg)
    except Exception as e:
        STABLE_QUEUE_XL.pop(0)
        await ctx.reply(e)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        return

    async with ctx.typing():
        files: list[discord.File] = []
        for file in out:
            with open(file, "rb") as f:
                files.append(
                    discord.File(f, filename="image.png")
                )
        await ctx.reply(f"# Stable XL: {_prompt}",files=files)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        for f in out:
            remove(f)
        STABLE_QUEUE_XL.pop(0)

DALLE_QUEUE = []
@bot.command(aliases=['dalle'])
async def Dalle(ctx : commands.Context) -> None:
    if not await CheckChannel(ctx):
        return

    global DALLE_QUEUE

    prompt = ctx.message.content.split(' ')
    prompt = prompt[1:]

    if len(prompt) < 1:
        ctx.reply("Need a prompt buddy!")
        return

    stored_prompt = getSha256(prompt)
    DALLE_QUEUE.append(stored_prompt)
    await DEBUG_CHANNEL.send(f"{curTime()}  -  {ctx.author} used the Dalle command")
    print(f"{curTime()}  -  {ctx.author} used the Dalle command")
    await ctx.message.add_reaction("⏳")

    while len(DALLE_QUEUE) > 1: 
        if stored_prompt == DALLE_QUEUE[0]:
            break
        await sleep(1)

    _prompt = ''
    for word in prompt:
        _prompt += f'{word} '

    try:
        out = await dalle(_prompt)
    except Exception as e:
        DALLE_QUEUE.pop(0)
        await ctx.reply(e)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        return

    async with ctx.typing():
        files: list[discord.File] = []
        for file in out:
            with open(file, "rb") as f:
                files.append(
                    discord.File(f, filename="image.png")
                )
        await ctx.reply(f"# Dalle: {_prompt}",files=files)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        for f in out:
            remove(f)
        DALLE_QUEUE.pop(0)

VIDGEN_QUEUE = []
@bot.command(aliases=['vg'])
async def VidGen(ctx : commands.Context) -> None:
    if not await CheckChannel(ctx):
        return

    global VIDGEN_QUEUE

    prompt = ctx.message.content.split(' ')
    prompt = prompt[1:]

    if len(prompt) < 1:
        ctx.reply("Need a prompt buddy!")
        return

    stored_prompt = getSha256(prompt)
    VIDGEN_QUEUE.append(stored_prompt)
    await DEBUG_CHANNEL.send(f"{curTime()}  -  {ctx.author} used the Video Gen command")
    print(f"{curTime()}  -  {ctx.author} used the Video Gen command")
    await ctx.message.add_reaction("⏳")

    while len(VIDGEN_QUEUE) > 1: 
        if stored_prompt == VIDGEN_QUEUE[0]:
            break
        await sleep(1)

    _prompt = ''
    for word in prompt:
        _prompt += f'{word} '

    try:
        out = await sdVidGenFunction(_prompt)
    except Exception as e:
        VIDGEN_QUEUE.pop(0)
        await ctx.reply(e)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        return

    async with ctx.typing():
        with open(out, "rb") as f:
            file = discord.File(f, filename="video.mp4")
            await ctx.reply(f"# Video Gen: {_prompt}",file=file)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        remove(out)
        VIDGEN_QUEUE.pop(0)

STABLE_AUDIO_QUEUE = []
@bot.command(aliases=['vg'])
async def StableAudio(ctx : commands.Context) -> None:
    if not await CheckChannel(ctx):
        return

    global STABLE_AUDIO_QUEUE

    prompt = ctx.message.content.split(' ')
    prompt = prompt[1:]

    if len(prompt) < 1:
        ctx.reply("Need a prompt buddy!")
        return

    stored_prompt = getSha256(prompt)
    STABLE_AUDIO_QUEUE.append(stored_prompt)
    await DEBUG_CHANNEL.send(f"{curTime()}  -  {ctx.author} used the Stable Audio command")
    print(f"{curTime()}  -  {ctx.author} used the Stable Audio command")
    await ctx.message.add_reaction("⏳")

    while len(STABLE_AUDIO_QUEUE) > 1: 
        if stored_prompt == STABLE_AUDIO_QUEUE[0]:
            break
        await sleep(1)

    _prompt = ''
    _neg = ''
    _addNeg = False
    for word in prompt:
        if word.lower() == '!neg':
            _addNeg = True
            continue
        if _addNeg:
            _neg += f'{word} '
        else:
            _prompt += f'{word} '

    try:
        out = await stableAudio(_prompt, _neg)
    except Exception as e:
        STABLE_AUDIO_QUEUE.pop(0)
        await ctx.reply(e)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        return

    async with ctx.typing():
        with open(out, "rb") as f:
            file = discord.File(f, filename="video.mp4")
            await ctx.reply(f"# Stable Audio: {_prompt}",file=file)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        remove(out)
        STABLE_AUDIO_QUEUE.pop(0)

STABLE_MUSIC_QUEUE = []
@bot.command(aliases=['vg'])
async def StableMusic(ctx : commands.Context) -> None:
    if not await CheckChannel(ctx):
        return

    global STABLE_MUSIC_QUEUE

    prompt = ctx.message.content.split(' ')
    prompt = prompt[1:]

    if len(prompt) < 1:
        ctx.reply("Need a prompt buddy!")
        return

    stored_prompt = getSha256(prompt)
    STABLE_MUSIC_QUEUE.append(stored_prompt)
    await DEBUG_CHANNEL.send(f"{curTime()}  -  {ctx.author} used the Stable Music command")
    print(f"{curTime()}  -  {ctx.author} used the Stable Music command")
    await ctx.message.add_reaction("⏳")

    while len(STABLE_MUSIC_QUEUE) > 1: 
        if stored_prompt == STABLE_MUSIC_QUEUE[0]:
            break
        await sleep(1)

    _prompt = ''
    _neg = ''
    _addNeg = False
    for word in prompt:
        if word.lower() == '!neg':
            _addNeg = True
            continue
        if _addNeg:
            _neg += f'{word} '
        else:
            _prompt += f'{word} '

    try:
        out = await stableMusic(_prompt, _neg)
    except Exception as e:
        STABLE_MUSIC_QUEUE.pop(0)
        await ctx.reply(e)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        return

    async with ctx.typing():
        with open(out, "rb") as f:
            file = discord.File(f, filename="video.mp4")
            await ctx.reply(f"# Stable Music: {_prompt}",file=file)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        remove(out)
        STABLE_MUSIC_QUEUE.pop(0)



@bot.command(aliases=['bond', 'bp'])
async def bondprice(ctx : commands.Context):
    if not await CheckChannel(ctx):
        return
    
    await DEBUG_CHANNEL.send(f"{curTime()}  -  {ctx.author} used the Bond Price (OSRS) command")
    print(f"{curTime()}  -  {ctx.author} used the Bond Price (OSRS) command")
    await ctx.message.add_reaction("⏳")

    try:
        sellPrice, buyPrice = await getBondPriceOSRS()
    except Exception as e:
        await ctx.reply(e)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        return

    async with ctx.typing():
        embed=discord.Embed(title="Old School RuneScape current bond prices", url="https://prices.runescape.wiki/osrs/item/13190", description="Current bond prices directly off the wiki!", color=0xf5c211)
        embed.set_thumbnail(url="https://oldschool.runescape.wiki/images/Old_school_bond_detail.png")
        embed.add_field(name="Sell Price: ", value=f":coin: {sellPrice}", inline=False)
        embed.add_field(name="Buy Price: ", value=f":coin: {buyPrice}", inline=False)
        await ctx.reply(embed=embed)
        await ctx.message.remove_reaction("⏳", member=bot.user)

@bot.command(aliases=['tp', 'tokenprice'])
async def TokenPrice(ctx : commands.Context):
    if not await CheckChannel(ctx):
        return
    
    await DEBUG_CHANNEL.send(f"{curTime()}  -  {ctx.author} used the Token Price command")
    print(f"{curTime()}  -  {ctx.author} used the Token Price command")
    await ctx.message.add_reaction("⏳")

    try:
        tprice = await getWoWTokenPrice()
    except Exception as e:
        await ctx.reply(e)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        return

    async with ctx.typing():
        embed=discord.Embed(title="World of Warcraft Token Prices", url="https://wowauction.us", description="Current WoW Token prices directly off WoW Auction", color=0xf5c211)
        embed.set_thumbnail(url="https://wow.zamimg.com/images/wow/icons/large/wow_token01.jpg")
        embed.add_field(name="North America:", value="", inline=False)
        embed.add_field(name="Retail:", value=f":coin: {tprice[0]}", inline=True)
        embed.add_field(name="Classic:", value=f":coin: {tprice[2]}", inline=True)
        embed.add_field(name="", value="---", inline=False)
        embed.add_field(name="Europe:", value="", inline=False)
        embed.add_field(name="Retail:", value=f":coin: {tprice[1]}", inline=True)
        embed.add_field(name="Classic:", value=f":coin: {tprice[3]}", inline=True)
        await ctx.reply(embed=embed)
        await ctx.message.remove_reaction("⏳", member=bot.user)

if __name__ == "__main__":
    with open("inc/token.txt") as f:
        T = f.readline().strip()
    bot.run(T)
