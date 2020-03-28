import discord
import subprocess
import sys
from discord.ext import commands


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def nickname(self, ctx, *, name: str = None):
        try:
            await ctx.guild.me.edit(nick=name)
            if name:
                await ctx.send(f"Successfully changed nickname to **{name}**")
            else:
                await ctx.send("Successfully removed nickname")
        except Exception as err:
            await ctx.send(err)

    @commands.command()
    @commands.is_owner()
    async def reboot(self, ctx):
        await self.bot.logout()
        subprocess.call([sys.executable, "Noodles.py"])


def setup(bot):
    bot.add_cog(Owner(bot))
