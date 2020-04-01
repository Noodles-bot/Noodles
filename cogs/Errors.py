import discord
from discord.ext import commands


class Errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title='Invalid command',
                                  description=f'{error}, for a list of the commands use `{ctx.prefix}help`',
                                  color=0xFFA500)
            await ctx.send(embed=embed)
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
            raise error


def setup(bot):
    bot.add_cog(Errors(bot))
