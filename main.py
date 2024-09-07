from discord.ext import commands
from core.CORE import (curTime, stableDiff, stableMusic, stableAudio)
from core.dalle import dalle
from core.OSRS import getBondPriceOSRS
from core.WoW import getWoWTokenPrice
from core.SDXL_Google import Stable_XL
from core.budgetGPT import StableLM
from core.audioldm import stableaudioLDM
from core.sha import getSha256
from core.removebg import RemoveBackGroundFunction
from asyncio import sleep
from os import remove
import discord
import random

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

DEBUG_CHANNEL = None
BOT_CHANNEL = None
@bot.listen()
async def on_ready():
    global DEBUG_CHANNEL, BOT_CHANNEL
    name = str(bot.user).split("#")[0]
    print(f'{name} Online',f'Ping: {int(bot.latency * 1000)}ms', sep="  -  ")
    DEBUG_CHANNEL = bot.get_channel(1048564475659288666)
    BOT_CHANNEL = bot.get_channel(1048600881593061416)
    await DEBUG_CHANNEL.send("----------------------------------------------------------------------")
    await DEBUG_CHANNEL.send(f'{curTime()}\t-\t{name} Online!\t-\tPing: {int(bot.latency * 1000)}ms')
    with open("inc/vidya.txt") as f:
        vidya = f.readlines()
    await bot.change_presence(status=discord.Status.dnd,activity=discord.Game(random.choice(vidya)))

@bot.listen()
async def on_resumed():
    with open("inc/vidya.txt") as f:
        vidya = f.readlines()
    await bot.change_presence(status=discord.Status.dnd,activity=discord.Game(random.choice(vidya)))

async def CheckChannel(c : commands.Context):
    if c.channel == BOT_CHANNEL:
        return True
    else:
        m = await BOT_CHANNEL.send(c.message.author.mention + " Use bot commands in the bot channel!")
        await c.message.delete()
        await m.delete(delay=10)
        return False

STABLE_QUEUE = []
@bot.command(aliases=['sd'])
async def stable(ctx : commands.Context, *, prompt : str):
    if not await CheckChannel(ctx):
        return
    global STABLE_QUEUE
    stored_prompt = getSha256(prompt)
    STABLE_QUEUE.append(stored_prompt)
    await DEBUG_CHANNEL.send(f"{curTime()}  -  {ctx.author} used the stable diffusion command")
    print(f"{curTime()}  -  {ctx.author} used the stable diffusion command")
    await ctx.message.add_reaction("⏳")

    while len(STABLE_QUEUE) > 1: 
        if stored_prompt == STABLE_QUEUE[0]:
            break
        await sleep(1)
    
    neg = prompt.split("!neg")
    
    try:
        if len(neg) > 1:
            out = await stableDiff(neg[0], neg[1])
        else:
            out = await stableDiff(prompt)
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
        if len(neg) > 1:
            await ctx.reply(f"# Stable Diff: {neg[0]}\nnegative prompt: {neg[1]}",files=files)
        else:
            await ctx.reply(f"# Stable Diff: {prompt}",files=files)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        for f in out:
            remove(f)
        STABLE_QUEUE.pop(0)

@stable.error
async def sd_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if not await CheckChannel(ctx):
            return
        await ctx.reply("Forgot a prompt there buddy", delete_after=15)
        await ctx.message.delete(delay=15)

STABLE_XL_QUEUE = []
@bot.command(aliases=['sdxl', 'sdx'])
async def stableXL(ctx : commands.Context, *, prompt : str):
    if not await CheckChannel(ctx):
        return
    global STABLE_XL_QUEUE
    stored_prompt = (prompt, curTime())
    stored_prompt = getSha256(prompt)
    STABLE_XL_QUEUE.append(stored_prompt)
    await DEBUG_CHANNEL.send(f"{curTime()}  -  {ctx.author} used the stable XL command")
    print(f"{curTime()}  -  {ctx.author} used the stable XL command")
    await ctx.message.add_reaction("⏳")

    while len(STABLE_XL_QUEUE) > 1: 
        if stored_prompt == STABLE_XL_QUEUE[0]:
            break
        await sleep(1)
    
    neg = prompt.split("!neg")
    
    try:
        if len(neg) > 1:
            out = await Stable_XL(neg[0], neg[1])
        else:
            out = await Stable_XL(prompt)
    except Exception as e:
        STABLE_XL_QUEUE.pop(0)
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
        if len(neg) > 1:
            await ctx.reply(f"# Stable Diff XL: {neg[0]}\nnegative prompt: {neg[1]}",files=files)
        else:
            await ctx.reply(f"# Stable Diff XL: {prompt}",files=files)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        for f in out:
            remove(f)
        STABLE_XL_QUEUE.pop(0)

