import asyncio
import html
import random

import discord
import requests
from discord.ext import commands

from utils.fun.data import *


def coinflip():
    return random.randint(0, 1)


def random_number(num1: int, num2: int):
    return random.randrange(num1, num2)


class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def get_money(self, ctx):
        if not ctx.guild:
            return ":ramen:"

        money = await self.bot.pg_con.fetch("SELECT money_name, guild_id FROM guild_settings WHERE guild_id = $1",
                                            str(ctx.guild.id))
        money = money[0][0]
        return money

    @commands.Cog.listener(name='on_message')
    async def db_insert(self, ctx):
        i = await self.bot.pg_con.fetch("SELECT * FROM waifu WHERE user_id = $1", str(ctx.author.id))
        if not i:
            await self.bot.pg_con.execute("INSERT INTO waifu (user_id) VALUES ($1)", str(ctx.author.id))

    async def claimed_by(self, user_id):
        i = await self.bot.pg_con.fetch("SELECT claimed_id, price FROM waifu WHERE user_id = $1", user_id)
        return i[0][0]

    async def claim(self, user_id, claim_id):
        await self.bot.pg_con.execute("UPDATE waifu SET claimed_id = $1 WHERE user_id = $1", user_id, claim_id)
        return

    async def get_price(self, user_id):
        i = await self.bot.pg_con.fetch("SELECT price, user_id FROM waifu WHERE user_id = $1", user_id)
        return i[0][0]

    async def get_waifus(self, user_id):
        return await self.bot.pg_con.fetch("SELECT user_id, price FROM waifu WHERE claimed_id = $1", user_id)

    @commands.command(aliases=['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        """Gets your balance or someone else's"""
        money_name = await self.get_money(ctx=ctx)
        member = ctx.author if not member else member
        author_id = str(member.id)
        sql = self.bot.get_cog('Sql')
        if sql is None:
            print("SQL is none")
        test = await self.bot.pg_con.fetch("SELECT bal, bank FROM users WHERE user_id = $1 AND NOT guild_id = $2",
                                           str(ctx.author.id), str(ctx.guild.id))
        if test:
            await self.bot.pg_con.execute("UPDATE users SET bal = $1, bank = $2 WHERE user_id = $3 AND guild_id = $4",
                                          test[0][0], test[0][1], str(ctx.author.id), str(ctx.guild.id))
        result = await sql.get_balance(author_id=author_id)
        bank = await sql.get_bank(author_id=author_id)
        embed = discord.Embed(title='Balance',
                              description=f'Bank: **{bank[0][0]}/{await sql.bank_size(author_id=author_id)}** {money_name}\n\nPocket: **{result[0][0]}** {money_name}',
                              color=color)

        await ctx.send(embed=embed)

    @commands.command(aliases=['give'])
    async def transfer(self, ctx, rec: discord.Member, amount):
        """Gives the user money"""
        money_name = await self.get_money(ctx=ctx)
        author_id = str(ctx.author.id)
        rec_id = str(rec.id)
        sql = self.bot.get_cog('Sql')
        if amount.lower() == 'all':
            amt = await sql.get_balance(author_id=str(ctx.author.id))
            amount = amt[0][0]
        if rec is ctx.author:
            await ctx.send("cant give yourself money smh my head")
            return

        if int(amount) <= 0:
            await ctx.send("stop trying to break the system")
            return

        result = await self.bot.pg_con.fetchrow("SELECT bal, user_id FROM users WHERE user_id = $1",
                                                author_id)
        if int(amount) > int(result[0]):
            await ctx.send(f"{ctx.author.mention} is way too poor to transfer {amount} {money_name}")
            return

        await sql.withdraw(amount=int(amount), author_id=author_id)
        await sql.deposit(amount=int(amount), author_id=rec_id)

        await ctx.send(
            f"Successfully transferred {amount} {money_name} to {ctx.guild.get_member(int(rec_id)).display_name}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def execute(self, ctx, *, command):
        await self.bot.pg_con.execute(command)
        await ctx.send(f'Executed:\n```sql\n{command}\n``` successfully')

    @commands.command()
    async def rich(self, ctx):
        """Gets the richest users in the guild"""
        money_name = await self.get_money(ctx=ctx)
        guild_id = str(ctx.guild.id)

        result = await self.bot.pg_con.fetch(
            "SELECT user_id, bal FROM public.users WHERE guild_id = $1 ORDER BY bal DESC LIMIT 5", guild_id)

        embed = discord.Embed(color=color)
        embed.set_author(name="Top 5 richest users")
        embed.add_field(name="#1",
                        value=f"User: {ctx.guild.get_member(int(result[0][0])).display_name} \n**{money_name}: {result[0][1]}**",
                        inline=False)
        embed.add_field(name="#2",
                        value=f"User: {ctx.guild.get_member(int(result[1][0])).display_name} \n**{money_name}: {result[1][1]}**",
                        inline=False)
        embed.add_field(name="#3",
                        value=f"User: {ctx.guild.get_member(int(result[2][0])).display_name} \n**{money_name}: {result[2][1]}**",
                        inline=False)
        embed.add_field(name="#4",
                        value=f"User: {ctx.guild.get_member(int(result[3][0])).display_name} \n**{money_name}: {result[3][1]}**",
                        inline=False)
        embed.add_field(name="#5",
                        value=f"User: {ctx.guild.get_member(int(result[4][0])).display_name} \n**{money_name}: {result[4][1]}**",
                        inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def search(self, ctx):
        """Searches in a random place for money"""
        money_name = await self.get_money(ctx=ctx)
        sql = self.bot.get_cog('Sql')
        places = ["Ducc's pond", "the dumpster", "your pocket", "the epic games store", "your shoe"]
        amt = random.randint(1, 150)
        if amt > 10:
            await sql.deposit(amount=amt, author_id=str(ctx.author.id))
            await ctx.send(f'You looked in {random.choice(places)} and found **{amt}** {money_name}')
        else:
            fine = random.randint(60, 120)
            await sql.withdraw(amount=fine, author_id=str(ctx.author.id))
            await ctx.send(f"You were caught talking to the swans, you were fined **{fine}** {money_name}")

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, amount: str):
        """Deposits you money to the bank"""
        money_name = await self.get_money(ctx=ctx)
        sql = self.bot.get_cog('Sql')
        if sql is not None:
            user1 = await sql.get_user(author_id=str(ctx.author.id), guild_id=str(ctx.guild.id))
            if amount.lower() == 'all':
                amt = await sql.bank_left(author_id=str(ctx.author.id))
                if amt > user1['bal']:
                    amount = amt - (amt - user1['bal'])
                else:
                    amount = amt
            if int(amount) > await sql.bank_left(author_id=str(ctx.author.id)):
                await ctx.send("You don't have enough space in your bank")
                return
            if user1['bal'] >= int(amount):
                await sql.depbank(amount=int(amount), author_id=str(ctx.author.id))
                await ctx.send(f'Deposited **{amount}** {money_name} to bank')
        else:
            print("Sql is None")

    @commands.command(aliases=['with'])
    async def withdraw(self, ctx, amount):
        """Withdraws your money from the bank"""
        money_name = await self.get_money(ctx=ctx)
        sql = self.bot.get_cog('Sql')
        if sql is not None:
            user1 = await sql.get_user(author_id=str(ctx.author.id), guild_id=str(ctx.guild.id))
            if amount.lower() == 'all':
                amt = await sql.get_bank(author_id=str(ctx.author.id))
                amount = amt[0][0]
            if user1['bank'] >= int(amount) >= 0:
                await sql.withbank(amount=int(amount), author_id=str(ctx.author.id))
                await ctx.send(f'Withdrawn **{amount}** {money_name} from bank')

    @commands.Cog.listener()
    async def on_command(self, ctx):
        sql = self.bot.get_cog('Sql')
        if sql is not None:
            usr = await sql.getbank(author_id=str(ctx.author.id))
            if usr is None:
                await sql.create_bank(author_id=str(ctx.author.id))
            user = await sql.getbank(author_id=str(ctx.author.id))
            await self.bot.pg_con.execute("UPDATE bank SET bankxp = $1 WHERE user_id = $2", user['bankxp'] + 1,
                                          str(ctx.author.id))

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def steal(self, ctx, member: discord.Member):
        """Steals money from a user, but be aware you can fail"""
        money_name = await self.get_money(ctx=ctx)
        sql = self.bot.get_cog('Sql')
        if member == ctx.author:
            await ctx.send("You can't steal from yourself pathetic piece of shit")
            return
        if sql is not None:
            num = random.randint(0, 2)
            steal = random.uniform(0.30, 0.50)
            fine = random.uniform(0.15, 0.20)
            msg = await ctx.send("Going in for the steal... :eyes:")
            await asyncio.sleep(random.randint(1, 3))
            usr = await sql.get_balance(author_id=str(member.id))
            if num == 0:  # user steals
                await sql.withdraw(amount=usr[0][0] * steal, author_id=str(member.id))
                await sql.deposit(amount=usr[0][0] * steal, author_id=str(ctx.author.id))
                await msg.edit(
                    content=f"You stole **{int(usr[0][0] * steal)}** successfully. F in the chat for {member.display_name}")
            else:  # user gets fined
                usr = await sql.get_balance(author_id=str(ctx.author.id))
                await sql.withdraw(amount=usr[0][0] * fine, author_id=str(ctx.author.id))
                await sql.deposit(amount=usr[0][0] * fine, author_id=str(member.id))
                await msg.edit(
                    content=f"You were caught trying to steal from {member.display_name} you gave them **{int(usr[0][0] * fine)}** {money_name}")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def beg(self, ctx):
        """Begs a random user in the server for money"""
        money_name = await self.get_money(ctx=ctx)
        sql = self.bot.get_cog('Sql')
        if sql is not None:
            people = [f.display_name for f in ctx.guild.members]
            amt = random.randint(1, 60)
            rand = random.randint(1, 1000)
            if rand == 666:
                amt = random.randint(900, 1300)
                await sql.deposit(amount=amt, author_id=str(ctx.author.id))
                await ctx.send(
                    f'**{random.choice(richppl)}** has donated {amt} {money_name} to {ctx.author.display_name}')
            if amt < 21:
                await ctx.send(f'**{random.choice(people)}:** {random.choice(saying)}')
            else:
                await sql.deposit(amount=amt, author_id=str(ctx.author.id))
                await ctx.send(
                    f'**{random.choice(people)}** has donated {amt} {money_name} to {ctx.author.display_name}')

    @commands.command(aliases=['pm'])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def postmeme(self, ctx):
        """Posts a meme to the web, you need an laptop for this"""
        money_name = await self.get_money(ctx=ctx)
        sql = self.bot.get_cog('Sql')
        if sql is not None:
            has_pc = await self.bot.pg_con.fetch("SELECT laptop FROM inventory WHERE user_id = $1", str(ctx.author.id))
            if has_pc[0][0] == 0:
                await ctx.send("hol' up you need an laptop first dumb dumb")
                return
            trending = random.randint(0, 10)
            if trending <= 2:
                broken_pc = random.randint(0, 50)
                downvote = random.randint(200, 10000)
                if broken_pc <= 2:
                    await self.bot.pg_con.execute("UPDATE inventory SET laptop = laptop - 1 WHERE user_id = $1",
                                                  str(ctx.author.id))
                    await ctx.send(
                        f'***OOF YOUR MEME DIED*** it got **-{downvote}** downvotes, and your laptop broke aswell F')
                    return
                else:
                    await ctx.send(f'***OOF YOUR MEME DIED*** it got **-{downvote}** downvotes')
                    return
            elif trending >= 8:
                votes = random.randint(200, 10000)
                cash = random.randint(150, 800)
                await sql.deposit(amount=cash, author_id=str(ctx.author.id))
                await ctx.send(f"**NICEEE** your meme got **{votes}** upvotes. You got **{cash}** {money_name}")
            else:
                votes = random.randint(30, 1000)
                cash = random.randint(20, 120)
                await sql.deposit(amount=cash, author_id=str(ctx.author.id))
                await ctx.send(
                    f"Your meme got **{votes}** upvotes, {random.choice(meme)}. You got **{cash}** {money_name}")

    @commands.command(aliases=['store'])
    async def shop(self, ctx):
        """Shows all the items in the shop"""
        i = []
        result = await self.bot.pg_con.fetch("SELECT * FROM shop")
        embed = discord.Embed(title='Shop', color=color)

        for items in result:
            if items['item_name'] == 'french':
                p = 'french horn'
            else:
                p = items['item_name']

            i.append(
                f'Item: {items["item_emote"]} {p.capitalize()} - {items["item_type"].capitalize()}\nPrice: **{items["item_price"]}**')

        embed.add_field(name="Items:",
                        value='\n\n'.join(sorted(i)),
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, item: str):
        """Buys an item from the store"""
        money_name = await self.get_money(ctx=ctx)
        sql = self.bot.get_cog('Sql')
        if sql is not None:

            item = item.lower()
            result = await self.bot.pg_con.fetch("SELECT item_id, item_price, item_name FROM shop WHERE item_name = $1",
                                                 item)
            bal = await sql.get_balance(author_id=str(ctx.author.id))
            if not result:
                await ctx.send(f"Not a valid item, for the list of items use {ctx.prefix}shop")
                return
            if result[0][1] > bal[0][0]:
                await ctx.send("Lmao ur way too poor")
                return

            await sql.withdraw(amount=int(result[0][1]), author_id=str(ctx.author.id))
            user = await self.bot.pg_con.fetch("SELECT * FROM inventory WHERE user_id = $1", str(ctx.author.id))
            if not user:
                await self.bot.pg_con.execute("INSERT INTO inventory (user_id) VALUES ($1)", str(ctx.author.id))
            await self.bot.pg_con.execute(
                f"UPDATE inventory SET {result[0][2]} = {result[0][2]} + 1 WHERE user_id = $1", str(ctx.author.id))
            await ctx.send(f"Bought {result[0][2]} for **{result[0][1]}** {money_name}")

    @commands.command(aliases=['inv'])
    async def inventory(self, ctx):
        """Gets the items in your inventory"""
        items = ['cookie', 'laptop', 'noodles', 'guitar', 'french']  # TODO: Make this automatic
        sql = self.bot.get_cog('Sql')
        if sql is not None:
            i = []
            inv = await self.bot.pg_con.fetch("SELECT * FROM inventory WHERE user_id = $1",
                                              str(ctx.author.id))
            for index, e in enumerate(items, 1):
                item = await self.bot.pg_con.fetch(
                    "SELECT item_name, item_emote, item_type FROM shop WHERE item_name = $1", e)
                if inv[0][index] == 0:
                    continue
                i.append(f"Item: {item[0][1]} {item[0][0]}\n"
                         f"Amount: {inv[0][index]}")
            embed = discord.Embed(title="Inventory", description='\n\n'.join(sorted(i)), color=color)
            await ctx.send(embed=embed)

    @commands.command()
    async def use(self, ctx, item: str):
        """Uses an item"""
        sql = self.bot.get_cog('Sql')
        if sql is not None:
            if item.lower() == 'cookie':
                inv = await self.bot.pg_con.fetch("SELECT cookie FROM inventory WHERE user_id = $1", str(ctx.author.id))
                if inv[0][0] == 0:
                    await ctx.send(f"Bruh moment, you don't even have {item}'s")
                    return
                await self.bot.pg_con.execute("UPDATE inventory SET cookie = cookie - 1 WHERE user_id = $1",
                                              str(ctx.author.id))
                await ctx.send("You ate the cookie! Yummy! :yum:")
            elif item.lower() == 'noodles':
                inv = await self.bot.pg_con.fetch("SELECT noodles FROM inventory WHERE user_id = $1",
                                                  str(ctx.author.id))
                if inv[0][0] == 0:
                    await ctx.send(f"Bruh moment, you don't even have {item}'s")
                    return
                await self.bot.pg_con.execute("UPDATE inventory SET noodles = noodles - 1 WHERE user_id = $1",
                                              str(ctx.author.id))
                await ctx.send("You ate the noodles! Slurp!! :yum:")
            else:
                await ctx.send("That's not an item smh my head")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def addshop(self, ctx, item_name, item_rarity: int, item_price: int, item_id: int, item_type, item_emote):
        await self.bot.pg_con.execute(
            "INSERT INTO shop (item_name, item_rarity, item_price, item_id, item_type, item_emote) VALUES ($1, $2, $3, $4, $5, $6)",
            item_name, item_rarity, item_price, item_id, item_type, item_emote)
        await self.bot.pg_con.execute(f"ALTER TABLE inventory ADD {item_name} INT DEFAULT 0 NOT NULL")
        await ctx.send(f"Added {item_name} to shop")

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def play(self, ctx):
        i = await self.bot.pg_con.execute("SELECT * WHERE user_id = $1 AND ")
        pass

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def gamble(self, ctx, money):
        """Gambles all your money away"""
        money_name = await self.get_money(ctx=ctx)
        sql = self.bot.get_cog('Sql')
        if sql is not None:
            user1 = await sql.get_user(author_id=str(ctx.author.id), guild_id=str(ctx.guild.id))
            if money.lower() == 'all':
                amt = await sql.get_balance(author_id=str(ctx.author.id))
                money = amt[0][0]
            if user1['bal'] >= int(money) > 0:
                num1 = random_number(1, 12)  # user
                num2 = random_number(1, 12)  # bot

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
        """Slot all your money"""
        money_name = await self.get_money(ctx=ctx)
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

    @commands.command(aliases=['quiz'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def trivia(self, ctx):
        """Test your big brain"""
        money_name = await self.get_money(ctx=ctx)
        sql = self.bot.get_cog('Sql')
        if sql is not None:
            worth = {
                "easy": 100,
                "medium": 150,
                "hard": 200
            }
            response = requests.get('https://opentdb.com/api.php?amount=1&type=multiple')
            question = response.json()

            l = []
            alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u',
                    'v', 'w', 'x', 'y', 'z']

            choices = question['results'][0]["incorrect_answers"]
            choices.append(question['results'][0]['correct_answer'])
            random.shuffle(choices)

            for index, c in enumerate(choices, 1):
                l.append(f'{alph[index - 1].capitalize()}) *{html.unescape(c)}*')

            e = discord.Embed(title=f"{ctx.author.display_name}'s trivia question",
                              description=f"**{html.unescape(question['results'][0]['question'])}**\n*You have 15 seconds to answer*\n\n" + '\n'.join(
                                  l), color=color)
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
                    f"No {random.choice(dumb)}, the answer was: `{html.unescape(question['results'][0]['correct_answer'].capitalize())}`")

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        """Get your daily cash"""
        if ctx.author == self.bot.user:
            return

        if ctx.author.bot:
            return

        author_id = str(ctx.author.id)

        i = await self.bot.pg_con.fetch("SELECT bal FROM users WHERE user_id = $1", author_id)
        if i[0] is None:
            await self.bot.pg_con.execute("INSERT INTO users (bal) VALUES (100)")

        user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1", author_id)

        await self.bot.pg_con.execute("UPDATE users SET bal = $1 WHERE user_id  = $2",
                                      user['bal'] + 500,
                                      author_id)

        await ctx.send(f'Added 500 {await self.get_money(ctx=ctx)}')

    @commands.group(name='waifu')
    @commands.guild_only()
    async def waifu(self, ctx):
        """This command works with subcommands check help waifu for more info"""
        money_name = await self.get_money(ctx=ctx)
        pass

    @waifu.command()
    @commands.guild_only()
    async def claim(self, ctx, user: discord.Member, amount: int):
        """Claim a user"""
        sql = self.bot.get_cog('Sql')
        price = await self.get_price(user_id=str(user.id))
        money_name = await self.get_money(ctx=ctx)
        bal = await sql.get_balance(author_id=str(ctx.author.id))
        if user.id == ctx.author.id:
            await ctx.send("You can't claim yourself smh")
            return
        if amount > bal[0][0]:
            await ctx.send("LMAO ur way too poor")
            return
        if amount > price:
            await self.bot.pg_con.execute("UPDATE waifu SET price = $1 WHERE user_id = $2", amount, str(user.id))
            await self.bot.pg_con.execute("UPDATE waifu SET claimed_id = $1 WHERE user_id = $2", str(ctx.author.id),
                                          str(user.id))
            await sql.withdraw(amount=amount, author_id=str(ctx.author.id))
            await ctx.send(f"Claimed {user.name} succesfully for {amount} {money_name}")
        else:
            claimed = await self.claimed_by(user_id=str(user.id))
            await ctx.send(
                f'Sorry bud, {user.display_name} is currently claimed by {ctx.guild.get_member(int(claimed)).display_name} for {price} {money_name}')
            return

    @waifu.command(aliases=['stats'])
    @commands.guild_only()
    async def about(self, ctx, member: discord.Member = None):
        """Get info about waifu"""
        waifus = []
        member = member or ctx.author
        claimed = await self.claimed_by(user_id=str(member.id))
        price = await self.get_price(user_id=str(member.id))
        claimed = int(claimed)
        if claimed == 0:
            claimed = 'Nobody'
        else:
            claimed = await self.bot.fetch_user(int(claimed))
            claimed = claimed.display_name
        w = await self.get_waifus(user_id=str(member.id))
        if not w:
            waifus.append('Nobody')
            amount = 0
        else:
            for waifu in w:
                try:
                    i = await self.bot.fetch_user(int(waifu["user_id"]))
                    waifus.append(f'{i.name}')
                except discord.ext.commands.errors.CommandInvokeError:
                    continue
            amount = len(waifus)
        embed = discord.Embed(title='', description=f'**Info about waifu {member.name}**\n\n', color=color)
        embed.add_field(name='**Price**:', value=price, inline=True)
        embed.add_field(name='**Claimed by:**', value=claimed, inline=True)
        embed.add_field(name=f'**Waifus ({amount}):**', value='\n'.join(sorted(waifus)), inline=False)
        await ctx.send(embed=embed)

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            i1 = error.retry_after / 60
            i2 = i1 / 60
            msg = f'Your daily money can only be used once a day, please try again in {int(i2)}h'
            await ctx.send(msg)

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

    @postmeme.error
    async def meme_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = f'Whoa Whoa slow down, please try again in {round(error.retry_after, 2)}s'
            await ctx.send(msg)

    @search.error
    async def search_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = f'Whoa Whoa slow down, please try again in {round(error.retry_after, 2)}s'
            await ctx.send(msg)

    @steal.error
    async def search_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = f'Whoa Whoa slow down, please try again in {round(error.retry_after, 2)}s'
            await ctx.send(msg)

    @beg.error
    async def search_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = f'Whoa Whoa slow down, please try again in {round(error.retry_after, 2)}s'
            await ctx.send(msg)


def setup(bot):
    bot.add_cog(Economy(bot))
