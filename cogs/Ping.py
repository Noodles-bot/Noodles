import discord
from discord.ext import commands
import time


class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['advanced_ping', 'msping', 'advanced'])
    async def adv_ping(self, ctx):
        try:
            t1 = time.perf_counter()
            await ctx.trigger_typing()
            ta = t1
            t2 = time.perf_counter()
            await ctx.trigger_typing()
            tb = t2
            ra = round((tb - ta) * 1000, 3)
        finally:
            pass
        try:
            t1b = time.perf_counter()
            await ctx.trigger_typing()
            ta2 = t1b
            t2b = time.perf_counter()
            await ctx.trigger_typing()
            tb2 = t2b
            ra2 = round((tb2 - ta2) * 1000, 3)
        finally:
            pass
        try:
            t1c = time.perf_counter()
            await ctx.trigger_typing()
            ta3 = t1c

            t2c = time.perf_counter()
            await ctx.trigger_typing()
            tb3 = t2c

            ra3 = round((tb3 - ta3) * 1000, 3)
        finally:
            pass
        try:
            t1d = time.perf_counter()
            await ctx.trigger_typing()
            ta4 = t1d

            t2d = time.perf_counter()
            await ctx.trigger_typing()
            tb4 = t2d

            ra4 = round((tb4 - ta4) * 1000, 3)
        finally:
            pass

        e = discord.Embed(title="Advanced Ping", colour=0xFFA500)
        e.add_field(name='Ping 1', value=f'{str(ra)}ms')
        e.add_field(name='Ping 2', value=f'{str(ra2)}ms')
        e.add_field(name='Ping 3', value=f'{str(ra3)}ms')
        e.add_field(name='Ping 4', value=f'{str(ra4)}ms')
        await ctx.send(embed=e)

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(title=' ',
                              description=f'Pong! :ping_pong:\n *Response time: {round(self.bot.latency * 1000, 3)}ms*',
                              color=0xFFA500)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Ping(bot))
