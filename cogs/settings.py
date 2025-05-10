import discord
from discord.ext import commands
from discord import app_commands
from googletrans import Translator
import json
import os

GUILD_ID = int(os.getenv("GUILD_ID"))

SETTINGS_FILE = "settings.json"

class SettingsManager:
    def __init__(self, filepath=SETTINGS_FILE):
        self.filepath = filepath
        self.settings = self.load()

    def load(self):
        if not os.path.exists(self.filepath):
            return {}
        with open(self.filepath, "r") as f:
            return json.load(f)

    def save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.settings, f, indent=4)

    def get_guild_settings(self, guild_id):
        return self.settings.get(str(guild_id), {})

    def update_guild_setting(self, guild_id, key, value):
        guild_id = str(guild_id)
        if guild_id not in self.settings:
            self.settings[guild_id] = {}
        self.settings[guild_id][key] = value
        self.save()


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()
        self.settings_manager = SettingsManager()

    def get_settings(self, guild_id):
        return self.settings_manager.get_guild_settings(guild_id)

    def update_setting(self, guild_id, key, value):
        self.settings_manager.update_guild_setting(guild_id, key, value)

    @app_commands.command(name='setprefix', description="Change the bot's command prefix.")
    async def set_prefix(self, interaction: discord.Interaction, new_prefix: str):
        self.update_setting(interaction.guild.id, 'prefix', new_prefix)
        embed = discord.Embed(
            title="Prefix Updated",
            description=f"The command prefix has been set to {new_prefix}.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='welcome', description="Manage welcome messages.")
    async def manage_welcome(self, interaction: discord.Interaction, option: str, value: str = None):
        guild_id = interaction.guild.id
        if option == "enable":
            self.update_setting(guild_id, 'welcome_enabled', True)
            embed = discord.Embed(
                title="Welcome Messages Enabled",
                description="Welcome messages have been enabled.",
                color=discord.Color.green()
            )
        elif option == "disable":
            self.update_setting(guild_id, 'welcome_enabled', False)
            embed = discord.Embed(
                title="Welcome Messages Disabled",
                description="Welcome messages have been disabled.",
                color=discord.Color.red()
            )
        elif option == "message" and value:
            self.update_setting(guild_id, 'welcome_message', value)
            embed = discord.Embed(
                title="Welcome Message Updated",
                description=f"Welcome message set to: {value}",
                color=discord.Color.green()
            )
        elif option == "channel" and value:
            self.update_setting(guild_id, 'welcome_channel', value)
            embed = discord.Embed(
                title="Welcome Channel Updated",
                description=f"Welcome messages will be sent to: {value}",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="Error",
                description="Invalid option or missing value.",
                color=discord.Color.red()
            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='customcommand', description="Manage custom commands.")
    async def manage_custom_command(self, interaction: discord.Interaction, action: str, trigger: str = None, response: str = None):
        guild_id = interaction.guild.id
        settings = self.get_settings(guild_id)
        custom_commands = settings.get("custom_commands", {})

        if action == "add" and trigger and response:
            custom_commands[trigger] = response
            self.update_setting(guild_id, "custom_commands", custom_commands)
            embed = discord.Embed(
                title="Custom Command Added",
                description=f"Trigger: {trigger}\nResponse: {response}",
                color=discord.Color.green()
            )
        elif action == "remove" and trigger:
            if trigger in custom_commands:
                del custom_commands[trigger]
                self.update_setting(guild_id, "custom_commands", custom_commands)
                embed = discord.Embed(
                    title="Custom Command Removed",
                    description=f"Trigger: {trigger} has been removed.",
                    color=discord.Color.green()
                )
            else:
                embed = discord.Embed(
                    title="Error",
                    description=f"Trigger: {trigger} does not exist.",
                    color=discord.Color.red()
                )
        else:
            embed = discord.Embed(
                title="Error",
                description="Invalid action or missing parameters.",
                color=discord.Color.red()
            )
        await interaction.response.send_message(embed=embed)

    async def cog_load(self):
        self.bot.tree.add_command(self.set_prefix, guild=discord.Object(id=GUILD_ID))
        self.bot.tree.add_command(self.manage_welcome, guild=discord.Object(id=GUILD_ID))
        self.bot.tree.add_command(self.manage_custom_command, guild=discord.Object(id=GUILD_ID))

async def setup(bot):
    await bot.add_cog(Settings(bot))
