import re

import discord
from PIL import Image
from discord.ext import commands
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    hlen = int(len(hex))
    print(type(hlen))
    return tuple(int(hex[i:i + hlen / 3], 16) for i in range(0, hlen, hlen / 3))


class Hexroles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    """
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            await self.cleanup_roles(guild)

    @commands.command()
    async def viewcolor(self, ctx, color):
        im = Image.new("RGB", (100, 100), color)
        im.save('color.png')
        await ctx.send(file=discord.File("C:/Users/Matthew/Documents/Scripts/Python/Discord/Noodles/color.png",
                                         filename="color.png"))

    @commands.command()
    async def color(self, ctx, *, color):
        color = color.upper()
        hex = hex_to_rgb(hex=color)
        role = discord.utils.get(ctx.guild.roles, name=color)
        if role:
            await ctx.author.add_roles(role, reason="Adding existing role to user")
        else:
            new_role = await ctx.guild.create_role(name=ctx.message.content,
                                                   color=discord.Colour.from_rgb(hex[0], hex[1], hex[3]))
            await ctx.author.add_roles(new_role, reason="Created new role for user")

        await ctx.channel.send('Added role')
    """

def setup(bot):
    bot.add_cog(Hexroles(bot))
