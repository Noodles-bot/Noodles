import re

import discord
from discord.ext import commands


class Shop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shop(self, ctx):

        result = await self.bot.pg_con.fetch("SELECT shop_items, shop_price FROM public.data")
        embed = discord.Embed(color=0xFFA500)
        embed.set_author(name="Shop")
        embed.add_field(name="#1",
                        value=f"Item: {result[0][0]} \n**Price: {result[0][1]}**",
                        inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, msg: str):
        author_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        item = msg.lower()
        data = await self.bot.pg_con.fetch("SELECT shop_items, shop_price FROM public.data")
        if item in data[0][0]:
            items = await self.bot.pg_con.fetchrow("SELECT shop_items, shop_price FROM data WHERE shop_items = $1",
                                                   item)
            user = await self.bot.pg_con.fetchrow(
                "SELECT bal, guild_id FROM users WHERE user_id = $1 AND guild_id = $2",
                author_id,
                guild_id)
            print(items)
            i2 = str(items)
            i1 = i2.lower()
            i = re.sub("<>_='abcdefghijklmnopqrsxyz", '', i1)
            print(i)
            if int(user[0][0]) >= int(i):
                await self.bot.pg_con.execute('UPDATE users SET $1 TRUE WHERE user_id = $2, guild_id = $3', item,
                                              author_id, guild_id)
                await self.bot.pg_con.execute('UPDATE users SET bal = 1$ WHERE user_id = $2, guild_id = $3',
                                              user['bal'] - items[0][1],
                                              author_id, guild_id)
                await ctx.send(f'Bought {item} succesfully')
            else:
                await ctx.send(f'You are way too poor to afford {item}')
        else:
            await ctx.send(f'{item} is not an valid item')

    @commands.command(aliases=['inv'])
    async def inventory(self, ctx):
        author_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)

        data = await self.bot.pg_con.fetchone('SELECT test FROM users WHERE user_id = $1, guild_id = $2', author_id,
                                              guild_id)
        if data[0]:
            await ctx.send('You have test in your inventory')
        else:
            await ctx.send('You have nothing in your inventory')


def setup(bot):
    bot.add_cog(Shop(bot))