@stableXL.error
async def sd_XL_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if not await CheckChannel(ctx):
            return
        await ctx.reply("Forgot a prompt there buddy", delete_after=15)
        await ctx.message.delete(delay=15)

STABLE_AUDIO_QUEUE = []
@bot.command(aliases=["sa"])
async def stableAu(ctx : commands.Context, *, prompt : str):
    if not await CheckChannel(ctx):
        return
    global STABLE_AUDIO_QUEUE
    await DEBUG_CHANNEL.send(f"{curTime()}  -  {ctx.author} used the stable audio command")
    print(f"{curTime()}  -  {ctx.author} used the stable audio command")
    stored_prompt = getSha256(prompt)
    STABLE_AUDIO_QUEUE.append(stored_prompt)
    await ctx.message.add_reaction("⏳")

    while len(STABLE_AUDIO_QUEUE) > 1: 
        if stored_prompt == STABLE_AUDIO_QUEUE[0]:
            break
        await sleep(0.5)

    neg = prompt.split("!neg")

    try:
        if len(neg) > 1:
            out = await stableAudio(neg[0], neg[1])
        else:
            out = await stableAudio(prompt)
    except Exception as e:
        STABLE_AUDIO_QUEUE.pop(0)
        await ctx.reply(e)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        return

    async with ctx.typing():
        with open(out, "rb") as f:
            file = discord.File(f, filename="video.mp4")
        if len(neg) > 1:
            await ctx.reply(f"# Stable Audio: {neg[0]}\nnegative prompt: {neg[1]}",file=file)
        else:
            await ctx.reply(f"# Stable Audio: {prompt}",file=file)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        remove(out)
        STABLE_AUDIO_QUEUE.pop(0)

@stableAu.error
async def sa_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if not await CheckChannel(ctx):
            return
        await ctx.reply("Forgot a prompt there buddy", delete_after=15)
        await ctx.message.delete(delay=15)

STABLE_AUDIO_LDM_QUEUE = []
@bot.command(aliases=["sal"])
async def stableAuldmldm(ctx : commands.Context, *, prompt : str):
    if not await CheckChannel(ctx):
        return
    global STABLE_AUDIO_LDM_QUEUE
    await DEBUG_CHANNEL.send(f"{curTime()}  -  {ctx.author} used the stable audio command")
    print(f"{curTime()}  -  {ctx.author} used the stable audio command")
    stored_prompt = getSha256(prompt)
    STABLE_AUDIO_LDM_QUEUE.append(stored_prompt)
    await ctx.message.add_reaction("⏳")

    while len(STABLE_AUDIO_LDM_QUEUE) > 1: 
        if stored_prompt == STABLE_AUDIO_LDM_QUEUE[0]:
            break
        await sleep(0.5)

    neg = prompt.split("!neg")

    try:
        if len(neg) > 1:
            out = await stableaudioLDM(neg[0], neg[1])
        else:
            out = await stableaudioLDM(prompt)
    except Exception as e:
        STABLE_AUDIO_LDM_QUEUE.pop(0)
        await ctx.reply(e)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        return

    async with ctx.typing():
        with open(out, "rb") as f:
            file = discord.File(f, filename="video.mp4")
        if len(neg) > 1:
            await ctx.reply(f"# Stable Audio: {neg[0]}\nnegative prompt: {neg[1]}",file=file)
        else:
            await ctx.reply(f"# Stable Audio: {prompt}",file=file)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        remove(out)
        STABLE_AUDIO_LDM_QUEUE.pop(0)

@stableAuldmldm.error
async def sa_ldm_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if not await CheckChannel(ctx):
            return
        await ctx.reply("Forgot a prompt there buddy", delete_after=15)
        await ctx.message.delete(delay=15)

