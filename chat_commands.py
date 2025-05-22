from os import path, remove
from core.misc import (
    curTime,
    STABLE_QUEUE,
    STABLE_XL_QUEUE,
    DALLE_QUEUE,
    VS_QUEUE,
    BARK_QUEUE,
)
from core.sha import getSha256
from core.CORE import stableDiff
from core.SDXL_Google import Stable_XL
from core.dalle import dalle
from core.voice import voiceSynthFunction
from core.WoW import getWoWTokenPrice
from core.OSRS import getBondPriceOSRS
from asyncio import sleep
from discord.ext import commands
import discord


class ChatCommands(commands.Cog):
    def __init__(self, bot, botChannel, debugChannel):
        self.bot = bot
        self.BOT_CHANNEL = botChannel
        self.DEBUG_CHANNEL = debugChannel
        self.stableQueue = STABLE_QUEUE
        self.stableXLQueue = STABLE_XL_QUEUE
        self.dalleQueue = DALLE_QUEUE
        self.vsQueue = VS_QUEUE
        self.barkQueue = BARK_QUEUE

    async def checkChannel(self, c: commands.Context) -> None:
        if c.channel == self.BOT_CHANNEL:
            return True
        else:
            m = await self.BOT_CHANNEL.send(
                c.message.author.mention + " Use bot commands in the bot channel!"
            )
            await c.message.delete()
            await m.delete(delay=10)
            return False

    @commands.hybrid_command(name="stablediffusion", aliases=["sd"])
    async def StableDiff(self, ctx: commands.Context, inp) -> None:
        if not await self.checkChannel(ctx):
            return

        if ctx.interaction:
            print(inp)
            await ctx.reply("ayyy", ephemeral=True)
            prompt = inp
        else:
            prompt = ctx.message.content.split(" ")
            prompt = prompt[1:]

        if len(prompt) < 1:
            await ctx.reply("Need a prompt buddy!")
            return

        stored_prompt = getSha256(prompt)
        self.stableQueue.append(stored_prompt)
        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the stable diffusion command"
        )
        print(f"{curTime()}  -  {ctx.author} used the stable diffusion command")
        #await ctx.message.add_reaction("⏳")

        while len(self.stableQueue) > 1:
            if stored_prompt == self.stableQueue[0]:
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
            self.stableQueue.pop(0)
            await ctx.reply(e)
            #await ctx.message.remove_reaction("⏳", member=self.bot.user)
            return

        async with ctx.typing():
            files: list[discord.File] = []
            for file in out:
                with open(file, "rb") as f:
                    files.append(discord.File(f, filename=f"{stored_prompt}.png"))
            await ctx.reply(f"# Stable Diff: {_prompt}", files=files)
            #await ctx.message.remove_reaction("⏳", member=self.bot.user)
            for f in out:
                remove(f)
            self.stableQueue.pop(0)

    @commands.command(aliases=["sdx"])
    async def StableDiffXL(self, ctx: commands.Context) -> None:
        if not await self.checkChannel(ctx):
            return

        prompt = ctx.message.content.split(" ")
        prompt = prompt[1:]

        if len(prompt) < 1:
            await ctx.reply("Need a prompt buddy!")
            return

        stored_prompt = getSha256(prompt)
        self.stableXLQueue.append(stored_prompt)
        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the stable XL command"
        )
        print(f"{curTime()}  -  {ctx.author} used the stable XL command")
        await ctx.message.add_reaction("⏳")

        while len(self.stableXLQueue) > 1:
            if stored_prompt == self.stableXLQueue[0]:
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
            self.stableXLQueue.pop(0)
            await ctx.reply(e)
            await ctx.message.remove_reaction("⏳", member=self.bot.user)
            return

        async with ctx.typing():
            files: list[discord.File] = []
            for file in out:
                with open(file, "rb") as f:
                    files.append(discord.File(f, filename=f"{stored_prompt}.png"))
            await ctx.reply(f"# Stable XL: {_prompt}", files=files)
            await ctx.message.remove_reaction("⏳", member=self.bot.user)
            for f in out:
                remove(f)
            self.stableXLQueue.pop(0)

    @commands.command(aliases=["dalle"])
    async def Dalle(self, ctx: commands.Context) -> None:
        if not await self.checkChannel(ctx):
            return

        prompt = ctx.message.content.split(" ")
        prompt = prompt[1:]

        if len(prompt) < 1:
            await ctx.reply("Need a prompt buddy!")
            return

        stored_prompt = getSha256(prompt)
        self.dalleQueue.append(stored_prompt)
        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the Dalle command"
        )
        print(f"{curTime()}  -  {ctx.author} used the Dalle command")
        await ctx.message.add_reaction("⏳")

        while len(self.dalleQueue) > 1:
            if stored_prompt == self.dalleQueue[0]:
                break
            await sleep(1)

        _prompt = ""
        for word in prompt:
            _prompt += f"{word} "

        try:
            out = await dalle(_prompt)
        except Exception as e:
            self.dalleQueue.pop(0)
            await ctx.reply(e)
            await ctx.message.remove_reaction("⏳", member=self.bot.user)
            return

        async with ctx.typing():
            files: list[discord.File] = []
            for file in out:
                with open(file, "rb") as f:
                    files.append(discord.File(f, filename=f"{stored_prompt}.png"))
            await ctx.reply(f"# Dalle: {_prompt}", files=files)
            await ctx.message.remove_reaction("⏳", member=self.bot.user)
            for f in out:
                remove(f)
            self.dalleQueue.pop(0)

    @commands.command(aliases=["vs"])
    async def VoiceSynth(self, ctx: commands.Context) -> None:
        if not await self.checkChannel(ctx):
            return

        prompt = ctx.message.content.split(" ")
        prompt = prompt[1:]

        if len(prompt) < 1:
            await ctx.reply("Need a prompt buddy!")
            return

        stored_prompt = getSha256(prompt)
        self.vsQueue.append(stored_prompt)
        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the Voice Synth command"
        )
        print(f"{curTime()}  -  {ctx.author} used the Voice Synth command")
        await ctx.message.add_reaction("⏳")

        while len(self.vsQueue) > 1:
            if stored_prompt == self.vsQueue[0]:
                break
            await sleep(1)

        _prompt = ""
        for word in prompt:
            _prompt += f"{word} "

        try:
            out = await voiceSynthFunction(_prompt)
        except Exception as e:
            self.vsQueue.pop(0)
            await ctx.reply(e)
            await ctx.message.remove_reaction("⏳", member=self.bot.user)
            return

        if len(_prompt) > 1500:
            _prompt = ""
        try:
            async with ctx.typing():
                with open(out, "rb") as f:
                    _name = path.basename(out)
                    file = discord.File(f, filename=_name)
                    await ctx.reply(f"# Voice Synth: {_prompt}", file=file)
                await ctx.message.remove_reaction("⏳", member=self.bot.user)
                remove(out)
                self.vsQueue.pop(0)
        except Exception as e:
            self.vsQueue.pop(0)
            remove(out)
            await ctx.reply(e)
            await ctx.message.remove_reaction("⏳", member=self.bot.user)
            return

    @commands.command(aliases=["bond", "bp"])
    async def bondprice(self, ctx: commands.Context):
        if not await self.checkChannel(ctx):
            return

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the Bond Price (OSRS) command"
        )
        print(f"{curTime()}  -  {ctx.author} used the Bond Price (OSRS) command")
        await ctx.message.add_reaction("⏳")

        try:
            sellPrice, buyPrice = await getBondPriceOSRS()
        except Exception as e:
            await ctx.reply(e)
            await ctx.message.remove_reaction("⏳", member=self.bot.user)
            return

        async with ctx.typing():
            embed = discord.Embed(
                title="Old School RuneScape current bond prices",
                url="https://prices.runescape.wiki/osrs/item/13190",
                description="Current bond prices directly off the wiki!",
                color=0xF5C211,
            )
            embed.set_thumbnail(
                url="https://oldschool.runescape.wiki/images/Old_school_bond_detail.png"
            )
            embed.add_field(
                name="Sell Price: ", value=f":coin: {sellPrice}", inline=False
            )
            embed.add_field(
                name="Buy Price: ", value=f":coin: {buyPrice}", inline=False
            )
            await ctx.reply(embed=embed)
            await ctx.message.remove_reaction("⏳", member=self.bot.user)

    @commands.command(aliases=["tp", "tokenprice"])
    async def TokenPrice(self, ctx: commands.Context):
        if not await self.checkChannel(ctx):
            return

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the Token Price command"
        )
        print(f"{curTime()}  -  {ctx.author} used the Token Price command")
        await ctx.message.add_reaction("⏳")

        try:
            tprice = await getWoWTokenPrice()
        except Exception as e:
            await ctx.reply(e)
            await ctx.message.remove_reaction("⏳", member=self.bot.user)
            return

        async with ctx.typing():
            embed = discord.Embed(
                title="World of Warcraft Token Prices",
                url="https://wowauction.us",
                description="Current WoW Token prices directly off WoW Auction",
                color=0xF5C211,
            )
            embed.set_thumbnail(
                url="https://wow.zamimg.com/images/wow/icons/large/wow_token01.jpg"
            )
            embed.add_field(name="North America:", value="", inline=False)
            embed.add_field(name="Retail:", value=f":coin: {tprice[0]}", inline=True)
            embed.add_field(name="Classic:", value=f":coin: {tprice[2]}", inline=True)
            embed.add_field(name="", value="---", inline=False)
            embed.add_field(name="Europe:", value="", inline=False)
            embed.add_field(name="Retail:", value=f":coin: {tprice[1]}", inline=True)
            embed.add_field(name="Classic:", value=f":coin: {tprice[3]}", inline=True)
            await ctx.reply(embed=embed)
            await ctx.message.remove_reaction("⏳", member=self.bot.user)
