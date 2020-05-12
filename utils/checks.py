import discord
from discord.ext import commands


class MissingPermissions:
    pass


def is_owner_or_admin():
    def predicate(ctx):
        if ctx.message.author.guild_permissions.administrator:
            return True
        elif ctx.author.id == 357918459058978816:
            return True
        else:
            raise discord.Forbidden("You are missing administrator permissions to use this command")

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