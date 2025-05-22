import random
import discord
from chat_commands import ChatCommands
from discord.ext import commands
from core.misc import curTime

INTENTS = discord.Intents.all()
BOT = commands.Bot(command_prefix="!", intents=INTENTS)

@BOT.listen()
async def on_ready() -> None:
    name = str(BOT.user).split("#")[0]
    print(f'{curTime()}', f'{name} Online',f'Ping: {int(BOT.latency * 1000)}ms', sep="  -  ")
    BOT_CHANNEL = BOT.get_channel(1048600881593061416)
    DEBUG_CHANNEL = BOT.get_channel(1048564475659288666)
    await BOT.add_cog(ChatCommands(BOT, BOT_CHANNEL, DEBUG_CHANNEL))
    with open("inc/vidya.txt") as f:
        vidya = f.readlines()
        await BOT.change_presence(status=discord.Status.dnd,activity=discord.Game(random.choice(vidya)))
    await DEBUG_CHANNEL.send("----------------------------------------------------------------------")
    await DEBUG_CHANNEL.send(f'{name} Online!\t-\tPing: {int(BOT.latency * 1000)}ms')
    ay = await BOT.tree.sync()
    print(len(ay))

@BOT.listen()
async def on_resumed() -> None:
    with open("inc/vidya.txt") as f:
        vidya = f.readlines()
        await BOT.change_presence(status=discord.Status.dnd,activity=discord.Game(random.choice(vidya)))

if __name__ == "__main__":
    with open("inc/token.txt") as f:
        T = f.readline().strip()

    BOT.run(T)
