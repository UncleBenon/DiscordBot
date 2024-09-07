from discord.ext import commands
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
    await DEBUG_CHANNEL.send(f'{name} Online!\t-\tPing: {int(bot.latency * 1000)}ms')
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

if __name__ == "__main__":
    with open("inc/token.txt") as f:
        T = f.readline().strip()
    bot.run(T)
