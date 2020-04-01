import random

import discord
from discord.ext import commands
from utils.fun.data import tips

# import time
# import asyncio
# import re


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        name = str(member.guild.name)
        print(f'{member} has left {name} :(((')

    @commands.Cog.listener(name="on_message")
    async def cet(self, message):
        if '<:CST:672605143992369165>' in message.content:
            channel = message.channel
            await channel.send('<:CET:672963638306537483>')

        """
        dad = re.split("i\'?m", message.content.lower(), 1)
        if dad != " ":
            # await message.channel.send(f"Hi{dad} , I'm dad")
            print(dad)
        """

    @commands.Cog.listener()
    async def on_member_join(self, member):
        people = []
        for user in member.guild.members:
            people.append(user)
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Activity(type=discord.ActivityType.watching,
                                                                 name=f'{len(self.bot.users):,} users'))
        id = str(member.guild.id)
        name = str(member.guild)
        if "665249179496349716" in id:
            role = discord.utils.get(member.guild.roles, id=681158437434163268)
            await member.add_roles(role, atomic=True)
        print(f'{member} joined {name}')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        g = await self.bot.pg_con.fetch("SELECT * FROM guild_settings WHERE guild_id = $1", str(guild.id))
        if not g:
            await self.bot.pg_con.fetch("INSERT INTO guild_settings (guild_id) VALUES ($1)", str(guild.id))

    @commands.command()
    @commands.is_owner()
    async def insert(self, ctx):
        g = await self.bot.pg_con.fetch("SELECT * FROM guild_settings WHERE guild_id = $1", str(ctx.guild.id))
        if not g:
            await self.bot.pg_con.fetch("INSERT INTO guild_settings (guild_id) VALUES ($1)", str(ctx.guild.id))
            await ctx.send(f"Inserted {ctx.guild.id} into the database")
        else:
            await ctx.send(f"{ctx.guild.id} already in database")

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if random.randint(0, 30) == 15:
            await ctx.send(f"tip: {random.choice(tips).replace('%prefix%', str(ctx.prefix))}")


def setup(bot):
    bot.add_cog(Events(bot))
