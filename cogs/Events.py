import discord
from discord.ext import commands


# import time
# import asyncio
# import re


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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
        id = str(member.guild.id)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                 name=f'{len(bot.users):,} users | {len(bot.guilds)} guilds'))
        if "665249179496349716" in id:
            if member.bot:
                role = discord.utils.get(member.guild.roles, id=665390281100623872)
            else:
                role = discord.utils.get(member.guild.roles, id=681163948149702776)
            await member.add_roles(role, atomic=True)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        g = await self.bot.pg_con.fetch("SELECT * FROM guild_settings WHERE guild_id = $1", str(guild.id))
        if not g:
            await self.bot.pg_con.fetch("INSERT INTO guild_settings (guild_id) VALUES ($1)", str(guild.id))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def insert(self, ctx):
        g = await self.bot.pg_con.fetch("SELECT * FROM guild_settings WHERE guild_id = $1", str(ctx.guild.id))
        if not g:
            await self.bot.pg_con.fetch("INSERT INTO guild_settings (guild_id) VALUES ($1)", str(ctx.guild.id))
            await ctx.send(f"Inserted {ctx.guild.id} into the database")
        else:
            await ctx.send(f"{ctx.guild.id} already in database")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, discord.Forbidden):
            await ctx.send("Looks like I'm missing permissions in this server, if you want to use these commands, "
                           "please update the perms")
        elif isinstance(error, commands.CommandOnCooldown):
            pass
        else:
            await ctx.message.add_reaction('⚠')
            emoji = ''

            while True:
                if emoji == '⚠':
                    await ctx.message.clear_reactions()
                    embed = discord.Embed(title='ERROR!',
                                          description=f'```\n{error}\n```',
                                          color=0xFFA500)
                    await ctx.send(embed=embed)
                    break
                try:
                    res = await self.bot.wait_for('reaction_add', timeout=10.0)
                except:
                    break
                if str(res[1]) == str(ctx.author):
                    emoji = str(res[0].emoji)
                    await ctx.message.remove_reaction(res[0].emoji, res[1])


def setup(bot):
    bot.add_cog(Events(bot))
