import discord
import requests
from discord.ext import commands
import random
import asyncio
import html
from utils.tools import get_money
from utils.fun.data import smart, dumb


def coinflip():
    return random.randint(0, 1)


def randomnumber(num1: int, num2: int):
    return random.randrange(num1, num2)


class Gambling(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gamble(self, ctx, money):
        money_name = await get_money(ctx=ctx)
        sql = self.bot.get_cog('Sql')
        if sql is not None:
            user1 = await sql.get_user(author_id=str(ctx.author.id), guild_id=str(ctx.guild.id))
            if money.lower() == 'all':
                amt = await sql.get_balance(author_id=str(ctx.author.id))
                money = amt[0][0]
            if user1['bal'] >= int(money) > 0:
                num1 = randomnumber(1, 12)  # user
                num2 = randomnumber(1, 12)  # bot

                money = int(money)
                await sql.withdraw(amount=money, author_id=str(ctx.author.id))
                if num1 > num2:  # user wins
                    await sql.deposit(amount=money * 2.5, author_id=str(ctx.author.id))
                    bal = await sql.get_balance(author_id=str(ctx.author.id))
                    win = discord.Embed(title=f"{ctx.author.name}'s Gambling game",
                                        description=f"You won **{int(money * 2.5)}** {money_name}\n\nNew balance is: **{int(round(bal[0][0], 0))}** {money_name}",
                                        color=0x228B22)
                    win.add_field(name=ctx.author.name, value=f'Rolled `{num1}`', inline=True)
                    win.add_field(name=self.bot.user.name, value=f'Rolled `{num2}`', inline=True)
                    await ctx.send(embed=win)
                elif num1 < num2:  # bot wins
                    bal = await sql.get_balance(author_id=str(ctx.author.id))
                    lose = discord.Embed(title=f"{ctx.author.name}'s Gambling game",
                                         description=f"You lost **{money}** {money_name}\n\nNew balance is: **{int(round(bal[0][0], 0))}** {money_name}",
                                         color=0xFF0000)
                    lose.add_field(name=ctx.author.name, value=f'Rolled `{num1}`', inline=True)
                    lose.add_field(name=self.bot.user.name, value=f'Rolled `{num2}`', inline=True)
                    await ctx.send(embed=lose)
                elif num1 == num2:
                    await sql.deposit(amount=money, author_id=str(ctx.author.id))
                    bal = await sql.get_balance(author_id=str(ctx.author.id))
                    eq = discord.Embed(title=f"{ctx.author.name}'s Gambling game",
                                       description=f"You both rolled the same number\nYour bet will be refunded\n\nNew balance is: **{int(round(bal[0][0], 0))}** {money_name}")
                    eq.add_field(name=ctx.author.name, value=f'Rolled `{num1}`', inline=True)
                    eq.add_field(name=self.bot.user.name, value=f'Rolled `{num2}`', inline=True)
                    await ctx.send(embed=eq)
            else:
                await ctx.send("Nice try, sadly you can't gamble your imaginary wealth")

    @commands.command(aliases=['slot'])
    async def slots(self, ctx, money):
        money_name = await get_money(ctx=ctx)
        sql = self.bot.get_cog('Sql')
        if sql is not None:
            if money.lower() == 'all':
                amt = await sql.get_balance(author_id=str(ctx.author.id))
                money = amt[0][0]
            if int(money) <= 0:
                await ctx.send("Please use amounts above 1")
                return
            money = int(money)
            balance = await sql.get_balance(author_id=str(ctx.author.id), guild_id=str(ctx.guild.id))
            if int(money) > balance[0][0]:
                await ctx.send("Nice try, sadly you can't gamble your imaginary wealth")
                return

            slots = ['chocolate_bar', 'bell', 'tangerine', 'apple', 'cherries', 'seven']
            slot1 = slots[random.randint(0, 5)]
            slot2 = slots[random.randint(0, 5)]
            slot3 = slots[random.randint(0, 5)]

            await sql.withdraw(amount=money, author_id=str(ctx.author.id))
            slotOutput = '|\t:{}:\t|\t:{}:\t|\t:{}:\t|\n'.format(slot1, slot2, slot3)
            default = discord.Embed(title='Slots', description=slotOutput)
            msg = await ctx.send(embed=default)
            if slot1 == slot2 and slot2 == slot3 and slot3 != 'seven':
                await sql.deposit(amount=money * 2.5, author_id=str(ctx.author.id))
                i = slotOutput
                c = True
            elif slot1 == 'seven' and slot2 == 'seven' and slot3 == 'seven':
                await sql.deposit(amount=money * 5, author_id=str(ctx.author.id))
                i = slotOutput
                c = True

            elif slot1 == slot2 or slot1 == slot3 or slot2 == slot3:
                await sql.deposit(amount=money * 1.5, author_id=str(ctx.author.id))
                i = slotOutput
                c = True
            else:
                i = slotOutput
                c = False
            await asyncio.sleep(random.randrange(1, 3))
            bal = await sql.get_balance(author_id=str(ctx.author.id))
            win = discord.Embed(title='Slots',
                                description=f"**CONGRATS YOU WON!!**\n\nNew balance is:**{int(bal[0][0])} {money_name}**\n\n{i}",
                                color=0x228B22)
            lose = discord.Embed(title='Slots',
                                 description=f"**You lost <:sad:666637638643744788>**\n\nNew balance is: **{int(bal[0][0])} {money_name}**\n\n{i}",
                                 color=0xFF0000)
            if c:
                await msg.edit(embed=win)
            else:
                await msg.edit(embed=lose)

    @commands.command()
    async def test(self, ctx):
        sql = self.bot.get_cog('Sql')
        if sql is not None:
            bank = await sql.get_bank_all(guild_id=str(ctx.guild.id))
            await ctx.send(bank[0])

    @commands.command(aliases=['quiz'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def trivia(self, ctx):
        money_name = await get_money(ctx=ctx)
        sql = self.bot.get_cog('Sql')
        if sql is not None:
            worth = {
                "easy": 100,
                "medium": 150,
                "hard": 200
            }
            response = requests.get('https://opentdb.com/api.php?amount=1&type=multiple')
            question = response.json()

            list = []
            alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u',
                    'v', 'w', 'x', 'y', 'z']

            choices = question['results'][0]["incorrect_answers"]
            choices.append(question['results'][0]['correct_answer'])
            random.shuffle(choices)

            for index, c in enumerate(choices, 1):
                list.append(f'{alph[index - 1].capitalize()}) *{html.unescape(c)}*')

            e = discord.Embed(title=f"{ctx.author.display_name}'s trivia question",
                              description=f"**{html.unescape(question['results'][0]['question'])}**\n*You have 15 seconds to answer*\n\n" + '\n'.join(
                                  list), color=0xFFA500)
            e.add_field(name='Worth', value=f"`{worth[question['results'][0]['difficulty']]}`", inline=True)
            e.add_field(name='Difficulty', value=f"`{question['results'][0]['difficulty'].capitalize()}`", inline=True)
            e.add_field(name='Category', value=f'`{question["results"][0]["category"].capitalize()}`')
            e.set_footer(text=f'Powered by: https://opentdb.com/')
            await ctx.send(embed=e)

            answer = choices.index(''.join(question['results'][0]['correct_answer']))

            try:
                m = await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=15.0)
            except asyncio.TimeoutError:
                await ctx.send('What the heck, you didn\'t answer!!')
                return
            if m.content.lower() == alph[answer]:
                await ctx.send(
                    f"Correct {random.choice(smart)}, you earned {worth[question['results'][0]['difficulty']]} {money_name}")
                await sql.deposit(amount=int(worth[question['results'][0]['difficulty']]),
                                  author_id=str(ctx.author.id))
            else:
                await ctx.send(
                    f"No {random.choice(dumb)}, the answer was: `{question['results'][0]['correct_answer'].capitalize()}`")

    @gamble.error
    async def search_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = f'Whoa Whoa slow down, please try again in {round(error.retry_after, 2)}s'
            await ctx.send(msg)

    @trivia.error
    async def trivia_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = f'Whoa Whoa slow down, please try again in {round(error.retry_after, 2)}s'
            await ctx.send(msg)


def setup(bot):
    bot.add_cog(Gambling(bot))
