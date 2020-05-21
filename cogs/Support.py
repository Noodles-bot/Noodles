from uuid import uuid4

from discord.ext import commands


class Support(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, name='support', aliases=['chat'])
    async def support_group(self, ctx):
        await ctx.send(uuid4())


def setup(bot):
    bot.add_cog(Support(bot))
