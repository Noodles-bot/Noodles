import discord
from discord.ext import commands


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


def setup(bot):
    bot.add_cog(Events(bot))
