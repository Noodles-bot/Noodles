import re

import discord
from discord.ext import commands
import random
import asyncio

from utils.fun.data import saying, richppl, meme
from utils.tools import get_money


class Banking(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        money_name = await get_money(ctx=ctx)
        member = ctx.author if not member else member
        author_id = str(member.id)
        sql = self.bot.get_cog('Sql')
        if sql is None:
            print("SQL is none")
        result = await sql.get_balance(author_id=author_id)
        bank = await sql.get_bank(author_id=author_id)
        embed = discord.Embed(title='Balance',
                              description=f'Bank: **{bank[0][0]}/{await sql.bank_size(author_id=author_id)}** {money_name}\n\nPocket: **{result[0][0]}** {money_name}',
                              color=0xFFA500)

        await ctx.send(embed=embed)

    @commands.command(aliases=['give'])
    async def transfer(self, ctx, rec: discord.Member, amount):
        money_name = await get_money(ctx=ctx)
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

    @commands.command()
    @commands.is_owner()
    async def execute(self, ctx, *, command):
        money_name = await get_money(ctx=ctx)
        await self.bot.pg_con.execute(command)
        await ctx.send(f'Executed:\n```sql\n{command}\n``` successfully')

    @commands.command()
    async def rich(self, ctx):
        money_name = await get_money(ctx=ctx)
        guild_id = str(ctx.guild.id)

        result = await self.bot.pg_con.fetch(
            "SELECT user_id, bal FROM public.users WHERE guild_id = $1 ORDER BY bal DESC LIMIT 5", guild_id)

        embed = discord.Embed(color=0xFFA500)
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

    @commands.command(aliases=['db'])
    async def database(self, ctx):
        sql = self.bot.get_cog('Sql')
        await ctx.send(await sql.get_user(author_id=str(ctx.author.id), guild_id=str(ctx.guild.id)))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def search(self, ctx):
        money_name = await get_money(ctx=ctx)
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
        money_name = await get_money(ctx=ctx)
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
        money_name = await get_money(ctx=ctx)
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
            if await sql.bank_lvl_up(str(ctx.author.id)):
                i = True

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def steal(self, ctx, member: discord.Member):
        money_name = await get_money(ctx=ctx)
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
        money_name = await get_money(ctx=ctx)
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
        money_name = await get_money(ctx=ctx)
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
    bot.add_cog(Banking(bot))
