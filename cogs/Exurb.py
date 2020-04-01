import praw
from discord.ext import commands


class Exurb(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        reddit = praw.Reddit(client_id='hUO84B7-xGsLOg',
                             client_secret='K04KuFUhOFbJ5dzNjmkMYR0TSfs',
                             username='Cake-day-29feb',
                             password='Jupiter22',
                             user_agent='Matt-O-Bot')
        members = self.bot.get_channel(690125363170508906)
        await members.edit(name=f"Sub members: {reddit.subreddit('exurb1a').subscribers}")

    @commands.command()
    @commands.is_owner()
    async def refresh(self, ctx):
        reddit = praw.Reddit(client_id='hUO84B7-xGsLOg',
                             client_secret='K04KuFUhOFbJ5dzNjmkMYR0TSfs',
                             username='Cake-day-29feb',
                             password='Jupiter22',
                             user_agent='Matt-O-Bot')
        members = self.bot.get_channel(690125363170508906)
        await members.edit(name=f"Sub members: {reddit.subreddit('exurb1a').subscribers}")
        people = []
        id = str(ctx.guild.id)
        for user in ctx.guild.members:
            people.append(user)
        if "564974738716360724" in id:
            members = self.bot.get_channel(689483433667199036)
            await members.edit(name=f'Members: {len(people):,}')
        await ctx.send('refreshed succesfully')


def setup(bot):
    bot.add_cog(Exurb(bot))
