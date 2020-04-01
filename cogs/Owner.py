import asyncpg
import discord
import json
from discord.ext import commands

from utils import checks
from utils.tools import get_money


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

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def todo(self, ctx, *, todo):
        await self.bot.pg_con.execute("INSERT INTO todo (todo, num, is_pinned) VALUES ($1, $2, FALSE)", todo, 1)
        await ctx.send("Inserted into the database")

    @todo.command()
    async def view(self, ctx, *, todo):
        print('test')

    @commands.command(aliases=['setmoney'])
    @checks.is_owner_or_admin()
    async def set_money(self, ctx, *, name):
        with open(r"/utils/json/money.json", 'r') as f:
            money = json.load(f)

        money[str(ctx.guild.id)] = name
        await ctx.send(f"New money name is `{name}`")

        with open(r'/utils/json/money.json', 'w') as f:
            json.dump(money, f, indent=4)


def setup(bot):
    bot.add_cog(Owner(bot))
