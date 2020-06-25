import random

import discord
from discord.ext import commands

from utils import checks


class People(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def gay(self, ctx):
        await ctx.send("YOU'RE REALLY GAY")

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def secks(self, ctx):
        embed = discord.Embed()
        embed.set_image(url='http://i.imgur.com/X8vQxhF.jpg')

        await ctx.send(embed=embed)

    @commands.command(aliases=['matthew, Matthew'], hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def matt(self, ctx):
        await ctx.send('Matthew is so cute')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def perhaps(self, ctx):
        embed = discord.Embed()
        embed.set_image(url='https://cdn.discordapp.com/attachments/677833260323176456/679641540947214337/978.jpg')

        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def danny(self, ctx):
        epicnes = ['Danny is really epic',
                   'Danny is so handsome',
                   'Danny the best memer',
                   'Danny is pro in modern warfare']
        await ctx.send(f'{random.choice(epicnes)}')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def harsha(self, ctx):
        await ctx.send('Harsha has a fat cow ass')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def frying_pan(self, ctx):
        embed = discord.Embed()
        embed.set_image(url='https://cdn.discordapp.com/attachments/665296596287619092/675590016159842313/image0.gif')

        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def moose(self, ctx):
        embed = discord.Embed()
        embed.set_image(
            url='https://cdn.discordapp.com/attachments/665296596287619092/675590507446927370/image0-11.gif')

        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def cousin(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/665296596287619092/675590520730419210/image0-13.gif')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def fap(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/665296596287619092/675592148808237066/image0.gif')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def panda(self, ctx):
        await ctx.send('<a:Panda:669284718604320769>')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def hug(self, ctx):
        await ctx.send(f'here have a hug! <:PepeHug:675713788967649290>')

    @commands.command(aliases=['link, Link'], hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def link(self, ctx):
        responses = ["https://www.rageon.com/products/perhaps-7",
                     "https://www.buzzfeed.com/charlemilyg/which-subway-sandwich-are-you-329mf",
                     "https://youtu.be/pKy-kj2bBGw",
                     "https://www.youtube.com/watch?v=CsGYh8AacgY&app=desktop"
                     "https://www.youtube.com/watch?v=QIWj8iSMX84",
                     "https://www.youtube.com/watch?feature=youtu.be&v=1BB6wj6RyKo&app=desktop",
                     "https://www.youtube.com/watch?v=ehH9OQMQXIk&app=desktop"]
        await ctx.send(f'{random.choice(responses)}')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def spez(self, ctx):
        await ctx.send('Things spez says: \nDoot Doot\nJuicy secks\nThank you for coming to my ted talk')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def hornypolice(self, ctx):
        await ctx.send(
            ':red_circle::blue_circle::red_circle::blue_circle::red_circle:THIS IS THE HORNY '
            'POLICE:red_circle::blue_circle::red_circle::blue_circle::red_circle:\n\nYOU ARE UNDER ARREST FOR A CLASS '
            'D HORNY FELONY. DO NOT RESIST ARREST OR YOUR PENIS AND/OR VAGINA WILL BE FORCIBLY REMOVED FROM '
            'YOU.\n\nYOU ARE ACCUSED OF SUGGESTING HAVING SECKS WITH A FEMALE.\n\nPUT DOWN ANY WEAPONS AND/OR '
            'SECKS-RELATED ITEMS YOU HAVE ON YOUR PERSON AND EXTEND YOUR ARMS SO WE CAN HANDCUFF YOU.\n\nYOU WILL BE '
            'FINED UP TO 100,000 DOLLARS AND WILL SERVE UP TO 20 YEARS IN HORNY JAIL.\n\nYOU HAVE THE RIGHT TO REMAIN '
            'SILENT. ANYTHING YOU SAY CAN AND WILL BE USED AGAINST YOU IN HORNY COURT.\n\nYOU HAVE THE RIGHT TO A '
            'HORNY ATTORNEY. IF YOU CAN NOT AFFORD ONE, ONE WILL BE PROVIDED TO YOU.\n\nTHANK YOU FOR COMPLYING '
            '\n\n:red_circle::blue_circle::red_circle::blue_circle::red_circle::blue_circle::red_circle::blue_circle'
            '::red_circle::blue_circle:')

    @commands.command(hidden=True, aliases=['crisp'])
    @checks.is_guild(guild=718691884070993932)
    async def crispy(self, ctx):
        epicnes = ['I love you all to bits',
                   'Crispy is so cute',
                   'Crispy is the best in this server',
                   'Everyone loves Crispy']
        await ctx.send(f'{random.choice(epicnes)}')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def locke(self, ctx):
        await ctx.send('WeeWoo WeeWoo\n\nLocke is coming to arrest you\n\nWeeWoo WeeWoo')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def toast(self, ctx):
        await ctx.send('Here, have a delicious toast <a:Toast:669286080519864350>')

    @commands.command(hidden=True, name='mel')
    @checks.is_guild(guild=718691884070993932)
    async def _mel(self, ctx):
        await ctx.send('Arctic Monkeys is the best band ever and anyone who disagrees is automatically my enemy')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def demod(self, ctx):
        await ctx.send('demodding user... ')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def mod(self, ctx):
        await ctx.send('Did you really think that it was this easy!? Bruh moment level 4 ')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def nick(self, ctx):
        await ctx.send('detroit:point_right: \n:leg::leg:')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def kap(self, ctx):
        await ctx.send('Do it')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def shark(self, ctx):
        await ctx.send('<@479818382280228865> woof woof')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def rarity(self, ctx):
        await ctx.send('Rarity do be loving Chipotle™ doe')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def genes(self, ctx):
        await ctx.send('screwedbygenie')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def paps(self, ctx):
        await ctx.send('Paps do be an epic gamer doe, we should appreciate her more.')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def lovepolice(self, ctx):
        await ctx.send(
            ":heart: :blue_heart: :heart: :blue_heart: THIS IS THE LOVE POLICE :heart: :blue_heart: :heart: "
            ":blue_heart: \n\nI'M HERE TO LET YOU KNOW I LOVE YOU \n\n:blue_heart: :heart: :blue_heart: :heart: "
            ":blue_heart: :heart: :blue_heart: :heart:")

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def tsg(self, ctx):
        await ctx.send("I’m drunk, alcohol, calculus, WOOOOOOOOOO")

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def spam(self, ctx, *, i: str):
        await ctx.send(
            f'{i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i}')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def noah(self, ctx):
        await ctx.send('Noah is the best')

    @commands.command(aliases=['zombi', 'zomb'], hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def zombital(self, ctx):
        await ctx.send('Life is about one thing, and one thing only. Getting actions on dm.')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def mike(self, ctx):
        await ctx.send("Python is better than java don't @ me")

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def ducc(self, ctx):
        await ctx.send("vote ducc #ducc2020 (he's also very secksy)")

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def jack(self, ctx):
        await ctx.send('Dabbing on those Minecraft haters with my british accent ')

    @commands.command(aliases=['marbles', 'marbless', 'soda'], hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def marble(self, ctx):
        await ctx.send('<@703339033719472161> **Carbonate me mommy**')

    @commands.command(hidden=True)
    @checks.is_guild(guild=718691884070993932)
    async def vanilla(self, ctx):
        await ctx.send("i was forced to make this")

def setup(bot):
    bot.add_cog(People(bot))
