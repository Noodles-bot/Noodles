import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, msg=None):
        if msg == 'level':
            embed = discord.Embed(
                title='Help for Level',
                description="See your own current level or see someone else's current level\nCommand: `level "
                            '<user>`\nAliases: `lvl`',
                color=0xFFA500
            )
            await ctx.send(embed=embed)
        elif msg == 'avatar':
            embed = discord.Embed(
                title='Help for Avatar',
                description="See your own avatar or see someone else's avatar\nCommand: `avatar <user>`"
                            '\nAliases: `av`',
                color=0xFFA500
            )
            await ctx.send(embed=embed)
        elif msg == None:
            page1 = discord.Embed(
                title='Noodles Help',
                description='**Welcome to the Noodles help. Use the arrows to move**',
                colour=0xFFA500
            )
            page1.set_image(url='https://cdn1.iconfinder.com/data/icons/restaurants-and-food/107/noodles-512.png')
            page1.set_footer(text='Noodles Version 1.3.4 Alpha', icon_url=self.bot.user.avatar_url)
            page2 = discord.Embed(
                title='Fun 1/3',
                description="**for more info about command use `,help <command>`**",
                colour=0xFFA500
            )
            page2.add_field(name='8ball', value='The wisest answers', inline=True)
            page2.add_field(name='cousin', value='use it :eyes:', inline=True)
            page2.add_field(name='crispy', value='command for Crispy', inline=True)
            page2.add_field(name='danny', value='command for Danny', inline=True)
            page2.add_field(name='demod', value='demods an user', inline=True)
            page2.add_field(name='doot', value='annoys French', inline=True)
            page2.add_field(name='fap', value='use it :eyes:', inline=True)
            page2.add_field(name='french', value='command for French', inline=True)
            page2.add_field(name='frying_pan', value='use it :eyes:', inline=True)
            page2.add_field(name='gay', value='mods belike', inline=True)
            page2.add_field(name='genes', value='command for Genes', inline=True)
            page2.add_field(name='harsha', value='command for Harsha', inline=True)
            page2.add_field(name='hornypolice', value='calls the hornypolice', inline=True)
            page2.add_field(name='hug', value='hug!', inline=True)
            page2.add_field(name='kap', value='command for Kap', inline=True)
            page2.add_field(name='link', value='gives an random link', inline=True)
            page2.add_field(name='locke', value='command for Locke', inline=True)
            page2.add_field(name='lovepolice', value='calls the lovepolice', inline=True)
            page2.add_field(name='malcolm', value='command for Malcolm', inline=True)
            page2.add_field(name='mod', value='try it, nothing is impossible', inline=True)
            page2.add_field(name='moose', value='use it :eyes:', inline=True)
            page2.add_field(name='noah', value='command for Noah', inline=True)
            page2.add_field(name='panda', value='cute panda', inline=True)
            page2.add_field(name='paps', value='command for Paps', inline=True)
            page2.add_field(name='perhaps', value='PPC', inline=True)
            page2.add_field(name='rarity', value='command for Rarity', inline=True)
            page2.add_field(name='shark', value='command for Shark', inline=True)
            page2.add_field(name='spez', value='command for SSA', inline=True)
            page2.add_field(name='toast', value='Get a delicious toast', inline=True)
            page2.add_field(name='tsg', value='command for TSG', inline=True)
            page2.add_field(name='zombital', value='command for zombital', inline=True)
            page3 = discord.Embed(
                title='Misc',
                description="**for more info about command use `,help <command>`**",
                colour=0xFFA500
            )
            page3.add_field(name='level', value='shows your level in this server', inline=True)
            page3.add_field(name='avatar', value='shows avatar', inline=True)
            page3.add_field(name='embed', value='makes you say something in embed', inline=True)
            page3.add_field(name='cogs', value='shows active cogs', inline=True)
            page3.add_field(name='usercount', value='shows the current usercount in the server', inline=True)
            page3.add_field(name='userinfo', value='shows everything you want to know about someone', inline=True)
            page3.add_field(name='ping', value='shows the latency to my slow internet', inline=True)
            page4 = discord.Embed(
                title='Music bot',
                description="**for more info about command use `,help <command>`**",
                colour=0xFFA500
            )
            page4.add_field(name='join', value='the bot will join your current channel', inline=True)
            page4.add_field(name='leave', value='the bot will leave your current channel', inline=True)
            page4.add_field(name='pause', value='pauses your music', inline=True)
            page4.add_field(name='play', value='use an link or just text example: `,play never gonna give you up`',
                            inline=True)
            page4.add_field(name='resume', value='resumes your music', inline=True)
            page4.add_field(name='skip', value='use this command if someone puts on fortnite parodies', inline=True)

            pages = [page1, page2, page3, page4]

            message = await ctx.send(embed=page1)

            await message.add_reaction('\u23ee')
            await message.add_reaction('\u25c0')
            await message.add_reaction('\u25b6')
            await message.add_reaction('\u23ed')
            await message.add_reaction('❌')

            i = 0
            emoji = ''

            while True:
                if emoji == '\u23ee':
                    i = 0
                    await message.edit(embed=pages[i])
                if emoji == '\u25c0':
                    if i > 0:
                        i -= 1
                        await message.edit(embed=pages[i])
                if emoji == '\u25b6':
                    if i < 3:  # change this integer when adding an page
                        i += 1
                        await message.edit(embed=pages[i])
                if emoji == '\u23ed':
                    i = 3  # change this integer when adding an page
                    await message.edit(embed=pages[i])
                if emoji == '❌':
                    return await message.delete()

                try:
                    res = await self.bot.wait_for('reaction_add', timeout=30.0)
                except:
                    return await message.delete()

                if res == None:
                    break
                if str(res[1]) == str(ctx.author):
                    emoji = str(res[0].emoji)
                    await message.remove_reaction(res[0].emoji, res[1])

            await message.clear_reactions()
        else:
            embed = discord.Embed(
                title='Not set up (yet) / Non existent',
                description='This is an invalid help, or its not setup yet.',
                color=0xFFA500
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def helpadmin(self, ctx):
        embed = discord.Embed(title='Help for Mods. [] = necessary <> = optional',
                              color=0xFFA500)
        embed.add_field(name='kick', value=',kick [user] <reason>', inline=False)
        embed.add_field(name='ban', value=',ban [user] <reason>', inline=False)
        embed.add_field(name='clear', value=',clear [integer amount]', inline=False)
        embed.add_field(name='mute', value=f'{ctx.prefix}mute [user] <time in minutes, default 5 minutes>',
                        inline=False)
        embed.add_field(name='mute', value=f'{ctx.prefix}unmute [user]', inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def commands(self, ctx):
        cmd = []
        for name in self.bot.commands:
            cmd.append(name.name)
        embed = discord.Embed(title='Commands:', description=ctx.prefix + f'\n{ctx.prefix}'.join(sorted(cmd)), color=0xFFA500)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