GPTQUEUE = []
@bot.command(aliases=["gpt", "GPT"])
async def budgetChatGpt(ctx : commands.Context, *, prompt: str):
    if not await CheckChannel(ctx):
        return
    global GPTQUEUE
    stored_prompt = getSha256(prompt)
    GPTQUEUE.append(stored_prompt)
    await DEBUG_CHANNEL.send(f"{curTime()}  -  {ctx.author} used the GPT command")
    print(f"{curTime()}  -  {ctx.author} used the GPT command")
    await ctx.message.add_reaction("⏳")

    while len(GPTQUEUE) > 1: 
        if stored_prompt == GPTQUEUE[0]:
            break
        await sleep(0.5)
    
    try:
        out = await StableLM(prompt)
    except Exception as e:
        GPTQUEUE.pop(0)
        await ctx.reply(e)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        return

    async with ctx.typing():
        GPTQUEUE.pop(0)
        if isinstance(out, str):
            await ctx.reply(out.strip("<|im_end|>"))
        elif isinstance(out, list):
            _counter = 0
            _out = ""
            for i, line in enumerate(out):
                if i == 0:
                    _out = line
                    continue
                _out = f"{_out}\n{line.strip('<|im_end|>')}"
                _counter = len(_out)
                if _counter >= 1500:
                    await ctx.reply(_out)
                    _out = ""
                    _counter = 0
            if len(_out) > 0:
                await ctx.reply(_out)

        await ctx.message.remove_reaction("⏳", member=bot.user)

@budgetChatGpt.error
async def gpt_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if not await CheckChannel(ctx):
            return
        await ctx.reply("Forgot a prompt there buddy", delete_after=15)
        await ctx.message.delete(delay=15)

STABLE_MUSIC_QUEUE = []
@bot.command(aliases=["sm"])
async def stableMu(ctx : commands.Context, *, prompt : str):
    if not await CheckChannel(ctx):
        return
    global STABLE_MUSIC_QUEUE
    stored_prompt = getSha256(prompt)
    STABLE_MUSIC_QUEUE.append(stored_prompt)
    await DEBUG_CHANNEL.send(f"{curTime()}  -  {ctx.author} used the stable music command")
    print(f"{curTime()}  -  {ctx.author} used the stable music command")
    await ctx.message.add_reaction("⏳")

    while len(STABLE_MUSIC_QUEUE) > 1: 
        if stored_prompt == STABLE_MUSIC_QUEUE[0]:
            break
        await sleep(0.5)
    
    neg = prompt.split("!neg")
    
    try:
        if len(neg) > 1:
            out = await stableMusic(neg[0], neg[1])
        else:
            out = await stableMusic(prompt)
    except Exception as e:
        STABLE_MUSIC_QUEUE.pop(0)
        await ctx.reply(e)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        return

    async with ctx.typing():
        with open(out, "rb") as f:
            file = discord.File(f, filename="video.mp4")
        if len(neg) > 1:
            await ctx.reply(f"# Stable Music: {neg[0]}\nnegative prompt: {neg[1]}",file=file)
        else:
            await ctx.reply(f"# Stable Music: {prompt}",file=file)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        remove(out)
        STABLE_MUSIC_QUEUE.pop(0)

@stableMu.error
async def sm_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if not await CheckChannel(ctx):
            return
        await ctx.reply("Forgot a prompt there buddy", delete_after=15)
        await ctx.message.delete(delay=15)

DALLE_QUEUE = []
@bot.command(aliases=['dalle'])
async def Dalle(ctx : commands.Context, *, prompt):
    if not await CheckChannel(ctx):
        return

    global DALLE_QUEUE
    stored_prompt = getSha256(prompt)
    DALLE_QUEUE.append(stored_prompt)
    await DEBUG_CHANNEL.send(f"{curTime()}  -  {ctx.author} used the dalle command")
    print(f"{curTime()}  -  {ctx.author} used the dalle command")
    await ctx.message.add_reaction("⏳")

    while len(DALLE_QUEUE) > 1: 
        if stored_prompt == DALLE_QUEUE[0]:
            break
        await sleep(0.5)

    try:
        out = await dalle(prompt)
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
        await ctx.reply(f"# Dalle: {prompt}",files=files)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        for f in out:
            remove(f)
        DALLE_QUEUE.pop(0)

