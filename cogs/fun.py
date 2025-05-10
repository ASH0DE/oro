import os 
import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio

GUILD_ID = int(os.getenv("GUILD_ID"))

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.tree.add_command(self.hug, guild=discord.Object(id=GUILD_ID))
        self.bot.tree.add_command(self.magic_8ball, guild=discord.Object(id=GUILD_ID))
        self.bot.tree.add_command(self.rate, guild=discord.Object(id=GUILD_ID))
        self.bot.tree.add_command(self.percent, guild=discord.Object(id=GUILD_ID))
        self.bot.tree.add_command(self.choose, guild=discord.Object(id=GUILD_ID))
        self.bot.tree.add_command(self.roll, guild=discord.Object(id=GUILD_ID))
        self.bot.tree.add_command(self.reverse, guild=discord.Object(id=GUILD_ID))
        self.bot.tree.add_command(self.repeat, guild=discord.Object(id=GUILD_ID))
        self.bot.tree.add_command(self.compliment, guild=discord.Object(id=GUILD_ID))
        self.bot.tree.add_command(self.roast, guild=discord.Object(id=GUILD_ID))
        self.bot.tree.add_command(self.ship, guild=discord.Object(id=GUILD_ID))
        self.bot.tree.add_command(self.hacker, guild=discord.Object(id=GUILD_ID))

    @app_commands.command(name="hug", description="Send a virtual hug to someone.")
    async def hug(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            embed = discord.Embed(
                title="Hug Command",
                description="You need to mention someone to hug!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        if member == interaction.user:
            await interaction.response.send_message("You can't hug yourself... but here's a virtual hug anyway 🤗", ephemeral=True)
            return
        hugs = [
            f"{interaction.user.mention} gives {member.mention} a big warm hug! 🤗",
            f"{interaction.user.mention} hugs {member.mention} tightly! 🫂",
            f"{interaction.user.mention} sends a virtual hug to {member.mention}! ❤️"
        ]
        embed = discord.Embed(
            title="Hug Command",
            description=random.choice(hugs),
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="8ball", description="Ask the Magic 8-ball a question.")
    async def magic_8ball(self, interaction: discord.Interaction, question: str):
        responses = [
            "It is certain.", "It is decidedly so.", "Without a doubt.",
            "Yes – definitely.", "You may rely on it.", "As I see it, yes.",
            "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
            "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
            "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.",
            "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."
        ]
        embed = discord.Embed(
            title="Magic 8-Ball",
            description=f"🎱 Question: {question}\nAnswer: {random.choice(responses)}",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="rate", description="Bot rates a thing from 1 to 10.")
    async def rate(self, interaction: discord.Interaction, thing: str):
        rating = random.randint(1, 10)
        embed = discord.Embed(
            title="Rating",
            description=f"I rate **{thing}** a **{rating}/10**!",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="percent", description="Random percent (e.g., '💖 78% awesome!').")
    async def percent(self, interaction: discord.Interaction, member: discord.Member):
        percentage = random.randint(0, 100)
        embed = discord.Embed(
            title="Random Percent",
            description=f"{member.mention} is **{percentage}% awesome!** 💖",
            color=discord.Color.purple()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="choose", description="Randomly chooses from given options.")
    async def choose(self, interaction: discord.Interaction, options: str):
        choices = [opt.strip() for opt in options.split(",") if opt.strip()]
        if len(choices) < 2:
            embed = discord.Embed(
                title="Choose Command",
                description="You need to provide at least two options!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        choice = random.choice(choices)
        embed = discord.Embed(
            title="Choose Command",
            description=f"I choose: **{choice}**!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="roll", description="Rolls a die (default 6 sides).")
    async def roll(self, interaction: discord.Interaction, sides: int = 6):
        result = random.randint(1, sides)
        embed = discord.Embed(
            title="Roll Command",
            description=f"🎲 You rolled a **{result}** on a {sides}-sided die!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="reverse", description="Reverses the text.")
    async def reverse(self, interaction: discord.Interaction, text: str):
        reversed_text = text[::-1]
        embed = discord.Embed(
            title="Reverse Command",
            description=f"🔄 {reversed_text}",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="repeat", description="Bot repeats the text.")
    async def repeat(self, interaction: discord.Interaction, text: str):
        embed = discord.Embed(
            title="Repeat Command",
            description=f"🔁 {text}",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="compliment", description="Sends a wholesome compliment.")
    async def compliment(self, interaction: discord.Interaction, member: discord.Member):
        compliments = [
            "You're amazing!", "You're a star!", "You're so talented!",
            "You're a wonderful person!", "You're an inspiration!"
        ]
        embed = discord.Embed(
            title="Compliment",
            description=f"{member.mention}, {random.choice(compliments)} 💖",
            color=discord.Color.pink()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="roast", description="Roasts a user.")
    async def roast(self, interaction: discord.Interaction, member: discord.Member):
        if member == interaction.user:
            await interaction.response.send_message("You can't roast yourself... or can you?", ephemeral=True)
            return
        roasts = [
            "You're like a cloud. When you disappear, it's a beautiful day.",
            "You're proof that even the worst people can survive anything.",
            "You're like a software bug that can't be fixed."
        ]
        embed = discord.Embed(
            title="Roast",
            description=f"{member.mention}, {random.choice(roasts)} 🔥",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ship", description="Ships two users together!")
    @app_commands.describe(user1="First user", user2="Second user")
    async def ship(self, interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
        percent = random.randint(0, 100)
        bar = "█" * (percent // 10) + "░" * (10 - (percent // 10))
        embed = discord.Embed(
            title="💘 Shipping Results!",
            description=f"{user1.mention} ❤️ {user2.mention}\nLove Meter: `{bar}` **{percent}%**",
            color=discord.Color.magenta()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="hacker", description="Pretends to hack a user.")
    async def hacker(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(f"🧠 Hacking {member.mention}...")
        await asyncio.sleep(1)
        messages = [
            "🔍 Searching files...",
            "📁 Downloading data...",
            "💾 Installing virus...",
            "💣 BOOM! Hack complete!"
        ]
        for msg in messages:
            await asyncio.sleep(1)
            await interaction.followup.send(msg)

async def setup(bot):
    await bot.add_cog(Fun(bot))
