import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os

GUILD_ID = int(os.getenv("GUILD_ID"))

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {}  # store warnings per user

    async def cog_load(self):
        guild = discord.Object(id=GUILD_ID)
        self.bot.tree.add_command(self.kick, guild=guild)
        self.bot.tree.add_command(self.ban, guild=guild)
        self.bot.tree.add_command(self.unban, guild=guild)
        self.bot.tree.add_command(self.mute, guild=guild)
        self.bot.tree.add_command(self.tempban, guild=guild)
        self.bot.tree.add_command(self.warn, guild=guild)
        self.bot.tree.add_command(self.warnings_cmd, guild=guild)
        self.bot.tree.add_command(self.clear, guild=guild)
        self.bot.tree.add_command(self.lock, guild=guild)
        self.bot.tree.add_command(self.unlock, guild=guild)
        self.bot.tree.add_command(self.serverinfo, guild=guild)
        self.bot.tree.add_command(self.userinfo, guild=guild)
        self.bot.tree.add_command(self.avatar, guild=guild)

    @app_commands.command(name="kick", description="Kicks a member from the server.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await member.kick(reason=reason)
        embed = discord.Embed(title="Member Kicked", description=f"{member.mention} has been kicked.", color=discord.Color.red())
        embed.add_field(name="Reason", value=reason or "No reason provided", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ban", description="Bans a member from the server.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await member.ban(reason=reason)
        embed = discord.Embed(title="Member Banned", description=f"{member.mention} has been banned.", color=discord.Color.red())
        embed.add_field(name="Reason", value=reason or "No reason provided", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unban", description="Unbans a member from the server.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, member_name: str):
        banned_users = await interaction.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if user.name == member_name:
                await interaction.guild.unban(user)
                embed = discord.Embed(title="Member Unbanned", description=f"{user.mention} has been unbanned.", color=discord.Color.green())
                await interaction.response.send_message(embed=embed)
                return
        await interaction.response.send_message(f"User {member_name} not found in banned list.", ephemeral=True)

    @app_commands.command(name="mute", description="Mutes a member for a specified duration.")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = None):
        mute_role = discord.utils.get(interaction.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await interaction.guild.create_role(name="Muted")
            for channel in interaction.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False)

        await member.add_roles(mute_role, reason=reason)
        embed = discord.Embed(title="Member Muted", description=f"{member.mention} has been muted for {duration} seconds.", color=discord.Color.orange())
        embed.add_field(name="Reason", value=reason or "No reason provided", inline=False)
        await interaction.response.send_message(embed=embed)

        await asyncio.sleep(duration)
        await member.remove_roles(mute_role)
        await interaction.followup.send(embed=discord.Embed(
            title="Member Unmuted",
            description=f"{member.mention} has been unmuted.",
            color=discord.Color.green()
        ))

    @app_commands.command(name="tempban", description="Temporarily bans a member for a specified duration.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def tempban(self, interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = None):
        await member.ban(reason=reason)
        embed = discord.Embed(title="Member Temporarily Banned", description=f"{member.mention} has been temporarily banned for {duration} seconds.", color=discord.Color.red())
        embed.add_field(name="Reason", value=reason or "No reason provided", inline=False)
        await interaction.response.send_message(embed=embed)

        await asyncio.sleep(duration)
        await interaction.guild.unban(member)
        await interaction.followup.send(embed=discord.Embed(
            title="Member Unbanned",
            description=f"{member.mention} has been unbanned after temporary ban.",
            color=discord.Color.green()
        ))

    @app_commands.command(name="warn", description="Warns a user.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if member.id not in self.warnings:
            self.warnings[member.id] = []
        self.warnings[member.id].append(reason)
        embed = discord.Embed(title="User Warned", description=f"{member.mention} has been warned.", color=discord.Color.orange())
        embed.add_field(name="Reason", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="warnings", description="View warnings for a user.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warnings_cmd(self, interaction: discord.Interaction, member: discord.Member):
        warns = self.warnings.get(member.id, [])
        if not warns:
            await interaction.response.send_message(f"{member.mention} has no warnings.")
        else:
            embed = discord.Embed(title="Warnings", color=discord.Color.red())
            for i, w in enumerate(warns, 1):
                embed.add_field(name=f"Warning {i}", value=w, inline=False)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="clear", description="Clears a number of messages.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        try:
            await interaction.response.send_message(f"🧹 Cleared {amount} messages.", ephemeral=True)
            await interaction.channel.purge(limit=amount)
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)

    @app_commands.command(name="lock", description="Locks the current channel.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction):
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = False
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message("🔒 Channel locked.")

    @app_commands.command(name="unlock", description="Unlocks the current channel.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction):
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = True
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message("🔓 Channel unlocked.")

    @app_commands.command(name="serverinfo", description="Displays information about the server.")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(title="Server Information", color=discord.Color.blue())
        embed.add_field(name="Server Name", value=guild.name, inline=False)
        embed.add_field(name="Server ID", value=guild.id, inline=False)
        embed.add_field(name="Owner", value=guild.owner, inline=False)
        embed.add_field(name="Member Count", value=guild.member_count, inline=False)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="userinfo", description="Displays information about a user.")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        embed = discord.Embed(title="User Information", color=discord.Color.green())
        embed.add_field(name="Username", value=str(member), inline=False)
        embed.add_field(name="User ID", value=member.id, inline=False)
        embed.add_field(name="Joined At", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Account Created At", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="avatar", description="Displays the avatar of a user.")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        embed = discord.Embed(title=f"{member}'s Avatar", color=discord.Color.purple())
        embed.set_image(url=member.avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Admin(bot))