@Dalle.error
async def dalle_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if not await CheckChannel(ctx):
            return
        await ctx.reply("Forgot a prompt there buddy", delete_after=15)
        await ctx.message.delete(delay=15)

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
        await ctx.send(embed=embed)
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
        await ctx.send(embed=embed)
        await ctx.message.remove_reaction("⏳", member=bot.user)

@bot.command(aliases=['8ball'])
async def eightball(ctx : commands.Context): # Generic 8ball that literally every bot has.
    if not await CheckChannel(ctx):
        return
    async with ctx.typing():
        await DEBUG_CHANNEL.send(f"{curTime()}  -  {ctx.author} used the 8ball command")
        print(f"{curTime()}  -  {ctx.author} used the 8ball command")
        eightballresponse = [
            "As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
            "Don’t count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.", "My sources say no.",
            "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.",
            "Yes.", "Yes – definitely.", "You may rely on it."
        ]
        await ctx.reply(random.choice(eightballresponse))

FB_MUSIC_QUEUE = []
@bot.command(aliases=["fbm"])
async def facebookMU(ctx : commands.Context, *, prompt : str):
    if not await CheckChannel(ctx):
        return
    global FB_MUSIC_QUEUE
    stored_prompt = getSha256(prompt)
    FB_MUSIC_QUEUE.append(stored_prompt)
    await DEBUG_CHANNEL.send(f"{curTime()}  -  {ctx.author} used the facebook music command")
    print(f"{curTime()}  -  {ctx.author} used the facebook music command")
    await ctx.message.add_reaction("⏳")

    while len(FB_MUSIC_QUEUE) > 1: 
        if stored_prompt == FB_MUSIC_QUEUE[0]:
            break
        await sleep(0.5)
    
    try:
        out = await stableMusic(prompt)
    except Exception as e:
        FB_MUSIC_QUEUE.pop(0)
        await ctx.reply(e)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        return

    async with ctx.typing():
        with open(out, "rb") as f:
            file = discord.File(f, filename="video.mp4")
        await ctx.reply(f"# Facebook Music: {prompt}",file=file)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        remove(out)
        FB_MUSIC_QUEUE.pop(0)

@facebookMU.error
async def fb_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if not await CheckChannel(ctx):
            return
        await ctx.reply("Forgot a prompt there buddy", delete_after=15)
        await ctx.message.delete(delay=15)

RBG_QUEUE = []
@bot.command(aliases=["rbg"])
async def removeBg(ctx : commands.Context):
    if not await CheckChannel(ctx):
        return
    global RBG_QUEUE
    attachments = ctx.message.attachments
    if len(attachments) < 1:
        _msg = ctx.message.content.split(" ")
        _msg = _msg[1:] 
        attachments = [msg for msg in _msg if msg.startswith("https")]
        if len(attachments) < 1:
            await ctx.reply("need at least 1 image.")
            return
    stored_prompt = getSha256(str(ctx.author).encode())
    RBG_QUEUE.append(stored_prompt)
    await DEBUG_CHANNEL.send(f"{curTime()}  -  {ctx.author} used the Remove Background command")
    print(f"{curTime()}  -  {ctx.author} used the Remove Background command")
    await ctx.message.add_reaction("⏳")

    while len(RBG_QUEUE) > 1: 
        if stored_prompt == RBG_QUEUE[0]:
            break
        await sleep(0.5)

    out = []
    for file in attachments:
        try:
            if isinstance(file, str):
                out.append(await RemoveBackGroundFunction(file))
            else:
                out.append(await RemoveBackGroundFunction(file.url))
        except Exception as e:
            await ctx.reply(e)
            continue

    async with ctx.typing():
        files = []
        if len(out) > 0:
            for file in out:
                with open(file, "rb") as f:
                    files.append(
                        discord.File(f, filename="image.png")
                    )
            await ctx.reply("# Removed Background:", files=files)
            for file in out:
                remove(file)
        await ctx.message.remove_reaction("⏳", member=bot.user)
        RBG_QUEUE.pop(0)

if __name__ == "__main__":
    with open("inc/token.txt") as f:
        T = f.readline().strip()
    bot.run(T)
