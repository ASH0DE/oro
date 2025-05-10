import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import asyncio

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))  # Make sure your .env has a valid GUILD_ID

# Intents setup
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

# Bot setup
bot = commands.Bot(command_prefix="`", intents=intents)

# Sync slash commands and load cogs
async def setup_bot():
    # Set bot status
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="currently in development"
    ))

    # Load cogs from the "cogs" folder
    cog_count = 0
    cogs_folder = './cogs'
    if not os.path.exists(cogs_folder):
        print(f"Folder '{cogs_folder}' does not exist.")
        return

    for filename in os.listdir(cogs_folder):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                cog_count += 1
            except Exception as e:
                print(f"Failed to load cog {filename}: {e}")
    print(f"{cog_count} cog(s) loaded successfully.")

    # Sync slash commands to a specific guild (fast)
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"Synced {len(synced)} command(s) to guild {GUILD_ID}.")
    except discord.HTTPException as e:
        print(f"Failed to sync commands: {e}")

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await setup_bot()

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)
