from os import path, remove
from core.misc import curTime
from core.sha import getSha256
from core.stableDiff import stableDiff
from core.SDXL_Google import Stable_XL
from core.dalle import dalle
from core.voice import voiceSynthFunction
from core.bark import barkVoiceSynthFunc
from core.WoW import getWoWTokenPrice
from core.OSRS import getBondPriceOSRS
from core.removebg import RemoveBackGroundFunction
from core.ghiblify import ghiblifyFunction
from core.video_gen import vgMasterFunction
from core.flux import fluxMasterFunction
from asyncio import sleep
from discord.ext import commands
import discord


class ChatCommands(commands.Cog):
    def __init__(self, bot, botChannel, debugChannel):
        self.bot = bot
        self.BOT_CHANNEL = botChannel
        self.DEBUG_CHANNEL = debugChannel
        self.stableQueue = []
        self.stableXLQueue = []
        self.dalleQueue = []
        self.vsQueue = []
        self.rbgQueue = []
        self.barkQueue = []
        self.smQueue = []
        self.saQueue = []
        self.vgQueue = []
        self.ghibliQueue = []
        self.fluxQueue = []

    async def checkChannel(self, c: commands.Context) -> None:
        if c.channel == self.BOT_CHANNEL:
            return True
        else:
            await c.reply(
                "Use bot commands in the bot channel!", ephemeral=True, delete_after=10
            )
            try:
                await c.message.delete()
            except Exception as e:
                print(e)
            return False

    @commands.hybrid_command(
        name="sd",
        description="Stable Diffusion - Old jank Stable Diffusion, guaranteed a laugh.",
    )
    async def StableDiff(
        self, ctx: commands.Context, prompt: str, negative: str = None
    ) -> None:
        if not await self.checkChannel(ctx):
            return

        queueSha = getSha256(prompt)
        self.stableQueue.append(queueSha)

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the stable diff command\n\n{prompt[:1500]}"
        )
        print(f"{curTime()}  -  {ctx.author} used the stable diff command")

        storedMsg: discord.Message = None
        if len(self.stableQueue) > 1:
            storedMsg = await ctx.reply(
                f"in queue {len(self.stableQueue) - 1}", ephemeral=True
            )
        else:
            storedMsg = await ctx.reply("Generating", ephemeral=True)

        while self.stableQueue[0] != queueSha:
            await sleep(1)

        try:
            out = await stableDiff(prompt, negative)
        except Exception as e:
            self.stableQueue.pop(0)
            await ctx.reply(f"stable diff: {e}")
            await storedMsg.delete()
            return

        async with ctx.typing():
            self.stableQueue.pop(0)
            files: list[discord.File] = []
            for file in out:
                with open(file, "rb") as f:
                    files.append(discord.File(f, filename=f"{getSha256(f)}.png"))
            await ctx.reply(f"# Stable Diff: {prompt}", files=files)
            for f in out:
                remove(f)

        await storedMsg.delete()

    @commands.hybrid_command(
        name="sdx",
        description="Stable Diffusion XL - Beefier version of Stable Diffusion",
    )
    async def StableDiffXL(
        self, ctx: commands.Context, prompt: str, negative: str = None
    ) -> None:
        if not await self.checkChannel(ctx):
            return

        queueSha = getSha256(prompt)
        self.stableXLQueue.append(queueSha)

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the stable XL command\n\n{prompt[:1500]}"
        )
        print(f"{curTime()}  -  {ctx.author} used the stable XL command")

        storedMsg: discord.Message = None
        if len(self.stableXLQueue) > 1:
            storedMsg = await ctx.reply(
                f"in queue {len(self.stableXLQueue) - 1}", ephemeral=True
            )
        else:
            storedMsg = await ctx.reply("Generating", ephemeral=True)

        while self.stableXLQueue[0] != queueSha:
            await sleep(1)

        try:
            out = await Stable_XL(prompt, negative)
        except Exception as e:
            self.stableXLQueue.pop(0)
            await ctx.reply(f"stable XL: {e}")
            await storedMsg.delete()
            return

        async with ctx.typing():
            self.stableXLQueue.pop(0)
            files: list[discord.File] = []
            for file in out:
                with open(file, "rb") as f:
                    files.append(discord.File(f, filename=f"{getSha256(f)}.png"))
            await ctx.reply(f"# Stable XL: {prompt}", files=files)
            for f in out:
                remove(f)

        await storedMsg.delete()

    @commands.hybrid_command(
        name="dalle",
        description="Dalle - one of the very first image gens, very jank",
    )
    async def Dalle(self, ctx: commands.Context, prompt: str) -> None:
        if not await self.checkChannel(ctx):
            return

        queueSha = getSha256(prompt)
        self.dalleQueue.append(queueSha)

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the Dalle command\n\n{prompt[:1500]}"
        )
        print(f"{curTime()}  -  {ctx.author} used the Dalle command")

        storedMsg: discord.Message = None
        if len(self.dalleQueue) > 1:
            storedMsg = await ctx.reply(
                f"in queue {len(self.dalleQueue) - 1}", ephemeral=True
            )
        else:
            storedMsg = await ctx.reply("Generating", ephemeral=True)

        while self.dalleQueue[0] != queueSha:
            await sleep(1)

        try:
            out = await dalle(prompt)
        except Exception as e:
            self.dalleQueue.pop(0)
            await ctx.reply(f"dalle: {e}")
            await storedMsg.delete()
            return

        async with ctx.typing():
            self.dalleQueue.pop(0)
            files: list[discord.File] = []
            for file in out:
                with open(file, "rb") as f:
                    files.append(discord.File(f, filename=f"{getSha256(f)}.png"))
            await ctx.reply(f"# Dalle: {prompt}", files=files)
            for f in out:
                remove(f)

        await storedMsg.delete()

    @commands.hybrid_command(
        name="vs", description="Voice Synth - Make an AI say funny things"
    )
    async def VoiceSynth(self, ctx: commands.Context, prompt: str) -> None:
        if not await self.checkChannel(ctx):
            return

        queueSha = getSha256(prompt)
        self.vsQueue.append(queueSha)

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the voice synth command\n\n{prompt[:1500]}"
        )
        print(f"{curTime()}  -  {ctx.author} used the voice synth command")

        storedMsg: discord.Message = None
        if len(self.vsQueue) > 1:
            storedMsg = await ctx.reply(
                f"in queue {len(self.vsQueue) - 1}", ephemeral=True
            )
        else:
            storedMsg = await ctx.reply("Generating", ephemeral=True)

        while self.vsQueue[0] != queueSha:
            await sleep(1)

        try:
            out = await voiceSynthFunction(prompt)
        except Exception as e:
            self.vsQueue.pop(0)
            await ctx.reply(f"Voice Synth: {e}")
            await storedMsg.delete()
            return

        if len(prompt) > 1500:
            prompt = ""
        try:
            await storedMsg.delete()
            async with ctx.typing():
                with open(out, "rb") as f:
                    _name = path.basename(out)
                    file = discord.File(f, filename=_name)
                    await ctx.reply(f"# Voice Synth: {prompt}", file=file)
                remove(out)
                self.vsQueue.pop(0)
        except Exception as e:
            self.vsQueue.pop(0)
            remove(out)
            await ctx.reply(f"voice synth: {e}")
            return

    @commands.hybrid_command(
        name="bark", description="Bark Voice Synth - Make an AI say funny things"
    )
    async def BarkVoiceSynth(self, ctx: commands.Context, prompt: str) -> None:
        if not await self.checkChannel(ctx):
            return

        queueSha = getSha256(prompt)
        self.barkQueue.append(queueSha)

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the Bark voice synth command\n\n{prompt[:1500]}"
        )
        print(f"{curTime()}  -  {ctx.author} used the Bark voice synth command")

        storedMsg: discord.Message = None
        if len(self.barkQueue) > 1:
            storedMsg = await ctx.reply(
                f"in queue {len(self.barkQueue) - 1}", ephemeral=True
            )
        else:
            storedMsg = await ctx.reply("Generating", ephemeral=True)

        while self.barkQueue[0] != queueSha:
            await sleep(1)

        try:
            out, voice = await barkVoiceSynthFunc(prompt)
        except Exception as e:
            self.barkQueue.pop(0)
            await ctx.reply(f"Bark Voice Synth: {e}")
            await storedMsg.delete()
            return

        if len(prompt) > 1500:
            prompt = ""
        try:
            async with ctx.typing():
                await storedMsg.delete()
                with open(out, "rb") as f:
                    _name = path.basename(out)
                    file = discord.File(f, filename=_name)
                    await ctx.reply(f"# Bark Voice Synth: {prompt}\n{voice}", file=file)
                remove(out)
                self.barkQueue.pop(0)
        except Exception as e:
            self.barkQueue.pop(0)
            remove(out)
            await ctx.reply(f"Bark voice synth: {e}")
            return

    @commands.hybrid_command(
        name="rbg",
        description="Remove Background - Removes the background from an image",
    )
    async def remBg(
        self,
        ctx: commands.Context,
        image: discord.Attachment = None,
        imageurl: str = None,
    ):
        if not await self.checkChannel(ctx):
            return

        if not image and not imageurl:
            await ctx.reply(
                "Need an image.",
                ephemeral=True,
                delete_after=10,
            )
            return

        if image:
            img = image.url
        elif imageurl:
            img = imageurl

        if not img.startswith("http"):
            await ctx.reply(
                "Not a valid URL.",
                ephemeral=True,
                delete_after=10,
            )
            return

        queueSha = getSha256(img)
        self.rbgQueue.append(queueSha)

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the Remove Background command"
        )
        print(f"{curTime()}  -  {ctx.author} used the Remove Background command")

        storedMsg: discord.Message = None
        if len(self.rbgQueue) > 1:
            storedMsg = await ctx.reply(
                f"in queue {len(self.rbgQueue) - 1}", ephemeral=True
            )
        else:
            storedMsg = await ctx.reply("Working", ephemeral=True)

        while self.rbgQueue[0] != queueSha:
            await sleep(1)

        try:
            out = await RemoveBackGroundFunction(img)
        except Exception as e:
            self.rbgQueue.pop(0)
            await ctx.reply(f"rbg: {e}")
            await storedMsg.delete()
            return

        async with ctx.typing():
            self.rbgQueue.pop(0)
            with open(out, "rb") as f:
                file = discord.File(f, filename=f"{getSha256(f)}.png")
            await ctx.reply("# Remove Background: ", file=file)
            remove(out)

        await storedMsg.delete()

    @commands.hybrid_command(
        name="bp",
        description="Bond Price (OSRS) - Get the current price for a bond on Old School RuneScape",
    )
    async def bondprice(self, ctx: commands.Context):
        if not await self.checkChannel(ctx):
            return

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the Bond Price (OSRS) command"
        )
        print(f"{curTime()}  -  {ctx.author} used the Bond Price (OSRS) command")

        await ctx.reply("fetching", ephemeral=True, delete_after=10)

        try:
            sellPrice, buyPrice = await getBondPriceOSRS()
        except Exception as e:
            await ctx.reply(f"bond price: {e}")
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

    @commands.hybrid_command(
        name="tp",
        description="Token Price - Get the current token price for World of Warcraft.",
    )
    async def tokenprice(self, ctx: commands.Context):
        if not await self.checkChannel(ctx):
            return

        await ctx.reply("fetching", ephemeral=True, delete_after=10)

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the Token Price command"
        )
        print(f"{curTime()}  -  {ctx.author} used the Token Price command")

        try:
            tprice = await getWoWTokenPrice()
        except Exception as e:
            await ctx.reply(f"token price: {e}")
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

    @commands.hybrid_command(
        name="ghibli",
        description="Ghiblify - You should have seen this already.",
    )
    async def ghibliCommand(
        self,
        ctx: commands.Context,
        image: discord.Attachment = None,
        imageurl: str = None,
    ):
        if not await self.checkChannel(ctx):
            return

        if not image and not imageurl:
            await ctx.reply(
                "Need an image.",
                ephemeral=True,
                delete_after=10,
            )
            return

        if image:
            img = image.url
        elif imageurl:
            img = imageurl

        if not img.startswith("http"):
            await ctx.reply(
                "Not a valid URL.",
                ephemeral=True,
                delete_after=10,
            )
            return

        queueSha = getSha256(img)
        self.ghibliQueue.append(queueSha)

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the Ghiblify command"
        )
        print(f"{curTime()}  -  {ctx.author} used the Ghiblify command")

        storedMsg: discord.Message = None
        if len(self.ghibliQueue) > 1:
            storedMsg = await ctx.reply(
                f"in queue {len(self.ghibliQueue) - 1}", ephemeral=True
            )
        else:
            storedMsg = await ctx.reply("Working", ephemeral=True)

        while self.ghibliQueue[0] != queueSha:
            await sleep(1)

        try:
            out = await ghiblifyFunction(img)
        except Exception as e:
            self.ghibliQueue.pop(0)
            await ctx.reply(f"Ghiblify: {e}")
            await storedMsg.delete()
            return

        async with ctx.typing():
            self.ghibliQueue.pop(0)
            with open(out, "rb") as f:
                file = discord.File(f, filename=f"{getSha256(f)}.webp")
            await ctx.reply(f"# Ghiblify: \n{img}", file=file)
            remove(out)

        await storedMsg.delete()

    @commands.hybrid_command(
        name="vg", description="Video Gen - Make the AI Generate funny videos"
    )
    async def vgCommandd(self, ctx: commands.Context, prompt: str) -> None:
        if not await self.checkChannel(ctx):
            return

        queueSha = getSha256(prompt)
        self.vgQueue.append(queueSha)

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the video gen command\n\n{prompt[:1500]}"
        )
        print(f"{curTime()}  -  {ctx.author} used the video gen command")

        storedMsg: discord.Message = None
        if len(self.vgQueue) > 1:
            storedMsg = await ctx.reply(
                f"in queue {len(self.vgQueue) - 1}", ephemeral=True
            )
        else:
            storedMsg = await ctx.reply("Generating", ephemeral=True)

        while self.vgQueue[0] != queueSha:
            await sleep(1)

        try:
            out = await vgMasterFunction(prompt)
        except Exception as e:
            self.vgQueue.pop(0)
            await ctx.reply(f"video gen: {e}")
            await storedMsg.delete()
            return

        if len(prompt) > 1500:
            prompt = ""
        try:
            await storedMsg.delete()
            async with ctx.typing():
                with open(out, "rb") as f:
                    _name = path.basename(out)
                    file = discord.File(f, filename=_name)
                    await ctx.reply(f"# video gen: {prompt}", file=file)
                remove(out)
                self.vgQueue.pop(0)
        except Exception as e:
            self.vgQueue.pop(0)
            remove(out)
            await ctx.reply(f"video gen: {e}")
            return

    @commands.hybrid_command(
        name="flux", description="Flux Image Gen - the beefiest."
    )
    async def fluxCommand(self, ctx: commands.Context, prompt: str) -> None:
        if not await self.checkChannel(ctx):
            return

        queueSha = getSha256(prompt)
        self.fluxQueue.append(queueSha)

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the Flux command\n\n{prompt[:1500]}"
        )
        print(f"{curTime()}  -  {ctx.author} used the Flux command")

        storedMsg: discord.Message = None
        if len(self.fluxQueue) > 1:
            storedMsg = await ctx.reply(
                f"in queue {len(self.fluxQueue) - 1}", ephemeral=True
            )
        else:
            storedMsg = await ctx.reply("Generating", ephemeral=True)

        while self.fluxQueue[0] != queueSha:
            await sleep(1)

        try:
            out = await fluxMasterFunction(prompt)
        except Exception as e:
            self.fluxQueue.pop(0)
            await ctx.reply(f"Flux: {e}")
            await storedMsg.delete()
            return

        if len(prompt) > 1500:
            prompt = ""
        try:
            await storedMsg.delete()
            async with ctx.typing():
                with open(out, "rb") as f:
                    _name = path.basename(out)
                    file = discord.File(f, filename=_name)
                    await ctx.reply(f"# Flux: {prompt}", file=file)
                remove(out)
                self.fluxQueue.pop(0)
        except Exception as e:
            self.fluxQueue.pop(0)
            remove(out)
            await ctx.reply(f"Flux: {e}")
            return
