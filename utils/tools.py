import discord
import asyncio
import asyncpg
from utils.secret import *


def embedinator(author, color, message, *, formatUser=False, useNick=False):
    if formatUser:
        name = str(author)
    elif useNick:
        name = author.display_name
    else:
        name = author.name
    embed = discord.Embed(color=color, description=message)
    embed.set_author(name=name, icon_url=str(author.avatar_url).replace("webp", "png"))
    return embed





