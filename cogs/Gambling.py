import discord
from discord.ext import commands
import random
import asyncio


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
                                        description=f"You won **{int(money * 2.5)}** ducc dollars\n\nNew balance is: **{int(round(bal[0][0], 0))}** ducc dollars",
                                        color=0x228B22)
                    win.add_field(name=ctx.author.name, value=f'Rolled `{num1}`', inline=True)
                    win.add_field(name=self.bot.user.name, value=f'Rolled `{num2}`', inline=True)
                    await ctx.send(embed=win)
                elif num1 < num2:  # bot wins
                    bal = await sql.get_balance(author_id=str(ctx.author.id))
                    lose = discord.Embed(title=f"{ctx.author.name}'s Gambling game",
                                         description=f"You lost **{money}** ducc dollars\n\nNew balance is: **{int(round(bal[0][0], 0))}** ducc dollars",
                                         color=0xFF0000)
                    lose.add_field(name=ctx.author.name, value=f'Rolled `{num1}`', inline=True)
                    lose.add_field(name=self.bot.user.name, value=f'Rolled `{num2}`', inline=True)
                    await ctx.send(embed=lose)
                elif num1 == num2:
                    await sql.deposit(amount=money, author_id=str(ctx.author.id))
                    bal = await sql.get_balance(author_id=str(ctx.author.id))
                    eq = discord.Embed(title=f"{ctx.author.name}'s Gambling game",
                                       description=f"You both rolled the same number\nYour bet will be refunded\n\nNew balance is: **{int(round(bal[0][0], 0))}** ducc dollars")
                    eq.add_field(name=ctx.author.name, value=f'Rolled `{num1}`', inline=True)
                    eq.add_field(name=self.bot.user.name, value=f'Rolled `{num2}`', inline=True)
                    await ctx.send(embed=eq)
            else:
                await ctx.send("Nice try, sadly you can't gamble your imaginary wealth")

    @commands.command(aliases=['slot'])
    async def slots(self, ctx, money):
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
                                description=f"**CONGRATS YOU WON!!**\n\nNew balance is:**{int(bal[0][0])} ducc dollars**\n\n{i}",
                                color=0x228B22)
            lose = discord.Embed(title='Slots',
                                 description=f"**You lost <:sad:666637638643744788>**\n\nNew balance is: **{int(bal[0][0])} ducc dollars**\n\n{i}",
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

    @gamble.error
    async def search_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = f'Whoa Whoa slow down, please try again in {round(error.retry_after, 2)}s'
            await ctx.send(msg)


def setup(bot):
    bot.add_cog(Gambling(bot))
