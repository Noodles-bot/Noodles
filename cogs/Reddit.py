import aiohttp
import praw
import discord
import random

from discord.ext import commands

from utils.secret import *


class Reddit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def q(self, subreddit):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://www.reddit.com/r/{subreddit}/about/modqueue/.json') as r:
                retrieved = await r.json()  # returns dict
        return retrieved

    @commands.command()
    async def reddithot(self, ctx, subreddit=None):
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             username=username,
                             password=password,
                             user_agent=user_agent)
        if subreddit is None:
            for submission in reddit.front.hot(limit=5):
                if not submission.stickied:
                    await ctx.send(f'<{submission.url}>')
        else:
            for submission in reddit.subreddit(subreddit).hot(limit=5):
                if not submission.stickied:
                    await ctx.send(f'<{submission.url}>')

    @commands.command()
    async def membercount(self, ctx, subreddit):
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             username=username,
                             password=password,
                             user_agent=user_agent)
        await ctx.send(reddit.subreddit(subreddit).subscribers)

    @commands.command()
    async def meme(self, ctx):
        meme = []
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             username=username,
                             password=password,
                             user_agent=user_agent)
        for submission in reddit.subreddit('DankMemes+Memes+MemeEconomy').top('week', limit=50):
            if not submission.stickied:
                meme.append(submission)
        submission = random.choice(meme)
        embed = discord.Embed(title=submission.author.name, url=f'https://www.reddit.com{submission.permalink}',
                              color=0xFFA500)
        embed.set_image(url=submission.url)
        embed.set_footer(text=f'👍 {submission.score} | 💬  {submission.num_comments}')
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def modq(self, ctx, subreddit=None):
        modcomment = []
        modsub = []
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             username=username,
                             password=password,
                             user_agent=user_agent)
        async with ctx.typing():
            if subreddit is None:
                for item in reddit.subreddit('mod').mod.modqueue(only='comments', limit=None):
                    modcomment.append(item)
                for item in reddit.subreddit('mod').mod.modqueue(only='submissions', limit=None):
                    modsub.append(item)
                embed = discord.Embed(title='',
                                      description=f'Total Items: **{len(modcomment) + len(modsub)}**\n\nSubmissions: **{len(modsub)}**\nComments: **{len(modcomment)}**',
                                      color=0xFFA500)
                await ctx.send(embed=embed)
            else:
                for item in reddit.subreddit(subreddit).mod.modqueue(only='comments', limit=None):
                    modcomment.append(item)
                for item in reddit.subreddit(subreddit).mod.modqueue(only='submissions', limit=None):
                    modsub.append(item)
                embed = discord.Embed(title='',
                                      description=f'Total Items: **{len(modcomment) + len(modsub)}**\n\nSubmissions: **{len(modsub)}**\nComments: **{len(modcomment)}**',
                                      color=0xFFA500)

                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Reddit(bot))
