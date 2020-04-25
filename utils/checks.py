import asyncio

import asyncpg
from discord.ext import commands
import discord
from utils.secret import *


class MissingPermissions:
    pass


def is_owner_or_admin():
    def predicate(ctx):

        if ctx.message.author.guild_permissions.administrator:
            return True
        elif ctx.author.id == 357918459058978816:
            return True
        else:
            pass

    return commands.check(predicate)


def is_guild(guild):
    def predicate(ctx):
        if ctx.guild.id == guild:
            return True
        else:
            return False

    return commands.check(predicate)


def is_user(user_id: int):
    def predicate(ctx):
        if ctx.author.id == int(user_id):
            return True
        else:
            return False

    return commands.check(predicate)


def is_tester():
    async def predicate(ctx):
        conn = await asyncpg.connect(database=DATABASE, user=USER, password=PASSWORD)
        y = await conn.fetch("SELECT tester FROM users WHERE user_id = $1 ", str(ctx.author.id))
        await conn.close()
        print('hey')
        return y[0][0]

    return commands.check(predicate)
