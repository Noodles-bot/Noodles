import discord
from discord.ext import commands


# noinspection PyTypeChecker
class Daily(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        if ctx.author == self.bot.user:
            return

        if ctx.author.bot:
            return

        author_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)

        i = await self.bot.pg_con.fetch("SELECT bal FROM users WHERE user_id = $1", author_id)
        if i[0] is None:
            await self.bot.pg_con.execute("INSERT INTO users (bal) VALUES (100)")

        user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1", author_id)

        await self.bot.pg_con.execute("UPDATE users SET bal = $1 WHERE user_id  = $2",
                                      user['bal'] + 500,
                                      author_id)

        await ctx.send('Added 500 Ducc dollars')

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            i1 = error.retry_after / 60
            i2 = i1 / 60
            msg = f'Your daily money can only be used once a day, please try again in {int(i2)}h'
            await ctx.send(msg)


def setup(bot):
    bot.add_cog(Daily(bot))
