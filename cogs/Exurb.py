from asyncio import sleep

import discord
import praw
from discord.ext import commands

from utils import checks
from utils.fun.data import color
from utils.secret import *


class Exurb(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             username=username,
                             password=password,
                             user_agent=user_agent)
        members = self.bot.get_channel(690125363170508906)
        await members.edit(name=f"Sub members: {reddit.subreddit('exurb1a').subscribers}")

    @commands.command()
    @commands.is_owner()
    async def refresh(self, ctx):
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             username=username,
                             password=password,
                             user_agent=user_agent)
        members = self.bot.get_channel(690125363170508906)
        await members.edit(name=f"Sub members: {reddit.subreddit('exurb1a').subscribers}")
        people = []
        id = str(ctx.guild.id)
        for user in ctx.guild.members:
            people.append(user)
        if "564974738716360724" in id:
            members = self.bot.get_channel(689483433667199036)
            await members.edit(name=f'Members: {len(people):,}')
        await ctx.send('refreshed succesfully')

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel):
            return
        if "668213545909092354" == str(message.guild.id):
            role = discord.utils.get(message.guild.roles, id=697717366976675860)
            if role in message.author.roles:
                channel = self.bot.get_channel(697721101064732772)
                embed = discord.Embed(title='Jump link', url=message.jump_url, color=0xFF0000,
                                      description=message.content, timestamp=message.created_at)
                embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
                if message.attachments:
                    embed.set_image(url=message.attachments[0].url)
                embed.set_footer(text=message.id)

                msg = await channel.send(embed=embed)
                await msg.add_reaction('<:check:694305541417336872>')
                await msg.add_reaction('❌')
                emoji = ''
                channel = ''
                false = discord.Embed(title='Jump link', url=message.jump_url,
                                      description=message.content,
                                      color=0xFF0000, timestamp=message.created_at)
                false.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
                true = discord.Embed(title='Jump link', url=message.jump_url,
                                      description=message.content,
                                      color=0x228B22, timestamp=message.created_at)
                true.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
                while True:
                    if emoji == '<:check:694305541417336872>':
                        await msg.edit(embed=true)
                        await msg.clear_reactions()
                        break
                    elif emoji == '❌':
                        await msg.edit(embed=false)
                        await msg.clear_reactions()
                        break
                    res = await self.bot.wait_for('reaction_add')
                    if not res[1].bot:
                        emoji = str(res[0].emoji)

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_roles=True)
    @checks.is_guild(guild=668213545909092354)
    async def watchlist(self, ctx):
        l = []
        role = discord.utils.get(ctx.guild.roles, id=697717366976675860)
        for user in ctx.guild.members:
            if role in user.roles:
                l.append(user.mention)

        embed = discord.Embed(title=f"Watchlisted people ({len(l)}):", description='\n'.join(l), color=color)
        await ctx.send(embed=embed)

    @watchlist.command()
    @commands.has_permissions(manage_roles=True)
    @checks.is_guild(guild=668213545909092354)
    async def add(self, ctx, user: discord.Member, time: int = 5):
        time = time * 60
        if ctx.author == user:
            await ctx.send("You cannot watchlist yourself.")
        else:
            rolem = discord.utils.get(ctx.message.guild.roles, id=697717366976675860)
            if rolem not in user.roles:
                embed = discord.Embed(
                    title=f'User {user.name} has been successfully added to the watchlist for {time / 60}m.',
                    color=0xFFA500)
                embed.set_thumbnail(url=user.avatar_url)
                await ctx.send(embed=embed)
                await user.add_roles(rolem)
                await sleep(time)
                if rolem in user.roles:
                    try:
                        await user.remove_roles(rolem)
                        embed = discord.Embed(
                            title=f'User {user.name} has been removed of the watchlist automatically.', color=0xFFA500)
                        embed.add_field(name="Welcome back!", value="Behave this time")
                        embed.set_thumbnail(url=user.avatar_url)
                        await ctx.send(embed=embed)
                    except Exception:
                        print(f'User {user.name} could not be unmuted!')
            else:
                await ctx.send(f'User {user.mention} is already in the watchlist.')

    @watchlist.command()
    @commands.has_permissions(manage_roles=True)
    @checks.is_guild(guild=668213545909092354)
    async def remove(self, ctx, user: discord.Member):
        rolem = discord.utils.get(ctx.message.guild.roles, id=697717366976675860)
        if rolem in user.roles:
            embed = discord.Embed(title=f'User {user.name} has been removed from the watchlist manually.',
                                  color=0xFFA500)
            embed.add_field(name="Welcome back!", value="Behave this time")
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)
            await user.remove_roles(rolem)
        else:
            await ctx.send("User is not in watchlist")

    @watchlist.command()
    @commands.has_permissions(manage_roles=True)
    @checks.is_guild(guild=668213545909092354)
    async def perm(self, ctx, user: discord.Member):
        rolem = discord.utils.get(ctx.message.guild.roles, id=697717366976675860)
        if rolem not in user.roles:
            embed = discord.Embed(
                title=f'User {user.name} has been successfully added to the watchlist',
                color=0xFFA500)
            embed.add_field(name="Shhh!", value="<:shut:689407119728181437>")
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)
            await user.add_roles(rolem)
        else:
            await ctx.send(f"User {user.mention} is already in the watchlist")

    # TODO: make scoring system for this server
    """
    Commands:
    ,level add @role (xp)
    ,level remove @role
    ,levels {displays all levels in the following format in embed
    level 1 - @role [No ping] (xp needed)
    level 2 - @role (xp needed)
    .
    .
    .
    }
    
    and when it gives xp
    """

    # TODO: do this


"""
    [send embed of message]
    client.react(embed, :checkmark:)
    client.react(embed, :x:)
    
    on_add_reaction:
    if reaction==:checkmark: and message=embedFromBefore:
      embed.colour=green
      deleteAllReactions(embed)
    elif reaction==:x: and message=embedFromBefore
      embed.colour=red
      message.delete(TheMessageThatTheJumpLinkDirectsTo(originial message))
      deleteAllReactions(embed)
"""


def setup(bot):
    bot.add_cog(Exurb(bot))
