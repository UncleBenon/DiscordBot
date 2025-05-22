import discord
from discord.ext import commands

class SlashCommands(commands.Cog):
    def __init__(self, bot,  botChan, botDebug):
        self.bot = bot
        self.BOT_CHANNEL = botChan
        self.DEBUG_CHANNEL = botDebug

    @commands.tree
    async def testSlashCommand(interaction: discord.Interaction):
        await interaction.response.send_message(f"ayyyy {interaction.user.mention}!")
