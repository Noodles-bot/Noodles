import random
from datetime import datetime

import aiohttp
import discord
import praw
from discord.ext import commands

from utils.fun.data import color
from utils.secret import *


async def q(subreddit):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f'https://www.reddit.com/r/{subreddit}/about/modqueue/.json') as r:
            retrieved = await r.json()  # returns dict
    return retrieved


class Reddit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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

    @commands.command()
    async def actions(self, ctx, user):
        actions = []
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             username=username,
                             password=password,
                             user_agent=user_agent)
        b = discord.Embed(title='Loading....', color=color)
        b.set_image(url='https://acegif.com/wp-content/uploads/cat-typing-16.gif')
        msg = await ctx.send(embed=b)
        for log in reddit.subreddit('specialsnowflake').mod.log(limit=200000000, mod=user):
            if datetime.utcfromtimestamp(log.created_utc).month == datetime.now().month:
                actions.append(log.action)
            else:
                break
        f = discord.Embed(title=f'{user}\'s Report',
                          description=f'Total  actions in r/SpecialSnowflake this month: **{len(actions)}**',
                          color=color, timestamp=ctx.message.created_at)
        f.add_field(name='User bans', value=f"`{str(actions.count('banuser'))}`", inline=False)
        f.add_field(name='Flair edits', value=f'`{str(actions.count("editflair"))}`', inline=False)
        f.add_field(name='Approved posts', value=f'`{str(actions.count("approvelink"))}`', inline=False)
        f.add_field(name='Removed posts', value=f'`{str(actions.count("removelink"))}`', inline=False)
        await msg.edit(embed=f)

    @commands.command()
    async def karma(self, ctx, user):
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             username=username,
                             password=password,
                             user_agent=user_agent)
        user = reddit.redditor(user)
        b = discord.Embed(title='Loading....', color=color)
        b.set_image(url='https://acegif.com/wp-content/uploads/cat-typing-16.gif')
        msg = await ctx.send(embed=b)
        try:
            await msg.edit(embed=discord.Embed(title=f'Total Karma: {user.link_karma + user.comment_karma:,}',
                                               description=f'Post karma:\n**{user.link_karma:,}**\n\nComment karma:\n**{user.comment_karma:,}**',
                                               color=color))
        except discord.NotFound:
            await msg.edit("Unable to locate user, please try again")

    @commands.command()
    async def stats(self, ctx, user):

        b = discord.Embed(title='Loading....', color=color)
        b.set_image(url='https://acegif.com/wp-content/uploads/cat-typing-16.gif')

        msg = await ctx.send(embed=b)
        stats = self.stats(user)
        await msg.edit(embed=stats)
    """
    @commands.command()
    async def modstats(self, ctx, user):
        b = discord.Embed(title='Loading....', color=color)
        b.set_image(url='https://acegif.com/wp-content/uploads/cat-typing-16.gif')

        msg = await ctx.send(embed=b)
        p = requests.get(f'https://www.reddit.com/user/{user}/moderated_subreddits/.json')
        p = p.json()
        await asyncio.sleep(1.2)
        profile = requests.get(f'https://www.reddit.com/user/{user}/about.json?raw_json=1')
        profile = profile.json()
        total = 0
        print(p)
        for sub in p['data']:
            total += sub['subscribers']
        total_modded = '{:,}'.format(total)
        top_20 = []
        for sub in p['data']:
            if len(top_20) == 15:
                break
            top_20.append(f'{sub["sr_display_name_prefixed"]} ({sub["subscribers"]})')
        embed = discord.Embed(
            title='',
            color=color)
        embed.set_author(name=f'u/{user}', url=f'https://www.reddit.com/user/{user}')
        embed.set_thumbnail(url=profile['data']['icon_img'])
        embed.add_field(name='Total Subscribers', value=total_modded)
        embed.add_field(name=f'Top {len(top_20)} Moderated Subreddits', value='\n'.join(top_20), inline=False)
        await ctx.send(embed=embed)
    """


def setup(bot):
    bot.add_cog(Reddit(bot))
