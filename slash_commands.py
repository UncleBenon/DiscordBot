import discord
from discord.ext import commands

BOT: commands.Bot = None
DEBUG_CHANNEL: discord.GuildChannel = None
BOT_CHANNEL: discord.GuildChannel = None

@BOT.tree.command(name="Test Slash Command")
async def testSlashCommand(interaction: discord.Interaction):
    await interaction.response.send_message(f"ayyyy {interaction.user.mention}!")
