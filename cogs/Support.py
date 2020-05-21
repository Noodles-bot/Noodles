from uuid import uuid4

import discord
from discord.ext import commands

from utils import checks
from utils.fun.data import color


class Support(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, name='support', aliases=['chat'])
    @commands.guild_only()
    async def support_group(self, ctx):
        await ctx.message.delete()
        support_id = str(uuid4())
        ch = await self.bot.pg_con.fetch("SELECT support_channel FROM guild_settings WHERE guild_id = $1",
                                         str(ctx.guild.id))
        await self.bot.pg_con.execute("INSERT INTO support (id, user_id, guild_id) "
                                      "VALUES ($1, $2, $3)", support_id, str(ctx.author.id), str(ctx.guild.id))
        support_channel = self.bot.get_channel(int(ch[0][0]))

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
        channel = await ctx.guild.create_text_channel(name=f"{ctx.author.name}-{support_id}", overwrites=overwrites,
                                                      category=ctx.channel.category)
        await self.bot.pg_con.execute("UPDATE support SET helper_id = $1, channel_id = $2 WHERE id = $3",
                                      str(ctx.author.id), str(channel.id), support_id)
        user = await self.bot.pg_con.fetch("SELECT user_id FROM support WHERE id = $1", support_id)
        user = await self.bot.fetch_user(user[0][0])
        channel = self.bot.get_channel(channel.id)
        await user.send("Helper found!, you'll get trough this <3")
        await ctx.send("Accepted")
        await channel.send(ctx.author.mention)

    @support_group.command()
    async def exit(self, ctx):
        try:
            db = await self.bot.pg_con.fetch(
                "SELECT user_id, channel_id FROM support WHERE helper_id = $1 OR user_id = $1",
                str(ctx.author.id))
            await self.bot.pg_con.execute("DELETE FROM support WHERE user_id = $1 OR helper_id = $1",
                                          str(ctx.author.id))
            user = await self.bot.fetch_user(db[0][0])
            channel = self.bot.get_channel(int(db[0][1]))
            await user.send("Session was ended, I hope we were able to help you <:PepeHug:675713788967649290>")
            await channel.send("Session ended")
        except TypeError or IndexError:
            await ctx.send("Session already ended or your currently not in one")

    @support_group.command()
    @checks.is_owner_or_admin()
    @commands.guild_only()
    async def channel(self, ctx, channel: discord.TextChannel):
        await self.bot.pg_con.execute('UPDATE guild_settings SET support_channel = $1 WHERE guild_id = $2',
                                      str(channel.id), str(ctx.guild.id))
        await ctx.send(f"Updated help channel to {channel.mention}")

    @commands.Cog.listener(name='on_message')
    async def dm_listener(self, message):
        if message.guild is None:
            db = await self.bot.pg_con.fetch("SELECT channel_id FROM support WHERE user_id = $1",
                                             str(message.author.id))
            if db:
                channel = self.bot.get_channel(int(db[0][0]))
                await channel.send(f'**Anonymous user:** {message.content}')

    @commands.Cog.listener(name='on_message')
    async def channel_listener(self, message):
        if message.guild is not None:
            db = await self.bot.pg_con.fetch("SELECT user_id FROM support WHERE helper_id = $1 AND channel_id = $2",
                                             str(message.author.id), str(message.channel.id))
            if db:
                user = await self.bot.fetch_user(int(db[0][0]))
                await user.send(f"**Helper:** {message.content}")


def setup(bot):
    bot.add_cog(Support(bot))
