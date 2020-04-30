"""

    MIT License
    Copyright (c) 2020 Matthew
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

"""
import asyncio
import os
import discord
import asyncpg
import subprocess
import sys

from datetime import datetime
from discord.ext import commands
from utils.secret import *

__version__ = '0.4.11 Alpha'

text = r"""
 _   _                 _ _          
| \ | |               | | |         
|  \| | ___   ___   __| | | ___ ___ 
| . ` |/ _ \ / _ \ / _` | |/ _ / __|
| |\  | (_) | (_) | (_| | |  __\__ \
|_| \_|\___/ \___/ \__,_|_|\___|___/                           
"""
logo = r"""
         |
         |  /
         | /
   .~^(,&|/o.
  |`-------^|
  \         /
   `======='    
"""
print(text)
print(logo)


async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(
        dsn="postgres://zsqtcfcp:ePAhyuUmXR8c7GEwP-Xxjv2xYoaHgrKE@drona.db.elephantsql.com:5432/zsqtcfcp",
        min_size=1, max_size=5)


async def cleaner():
    while True:
        eshack = await bot.get_guild(564974738716360724)
        for user in eshack.members:
            if not user.roles:
                await user.kick(reason="Inactive")
        await asyncio.sleep(172800)


async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(",")(bot, message)

    prefixes = await bot.pg_con.fetch("SELECT prefix, guild_id FROM guild_settings WHERE guild_id = $1",
                                      str(message.guild.id))

    if not prefixes:
        await bot.pg_con.execute("INSERT INTO guild_settings (guild_id) VALUES ($1)", str(message.guild.id))

    prefixes = await bot.pg_con.fetch("SELECT prefix, guild_id FROM guild_settings WHERE guild_id = $1",
                                      str(message.guild.id))
    prefix = prefixes[0][0]
    return commands.when_mentioned_or(prefix)(bot, message)


bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)

# bot.remove_command('help')

bot.launch_time = datetime.utcnow()


@bot.event
async def on_ready():
    print('Logged in as')
    print(f'Bot-Name: {bot.user}')
    print(f'Bot-ID: {bot.user.id}')
    print(f'Discord.py Version: {discord.__version__}')
    print(f'Bot Version: {__version__}')
    bot.AppInfo = await bot.application_info()
    print(f'Owner: {bot.AppInfo.owner}')
    print(f'Latency: {round(bot.latency * 1000, 3)}ms')
    print('------')


@bot.command(aliases=['up'])
async def uptime(ctx):
    delta_uptime = datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    embed = discord.Embed(title='Uptime', description=f"{days}d, {hours}h, {minutes}m, {seconds}s", color=0xFFA500)
    await ctx.send(embed=embed)


@commands.command(hidden=True)
@commands.is_owner()
async def reboot(ctx):
    await ctx.send('Rebooting...')
    await bot.logout()
    subprocess.call([sys.executable, "Noodles.py"])


@bot.command(hidden=True)
@commands.is_owner()
async def reload(ctx, cog=None):
    cog = cog.lower()
    cog = cog.capitalize()
    if cog is None:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await ctx.message.add_reaction('<:loading:667529420013305857>')
                bot.unload_extension(f'cogs.{filename[:-3]}')
                bot.load_extension(f'cogs.{filename[:-3]}')
                cog1 = 'all cogs'

    else:
        try:
            await ctx.message.add_reaction('<:loading:667529420013305857>')
            bot.unload_extension(f"cogs.{cog}")
            bot.load_extension(f"cogs.{cog}")
            cog1 = f'cog `{cog}`'
        except Exception as error:
            print(f"{cog} can't be reloaded")
            await ctx.message.clear_reactions()
            raise error

    await ctx.message.clear_reactions()
    await ctx.send(f'Successfully reloaded {cog1}')


@bot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, cog=None):
    cog = cog.lower()
    cog = cog.capitalize()
    if cog is None:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await ctx.message.add_reaction('<:loading:667529420013305857>')
                bot.unload_extension(f'cogs.{filename[:-3]}')
                cog1 = 'all cogs'

    else:
        try:
            await ctx.message.add_reaction('<:loading:667529420013305857>')
            bot.unload_extension(f"cogs.{cog}")
            cog1 = f'cog `{cog}`'
        except Exception as error:
            print(f"{cog} can't be unloaded")
            await ctx.message.clear_reactions()
            raise error

    await ctx.message.clear_reactions()
    await ctx.send(f"Successfully unloaded {cog1}")


@bot.command(hidden=True)
@commands.is_owner()
async def load(ctx, cog=None):
    cog = cog.lower()
    cog = cog.capitalize()
    if cog is None:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await ctx.message.add_reaction('<:loading:667529420013305857>')
                bot.load_extension(f'cogs.{filename[:-3]}')
                cog1 = 'all cogs'

    else:
        try:
            await ctx.message.add_reaction('<:loading:667529420013305857>')
            bot.load_extension(f"cogs.{cog}")
            cog1 = f'cog `{cog}`'
        except Exception as error:
            await ctx.message.clear_reactions()
            await ctx.send(f"{cog} can't be loaded")
            raise error

    await ctx.message.clear_reactions()
    await ctx.send(f'Successfully loaded {cog1}')


for cog in os.listdir(r"./cogs"):
    if cog.endswith(".py") and not cog.startswith("_"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} can not be loaded")
            raise e

bot.loop.run_until_complete(create_db_pool())
bot.run(TOKEN)
