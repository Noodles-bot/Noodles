import codecs
import pathlib
import string

import psutil
import datetime
import discord
import os

from discord.ext import commands
from datetime import datetime

from utils.tools import embedinator


class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['about'])
    async def userinfo(self, ctx, member: discord.Member = None):
        emote = {
            "idle": '<:idle:689360441956499501>',
            "offline": '<:offline:689360441822150701>',
            "dnd": '<:dnd:689360442098843672>',
            "online": '<:online:689360442048643285>'
        }
        if member is None:
            member = ctx.author
        roles = []
        for role in member.roles:
            roles.append(role)

        embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

        embed.set_author(name=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Server name:", value=member.display_name)

        embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                        inline=True)
        embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                        inline=True)

        embed.add_field(name=f"Roles ({(len(roles)) - 1})",
                        value=" ".join([role.mention for role in roles if role.id != ctx.guild.id]))
        embed.add_field(name="Top role:", value=member.top_role.mention, inline=True)

        embed.add_field(name='Status:', value=emote[str(member.web_status)] + 'Web status' + '\n' + emote[
            str(member.mobile_status)] + 'Mobile Status' + '\n' + emote[
                                                  str(member.desktop_status)] + 'Desktop Status' + '\n', inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=['av', 'avata', 'pfp'])
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        avurl = str(member.avatar_url).replace("webp", "png")

        embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

        embed.set_author(name=f"{member} do be looking cute doe")

        embed.set_image(url=avurl)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=['users'])
    async def usercount(self, ctx):
        people = []
        for user in ctx.guild.members:
            people.append(user)
        name = ctx.guild.name
        embed = discord.Embed(title='Usercount',
                              description=f"""Number of epic gamers in {name}: {len(people)}""",
                              color=0xFFA500)
        await ctx.send(embed=embed)

    @commands.command()
    async def embed(self, ctx, title, description=None):
        if description is None:
            member = ctx.author
            embed = discord.Embed(title=f'{title}',
                                  description=f'{title}',
                                  color=0xFFA500)
            embed.set_author(name=f'{member}', icon_url=ctx.author.avatar_url)
        else:
            member = ctx.author
            embed = discord.Embed(title=f'{title}',
                                  description=f'{description}',
                                  color=0xFFA500)
            embed.set_author(name=f'{member}', icon_url=ctx.author.avatar_url)

        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command()
    async def status(self, ctx):
        emote = {
            "idle": '<:idle:689360441956499501>',
            "offline": '<:offline:689360441822150701>',
            "dnd": '<:dnd:689360442098843672>',
            "online": '<:online:689360442048643285>'
        }
        member = ctx.author
        embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
        embed.add_field(name='Status:', value=emote[str(member.web_status)] + 'Web status' + '\n' + emote[
            str(member.mobile_status)] + 'Mobile Status' + '\n' + emote[
                                                  str(member.desktop_status)] + 'Desktop Status' + '\n', inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=['fav', 'fetch'])
    async def fetchav(self, ctx, user_id: int):
        user = await self.bot.fetch_user(user_id)
        embed = discord.Embed(title='', description=f'**Showing the secksy avatar of: {user.name}**',
                              color=ctx.author.color)
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['src'])
    @commands.is_owner()
    async def source(self, ctx, *, command):
        import inspect
        try:
            command = self.bot.get_command(command).callback
        except:
            command = eval(command)
        source = inspect.getsource(command)
        await ctx.send('```py\n' + source.replace('```', '``') + '\n```')

    @commands.command(aliases=['poll'])
    async def vote(self, ctx, *, poll):
        embed = discord.Embed(
            title=' ',
            description=f"**I need ur opinion:**\n{poll}",
            color=0xFFA500)
        embed.set_footer(
            text=f'Vote created by {ctx.author.name}',
            icon_url=ctx.author.avatar_url_as(static_format='png'))
        embed.timestamp = ctx.message.created_at
        vote = await ctx.send(embed=embed)
        await vote.add_reaction('<:upvote:666047214082195456>')
        await vote.add_reaction('<:downvote:666047257312886834>')
        await vote.add_reaction('<:Perhaps:668675600940138516>')
        await ctx.message.delete()

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(color=0xFFA500)
        embed.add_field(name='info', value='**Uptime:** ')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def cpu(self, ctx):
        list = []
        usage = psutil.cpu_percent(interval=1, percpu=True)
        for index, value in enumerate(usage, 1):
            list.append(f'**Thread {index}**: {value}%')

        embed = discord.Embed(title='CPU info', color=0xFFA500)
        embed.add_field(name='Main info:',
                        value=f'**CPU cores: **{psutil.cpu_count(logical=False)}\n**CPU threads: **{psutil.cpu_count()}\n',
                        inline=False)
        embed.add_field(name='CPU usage:',
                        value=f'**Average usage: **{psutil.cpu_percent(interval=1)}%\n\n' + '\n'.join(list),
                        inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def ram(self, ctx):
        embed = discord.Embed(title='RAM info', color=0xFFA500)
        embed.add_field(name='Main info:',
                        value=f'**Total RAM: **{round(psutil.virtual_memory().total / 1000000000, 2)}GB\n**Frequency: **3200Mhz',
                        inline=False)
        embed.add_field(name='Usage:',
                        value=f'**Usage: **{psutil.virtual_memory().percent}%\n**Available: **{round(psutil.virtual_memory().available / 1000000000, 2)}GB\n**Used: **{round(psutil.virtual_memory().used / 1000000000, 2)}GB',
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['perms'])
    async def permissions(self, ctx):
        perms = []
        negperms = []
        permissions = ctx.channel.permissions_for(ctx.author)

        embed = discord.Embed(title=':customs:  Permissions', color=0xFFA500, timestamp=ctx.message.created_at)
        embed.add_field(name='Server', value=ctx.guild)
        embed.add_field(name='Channel', value=ctx.channel, inline=False)

        for item, valueBool in permissions:
            if valueBool:
                value = ':white_check_mark:'
                perms.append(f'{value}{item}')
            else:
                value = ':x:'
                negperms.append(f'{value}{item}')

        embed.add_field(name='Allowed permissions', value='\n'.join(perms), inline=True)
        embed.add_field(name='Denied permissions', value='\n'.join(negperms), inline=True)

        await ctx.send(embed=embed)

    @commands.command(aliases=['botperms'])
    async def botpermissions(self, ctx):
        perms = []
        negperms = []
        permissions = ctx.channel.permissions_for(ctx.me)

        embed = discord.Embed(title=':customs:  Permissions', color=0xFFA500, timestamp=ctx.message.created_at)
        embed.add_field(name='Server', value=ctx.guild)
        embed.add_field(name='Channel', value=ctx.channel, inline=False)

        for item, valueBool in permissions:
            if valueBool:
                value = ':white_check_mark:'
                perms.append(f'{value}{item}')
            else:
                value = ':x:'
                negperms.append(f'{value}{item}')

        embed.add_field(name='Allowed permissions', value='\n'.join(perms), inline=True)
        embed.add_field(name='Denied permissions', value='\n'.join(negperms), inline=True)

        await ctx.send(embed=embed)

    @commands.command()
    async def cogs(self, ctx):
        cogs = []
        for cog in self.bot.cogs:
            cogs.append(cog)
        embed = discord.Embed(title=f'Active cogs ({len(cogs) - 1}):', description='```' + '\n'.join(cogs) + '```',
                              color=0xFFA500)
        await ctx.send(embed=embed)

    @commands.command()
    async def info(self, ctx):
        """Command made by nickofolas#0660"""
        total = 0
        python_files = []
        for path, subdirs, files in os.walk('.'):
            for name in files:
                if name.endswith('.py'):
                    python_files.append(name)
                try:
                    with codecs.open('./' + str(pathlib.PurePath(path, name)),
                                     'r', 'utf-8') as f:
                        for i, l in enumerate(f):
                            if len(l.strip()) != 0 and name.endswith('.py'):
                                total += 1
                except:
                    pass
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = discord.Embed(
            title='',
            description='',
            color=0xFFA500)
        embed.add_field(
            name='**Bot Info**',
            value=
            f"**Current Uptime: **{days} days, {hours} hours, {minutes} minutes, {seconds} seconds\n"
            + f"**Total Guilds: **{len(self.bot.guilds)}\n" +
            f"**Available Emojis: **{len(self.bot.emojis)}\n" +
            f"**Visible Users: **{len(self.bot.users)}\n" +
            f"**discord.py Version: **{discord.__version__}\n" +
            f"**Bot Owner: **{(await self.bot.application_info()).owner.mention}"
        )
        embed.add_field(
            name='_ _',
            value=
            f"**Total Commands and Subcommands: **{len(set(self.bot.walk_commands()))}\n"
            + f"**Total Cogs: **{len(self.bot.cogs)}\n" +
            f"**Lines of Code: **{total:,}\n" + '**Memory Usage: **' + str(
                psutil.virtual_memory()[2]) + '%\n' +
            f'**Cached Messages: **{len(self.bot.cached_messages)}\n' +
            f'**Number of Files: **{len(python_files)}\n')
        await ctx.send(embed=embed)

    @commands.command()
    async def ascii(self, ctx, *, i):
        await ctx.send(' '.join(format(ord(x), 'b') for x in i))

    @commands.command()
    async def suggest(self, ctx, *, suggestion: str):
        if isinstance(ctx.channel, discord.DMChannel):
            guild = "`No server! Sent via Private Message!`"
        else:
            guild = f"{ctx.guild.id} / {ctx.guild.name}"
        msg = embedinator(ctx.author, 0xFFA500, suggestion, formatUser=True)
        msg.set_footer(text=f'User: {ctx.author.id} | Guild: {guild}')
        owner = self.bot.get_user(357918459058978816)
        await owner.send(embed=msg)
        await ctx.message.add_reaction('<:check:694305541417336872>')

    @commands.group(invoke_without_command=True)
    async def say(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(discord.utils.escape_mentions(msg))

    @commands.command()
    async def donate(self, ctx):
        await ctx.send(embed=discord.Embed(title='Click here to donate',
                                           url='https://www.paypal.com/donate/?token=fDj3XvUlVRXKKC94oQqqoiD26yQo41bzMCqs_-hu6P464XFFrzlKQnxkraualZlAkN1WFm&country.x=NL&locale.x=en_NL&Z3JncnB0=',
                                           color=0xFFA500))


def setup(bot):
    bot.add_cog(Misc(bot))
