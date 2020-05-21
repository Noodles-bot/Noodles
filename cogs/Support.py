from uuid import uuid4

from discord.ext import commands


class Support(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, name='support', aliases=['chat'])
    async def support_group(self, ctx):
        await self.bot.pg_con.execute("INSERT INTO support (id, user_id, guild_id)  "
                                      "VALUES ($1, $2, $3)", uuid4(), ctx.author.id, ctx.guild.id)


def setup(bot):
    bot.add_cog(Support(bot))
