import asyncio

import discord
from discord.ext import commands

from utils import checks


class Eshack(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cleaner(self):
        while True:
            eshack = await self.bot.get_guild(564974738716360724)
            for user in eshack.members:
                if not user.roles:
                    await user.kick(reason="Inactive")
            await asyncio.sleep(172800)


def setup(bot):
    bot.add_cog(Eshack(bot))
