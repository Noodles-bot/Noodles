import os
import json
import discord
import asyncpg
import subprocess
import sys
from datetime import datetime
from discord.ext import commands


async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(",")(bot, message)

    with open("prefixes.json", 'r') as f:
        prefixes = json.load(f)

    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or(",")(bot, message)

    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(bot, message)


bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)

bot.remove_command('help')


async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(database="Matt-O-Bot", user="postgres", password="Jupiter22")


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name=f'{len(bot.users):,} users'))
    bot.launch_time = datetime.utcnow()
    print('Bot is online.')
    print(f'Ping {round(bot.latency * 1000, 3)}ms')


@bot.command(aliases=['up'])
async def uptime(ctx):
    delta_uptime = datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    embed = discord.Embed(title='Uptime', description=f"{days}d, {hours}h, {minutes}m, {seconds}s", color=0xFFA500)
    await ctx.send(embed=embed)


@commands.command()
@commands.is_owner()
async def reboot(ctx):
    await ctx.send('Rebooting...')
    await bot.logout()
    subprocess.call([sys.executable, "Noodles.py"])


@bot.command()
@commands.is_owner()
async def reload(ctx, cog=None):
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


@bot.command()
@commands.is_owner()
async def unload(ctx, cog=None):
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
            print(f"{cog} can't be reloaded")
            await ctx.message.clear_reactions()
            raise error

    await ctx.message.clear_reactions()
    await ctx.send(f'Successfully unloaded {cog1}')


@bot.command()
@commands.is_owner()
async def load(ctx, cog=None):
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
            await ctx.send(f"{cog} can't be reloaded")
            raise error

    await ctx.message.clear_reactions()
    await ctx.send(f'Successfully loaded {cog1}')


for cog in os.listdir(".\\cogs"):
    if cog.endswith(".py") and not cog.startswith("_"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} can not be loaded")
            raise e

bot.loop.run_until_complete(create_db_pool())
bot.run(TOKEN)
