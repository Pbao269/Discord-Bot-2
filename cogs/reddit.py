import discord
from discord.ext import commands
from discord import app_commands
from random import choice
import os
import asyncpraw as praw
from dotenv import load_dotenv

load_dotenv(".env")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready!")
        
    @app_commands.command(name="meme", description="Fetch memes from reddit")
    async def meme(self, interaction: discord.Interaction):
        subreddit = await self.reddit.subreddit("memes")
        posts_list = []
        async for post in subreddit.rising(limit=30): 
            
            if (not post.over_18) and (post.author is not None) and any(post.url.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif"]):
                author_name = post.author.name
                posts_list.append((post.url, author_name))
            if post.author is None:
                posts_list.append((post.url, "N/A"))
        if posts_list:
            random_post = choice(posts_list)
            meme_embed = discord.Embed (title="Random Meme", description="Fetches random meme from r/memes", color=discord.Color.random())
            meme_embed.set_author(name=f"Meme requested by {interaction.user.name}", icon_url=interaction.user.avatar)
            meme_embed.set_image(url=random_post[0])
            meme_embed.set_footer(text=f"Post created by {random_post[1]}.", icon_url=None)
            await interaction.response.send_message(embed=meme_embed)
        else:
            await interaction.response.send_message("Unable to fetch post, try again later.")
    def cog_unload(self):
        self.bot.loop.create_task(self.reddit.close())
async def setup(bot):
    await bot.add_cog(Reddit(bot))
    
