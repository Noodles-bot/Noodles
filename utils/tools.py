import discord
import json


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


async def get_money(ctx):
    if not ctx.guild:
        return ":ramen:"

    with open("C:/Users/Matthew/Documents/Scripts/Python/Discord/Noodles/utils/json/money.json", 'r') as f:
        money = json.load(f)

    if str(ctx.guild.id) not in money:
        return ':ramen:'

    money = money[str(ctx.guild.id)]
    return money
