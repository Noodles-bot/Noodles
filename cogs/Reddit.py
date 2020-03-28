import praw
from discord.ext import commands


class Reddit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reddithot(self, ctx, subreddit=None):
        reddit = praw.Reddit(client_id='hUO84B7-xGsLOg',
                             client_secret='K04KuFUhOFbJ5dzNjmkMYR0TSfs',
                             username='Cake-day-29feb',
                             password='Jupiter22',
                             user_agent='Matt-O-Bot')
        if subreddit is None:
            for submission in reddit.front.hot(limit=5):
                if not submission.stickied:
                    await ctx.send(submission.title)
        else:
            for submission in reddit.subreddit(subreddit).hot(limit=5):
                if not submission.stickied:
                    await ctx.send(submission.title)

    @commands.command()
    async def membercount(self, ctx, subreddit):
        reddit = praw.Reddit(client_id='hUO84B7-xGsLOg',
                             client_secret='K04KuFUhOFbJ5dzNjmkMYR0TSfs',
                             username='Cake-day-29feb',
                             password='Jupiter22',
                             user_agent='Matt-O-Bot')
        await ctx.send(reddit.subreddit(subreddit).subscribers)


def setup(bot):
    bot.add_cog(Reddit(bot))
