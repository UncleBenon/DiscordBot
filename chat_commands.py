from os import path, remove
from core.misc import (
    curTime,
    STABLE_QUEUE,
    STABLE_XL_QUEUE,
    DALLE_QUEUE,
    VS_QUEUE,
)
from core.sha import getSha256
from core.CORE import stableDiff
from core.SDXL_Google import Stable_XL
from core.dalle import dalle
from core.voice import voiceSynthFunction
from asyncio import sleep
from discord.ext import commands
import discord

BOT: commands.Bot = None
DEBUG_CHANNEL: discord.GuildChannel = None
BOT_CHANNEL: discord.GuildChannel = None


async def checkChannel(c: commands.Context) -> None:
    if c.channel == BOT_CHANNEL:
        return True
    else:
        m = await BOT_CHANNEL.send(
            c.message.author.mention + " Use bot commands in the bot channel!"
        )
        await c.message.delete()
        await m.delete(delay=10)
        return False


@BOT.command(aliases=["sd"])
async def StableDiff(ctx: commands.Context) -> None:
    if not await checkChannel(ctx):
        return

    global STABLE_QUEUE

    prompt = ctx.message.content.split(" ")
    prompt = prompt[1:]

    if len(prompt) < 1:
        ctx.reply("Need a prompt buddy!")
        return

    stored_prompt = getSha256(prompt)
    STABLE_QUEUE.append(stored_prompt)
    await DEBUG_CHANNEL.send(
        f"{curTime()}  -  {ctx.author} used the stable diffusion command"
    )
    print(f"{curTime()}  -  {ctx.author} used the stable diffusion command")
    await ctx.message.add_reaction("⏳")

    while len(STABLE_QUEUE) > 1:
        if stored_prompt == STABLE_QUEUE[0]:
            break
        await sleep(1)

    _prompt = ""
    _neg = ""
    _addNeg = False
    for word in prompt:
        if word.lower() == "!neg":
            _addNeg = True
            continue
        if _addNeg:
            _neg += f"{word} "
        else:
            _prompt += f"{word} "

    try:
        out = await stableDiff(_prompt, _neg)
    except Exception as e:
        STABLE_QUEUE.pop(0)
        await ctx.reply(e)
        await ctx.message.remove_reaction("⏳", member=BOT.user)
        return

    async with ctx.typing():
        files: list[discord.File] = []
        for file in out:
            with open(file, "rb") as f:
                files.append(discord.File(f, filename=f"{stored_prompt}.png"))
        await ctx.reply(f"# Stable Diff: {_prompt}", files=files)
        await ctx.message.remove_reaction("⏳", member=BOT.user)
        for f in out:
            remove(f)
        STABLE_QUEUE.pop(0)


@BOT.command(aliases=["sdx"])
async def StableDiffXL(ctx: commands.Context) -> None:
    if not await checkChannel(ctx):
        return

    global STABLE_XL_QUEUE

    prompt = ctx.message.content.split(" ")
    prompt = prompt[1:]

    if len(prompt) < 1:
        ctx.reply("Need a prompt buddy!")
        return

    stored_prompt = getSha256(prompt)
    STABLE_XL_QUEUE.append(stored_prompt)
    await DEBUG_CHANNEL.send(f"{curTime()}  -  {ctx.author} used the stable XL command")
    print(f"{curTime()}  -  {ctx.author} used the stable XL command")
    await ctx.message.add_reaction("⏳")

    while len(STABLE_XL_QUEUE) > 1:
        if stored_prompt == STABLE_XL_QUEUE[0]:
            break
        await sleep(1)

    _prompt = ""
    _neg = ""
    _addNeg = False
    for word in prompt:
        if word.lower() == "!neg":
            _addNeg = True
            continue
        if _addNeg:
            _neg += f"{word} "
        else:
            _prompt += f"{word} "

    try:
        out = await Stable_XL(_prompt, _neg)
    except Exception as e:
        STABLE_XL_QUEUE.pop(0)
        await ctx.reply(e)
        await ctx.message.remove_reaction("⏳", member=BOT.user)
        return

    async with ctx.typing():
        files: list[discord.File] = []
        for file in out:
            with open(file, "rb") as f:
                files.append(discord.File(f, filename=f"{stored_prompt}.png"))
        await ctx.reply(f"# Stable XL: {_prompt}", files=files)
        await ctx.message.remove_reaction("⏳", member=BOT.user)
        for f in out:
            remove(f)
        STABLE_XL_QUEUE.pop(0)


@BOT.command(aliases=["dalle"])
async def Dalle(ctx: commands.Context) -> None:
    if not await checkChannel(ctx):
        return

    global DALLE_QUEUE

    prompt = ctx.message.content.split(" ")
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

    _prompt = ""
    for word in prompt:
        _prompt += f"{word} "

    try:
        out = await dalle(_prompt)
    except Exception as e:
        DALLE_QUEUE.pop(0)
        await ctx.reply(e)
        await ctx.message.remove_reaction("⏳", member=BOT.user)
        return

    async with ctx.typing():
        files: list[discord.File] = []
        for file in out:
            with open(file, "rb") as f:
                files.append(discord.File(f, filename=f"{stored_prompt}.png"))
        await ctx.reply(f"# Dalle: {_prompt}", files=files)
        await ctx.message.remove_reaction("⏳", member=BOT.user)
        for f in out:
            remove(f)
        DALLE_QUEUE.pop(0)


@BOT.command(aliases=["vs"])
async def VoiceSynth(ctx: commands.Context) -> None:
    if not await checkChannel(ctx):
        return

    global VS_QUEUE

    prompt = ctx.message.content.split(" ")
    prompt = prompt[1:]

    if len(prompt) < 1:
        ctx.reply("Need a prompt buddy!")
        return

    stored_prompt = getSha256(prompt)
    VS_QUEUE.append(stored_prompt)
    await DEBUG_CHANNEL.send(
        f"{curTime()}  -  {ctx.author} used the Voice Synth command"
    )
    print(f"{curTime()}  -  {ctx.author} used the Voice Synth command")
    await ctx.message.add_reaction("⏳")

    while len(VS_QUEUE) > 1:
        if stored_prompt == VS_QUEUE[0]:
            break
        await sleep(1)

    _prompt = ""
    for word in prompt:
        _prompt += f"{word} "

    try:
        out = await voiceSynthFunction(_prompt)
    except Exception as e:
        VS_QUEUE.pop(0)
        await ctx.reply(e)
        await ctx.message.remove_reaction("⏳", member=BOT.user)
        return

    if len(_prompt) > 1500:
        _prompt = ""
    try:
        async with ctx.typing():
            with open(out, "rb") as f:
                _name = path.basename(out)
                file = discord.File(f, filename=_name)
                await ctx.reply(f"# Voice Synth: {_prompt}", file=file)
            await ctx.message.remove_reaction("⏳", member=BOT.user)
            remove(out)
            VS_QUEUE.pop(0)
    except Exception as e:
        VS_QUEUE.pop(0)
        remove(out)
        await ctx.reply(e)
        await ctx.message.remove_reaction("⏳", member=BOT.user)
        return
