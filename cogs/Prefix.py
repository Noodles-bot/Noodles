import discord
from discord.ext import commands
import json

from utils import checks


async def is_guild_owner(ctx):
    return ctx.author.id == ctx.guild.owner.id


class Prefix(commands.Cog):
    bot = commands

    def __init__(self, bot):
        self.bot = bot

    @bot.command()
    @checks.is_owner_or_admin()
    async def prefix(self, ctx, *, pre):
        with open(r"C:\Users\Matthew\Documents\Scripts\Python\Discord\Noodles\prefixes.json", 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = pre
        await ctx.guild.get_member(self.bot.user.id).edit(nick=f'Noodles [{pre}]')
        await ctx.send(f"New Prefix is `{pre}`")

        with open(r'C:\Users\Matthew\Documents\Scripts\Python\Discord\Noodles\prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)


def setup(bot):
    bot.add_cog(Prefix(bot))
