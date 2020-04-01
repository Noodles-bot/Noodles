import re

import discord
from discord.ext import commands


class Shop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def update_inv(self, item, id):
        if item.lower() == 'cookie':
            await self.bot.pg_con.execute("UPDATE inventory SET cookie = cookie + 1 WHERE user_id = $1", id)
            return
        if item.lower() == 'laptop':
            await self.bot.pg_con.execute("UPDATE inventory SET laptop = laptop + 1 WHERE user_id = $1", id)
            return
        if item.lower() == 'noodles':
            await self.bot.pg_con.execute("UPDATE inventory SET noodles = noodles + 1 WHERE user_id = $1", id)
            return

    async def get_inv(self, item, inv):
        if item.lower() == 'cookie':
            if int(inv['cookie']) > 0:
                item = await self.bot.pg_con.fetch(
                    "SELECT item_name, item_emote, item_type FROM shop WHERE item_name = 'cookie'")
                return f'Item: {item[0][1]} {item[0][0]}\nAmount: {inv["cookie"]}'
        elif item.lower() == 'laptop':
            if int(inv['laptop']) > 0:
                item = await self.bot.pg_con.fetch(
                    "SELECT item_name, item_emote, item_type FROM shop WHERE item_name = 'laptop'")
                return f'Item: {item[0][1]} {item[0][0]}\nAmount: {inv["laptop"]}'
        elif item.lower() == 'noodles':
            if int(inv['noodles']) > 0:
                item = await self.bot.pg_con.fetch(
                    "SELECT item_name, item_emote, item_type FROM shop WHERE item_name = 'noodles'")
                return f'Item: {item[0][1]} {item[0][0]}\nAmount: {inv["noodles"]}'

    @commands.command()
    async def shop(self, ctx):
        i = []
        result = await self.bot.pg_con.fetch("SELECT * FROM shop")
        embed = discord.Embed(title='Shop', color=0xFFA500)
        for items in result:
            i.append(
                f'Item: {items["item_emote"]} {items["item_name"].capitalize()} - {items["item_type"].capitalize()}\nPrice: **{items["item_price"]}**')
        embed.add_field(name="Items:",
                        value='\n\n'.join(i),
                        inline=False)
        embed.timestamp()

        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, item: str):
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
            await self.update_inv(item=result[0][2], id=str(ctx.author.id))
            await ctx.send(f"Bought {result[0][2]} for **{result[0][1]}** ducc dollars")

    @commands.command(aliases=['inv'])
    async def inventory(self, ctx):
        sql = self.bot.get_cog('Sql')
        if sql is not None:
            i = []
            inv = await self.bot.pg_con.fetch("SELECT cookie, laptop, noodles FROM inventory WHERE user_id = $1",
                                              str(ctx.author.id))
            for items in inv:
                if items == str(ctx.author.id):
                    continue
                a = await self.get_inv(item='cookie', inv=items)
                b = await self.get_inv(item='laptop', inv=items)
                c = await self.get_inv(item='noodles', inv=items)
                if a is not None:
                    i.append(a)
                if b is not None:
                    i.append(b)
                if c is not None:
                    i.append(c)
            embed = discord.Embed(title="Inventory", description='\n\n'.join(i), color=0xFFA500)
            await ctx.send(embed=embed)

    @commands.command()
    async def use(self, ctx, item: str):
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

    @commands.command()
    @commands.is_owner()
    async def addshop(self, ctx, item_name, item_rarity, item_price, item_id, item_type, item_emote):
        await self.bot.pg_con.execute(
            "INSERT INTO shop (item_name, item_rarity, item_price, item_id, item_type, item_emote) VALUES ($1, $2, $3, $4, $5, $6)",
            item_name, item_rarity, item_price, item_id, item_type, item_emote)


def setup(bot):
    bot.add_cog(Shop(bot))
