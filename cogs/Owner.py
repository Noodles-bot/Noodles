import inspect
import os
import subprocess

import aiohttp
import discord
import io
import traceback
import textwrap
import copy
import asyncio
import json
import aiofiles
import requests
import matplotlib.pyplot as plt

from matplotlib.ticker import MultipleLocator
from typing import Optional
from contextlib import redirect_stdout
from discord.ext import commands
from imgurpython import ImgurClient

from utils import checks

client_id = 'ce5aa0309c82ab2'
client_secret = '4d963d5d20242373d3152b10aa9873c2143dce6f'

client = ImgurClient(client_id, client_secret)

session = aiohttp.ClientSession()


def cleanup_code(content):
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    return content.strip('` \n')


def rearrange(timeline, confirmed, recovered, deaths, active):
    i = 0
    while confirmed[i] == 0:
        i += 1
    return timeline[i:], confirmed[i:], logarify(recovered[i:]), logarify(deaths[i:]), logarify(active[i:])


def logarify(y):
    for i in range(len(y)):
        if y[i] == 0:
            y[i] = 1
    return y


class LengthError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class PlotEmpty(Exception):
    def __init__(self, *args):
        super().__init__(*args)


def human_format(num: int) -> str:
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000
    try:
        if f"{num:.1f}".split(".")[1] != "0":
            return '{:.1f}{}'.format(num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
    except:
        pass
    return '{}{}'.format(int(num), ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


async def _from_json(fpath):
    async with aiofiles.open(fpath, "r") as f:
        jso = json.load(f)
    return jso


async def get_data(country=None):
    timeline = []
    confirmed = []
    recovered = []
    active = []
    deaths = []
    if country is None:
        data = requests.get('https://covid19-update-api.herokuapp.com/api/v1/cases')
        data = data.json()
        death = requests.get('https://covid19-update-api.herokuapp.com/api/v1/death')
        death = death.json()
        for d in data["graphs"]['totalCases']["categories"]:
            timeline.append(d)
            confirmed.append(data["graphs"]['totalCases']["data"])
            recovered.append(data["graphs"]['totalCured']["data"])
            active.append(data["graphs"]["activeCases"]['data'])
            deaths.append(death["graphs"]["totalDeaths"]["data"])
    else:
        data = requests.get('https://covid19-update-api.herokuapp.com/api/v1/cases')
        data = data.json()
        death = requests.get('https://covid19-update-api.herokuapp.com/api/v1/death')
        death = death.json()
        for d in data["graphs"]['totalCases']["categories"]:
            timeline.append(d)
            confirmed.append(data["graphs"]['totalCases']["data"])
            recovered.append(data["graphs"]['totalCured']["data"])
            active.append(data["graphs"]["activeCases"]['data'])
            deaths.append(death["graphs"]["totalDeaths"]["data"])

    if not len(timeline):
        raise PlotEmpty(f"Plot empty, length : {len(timeline)}")

    return rearrange(timeline, confirmed, recovered, deaths, active)


class GlobalChannel(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            return await commands.TextChannelConverter().convert(ctx, argument)
        except commands.BadArgument:
            # Not found... so fall back to ID + global lookup
            try:
                channel_id = int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(f'Could not find a channel by ID {argument!r}.')
            else:
                channel = ctx.bot.get_channel(channel_id)
                if channel is None:
                    raise commands.BadArgument(f'Could not find a channel by ID {argument!r}.')
                return channel


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    async def get_money(self, ctx):
        if not ctx.guild:
            return ":ramen:"

        money = await self.bot.pg_con.fetch("SELECT money_name, guild_id FROM guild_settings WHERE guild_id = $1",
                                            str(ctx.guild.id))

        if str(ctx.guild.id) not in money:
            return ':ramen:'

        money = money[0][0]
        return money

    def cleanup_code(self, content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    @commands.command()
    @commands.is_owner()
    async def nickname(self, ctx, *, name: str = None):
        try:
            await ctx.guild.me.edit(nick=name)
            if name:
                await ctx.send(f"Successfully changed nickname to **{name}**")
            else:
                await ctx.send("Successfully removed nickname")
        except Exception as err:
            await ctx.send(err)

    @commands.command(aliases=['setmoney'])
    @checks.is_owner_or_admin()
    async def set_money(self, ctx, *, name):
        await self.bot.pg_con.execute("UPDATE guild_settings SET money_name = $1 WHERE guild_id = $2", name,
                                      str(ctx.guild.id))
        await ctx.send(f"New money name is `{name}`")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.bot.AppInfo = await self.bot.application_info()
        people = []
        roles = []
        for role in reversed(guild.roles):
            roles.append(role.mention)
        for user in guild.members:
            people.append(user)
        text_channel = len([x for x in guild.channels if type(x) == discord.channel.TextChannel])
        voice_channel = len([x for x in guild.channels if type(x) == discord.channel.VoiceChannel])
        features = ','.join(guild.features)
        embed = discord.Embed(title='Joined Guild', type='rich', description=f'**{guild.name} | {guild.id}**',
                              color=0x228B22)
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name='Main info',
                        value=f'**Channels:** {text_channel} <:text_channel:696498775711154196> | {voice_channel} <:voice_channel:696498810721009725>\n'
                              f'**Verification Level:** {guild.verification_level}\n'
                              f'**Features:** {features.lower().capitalize()}\n'
                              f'**Emotes:** {len(guild.emojis)}\n'
                              f'**Created on:** {guild.created_at.strftime("%a, %#d %B %Y")}\n'
                              f'**Max File Size:** {int(guild.filesize_limit / 1000000)} MB\n'
                              f'**Max Bitrate:** {int(guild.bitrate_limit / 1000)} KB/s\n'
                              f'**Region:** {str(guild.region).capitalize()}\n', inline=False)
        embed.add_field(name='Members', value=f'**Total:** {len(people)}\n'
                                              f'**Owner:** {guild.owner.mention}', inline=False)
        await self.bot.AppInfo.owner.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        self.bot.AppInfo = await self.bot.application_info()
        people = []
        for user in guild.members:
            people.append(user)
        text_channel = len([x for x in guild.channels if type(x) == discord.channel.TextChannel])
        voice_channel = len([x for x in guild.channels if type(x) == discord.channel.VoiceChannel])
        features = ','.join(guild.features)
        embed = discord.Embed(title='Left Guild', type='rich', description=f'**{guild.name} | {guild.id}**',
                              color=0xFF0000)
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name='Main info',
                        value=f'**Channels:** {text_channel} <:text_channel:696498775711154196> | {voice_channel} <:voice_channel:696498810721009725>\n'
                              f'**Verification Level:** {guild.verification_level}\n'
                              f'**Features:** {features.lower().capitalize()}\n'
                              f'**Emotes:** {len(guild.emojis)}\n'
                              f'**Created on:** {guild.created_at.strftime("%a, %#d %B %Y")}\n'
                              f'**Max File Size:** {int(guild.filesize_limit / 1000000)} MB\n'
                              f'**Max Bitrate:** {int(guild.bitrate_limit / 1000)} KB/s\n'
                              f'**Region:** {str(guild.region).capitalize()}\n', inline=False)
        embed.add_field(name='Members', value=f'**Total:** {len(people)}\n'
                                              f'**Owner:** {guild.owner.mention}', inline=False)
        await self.bot.AppInfo.owner.send(embed=embed)

    @commands.command(name='eval')
    @commands.is_owner()
    async def eval_(self, ctx, *, body: str):

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except Exception:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def sudo(self, ctx, channel: Optional[GlobalChannel], who: discord.User, *, command: str):
        msg = copy.copy(ctx.message)
        channel = channel or ctx.channel
        msg.channel = channel
        msg.author = channel.guild.get_member(who.id) or who
        msg.content = ctx.prefix + command
        new_ctx = await self.bot.get_context(msg, cls=type(ctx))
        await self.bot.invoke(new_ctx)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def do(self, ctx, times: int, *, command):
        msg = copy.copy(ctx.message)
        msg.content = ctx.prefix + command

        new_ctx = await self.bot.get_context(msg, cls=type(ctx))

        for i in range(times):
            await new_ctx.reinvoke()

    @commands.command(pass_context=True, hidden=True, aliases=['console'])
    @commands.is_owner()
    async def repl(self, ctx):
        variables = {
            'ctx': ctx,
            'bot': self.bot,
            'message': ctx.message,
            'guild': ctx.guild,
            'channel': ctx.channel,
            'author': ctx.author,
            '_': None,
        }

        if ctx.channel.id in self.sessions:
            await ctx.send('Already running a REPL session in this channel. Exit it with `exit()`.')
            return

        self.sessions.add(ctx.channel.id)
        await ctx.send('Enter code to execute. `exit()` to exit.')

        def check(m):
            return m.author.id == ctx.author.id and \
                   m.channel.id == ctx.channel.id and \
                   m.content.startswith('`')

        while True:
            try:
                response = await self.bot.wait_for('message', check=check, timeout=10.0 * 60.0)
            except asyncio.TimeoutError:
                await ctx.send('Exiting REPL session.')
                self.sessions.remove(ctx.channel.id)
                break

            cleaned = self.cleanup_code(response.content)

            if cleaned in ('quit', 'exit', 'exit()'):
                await ctx.send('Exiting.')
                self.sessions.remove(ctx.channel.id)
                return

            executor = exec
            if cleaned.count('\n') == 0:
                try:
                    code = compile(cleaned, '<repl session>', 'eval')
                except SyntaxError:
                    pass
                else:
                    executor = eval

            if executor is exec:
                try:
                    code = compile(cleaned, '<repl session>', 'exec')
                except SyntaxError as e:
                    await ctx.send(self.get_syntax_error(e))
                    continue

            variables['message'] = response

            fmt = None
            stdout = io.StringIO()

            try:
                with redirect_stdout(stdout):
                    result = executor(code, variables)
                    if inspect.isawaitable(result):
                        result = await result
            except Exception as e:
                value = stdout.getvalue()
                fmt = f'```py\n{value}{traceback.format_exc()}\n```'
            else:
                value = stdout.getvalue()
                if result is not None:
                    fmt = f'```py\n{value}{result}\n```'
                    variables['_'] = result
                elif value:
                    fmt = f'```py\n{value}\n```'

            try:
                if fmt is not None:
                    if len(fmt) > 2000:
                        await ctx.send('Content too big to be printed.')
                    else:
                        await ctx.send(fmt)
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                await ctx.send(f'Unexpected error: `{e}`')

    @commands.command()
    @commands.is_owner()
    async def select(self, ctx, code):
        y = await self.bot.pg_con.fetch(code)
        await ctx.send('```\n' +
                       str(y) +
                       '\n````')

    @commands.command()
    @commands.is_owner()
    async def plot_csv(self, ctx, country=None):  # TODO: Fix the data source
        timeline, confirmed, recovered, deaths, active = await get_data(country)
        fig, ax = plt.subplots()
        ax.spines['bottom'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        print(len(deaths[0]))
        for x in range(len(recovered[0]), len(confirmed[0])):
            recovered[0].insert(0, 0)
        ax.xaxis.set_major_locator(MultipleLocator(7))
        ax.plot(timeline, confirmed[0], ".-", color="orange")
        ax.plot(timeline, active[0], ".-", color="yellow", alpha=0.5)
        ax.plot(timeline, recovered[0], ".-", color="lightgreen")

        plt.fill_between(timeline, confirmed[0], active[0], color="orange", alpha=0.5)
        plt.fill_between(timeline, active[0], recovered[0], color="yellow", alpha=0.5)
        plt.fill_between(timeline, recovered[0], color="lightgreen", alpha=0.5)
        ticks = [i for i in range(len(timeline)) if i % 7 == 0]
        plt.xticks(ticks, rotation=30, ha="center")
        plt.grid(True)
        plt.ylabel("Total cases")
        plt.xlabel("")

        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        leg = plt.legend(["Total confirmed", "Total active", "Total recovered"], facecolor='0.1',
                         loc="upper left")
        for text in leg.get_texts():
            text.set_color("white")

        ax.set_ylim(ymin=1)
        ylabs = []
        locs, _ = plt.yticks()
        for iter_loc in locs:
            ylabs.append(human_format(int(iter_loc)))

        plt.yticks(locs, ylabs)
        plt.savefig('stats.png', transparent=True)

        plt.close(fig)
        await ctx.send(file=discord.File('stats.png',
                                         filename='stats.png'))

    @commands.command()
    @commands.is_owner()
    async def pull(self, ctx):
        stream = os.popen('git pull https://DankDumpster:Jupiter22yolO@github.com/DankDumpster/Noodles')
        output = stream.read()
        await ctx.send('```\n'
                       f'{output}\n'
                       f'```')

    @commands.command(aliases=['sh'])
    @commands.is_owner()
    async def shell(self, ctx, command: str):
        stream = os.popen(command)
        output = stream.read()
        await ctx.send('```\n'
                       f'{output}\n'
                       f'```')


def setup(bot):
    bot.add_cog(Owner(bot))
