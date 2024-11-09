import discord
from discord.ext import commands
from discord import app_commands

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
       print("Moderation commands ready!")    
       
    @app_commands.command(name="clear", description="Delete a specified amount of message from the channel.")
    @app_commands.checks.has_permissions(manage_messages = True)
    async def delete_messages(self, interaction: discord.Interaction, amount: int):
        if amount < 1:
            await interaction.channel.send(f"{interaction.user.mention}, please specify a value greater than one.")
            return
        await interaction.response.send_message(f"{amount} messages are being deleted, please wait...", ephemeral=True)
        deleted_messages = await interaction.channel.purge(limit=amount)
        await interaction.channel.send(f"{interaction.user.mention} has deleted {len(deleted_messages)} message(s).")
    
    @app_commands.command(name="kick", description="Kick a specific member.")
    @app_commands.checks.has_permissions(kick_members = True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member):
       await interaction.guild.kick(member)
       await interaction.response.send_message(f"Success! you have kicked {member.mention}", ephemeral=True)
    
    @app_commands.command(name="ban", description="Ban a specific member.")
    @app_commands.checks.has_permissions(ban_members = True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member):
       await interaction.guild.ban(member)
       await interaction.response.send_message(f"Success! you have banned {member.mention}", ephemeral=True)
    
    @app_commands.command(name="unban", description="Kick a specific member.")
    @app_commands.checks.has_permissions(ban_members = True)
    async def unban(self, interaction: discord.Interaction, user_id: str):
        user = await self.bot.fetch_user(user_id)
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"Success! you have unbanned {user.name}", ephemeral=True)
    
async def setup(bot):
    await bot.add_cog(Mod(bot))