import codecs
import datetime
import os
import pathlib
import platform
import time
from datetime import datetime

import aiohttp
import cpuinfo
import discord
import googletrans
import psutil
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands

from utils.fun.data import color
from utils.tools import embedinator

session = aiohttp.ClientSession()


def percentage(total, x):
    return "{:.2f}%".format(x * 100 / total) if total > 0 else 0


class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.trans = googletrans.Translator()
        self.thumb = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/COVID-19_Outbreak_World_Map.svg/langen-1000px-COVID-19_Outbreak_World_Map.svg.png?t="

    @commands.command(aliases=['about', 'ui'])
    async def userinfo(self, ctx, member: discord.Member = None):
        """Gets the info about you or someone else"""
        emote = {
            "idle": '<:idle:689360441956499501>',
            "offline": '<:offline:689360441822150701>',
            "dnd": '<:dnd:689360442098843672>',
            "online": '<:online:689360442048643285>',
            "streaming": '<:status_streaming:596576747294818305>'
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
        """Gets your secksy avatar"""
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
        """Gets the amount of users in current guild"""
        people = []
        for user in ctx.guild.members:
            people.append(user)
        name = ctx.guild.name
        embed = discord.Embed(title='Usercount',
                              description=f"""Number of epic gamers in {name}: {len(people)}""",
                              color=color)
        await ctx.send(embed=embed)

    @commands.command()
    async def embed(self, ctx, title, description=None):
        """Creates an custom embed with given text"""
        if description is None:
            member = ctx.author
            embed = discord.Embed(title=f'{title}',
                                  description=f'{title}',
                                  color=color)
            embed.set_author(name=f'{member}', icon_url=ctx.author.avatar_url)
        else:
            member = ctx.author
            embed = discord.Embed(title=f'{title}',
                                  description=f'{description}',
                                  color=color)
            embed.set_author(name=f'{member}', icon_url=ctx.author.avatar_url)

        await ctx.message.delete()
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
        """Creates an poll"""
        embed = discord.Embed(
            title=' ',
            description=f"**I need ur opinion:**\n{poll}",
            color=color)
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
    @commands.is_owner()
    async def cpu(self, ctx):
        """Gets info about the cpu"""
        cpus = []
        usage = psutil.cpu_percent(interval=1, percpu=True)
        for index, value in enumerate(usage, 1):
            cpus.append(f'**Thread {index}**: {value}%')

        info = cpuinfo.get_cpu_info()
        embed = discord.Embed(title='CPU info', color=color)
        embed.add_field(name='Main info:',
                        value=f'**CPU:** {info["brand"].replace("(R)", "®")}\n'
                              f'**CPU cores: **{psutil.cpu_count(logical=False)}\n'
                              f'**CPU threads: **{psutil.cpu_count()}\n'
                              f'**CPU frequency: **{info["hz_actual"]}',
                        inline=False)
        embed.add_field(name='CPU usage:',
                        value=f'**Average usage: **{psutil.cpu_percent(interval=1)}%\n\n' + '\n'.join(cpus),
                        inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def ram(self, ctx):
        """Gets info about the ram"""
        embed = discord.Embed(title='RAM info', color=color)
        embed.add_field(name='Main info:',
                        value=f'**Total RAM: **{round(psutil.virtual_memory().total / 1000000000, 2)}GB\n**Frequency: **Null',
                        inline=False)
        embed.add_field(name='Usage:',
                        value=f'**Usage: **{psutil.virtual_memory().percent}%\n**Available: **{round(psutil.virtual_memory().available / 1000000000, 2)}GB\n**Used: **{round(psutil.virtual_memory().used / 1000000000, 2)}GB',
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['perms'])
    async def permissions(self, ctx):
        """Gets the permissions for user"""
        perms = []
        negperms = []
        permissions = ctx.channel.permissions_for(ctx.author)

        embed = discord.Embed(title=':customs:  Permissions', color=color, timestamp=ctx.message.created_at)
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
        """Gets the bots permissions"""
        perms = []
        negperms = []
        permissions = ctx.channel.permissions_for(ctx.me)

        embed = discord.Embed(title=':customs:  Permissions', color=color, timestamp=ctx.message.created_at)
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
        """Shows all active cogs"""
        cogs = []
        for cog in self.bot.cogs:
            cogs.append(cog)
        embed = discord.Embed(title=f'Active cogs ({len(cogs) - 1}):', description='```' + '\n'.join(cogs) + '```',
                              color=color)
        await ctx.send(embed=embed)

    @commands.command()
    async def info(self, ctx):
        """Gets info about bot"""
        total = 0
        python_files = []
        cpp_files = []
        for path, subdirs, files in os.walk('.'):
            for name in files:
                if name.endswith('.py'):
                    python_files.append(name)
                if name.endswith('.cpp'):
                    cpp_files.append(name)
                try:
                    with codecs.open('./' + str(pathlib.PurePath(path, name)),
                                     'r', 'utf-8') as f:
                        for i, l in enumerate(f):
                            if len(l.strip()) != 0 and name.endswith('.py') or name.endswith('.c++') or name.endswith(
                                    '.c'):
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
            color=color)
        embed.add_field(
            name='**Bot Info**',
            value=f"**Current Uptime: **{days} days, {hours} hours, {minutes} minutes, {seconds} seconds\n"
                  + f"**Total Guilds: **{len(self.bot.guilds)}\n" +
                  f"**Available Emojis: **{len(self.bot.emojis)}\n" +
                  f"**Visible Users: **{len(self.bot.users) + 6000}\n" +
                  f"**discord.py Version: **{discord.__version__}\n" +
                  f"**Bot Owner: **{(await self.bot.application_info()).owner.mention}"
        )
        embed.add_field(
            name='_ _',
            value=f"**Total Commands and Subcommands: **{len(set(self.bot.walk_commands()))}\n"
                  + f"**Total Cogs: **{len(self.bot.cogs)}\n" +
                  f"**Lines of Code: **{total:,}\n" + '**Memory Usage: **' + str(
                psutil.virtual_memory()[2]) + '%\n' +
                  f'**Cached Messages: **{len(self.bot.cached_messages)}\n' +
                  f'**Number of Python files: **{len(python_files)}\n'
                  f'**Number of C++ files: **{len(cpp_files)}\n')
        embed.set_footer(text='Python ' + platform.python_version() + ' | C++20 | C18')
        embed.add_field(name='For more help',
                        value='[Join the discord server](https://discordapp.com/invite/Kzcr6pE)',
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def suggest(self, ctx, *, suggestion: str):
        """Sends a suggestion to the creator"""
        if isinstance(ctx.channel, discord.DMChannel):
            guild = "`No server! Sent via Private Message!`"
        else:
            guild = f"{ctx.guild.id} / {ctx.guild.name}"
        msg = embedinator(ctx.author, color, suggestion, formatUser=True)
        msg.set_footer(text=f'User: {ctx.author.id} | Guild: {guild}')
        owner = self.bot.get_user(357918459058978816)
        await owner.send(embed=msg)
        await ctx.message.add_reaction('<:check:694305541417336872>')

    @commands.group(invoke_without_command=True)
    async def say(self, ctx, *, msg):
        """Make the bot say anything"""
        await ctx.message.delete()
        await ctx.send(discord.utils.escape_mentions(msg))

    @commands.command()
    async def donate(self, ctx):
        """Helps the creator out and gives you some sweet perks"""
        await ctx.send(embed=discord.Embed(title='Click here to donate',
                                           url='https://www.patreon.com/DankDumpster',
                                           color=color))

    @commands.command()
    async def ping(self, ctx):
        """Shows the bot latency"""
        embed = discord.Embed(title=' ',
                              description=f'Pong! :ping_pong:\n*Bot latency:* {round(self.bot.latency * 1000, 3)}ms',
                              color=color)
        t1 = time.perf_counter()
        msg = await ctx.send(embed=embed)
        t2 = time.perf_counter()
        e1 = discord.Embed(title=' ',
                           description=f'Pong! :ping_pong:\n*Bot latency:* {round(self.bot.latency * 1000, 3)}ms\n*Actual response time:* {round((t2 - t1) * 1000, 3)}ms',
                           color=color)
        await msg.edit(embed=e1)

    @commands.command()
    async def guild(self, ctx):
        """Gets info about the current guild"""
        people = []
        roles = []
        for role in reversed(ctx.guild.roles):
            roles.append(role.mention)
        for user in ctx.guild.members:
            people.append(user)
        text_channel = len([x for x in ctx.guild.channels if type(x) == discord.channel.TextChannel])
        voice_channel = len([x for x in ctx.guild.channels if type(x) == discord.channel.VoiceChannel])
        features = ','.join(ctx.guild.features)

        embed = discord.Embed(title='', type='rich', description=f'**{ctx.guild.name} | {ctx.guild.id}**', color=color)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name='Main info',
                        value=f'**Channels:** {text_channel} <:687064764421373954:703317109819572274> | {voice_channel} <:687064782167212165:703317110000189620> \n'
                              f'**Verification Level:** {ctx.guild.verification_level}\n'
                              f'**Features:** {features.lower().capitalize()}\n'
                              f'**Emotes:** {len(ctx.guild.emojis)}\n'
                              f'**Created on:** {ctx.guild.created_at.strftime("%a, %#d %B %Y")}\n'
                              f'**Max File Size:** {int(ctx.guild.filesize_limit / 1000000)} MB\n'
                              f'**Max Bitrate:** {int(ctx.guild.bitrate_limit / 1000)} KB/s\n'
                              f'**Region:** {str(ctx.guild.region).capitalize()}\n', inline=False)
        embed.add_field(name='Members', value=f'**Total:** {len(people)}\n'
                                              f'**Owner:** {ctx.guild.owner.mention}', inline=False)
        embed.add_field(name=f'Top 10 roles ({len(ctx.guild.roles)} total)', value=''.join(roles[0:10]))
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        """Sends an invite to add the bot"""
        await ctx.send(
            'http://invite.noodles-bot.live/')

    @commands.command(aliases=['trans'])
    async def translate(self, ctx, *, message: commands.clean_content):
        """Tries to auto recognize the language you're trying to translate"""

        loop = self.bot.loop

        try:
            ret = await loop.run_in_executor(None, self.trans.translate, message)
        except Exception as e:
            return await ctx.send(f'An error occurred: {e.__class__.__name__}: {e}')

        embed = discord.Embed(title='Translated', color=color)
        src = googletrans.LANGUAGES.get(ret.src, '(auto-detected)').title()
        dest = googletrans.LANGUAGES.get(ret.dest, 'Unknown').title()
        embed.add_field(name=f'From {src}', value=ret.origin, inline=False)
        embed.add_field(name=f'To {dest}', value=ret.text, inline=False)
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def covid(self, ctx, country=None):
        """Gets info about country or info about the worlds cases"""
        if country is None:
            async with session.get('https://corona.lmao.ninja/v2/all') as resp:
                data = await resp.json(content_type=None)
            embed = discord.Embed(title='', color=color)
            embed.set_author(name=f'Coronavirus COVID-19 stats',
                             icon_url='https://i.imgur.com/htEqt0S.png')
            embed.add_field(name='<:sick:702950542648803358> **Confirmed**',
                            value=f'{data["cases"]:,}')
            embed.add_field(name='<:recoverd:702950542120321026> **Recovered**',
                            value=f'{data["recovered"]:,} (**{percentage(data["cases"], data["recovered"])}**)')
            embed.add_field(name='<:death:702950444036784238> **Deaths**',
                            value=f'{data["deaths"]:,} (**{percentage(data["cases"], data["deaths"])}**)')
            embed.add_field(name='<:date:702950443789189151> **Today\nconfirmed**',
                            value=f'+{data["todayCases"]:,} (**{percentage(data["cases"], data["todayCases"])}**)')
            embed.add_field(name='<:date:702950443789189151> **Today\ndeaths**',
                            value=f'+{data["todayDeaths"]:,} (**{percentage(data["cases"], data["todayDeaths"])}**)')
            embed.add_field(name='<:sick:702950443885789184> **Active**',
                            value=f'{data["active"]:,} (**{percentage(data["cases"], data["active"])}**)')
            embed.add_field(name=':hospital: **Critical**',
                            value=f'{data["critical"]:,} (**{percentage(data["active"], data["critical"])}**)')
            embed.add_field(name=':syringe: **Tests**',
                            value=f'{data["tests"]:,}')
            date = data["updated"] / 1000
            date = datetime.fromtimestamp(date).strftime("%#d %B %Y, %I:%M %p CET")
            embed.set_footer(text="Last updated at: " + date)
            embed.set_thumbnail(url=self.thumb)
            embed.set_image(url='attachment://stats.png')
            await ctx.send(embed=embed,
                           file=discord.File('stats.png',
                                             filename='stats.png'))
        else:
            try:
                async with session.get(f'https://corona.lmao.ninja/v2/countries/{country}') as resp:
                    data = await resp.json(content_type='application/json')
                # async with session.get(f'https://corona.lmao.ninja/v2/yesterday/{country}') as resp:
                #    y = await resp.json(content_type='text/html')
                # todayRecovered = data['recovered'] - y['recovered']
                embed = discord.Embed(title='', color=color)
                embed.set_author(name=f'Coronavirus COVID-19 stats - {data["country"]}',
                                 icon_url=data['countryInfo']['flag'])
                embed.add_field(name='<:sick:702950542648803358> **Confirmed**',
                                value=f'{data["cases"]:,}')
                embed.add_field(name='<:recoverd:702950542120321026> **Recovered**',
                                value=f'{data["recovered"]:,} (**{percentage(data["cases"], data["recovered"])}**)')
                embed.add_field(name='<:death:702950444036784238> **Deaths**',
                                value=f'{data["deaths"]:,} (**{percentage(data["cases"], data["deaths"])}**)')
                embed.add_field(name='<:date:702950443789189151> **Today\nconfirmed**',
                                value=f'+{data["todayCases"]:,} (**{percentage(data["cases"], data["todayCases"])}**)')
                # embed.add_field(name='<:date:702950443789189151> **Today\nrecovered**',
                #              value=f'+{todayRecovered:,} (**{percentage(data["cases"], todayRecovered)}**)')
                embed.add_field(name='<:date:702950443789189151> **Today\ndeaths**',
                                value=f'+{data["todayDeaths"]:,} (**{percentage(data["cases"], data["todayDeaths"])}**)')
                embed.add_field(name='<:sick:702950443885789184> **Active**',
                                value=f'{data["active"]:,} (**{percentage(data["cases"], data["active"])}**)')
                embed.add_field(name=':hospital: **Critical**',
                                value=f'{data["critical"]:,} (**{percentage(data["active"], data["critical"])}**)')
                embed.add_field(name=':syringe: **Tests**',
                                value=f'{data["tests"]:,}')
                date = data["updated"] / 1000
                date = datetime.fromtimestamp(date).strftime("%#d %B %Y, %I:%M %p CET")
                embed.set_footer(text="Last updated at: " + date)
                await ctx.send(embed=embed)
            except KeyError:
                async with session.get(f'https://corona.lmao.ninja/v2/countries/{country}') as resp:
                    data = await resp.json(content_type=None)
                embed = discord.Embed(title='', description=data["message"], color=color)
                await ctx.send(embed=embed)

    @covid.command()
    async def state(self, ctx, state=None):
        """"Gets info about state or states in the USA, affected by COVID-19"""
        if state is None:
            states = []
            async with session.get('https://corona.lmao.ninja/v2/states?sort=cases') as resp:
                data = await resp.json(content_type=None)
            async with session.get('https://corona.lmao.ninja/v2/countries/us') as resp:
                i = await resp.json(content_type=None)
            for index, d in enumerate(data, 0):
                if (index % 2) == 0:
                    states.append(f'{data[index]["state"]}: {data[index]["cases"]} [+{data[index]["todayCases"]}]')
                else:
                    states.append(
                        f'**{data[index]["state"]}: {data[index]["cases"]} [+{data[index]["todayCases"]}]**')
                if index >= 65:
                    break

            embed = discord.Embed(title='',
                                  description=f'<:sick:702950542648803358> Confirmed **{i["cases"]:,}** [+**{i["todayCases"]:,}**]\n'
                                              f'<:death:702950444036784238> Deaths **{i["deaths"]:,}** [+**{i["todayDeaths"]:,}**]'
                                              f'\n\n' + '\n'.join(states), color=color)
            embed.set_thumbnail(url='https://i.imgur.com/VeaLsEv.png')
            date = i["updated"] / 1000
            date = datetime.fromtimestamp(date).strftime("%#d %B %Y, %I:%M %p CET")
            embed.set_footer(text="Last updated at: " + date)
            embed.set_author(name=f'All states affected by Coronavirus COVID-19',
                             icon_url=i["countryInfo"]["flag"])
            await ctx.send(embed=embed)
        else:
            try:
                async with session.get(f'https://corona.lmao.ninja/v2/states/{state}') as resp:
                    data = await resp.json(content_type=None)
                embed = discord.Embed(title='', color=color)
                embed.set_author(name=f'Coronavirus COVID-19 stats - {data["state"]}')
                embed.add_field(name='<:sick:702950542648803358> **Confirmed**',
                                value=f'{data["cases"]:,}')
                embed.add_field(name='<:death:702950444036784238> **Deaths**',
                                value=f'{data["deaths"]:,} (**{percentage(data["cases"], data["deaths"])}**)')
                embed.add_field(name='<:date:702950443789189151> **Today\nconfirmed**',
                                value=f'+{data["todayCases"]:,} (**{percentage(data["cases"], data["todayCases"])}**)')
                embed.add_field(name='<:date:702950443789189151> **Today\ndeaths**',
                                value=f'+{data["todayDeaths"]:,} (**{percentage(data["cases"], data["todayDeaths"])}**)')
                embed.add_field(name='<:sick:702950443885789184> **Active**',
                                value=f'{data["active"]:,} (**{percentage(data["cases"], data["active"])}**)')
                embed.add_field(name=':syringe: **Tests**',
                                value=f'{data["tests"]:,}')
                await ctx.send(embed=embed)
            except KeyError:
                async with session.get(f'https://corona.lmao.ninja/v2/states/{state}') as resp:
                    data = await resp.json(content_type=None)
                embed = discord.Embed(title='', description=data["message"], color=color)
                await ctx.send(embed=embed)

    @covid.command()
    async def countries(self, ctx):
        """Gets top 65 countries affected by the COVID-19 virus"""
        countries = []
        async with session.get('https://corona.lmao.ninja/v2/countries?sort=cases') as resp:
            data = await resp.json(content_type=None)
        async with session.get('https://corona.lmao.ninja/v2/all') as resp:
            i = await resp.json(content_type=None)

        for index, d in enumerate(data, 0):
            if (index % 2) == 0:
                countries.append(f'{data[index]["country"]}: {data[index]["cases"]} [+{data[index]["todayCases"]}]')
            else:
                countries.append(f'**{data[index]["country"]}: {data[index]["cases"]} [+{data[index]["todayCases"]}]**')
            if index >= 65:
                break

        embed = discord.Embed(title='',
                              description=f'<:sick:702950542648803358> Confirmed **{i["cases"]:,}** [+**{i["todayCases"]:,}**]\n'
                                          f'<:death:702950444036784238> Deaths **{i["deaths"]:,}** [+**{i["todayDeaths"]:,}**]'
                                          f'\n\n' + '\n'.join(countries), color=color)
        embed.set_thumbnail(url=self.thumb)
        date = i["updated"] / 1000
        date = datetime.fromtimestamp(date).strftime("%#d %B %Y, %I:%M %p CET")
        embed.set_footer(text="Last updated at: " + date)
        embed.set_author(name=f'All countries affected by Coronavirus COVID-19',
                         icon_url='https://i.imgur.com/htEqt0S.png')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def pillow(self, ctx, user: discord.Member = None):
        """Gets info about user using the pillow library"""
        msg = await ctx.send("Getting info....")
        if user is None:
            user = ctx.author
        img = Image.open("C:/Users/Matthew/Documents/Scripts/Python/Discord/Noodles/utils/img.png")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("C:/Users/Matthew/Documents/Scripts/Python/Discord/Noodles/utils/fonts/arialbd.ttf",
                                  100)
        fontbig = ImageFont.truetype("C:/Users/Matthew/Documents/Scripts/Python/Discord/Noodles/utils/fonts/font.ttf",
                                     350)
        draw.text((200, 10), "User Info:", (255, 255, 255), font=fontbig)
        draw.text((50, 500), "Username: {}".format(user.name), (255, 255, 255),
                  font=font)
        draw.text((50, 700), "ID: {}".format(user.id), (255, 255, 255), font=font)
        draw.text((50, 900), "User Status: {}".format(user.status), (255, 255, 255), font=font)
        draw.text((50, 1100), "Account created: {}".format(user.created_at.strftime("%a, %#d %B %Y UTC")),
                  (255, 255, 255),
                  font=font)
        draw.text((50, 1300), "Nickname: {}".format(user.display_name), (255, 255, 255),
                  font=font)
        draw.text((50, 1500), "Users' Top Role: {}".format(user.top_role), (255, 255, 255),
                  font=font)
        draw.text((50, 1700), "User Joined: {}".format(user.joined_at.strftime("%a, %#d %B %Y UTC")), (255, 255, 255),
                  font=font)
        img.save('infoimg2.png')
        await ctx.send(file=discord.File("C:/Users/Matthew/Documents/Scripts/Python/Discord/Noodles/infoimg2.png",
                                         filename="infoimg2.png"))
        await msg.delete()

    @commands.command()
    async def apply(self, ctx, reason='No reason'):
        channel = self.bot.get_channel(699442491178614794)
        await channel.send(f'User {ctx.author.id} ({ctx.author}) has applied with the following description:'
                           f'\n```\n'
                           f'{reason}'
                           f'\n```'
                           f'Use the command ,tester add {ctx.author.id} or ,tester deny {ctx.author.id}')
        await ctx.author.send('Your application has been received, please be patient...')

    @commands.group()
    async def tester(self, ctx):
        pass

    @tester.command()
    async def add(self, ctx, user_id):
        await self.bot.pg_con.execute("UPDATE users SET tester = true WHERE user_id = $1", str(user_id))
        user = await self.bot.fetch_user(int(user_id))
        await user.send(
            "You have been added to the tester program, you now have access to commands that are still in testing")
        await ctx.send("Approved")

    @tester.command()
    async def deny(self, ctx, user_id):
        await self.bot.pg_con.execute("UPDATE users SET tester = false WHERE user_id = $1", str(user_id))
        user = await self.bot.fetch_user(int(user_id))
        await user.send("You have been rejected for the tester program")
        await ctx.send("Denied")


def setup(bot):
    bot.add_cog(Misc(bot))
