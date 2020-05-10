import random

import aiohttp
import discord
from discord.ext import commands

from utils.fun.data import fight_results, insults
from utils.fun.fortunes import fortunes
from utils.secret import *

session = aiohttp.ClientSession()


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='8ball')
    async def _8ball(self, ctx, *, question):
        """Gives the wisest answers"""
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

    @commands.command(hidden=True)
    async def french(self, ctx):
        await ctx.send("French horn do be playing the french horn doe :postal_horn:")

    @commands.command(hidden=True)
    async def doot(self, ctx):
        await ctx.send('<@420788676516249601> <:doot_doot:673397860427104288> <:doot_doot:673397860427104288>')

    @commands.command(aliases=['flip'])
    async def coinflip(self, ctx):
        """Flips a coin"""
        coin = random.randrange(2)
        if coin == 0:
            msg = 'The coin has landed on Tails!!'
            await ctx.send(msg)
        if coin == 1:
            msg = 'The coin has landed on Heads!!'
            await ctx.send(msg)

    @commands.command()
    async def fight(self, ctx, user: discord.Member = None, *, weapon: str = None):
        """Fight a user"""
        if user is None or user == ctx.author:
            await ctx.send(
                f"{ctx.author.mention} fought themselves but only ended up in a mental institution, <:kek:665322685034922017>")
            return
        if weapon is None:
            await ctx.send(
                f"{ctx.author.mention} tried to fight {user.display_name} with nothing so {user.display_name} easily won, lmao you're a smol brain")
            return
        await ctx.send(
            f"{ctx.author.mention} used **{weapon}** on **{user.display_name}** {random.choice(fight_results).replace('%user%', str(user.display_name)).replace('%attacker%', ctx.author.mention)}")

    @commands.command(aliases=['catto'])
    async def cat(self, ctx):
        """Sends a cute catto"""
        async with session.get('https://aws.random.cat/meow') as resp:
            data = await resp.json()
        embed = discord.Embed(title='Meow!!', color=0xFFA500)
        embed.set_image(url=data['file'])
        embed.set_footer(text='Powered by: https://aws.random.cat/meow')
        await ctx.send(embed=embed)

    @commands.command(aliases=['doggo'])
    async def dog(self, ctx):
        """Sends a cute doggo"""
        async with session.get('https://random.dog/woof.json') as resp:
            data = await resp.json()
        embed = discord.Embed(title='Woof!! Woof!!', color=0xFFA500)
        embed.set_image(url=data['url'])
        embed.set_footer(text='Powered by: https://random.dog/woof.json')
        await ctx.send(embed=embed)

    @commands.command()
    async def fortune(self, ctx):
        """Gives a random fortune"""
        await ctx.send(f'```{random.choice(fortunes)}```')

    @commands.command()
    async def insult(self, ctx, user: discord.Member = None):
        """Insults you or a user"""
        member = user or ctx.author
        i = random.randint(0, 1)
        if i == 0:
            await ctx.send(random.choice(insults))
        else:
            async with session.get(f'https://insult.mattbas.org/api/insult.json?who={member.name}') as resp:
                data = await resp.json(content_type=None)
            await ctx.send(data['insult'])

    @commands.command(aliases=['comp'])
    async def compliment(self, ctx, user: discord.Member = None):
        """Gives a user or you a compliment"""
        member = user or ctx.author
        async with session.get('https://complimentr.com/api') as data:
            data = await data.json(content_type=None)
        await ctx.send(member.name + ", " + data['compliment'].capitalize())

    @commands.command()
    @commands.is_owner()
    async def memegen(self, ctx, arg1, arg2):
        async with session.get(
                'https://api.imgflip.com/caption_image?'
                'template_id=112126428'
                f'&username=DankDumpster&password={password}&text0={arg1}&text1={arg2}'
        ) as resp:
            data = await resp.json()
        if data['success']:
            await ctx.send(discord.Embed().set_image(url=data['data']['url']))
        else:
            await ctx.send(data['error_message'])


def setup(bot):
    bot.add_cog(Fun(bot))
