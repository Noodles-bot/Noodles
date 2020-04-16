import discord
from discord.ext import commands

from utils.fun.data import color


# TODO: Level role systeem
# Kuiken: 0-

class Kippi(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Kippi(bot))
