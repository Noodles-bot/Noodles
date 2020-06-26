import random
import string
from datetime import datetime

import aiohttp
import discord
import praw
from discord.ext import commands

from utils.fun.data import color, emotes
from utils.secret import *

session = aiohttp.ClientSession()


async def q(subreddit):
    async with session.get(f'https://www.reddit.com/r/{subreddit}/about/modqueue/.json') as r:
        retrieved = await r.json()  # returns dict
    return retrieved


class Reddit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  username=username,
                                  password=password,
                                  user_agent=user_agent)
        self.cat = 'https://media.giphy.com/media/E6jscXfv3AkWQ/giphy.gif'

    @commands.command()
    async def membercount(self, ctx, subreddit):
        await ctx.send(self.reddit.subreddit(subreddit).subscribers)

    @commands.command()
    async def meme(self, ctx):
        meme = []
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             username=username,
                             password=password,
                             user_agent=user_agent)
        for submission in self.reddit.subreddit('DankMemes+Memes+MemeEconomy').top('week'):
            if not submission.stickied:
                meme.append(submission)
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
        async with ctx.typing():
            subreddit = subreddit or 'mod'
            for item in self.reddit.subreddit(subreddit).mod.modqueue(only='comments', limit=None):
                modcomment.append(item)
            for item in self.reddit.subreddit(subreddit).mod.modqueue(only='submissions', limit=None):
                modsub.append(item)
            embed = discord.Embed(title='',
                                  description=f'Total Items: **{len(modcomment) + len(modsub)}**\n\nSubmissions: **{len(modsub)}**\nComments: **{len(modcomment)}**',
                                  color=0xFFA500)
            await ctx.send(embed=embed)

    @commands.command()
    async def actions(self, ctx, user=None):
        if user is None:
            u = await self.bot.pg_con.fetch("SELECT user_id, username FROM reddit WHERE user_id = $1",
                                            str(ctx.author.id))
            if not u:
                await ctx.send(f"Unable to locate user please use {ctx.prefix}verify or specify your username")
                return
            user = u[0][1]
        actions = []
        b = discord.Embed(title='Loading....', color=color)
        b.set_image(url=self.cat)
        msg = await ctx.send(embed=b)
        for log in self.reddit.subreddit('specialsnowflake').mod.log(limit=200000000, mod=user):
            if datetime.utcfromtimestamp(log.created_utc).month == datetime.now().month:
                actions.append(log.action)
            else:
                break
        f = discord.Embed(title=f'{user.capitalize()}\'s Report',
                          description=f'Total  actions in r/SpecialSnowflake this month: **{len(actions)}**',
                          color=color, timestamp=ctx.message.created_at)
        f.add_field(name='User bans', value=f"`{str(actions.count('banuser'))}`", inline=False)
        f.add_field(name='Flair edits', value=f'`{str(actions.count("editflair"))}`', inline=False)
        f.add_field(name='Approved posts', value=f'`{str(actions.count("approvelink"))}`', inline=False)
        f.add_field(name='Removed posts', value=f'`{str(actions.count("removelink"))}`', inline=False)
        await msg.edit(embed=f)

    @commands.command()
    async def karma(self, ctx, user=None):
        if user is None:
            u = await self.bot.pg_con.fetch("SELECT user_id, username FROM reddit WHERE user_id = $1",
                                            str(ctx.author.id))
            if not u:
                await ctx.send(f"Unable to locate user please use {ctx.prefix}verify or specify your username")
                return
            user = u[0][1]
        user = self.reddit.redditor(user)
        b = discord.Embed(title='Loading....', color=color)
        b.set_image(url=self.cat)
        msg = await ctx.send(embed=b)
        await msg.edit(embed=discord.Embed(title=f'Total Karma: {user.link_karma + user.comment_karma:,}',
                                           description=f'Post karma:\n**{user.link_karma:,}**\n\nComment karma:\n**{user.comment_karma:,}**',
                                           color=color))

    @commands.command(aliases=['reddit', 'stats', 'rs', 'r'])
    async def redditstats(self, ctx, user=None):

        b = discord.Embed(title='Loading....', color=color)
        b.set_image(url=self.cat)
        msg = await ctx.send(embed=b)

        if user is None:
            u = await self.bot.pg_con.fetch("SELECT user_id, username FROM reddit WHERE user_id = $1",
                                            str(ctx.author.id))
            if not u:
                await ctx.send(f"Unable to locate user please use {ctx.prefix}verify or specify your username")
                return
            user = u[0][1]

        async with session.get(url=f'https://www.reddit.com/user/{user}/trophies/.json') as resp:
            troph = await resp.json()
        async with session.get(url=f'https://www.reddit.com/user/{user}/moderated_subreddits/.json') as mod:
            mod = await mod.json()
        async with session.get(f'https://www.reddit.com/user/{user}/about/.json') as resp:
            about = await resp.json()
        trophies = []

        for trophy in troph['data']['trophies']:
            try:
                yes = trophy['data']['name'].lower()
                trophies.append(emotes[yes])
            except KeyError:
                print(trophy['data']['name'])

        icon = about['data']['icon_img']
        icon = icon.split('?')[0]
        banner = about['data']['subreddit']['banner_img']
        banner = banner.split('?')[0]
        embed = discord.Embed(title=about['data']['subreddit']['title'], color=color)
        embed.set_thumbnail(url=icon)
        if trophies:
            embed.add_field(name='**Trophies**', value=''.join(sorted(set(trophies))), inline=False)
        embed.set_author(name=about['data']['subreddit']['display_name_prefixed'],
                         url=f'https://www.reddit.com{about["data"]["subreddit"]["url"]}',
                         icon_url=banner)
        embed.add_field(name='**Karma**',
                        value=f'Total: **{about["data"]["link_karma"] + about["data"]["comment_karma"]:,}**\n'
                              f'Link: **{about["data"]["link_karma"]:,}**\n'
                              f'Comment: **{about["data"]["comment_karma"]:,}**', inline=True)
        if mod:
            subs = []
            for index, sub in enumerate(mod['data'], 0):
                subs.append(sub['sr_display_name_prefixed'] + f' ({sub["subscribers"]:,})')
                if index > 19:
                    break
            embed.add_field(name=f"**Top 20 moderated subreddits\nTotal:** {len(mod['data'])}",
                            value=f"\n".join(subs), inline=False)

        await msg.edit(embed=embed)

    @commands.command()
    async def verify(self, ctx):
        await ctx.author.send("What's your reddit username?")
        m = await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=10.0)
        letters = string.ascii_lowercase
        verify = ''.join([random.choice(letters) for i in range(6)])
        ig = m.content.lower().replace('u/', '')
        self.reddit.redditor(ig).message('Verify', f'Your verification is:\n\n **{verify}**\n\nPlease reply in dm')
        await ctx.author.send(f"Succesfully send verification to {m.content}")
        r = await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author)
        if r.content.lower() == verify.lower():
            i = await self.bot.conn.users.fetch_one({"reddit": str(username)})
            if not i:
                user = await self.bot.conn.users.fetch_one({"user_id": str(ctx.author.id)})
                user['misc']['reddit'] = str(username)
                await self.bot.conn.users.update_one({"user_id": str(ctx.author.id)}, {"$set": user}, upsert=False)
                await ctx.author.send("Succesfully verified")
            else:
                await ctx.author.send("You are already verified")
        else:
            await ctx.author.send("Incorrect verification")
            return


def setup(bot):
    bot.add_cog(Reddit(bot))
