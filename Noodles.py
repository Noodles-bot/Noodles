import os
import subprocess
import sys
from datetime import datetime

import asyncpg
import discord
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
        dsn=DATABASE,
        min_size=1, max_size=5)


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
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name=f'{len(bot.users) + 6000:,} users | {len(bot.guilds)} guilds'))


@bot.command(aliases=['up'], hidden=True)
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
