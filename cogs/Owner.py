import asyncio
import inspect
import json
import discord
import io
import traceback
import textwrap
import copy
from typing import Union, Optional
from contextlib import redirect_stdout
from discord.ext import commands

from utils import checks
from utils.tools import get_money


def cleanup_code(self, content):
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    return content.strip('` \n')


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

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def todo(self, ctx, *, todo):
        await self.bot.pg_con.execute("INSERT INTO todo (todo, num, is_pinned) VALUES ($1, $2, FALSE)", todo, 1)
        await ctx.send("Inserted into the database")

    @commands.command(aliases=['setmoney'])
    @checks.is_owner_or_admin()
    async def set_money(self, ctx, *, name):
        with open(r"C:/Users/Matthew/Documents/Scripts/Python/Discord/Noodles/utils/json/money.json", 'r') as f:
            money = json.load(f)

        money[str(ctx.guild.id)] = name
        await ctx.send(f"New money name is `{name}`")

        with open(r"C:/Users/Matthew/Documents/Scripts/Python/Discord/Noodles/utils/json/money.json", 'w') as f:
            json.dump(money, f, indent=4)

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

        body = cleanup_code(self, body)
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


def setup(bot):
    bot.add_cog(Owner(bot))
