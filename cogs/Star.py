import discord
from discord.ext import commands

from utils.fun.data import color
from utils import checks


class Star(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_list = []
        self.original_message = {}

    async def get_amt(self, guild_id):
        i = await self.bot.pg_con.fetch("SELECT star_amount, guild_id FROM guild_settings WHERE guild_id = $1",
                                        guild_id)
        return i[0][0]

    async def get_channel(self, guild_id):
        i = await self.bot.pg_con.fetch("SELECT star_channel, guild_id FROM guild_settings WHERE guild_id = $1",
                                        guild_id)
        return i[0][0]

    async def get_emote(self, guild_id):
        i = await self.bot.pg_con.fetch("SELECT star_emote, guild_id FROM guild_settings WHERE guild_id = $1", guild_id)
        return i[0][0]

    async def enabled(self, guild_id):
        i = await self.bot.pg_con.fetch("SELECT starboard, guild_id FROM guild_settings WHERE guild_id = $1", guild_id)
        return i[0][0]

    @commands.guild_only()
    @commands.group(name='star')
    async def star(self, ctx):
        pass

    @star.command(name='help')
    async def star_help(self, ctx):
        embed = discord.Embed(title='Star system settings:', color=color)
        embed.add_field(name="Amount", value=ctx.prefix + "star amount <amount, default 5>", inline=False)
        embed.add_field(name="Emote", value=ctx.prefix + "star emote <emote, default :star:>", inline=False)
        embed.add_field(name="Starboard", value=ctx.prefix + "star channel <channel, default #starboard>", inline=False)
        embed.add_field(name="Settings", value=ctx.prefix + "star settings", inline=False)
        embed.add_field(name='Enable/disable', value=ctx.prefix + "star enable/disable", inline=False)

        await ctx.send(embed=embed)

    @star.command(name='amount')
    @checks.is_owner_or_admin()
    async def star_amount(self, ctx, amount: int):
        await self.bot.pg_con.execute("UPDATE guild_settings SET star_amount = $1 WHERE guild_id = $2", amount,
                                      str(ctx.guild.id))
        await ctx.send(f'Set the star amount to {amount} {await self.get_emote(guild_id=str(ctx.guild.id))}')

    @star.command(name='emote')
    @checks.is_owner_or_admin()
    async def star_emote(self, ctx, emote: discord.Emoji):
        await self.bot.pg_con("UPDATE guild_settings SET star_emote = $1 WHERE guild_id = $2", emote, str(ctx.guild.id))
        await ctx.send(f"Set the emote to {emote}")

    @star.command(name='channel')
    @checks.is_owner_or_admin()
    async def star_channel(self, ctx, channel: discord.TextChannel):
        await self.bot.pg_con.execute("UPDATE guild_settings SET star_channel = $1 WHERE guild_id = $2",
                                      str(channel.id), str(ctx.guild.id))
        await ctx.send(f"Set the channel to {channel.mention}")

    @star.command(name='enable')
    @checks.is_owner_or_admin()
    async def star_enable(self, ctx):
        i = await self.bot.pg_con.fetch("SELECT starboard FROM guild_settings WHERE guild_id = $1", str(ctx.guild.id))
        if i is True:
            await ctx.send("Starboard already enabled")
            return
        await self.bot.pg_con.execute("UPDATE guild_settings SET starboard = TRUE WHERE guild_id = $1",
                                      str(ctx.guild.id))
        await ctx.send("Enabled starboard for this guild")

    @star.command(name='disable')
    @checks.is_owner_or_admin()
    async def star_disable(self, ctx):
        i = await self.bot.pg_con.fetch("SELECT starboard FROM guild_settings WHERE guild_id = $1", str(ctx.guild.id))
        if i is False:
            await ctx.send("Starboard already disabled")
            return
        await self.bot.pg_con.execute("UPDATE guild_settings SET starboard = FALSE WHERE guild_id = $1",
                                      str(ctx.guild.id))
        await ctx.send("Disabled starboard for this guild")

    @star.command(name='settings')
    @checks.is_owner_or_admin()
    async def star_settings(self, ctx):
        e = {
            True: "<:True:695608401752752148> `Enabled`",
            False: "<:False:695608401610276886> `Disabled`"

        }
        embed = discord.Embed(title=f'{ctx.guild.name}\'s starboard settings',
                              description=f'For info on how to change the settings use {ctx.prefix}star help',
                              color=color)
        channel = await self.get_channel(guild_id=str(ctx.guild.id))
        if channel == '0':
            try:
                channel = discord.utils.get(ctx.guild.channels, name="starboard").mention
            except AttributeError:
                channel = "None"
        else:
            channel = self.bot.get_channel(int(channel)).mention
        embed.add_field(name='Settings',
                        value=f'**Starboard**\n*If starboard is enabled*\n{e[await self.enabled(guild_id=str(ctx.guild.id))]}\n'
                              f'**Amount**\n*Checks for the amount of stars on an message*\n`{await self.get_amt(guild_id=str(ctx.guild.id))}`\n'
                              f'**Emote**\n*Checks for this emote in the reactions*\n{await self.get_emote(guild_id=str(ctx.guild.id))}\n'
                              f'**Channel**\n*Posts the starred message in this channel*\n{channel}\n')

        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.Cog.listener(name="on_reaction_add")
    async def star_event(self, reaction, user):
        if reaction.emoji == await self.get_emote(guild_id=str(user.guild.id)):
            if await self.enabled(guild_id=str(user.guild.id)):
                if reaction.count >= await self.get_amt(guild_id=str(user.guild.id)):
                    id = await self.get_channel(guild_id=str(user.guild.id))

                    if id == '0':
                        chnl = discord.utils.get(user.guild.channels, name="starboard")
                    else:
                        chnl = self.bot.get_channel(int(id))

                    if (user.guild.id, reaction.message.id,) in self.message_list:

                        emote = await self.get_emote(guild_id=str(user.guild.id))
                        e = discord.Embed(title='',
                                          description=reaction.message.content, color=color,
                                          timestamp=reaction.message.created_at)
                        e.set_author(name=f"{reaction.message.author}", icon_url=reaction.message.author.avatar_url)

                        if reaction.message.attachments:
                            e.set_image(url=reaction.message.attachments[0].url)
                        e.set_footer(text=reaction.message.id)
                        msg = self.original_message[str(reaction.message.id)]

                        await msg.edit(content=f'{emote} {reaction.count} {reaction.message.channel.mention}')
                        return

                    emote = await self.get_emote(guild_id=str(user.guild.id))
                    self.message_list.append((user.guild.id, reaction.message.id))
                    e = discord.Embed(title='Jump link', url=reaction.message.jump_url,
                                      description=reaction.message.content, color=color,
                                      timestamp=reaction.message.created_at)
                    e.set_author(name=f"{reaction.message.author}", icon_url=reaction.message.author.avatar_url)

                    if reaction.message.attachments:
                        e.set_image(url=reaction.message.attachments[0].url)

                    e.set_footer(text=reaction.message.id)
                    msg = await chnl.send(f'{emote} {reaction.count} {reaction.message.channel.mention}', embed=e)
                    self.original_message.update({f"{reaction.message.id}": msg})


def setup(bot):
    bot.add_cog(Star(bot))
