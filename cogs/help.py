import discord
from discord.ext import commands
import os 

GUILD_ID = int(os.getenv("GUILD_ID"))

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.tree.add_command(self.help_command, guild=discord.Object(id=GUILD_ID))

    @discord.app_commands.command(name='customhelp', description="Displays the list of commands and their descriptions.")
    async def help_command(self, interaction: discord.Interaction, cog_name: str = None):
        if cog_name:
            # If a specific cog is requested, show commands in that cog
            cog = self.bot.get_cog(cog_name)  # Capitalization should match exactly
            if cog:
                embed = discord.Embed(title=f"Commands in {cog_name} Cog", color=discord.Color.blue())
                for command in cog.walk_commands():
                    if isinstance(command, discord.app_commands.Command):
                        # Only show slash commands
                        embed.add_field(name=f'/{command.name}', value=command.description or "No description", inline=False)
            else:
                embed = discord.Embed(
                    title="Error",
                    description=f"The cog `{cog_name}` was not found.",
                    color=discord.Color.red()
                )
        else:
            # If no cog is specified, show commands for all cogs
            embed = discord.Embed(title="Bot Commands", color=discord.Color.blue())
            for cog_name, cog in self.bot.cogs.items():
                command_list = "\n".join([f'/{command.name}: {command.description or "No description"}' for command in cog.walk_commands() if isinstance(command, discord.app_commands.Command)])
                embed.add_field(name=cog_name, value=command_list if command_list else "No commands available", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
