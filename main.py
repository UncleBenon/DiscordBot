import random
import discord
import chat_commands
import slash_commands
from discord.ext import commands
from core.misc import curTime

INTENTS = discord.intents.all()
BOT = commands.Bot(command_prefix="!", intents=INTENTS)
chat_commands.BOT = BOT
slash_commands.BOT = BOT

DEBUG_CHANNEL = None
BOT_CHANNEL = None

@BOT.listen()
async def on_ready() -> None:
    global DEBUG_CHANNEL, BOT_CHANNEL
    name = str(BOT.user).split("#")[0]
    print(f'{curTime()}', f'{name} Online',f'Ping: {int(BOT.latency * 1000)}ms', sep="  -  ")
    DEBUG_CHANNEL = BOT.get_channel(1048564475659288666)
    BOT_CHANNEL = BOT.get_channel(1048600881593061416)
    chat_commands.DEBUG_CHANNEL = DEBUG_CHANNEL
    chat_commands.BOT_CHANNEL = BOT_CHANNEL
    slash_commands.DEBUG_CHANNEL = DEBUG_CHANNEL
    slash_commands.BOT_CHANNEL = BOT_CHANNEL
    try:
        sync = await BOT.tree.sync()
        print(f"Synced {len(sync)} command(s)")
    except Exception as e:
        print(e)
    with open("inc/vidya.txt") as f:
        vidya = f.readlines()
        await BOT.change_presence(activity=discord.Game(random.choice(vidya)))
    await DEBUG_CHANNEL.send("----------------------------------------------------------------------")
    await DEBUG_CHANNEL.send(f'{name} Online!\t-\tPing: {int(BOT.latency * 1000)}ms')

@BOT.listen()
async def on_resumed() -> None:
    with open("inc/vidya.txt") as f:
        vidya = f.readlines()
        await BOT.change_presence(activity=discord.Game(random.choice(vidya)))

if __name__ == "__main__":
    with open("inc/token.txt") as f:
        T = f.readline().strip()

    BOT.run(T)
