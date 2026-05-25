from os import path, remove
from core.misc import curTime, clamp
from core.sha import getSha256
from core.voice import voiceSynthFunction
from core.WoW import getWoWTokenPrice
from core.OSRS import getBondPriceOSRS
from core.removebg import RemoveBackGroundFunction
from core.ghiblify import ghiblifyFunction
from core.dream import dreamMasterFunc
from core.twitterDownload import downloadTwitterVideoFunction
from core.voice2 import voiceSynth2Function, VOICES
from asyncio import sleep
from discord.ext import commands
from discord import app_commands
import discord


class ChatCommands(commands.Cog):
    def __init__(self, bot, botChannel, debugChannel):
        self.bot = bot
        self.BOT_CHANNEL = botChannel
        self.DEBUG_CHANNEL = debugChannel
        self.vsQueue = []
        self.rbgQueue = []
        self.smQueue = []
        self.saQueue = []
        self.ghibliQueue = []
        self.dreamQueue = []
        self.twitVidQueue = []
        self.vs2Queue = []

    async def checkChannel(self, c: commands.Context) -> None:
        if c.channel == self.BOT_CHANNEL:
            return True
        else:
            await c.send(
                "Use bot commands in the bot channel!", ephemeral=True, delete_after=60
            )
            try:
                await c.message.delete()
            except Exception as e:
                print(e)
            return False

    @commands.hybrid_command(
        name="vs", description="Voice Synth - Make an AI say funny things"
    )
    async def VoiceSynth(self, ctx: commands.Context, prompt: str) -> None:
        if not ctx:
            return

        if not await self.checkChannel(ctx):
            return

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the voice synth command\n\n{prompt[:1500]}"
        )
        print(f"{curTime()}  -  {ctx.author} used the voice synth command")

        if len(self.vsQueue) > 0:
            stored = await ctx.send(f"in queue {len(self.vsQueue)}", ephemeral=True)
        else:
            stored = await ctx.send("Generating", ephemeral=True)

        queueSha = getSha256(prompt)
        self.vsQueue.append(queueSha)

        while self.vsQueue[0] != queueSha:
            await sleep(1)

        try:
            out = await voiceSynthFunction(prompt)
        except Exception as e:
            self.vsQueue.pop(0)
            await ctx.send(f"Voice Synth: {e}")
            await stored.delete()
            return

        if len(prompt) > 1500:
            prompt = ""
        try:
            async with ctx.typing():
                with open(out, "rb") as f:
                    _name = path.basename(out)
                    file = discord.File(f, filename=_name)
                    await ctx.send(
                        f"# Voice Synth: {prompt}\n{ctx.author.mention}", file=file
                    )
                await stored.delete()
                remove(out)
                self.vsQueue.pop(0)
        except Exception as e:
            self.vsQueue.pop(0)
            remove(out)
            await stored.delete()
            await ctx.send(f"voice synth: {e}")
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
        if not ctx:
            return

        if not await self.checkChannel(ctx):
            return

        if not image and not imageurl:
            await ctx.send(
                "Need an image.",
                ephemeral=True,
                delete_after=60,
            )
            return

        if image:
            img = image.url
        elif imageurl:
            img = imageurl

        if not img.startswith("http"):
            await ctx.send(
                "Not a valid URL.",
                ephemeral=True,
                delete_after=60,
            )
            return

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the Remove Background command"
        )
        print(f"{curTime()}  -  {ctx.author} used the Remove Background command")

        if len(self.rbgQueue) > 0:
            stored = await ctx.send(f"in queue {len(self.rbgQueue)}", ephemeral=True)
        else:
            stored = await ctx.send("Working", ephemeral=True)

        queueSha = getSha256(img)
        self.rbgQueue.append(queueSha)

        while self.rbgQueue[0] != queueSha:
            await sleep(1)

        try:
            out = await RemoveBackGroundFunction(img)
        except Exception as e:
            self.rbgQueue.pop(0)
            await ctx.send(f"rbg: {e}")
            await stored.delete()
            return

        async with ctx.typing():
            self.rbgQueue.pop(0)
            with open(out, "rb") as f:
                file = discord.File(f, filename=f"{getSha256(f)}.png")
            await ctx.send(f"# Remove Background: \n{ctx.author.mention}", file=file)
            await stored.delete()
            remove(out)

    @commands.hybrid_command(
        name="bp",
        description="Bond Price (OSRS) - Get the current price for a bond on Old School RuneScape",
    )
    async def bondprice(self, ctx: commands.Context):
        if not ctx:
            return

        if not await self.checkChannel(ctx):
            return

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the Bond Price (OSRS) command"
        )
        print(f"{curTime()}  -  {ctx.author} used the Bond Price (OSRS) command")

        stored = await ctx.send("fetching", ephemeral=True)

        try:
            sellPrice, buyPrice = await getBondPriceOSRS()
        except Exception as e:
            await ctx.send(f"bond price: {e}")
            await stored.delete()
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
            await ctx.send(embed=embed)
            await stored.delete()

    @commands.hybrid_command(
        name="tp",
        description="Token Price - Get the current token price for World of Warcraft.",
    )
    async def tokenprice(self, ctx: commands.Context):
        if not ctx:
            return

        if not await self.checkChannel(ctx):
            return

        stored = await ctx.send("fetching", ephemeral=True)

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the Token Price command"
        )
        print(f"{curTime()}  -  {ctx.author} used the Token Price command")

        try:
            tprice = await getWoWTokenPrice()
        except Exception as e:
            await ctx.send(f"token price: {e}")
            await stored.delete()
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
            await ctx.send(embed=embed)
            await stored.delete()

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
        if not ctx:
            return

        if not await self.checkChannel(ctx):
            return

        if not image and not imageurl:
            await ctx.send(
                "Need an image.",
                ephemeral=True,
                delete_after=60,
            )
            return

        if image:
            img = image.url
        elif imageurl:
            img = imageurl

        if not img.startswith("http"):
            await ctx.send(
                "Not a valid URL.",
                ephemeral=True,
                delete_after=60,
            )
            return

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the Ghiblify command"
        )
        print(f"{curTime()}  -  {ctx.author} used the Ghiblify command")

        if len(self.ghibliQueue) > 0:
            stored = await ctx.send(f"in queue {len(self.ghibliQueue)}", ephemeral=True)
        else:
            stored = await ctx.send("Working", ephemeral=True)

        queueSha = getSha256(img)
        self.ghibliQueue.append(queueSha)

        while self.ghibliQueue[0] != queueSha:
            await sleep(1)

        try:
            out = await ghiblifyFunction(img)
        except Exception as e:
            self.ghibliQueue.pop(0)
            await ctx.send(f"Ghiblify: {e}")
            await stored.delete()
            return

        async with ctx.typing():
            self.ghibliQueue.pop(0)
            with open(out, "rb") as f:
                file = discord.File(f, filename=f"{getSha256(f)}.webp")
            await ctx.send(f"# Ghiblify: \n{img}\n{ctx.author.mention}", file=file)
            await stored.delete()
            remove(out)

    @commands.hybrid_command(
        name="dream", description="Dream Image Gen - like flux, pretty beefy.."
    )
    @app_commands.choices(
        size=[
            app_commands.Choice(name="1:1", value="0"),
            app_commands.Choice(name="3:4", value="1"),
            app_commands.Choice(name="4:3", value="2"),
            app_commands.Choice(name="9:16", value="3"),
            app_commands.Choice(name="16:9", value="4"),
        ]
    )
    async def dreamCommand(
        self, ctx: commands.Context, prompt: str, size: str = "2"
    ) -> None:
        if not ctx:
            return

        if not await self.checkChannel(ctx):
            return

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the Dream command\nSize: {size}\n\n{prompt[:1500]}"
        )
        print(f"{curTime()}  -  {ctx.author} used the Dream command")

        if len(self.dreamQueue) > 0:
            stored = await ctx.send(f"in queue {len(self.dreamQueue)}", ephemeral=True)
        else:
            stored = await ctx.send("Generating", ephemeral=True)

        queueSha = getSha256(prompt)
        self.dreamQueue.append(queueSha)

        while self.dreamQueue[0] != queueSha:
            await sleep(1)

        try:
            out = await dreamMasterFunc(prompt, int(size))
        except Exception as e:
            self.dreamQueue.pop(0)
            await ctx.send(f"Dream: {e}")
            await stored.delete()
            return

        if len(prompt) > 1500:
            prompt = ""
        try:
            async with ctx.typing():
                with open(out, "rb") as f:
                    _name = path.basename(out)
                    file = discord.File(f, filename=_name)
                    await ctx.send(
                        f"# Dream: {prompt}\n{ctx.author.mention}", file=file
                    )
                await stored.delete()
                remove(out)
                self.dreamQueue.pop(0)
        except Exception as e:
            self.dreamQueue.pop(0)
            remove(out)
            await ctx.send(f"Dream: {e}")
            await stored.delete()
            return

    @commands.hybrid_command(
        name="twitvid",
        description="Downloads a video of twitter, if i did this correctly.",
    )
    async def twitvidcommand(self, ctx: commands.Context, url: str):
        if not ctx:
            return

        if not await self.checkChannel(ctx):
            return

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the TwitVid command\n<{url}>"
        )
        print(f"{curTime()}  -  {ctx.author} used the TwitVid command")

        if len(self.twitVidQueue) > 0:
            stored = await ctx.send(
                f"in queue {len(self.twitVidQueue)}", ephemeral=True
            )
        else:
            stored = await ctx.send("Fetching", ephemeral=True)

        queueSha = getSha256(url)
        self.twitVidQueue.append(queueSha)

        while self.twitVidQueue[0] != queueSha:
            await sleep(1)

        try:
            out = await downloadTwitterVideoFunction(url)
        except Exception as e:
            self.twitVidQueue.pop(0)
            await ctx.send(f"TwitVid: {e}")
            await stored.delete()
            return

        try:
            async with ctx.typing():
                with open(out, "rb") as f:
                    _name = path.basename(out)
                    file = discord.File(f, filename=_name)
                    await ctx.send(
                        f"# TwitVid: <{url}>\n{ctx.author.mention}", file=file
                    )
                await stored.delete()
                remove(out)
                self.twitVidQueue.pop(0)
        except Exception as e:
            self.twitVidQueue.pop(0)
            remove(out)
            await ctx.send(f"TwitVid: {e}")
            await stored.delete()
            return

    @commands.hybrid_command(
        name="vs2", description="Voice Synth 2 - Make an AI say funny things"
    )
    @app_commands.choices(
        voice=[
            app_commands.Choice(name="alba", value="0"),
            app_commands.Choice(name="marius", value="1"),
            app_commands.Choice(name="javert", value="2"),
            app_commands.Choice(name="jean", value="3"),
            app_commands.Choice(name="fantine", value="4"),
            app_commands.Choice(name="cosette", value="5"),
            app_commands.Choice(name="eponine", value="6"),
            app_commands.Choice(name="azelma", value="7"),
        ]
    )
    async def VoiceSynth2(
        self, ctx: commands.Context, prompt: str, voice: str = "0", temp: float = 1.5
    ) -> None:
        if not ctx:
            return

        if not await self.checkChannel(ctx):
            return

        temp = clamp(temp, 0.0, 2.0)

        await self.DEBUG_CHANNEL.send(
            f"{curTime()}  -  {ctx.author} used the voice synth 2 command\nVoice: {VOICES[int(voice)]}\nTemp: {temp}\n\n{prompt[:1000]}"
        )
        print(f"{curTime()}  -  {ctx.author} used the voice synth 2 command")

        if len(self.vs2Queue) > 0:
            stored = await ctx.send(f"in queue {len(self.vs2Queue)}", ephemeral=True)
        else:
            stored = await ctx.send("Generating", ephemeral=True)

        queueSha = getSha256(prompt)
        self.vs2Queue.append(queueSha)

        while self.vs2Queue[0] != queueSha:
            await sleep(1)

        try:
            out = await voiceSynth2Function(prompt, int(voice), temp)
        except Exception as e:
            self.vs2Queue.pop(0)
            await ctx.send(f"Voice Synth 2: {str(e)[:1500]}")
            await stored.delete()
            return

        if len(prompt) > 1500:
            prompt = ""
        try:
            async with ctx.typing():
                with open(out, "rb") as f:
                    _name = path.basename(out)
                    file = discord.File(f, filename=_name)
                    await ctx.send(
                        f"# Voice Synth 2: {prompt}\nVoice: {VOICES[int(voice)].capitalize()}, Temp: {temp}\n\n{ctx.author.mention}",
                        file=file,
                    )
                await stored.delete()
                remove(out)
                self.vs2Queue.pop(0)
        except Exception as e:
            self.vs2Queue.pop(0)
            remove(out)
            await stored.delete()
            await ctx.send(f"voice synth 2: {e}")
            return
