from uuid import uuid4

import discord
from discord.ext import commands

from utils.fun.data import color


class Support(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, name='support', aliases=['chat'])
    @commands.guild_only()
    async def support_group(self, ctx):
        support_id = str(uuid4())
        await self.bot.pg_con.execute("INSERT INTO support (id, user_id, guild_id) "
                                      "VALUES ($1, $2, $3)", support_id, str(ctx.author.id), str(ctx.guild.id))
        support_channel = self.bot.get_channel(712836970229006357)

        embed = discord.Embed(title='Support needed!',
                              description=f'To talk use:\n{ctx.prefix}support accept {support_id}',
                              color=color)
        await support_channel.send('<@357918459058978816> someone wants to talk!', embed=embed)
        await ctx.author.send('A helper will be with you shortly')

    @support_group.command()
    @commands.guild_only()
    async def accept(self, ctx, *, support_id: str):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await ctx.guild.create_text_channel(name=f"{support_id}-{ctx.author.name}", overwrites=overwrites,
                                                      category=ctx.channel.category)
        await self.bot.pg_con.execute("UPDATE support SET helper_id = $1, channel_id = $2 WHERE id = $3",
                                      str(ctx.author.id), str(channel.id), support_id)
        user = await self.bot.pg_con.fetch("SELECT user_id FROM support WHERE id = $1", support_id)
        await ctx.send(user[0][0])
        user = await self.bot.fetch_user(user[0][0])
        channel = self.bot.get_channel(channel.id)
        await user.send("Helper found!, you'll get trough this <3")
        await ctx.send("Accepted")
        await channel.send(ctx.author.mention)

    @commands.Cog.listener(name='on_message')
    @commands.dm_only()
    async def dm_listener(self, message):
        db = await self.bot.pg_con.fetch("SELECT channel_id FROM support WHERE user_id = $1", str(message.author.id))
        if db:
            channel = self.bot.get_channel(db[0][0])
            await channel.send(f'**Anonymous user:** {message.content}')


def setup(bot):
    bot.add_cog(Support(bot))
