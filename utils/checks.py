from discord.ext import commands
import discord


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
