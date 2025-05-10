# cogs/Test.py
from discord.ext import commands
from discord import app_commands, Interaction
import discord
import os

GUILD_ID = int(os.getenv("GUILD_ID"))

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Ping the bot!")
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message("Pong!")

    async def cog_load(self):
        self.bot.tree.add_command(self.ping, guild=discord.Object(id=GUILD_ID))

async def setup(bot):
    await bot.add_cog(Test(bot))
