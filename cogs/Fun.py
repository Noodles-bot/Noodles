import io
import requests
import random

import discord
from discord.ext import commands

from utils.fun.fortunes import fortunes
from utils.fun.data import fight_results


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gay(self, ctx):
        await ctx.send("YOU'RE REALLY GAY")

    @commands.command()
    async def secks(self, ctx):
        embed = discord.Embed()
        embed.set_image(url='http://i.imgur.com/X8vQxhF.jpg')

        await ctx.send(embed=embed)

    @commands.command()
    async def french(self, ctx):
        await ctx.send('French Horn is really gay')

    @commands.command(name='8ball')
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful.",
                     "You're gay"]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command(aliases=['matthew, Matthew'])
    async def matt(self, ctx):
        await ctx.send('Matthew is so cute')

    @commands.command()
    async def perhaps(self, ctx):
        embed = discord.Embed()
        embed.set_image(url='https://cdn.discordapp.com/attachments/677833260323176456/679641540947214337/978.jpg')

        await ctx.send(embed=embed)

    @commands.command()
    async def danny(self, ctx):
        epicnes = ['Danny is really epic',
                   'Danny is so handsome',
                   'Danny the best memer',
                   'Danny is pro in modern warfare']
        await ctx.send(f'{random.choice(epicnes)}')

    @commands.command()
    async def harsha(self, ctx):
        await ctx.send('Harsha has a fat cow ass')

    @commands.command()
    async def frying_pan(self, ctx):
        embed = discord.Embed()
        embed.set_image(url='https://cdn.discordapp.com/attachments/665296596287619092/675590016159842313/image0.gif')

        await ctx.send(embed=embed)

    @commands.command()
    async def koen(self, ctx):
        await ctx.send("Koen you're really gay")

    @commands.command()
    async def moose(self, ctx):
        embed = discord.Embed()
        embed.set_image(
            url='https://cdn.discordapp.com/attachments/665296596287619092/675590507446927370/image0-11.gif')

        await ctx.send(embed=embed)

    @commands.command()
    async def cousin(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/665296596287619092/675590520730419210/image0-13.gif')

    @commands.command()
    async def doot(self, ctx):
        await ctx.send('<@420788676516249601> <:doot_doot:673397860427104288> <:doot_doot:673397860427104288>')

    @commands.command()
    async def fap(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/665296596287619092/675592148808237066/image0.gif')

    @commands.command()
    async def panda(self, ctx):
        await ctx.send('<a:Panda:669284718604320769>')

    @commands.command()
    async def hug(self, ctx):
        await ctx.send(f'here have a hug! <:PepeHug:675713788967649290>')

    @commands.command(aliases=['link, Link'])
    async def link(self, ctx):
        responses = ["https://www.rageon.com/products/perhaps-7",
                     "https://www.buzzfeed.com/charlemilyg/which-subway-sandwich-are-you-329mf",
                     "https://youtu.be/pKy-kj2bBGw",
                     "https://www.youtube.com/watch?v=CsGYh8AacgY&app=desktop"
                     "https://www.youtube.com/watch?v=QIWj8iSMX84",
                     "https://www.youtube.com/watch?feature=youtu.be&v=1BB6wj6RyKo&app=desktop",
                     "https://www.youtube.com/watch?v=ehH9OQMQXIk&app=desktop"]
        await ctx.send(f'{random.choice(responses)}')

    @commands.command()
    async def spez(self, ctx):
        await ctx.send('Things spez says: \nDoot Doot\nJuicy secks\nThank you for coming to my ted talk')

    @commands.command()
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

    @commands.command()
    async def crispy(self, ctx):
        epicnes = ['I love you all to bits',
                   'Crispy is so cute',
                   'Crispy is the best in this server',
                   'Everyone loves Crispy']
        await ctx.send(f'{random.choice(epicnes)}')

    @commands.command()
    async def locke(self, ctx):
        await ctx.send('WeeWoo WeeWoo\n\nLocke is coming to arrest you\n\nWeeWoo WeeWoo')

    @commands.command()
    async def toast(self, ctx):
        await ctx.send('Here, have a delicious toast <a:Toast:669286080519864350>')

    @commands.command()
    async def malcolm(self, ctx):
        await ctx.send(':eyes: hehe')

    @commands.command()
    async def demod(self, ctx):
        await ctx.send('demodding user... ')

    @commands.command()
    async def mod(self, ctx):
        await ctx.send('Did you really think that it was this easy!? Bruh moment level 4 ')

    @commands.command()
    async def nick(self, ctx):
        await ctx.send('detroit:point_right: \n:leg::leg:')

    @commands.command()
    async def kap(self, ctx):
        await ctx.send('Do it')

    @commands.command()
    async def shark(self, ctx):
        await ctx.send('<@479818382280228865> woof woof')

    @commands.command()
    async def rarity(self, ctx):
        await ctx.send('Rarity do be loving Chipotle™ doe')

    @commands.command()
    async def genes(self, ctx):
        await ctx.send('screwedbygenie')

    @commands.command()
    async def paps(self, ctx):
        await ctx.send('Paps do be an epic gamer doe, we should appreciate her more.')

    @commands.command()
    async def lovepolice(self, ctx):
        await ctx.send(
            ":heart: :blue_heart: :heart: :blue_heart: THIS IS THE LOVE POLICE :heart: :blue_heart: :heart: "
            ":blue_heart: \n\nI'M HERE TO LET YOU KNOW I LOVE YOU \n\n:blue_heart: :heart: :blue_heart: :heart: "
            ":blue_heart: :heart: :blue_heart: :heart:")

    @commands.command()
    async def tsg(self, ctx):
        await ctx.send("I’m drunk, alcohol, calculus, WOOOOOOOOOO")

    @commands.command()
    async def spam(self, ctx, *, i: str):
        await ctx.send(
            f'{i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i} {i}')

    @commands.command()
    async def noah(self, ctx):
        await ctx.send('Noah is the best')

    @commands.command(aliases=['zombi', 'zomb'])
    async def zombital(self, ctx):
        await ctx.send('Life is about one thing, and one thing only. Getting actions on dm.')

    @commands.command()
    async def mike(self, ctx):
        await ctx.send("Python is better than java don't @ me")

    @commands.command(aliases=['flip'])
    async def coinflip(self, ctx):
        coin = random.randrange(2)
        if coin == 0:
            msg = 'The coin has landed on Tails!!'
            await ctx.send(msg)
        if coin == 1:
            msg = 'The coin has landed on Heads!!'
            await ctx.send(msg)

    @commands.command()
    async def ducc(self, ctx):
        await ctx.send("vote ducc #ducc2020 (he's also very secksy)")

    @commands.command()
    async def jack(self, ctx):
        await ctx.send('Dabbing on those Minecraft haters with my british accent ')

    @commands.command()
    async def fortune(self, ctx):
        await ctx.send(f'```{random.choice(fortunes)}```')

    @commands.command()
    async def fight(self, ctx, user: discord.Member = None, *, weapon: str = None):
        if user is None or user == ctx.author:
            await ctx.send(
                f"{ctx.author.mention} fought themselfs but only ended up in a mental institution, <:kek:665322685034922017>")
            return
        if weapon is None:
            await ctx.send(
                f"{ctx.author.mention} tried to fight {user.display_name} with nothing so {user.display_name} easily won, lmao you're a smol brain")
            return
        await ctx.send(
            f"{ctx.author.mention} used **{weapon}** on **{user.display_name}** {random.choice(fight_results).replace('%user%', str(user.display_name)).replace('%attacker%', ctx.author.mention)}")

    @commands.command(aliases=['catto'])
    async def cat(self, ctx):
        response = requests.get('https://aws.random.cat/meow')
        data = response.json()
        embed = discord.Embed(title='Meow!!', color=0xFFA500)
        embed.set_image(url=data['file'])
        embed.set_footer(text='Powered by: https://aws.random.cat/meow')
        await ctx.send(embed=embed)

    @commands.command(aliases=['doggo'])
    async def dog(self, ctx):
        response = requests.get('https://random.dog/woof.json')
        data = response.json()
        embed = discord.Embed(title='Woof!! Woof!!', color=0xFFA500)
        embed.set_image(url=data['url'])
        embed.set_footer(text='Powered by: https://random.dog/woof.json')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
