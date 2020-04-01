from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
import discord


class Pillow(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pillow(self, ctx, *, text: str):
        img = Image.new('RGB', (934, 282), color=(0, 0, 0))

        fnt = ImageFont.truetype('C:/Windows/Fonts/Arial.ttf', 40)
        d = ImageDraw.Draw(img)
        d.text((10, 10), text, font=fnt, fill=(255, 255, 255))

        img.save('discordtest.png')
        file = discord.File("C:/Users/Matthew/Documents/Scripts/Python/Discord/Noodles/discordtest.png",
                            filename="discordtest.png")
        await ctx.send(file=file)


def setup(bot):
    bot.add_cog(Pillow(bot))
