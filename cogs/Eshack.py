import discord
from discord.ext import commands

from utils import checks


class Eshack(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Server Moderator")
    @checks.is_guild(guild=564974738716360724)
    async def whitelist(self, ctx, i, name):
        i1 = i.lower()
        if i1 == 'add':
            c = self.bot.get_channel(675215762645975045)
            await c.send(f'Whitelist add {name}')
            await ctx.send(f'Added `{name}` to the whitelist')
        elif i1 == 'remove':
            c = self.bot.get_channel(675215762645975045)
            await c.send(f'Whitelist remove {name}')
            await ctx.send(f'Removed `{name}` from the whitelist')
        else:
            await ctx.send("Invalid syntax")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        people = []
        id = str(member.guild.id)
        for user in member.guild.members:
            people.append(user)
        if "564974738716360724" in id:
            members = self.bot.get_channel(689483433667199036)
            await members.edit(name=f'Members: {len(people)}')

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        id = str(channel.guild.id)
        channel_count = len([x for x in channel.guild.channels if type(x) == discord.channel.TextChannel])
        voice = len([x for x in channel.guild.channels if type(x) == discord.channel.VoiceChannel])
        if "564974738716360724" in id:
            channels = self.bot.get_channel(689483489640185927)
            vc = self.bot.get_channel(689483541574057992)
            await channels.edit(name=f'Channels: {channel_count}')
            await vc.edit(name=f'Voice Channels: {voice}')

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        id = str(channel.guild.id)
        channel_count = len([x for x in channel.guild.channels if type(x) == discord.channel.TextChannel])
        voice = len([x for x in channel.guild.channels if type(x) == discord.channel.VoiceChannel])
        if "564974738716360724" in id:
            channels = self.bot.get_channel(689483489640185927)
            vc = self.bot.get_channel(689483541574057992)
            await channels.edit(name=f'Channels: {channel_count}')
            await vc.edit(name=f'Voice Channels: {voice}')

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel):
            return
        msg = message.content.lower()
        if '564974738716360724' in str(message.guild.id):
            if '618960977664147477' == str(message.channel.id):
                return
            if '675215762645975045' == str(message.channel.id):
                return
            if '675493012733952046' in str(message.channel.id):
                await message.delete()
                ign = message.content
                channel = self.bot.get_channel(675215762645975045)
                await channel.send(f"Whitelist add {ign}")
                log = self.bot.get_channel(694657934780530739)
                role = discord.utils.get(message.author.guild.roles, id=589586005602992140)
                await message.author.add_roles(role, atomic=True)
                await message.author.send(
                    f'You have been added to the whitelist under the name `{ign}`. Please message a moderator if this is a mistake. Enjoy your stay at E-Shack')
                await log.send(f'Added {message.author.name} to the whitelist under the ign: **{ign}**')
            if 'tiktok' in msg:
                if message.author == self.bot.user:
                    return
                await message.delete()
                channel = message.channel
                await channel.send(
                    f'{message.author.mention} the usage of `tiktok` is not allowed in this server, take this as a warning')
            if 'owo' in msg:
                if message.author == self.bot.user:
                    return
                await message.delete()
                channel = message.channel
                await channel.send(
                    f'{message.author.mention} the usage of `owo` is not allowed in this server, take this as a warning')
            if 'uwu' in msg:
                if message.author == self.bot.user:
                    return
                await message.delete()
                channel = message.channel
                await channel.send(
                    f'{message.author.mention} the usage of `uwu` is not allowed in this server, take this as a warning')
            if 'tik tok' in msg:
                if message.author == self.bot.user:
                    return
                await message.delete()
                channel = message.channel
                await channel.send(
                    f'{message.author.mention} the usage of `tiktok` is not allowed in this server, take this as a warning')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        people = []
        for user in member.guild.members:
            people.append(user)
        id = str(member.guild.id)
        if "564974738716360724" in id:
            members = self.bot.get_channel(689476024723177488)
            await members.edit(name=f'Members: {len(people)}')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.id == 696913039764619274:
            print('log')
            if reaction.emoji.id == 565007889207656458:
                child = discord.utils.get(user.guild.roles, id=696564684026806282)
                await user.add_roles(child, atomic=True)
            elif reaction.emoji.id == 683550277801869312:
                azoki = discord.utils.get(user.guild.roles, id=696565008758341662)
                await user.add_roles(azoki, atomic=True)
            elif reaction.emoji.id == 565007885050970153:
                dyv = discord.utils.get(user.guild.roles, id=696564911035383929)
                await user.add_roles(dyv, atomic=True)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.message.id == 696913039764619274:
            if reaction.emoji.id == 565007889207656458:
                child = discord.utils.get(user.guild.roles, id=696564684026806282)
                await user.remove_roles(child, atomic=True)
            elif reaction.emoji.id == 683550277801869312:
                azoki = discord.utils.get(user.guild.roles, id=696565008758341662)
                await user.remove_roles(azoki, atomic=True)
            elif reaction.emoji.id == 565007885050970153:
                dyv = discord.utils.get(user.guild.roles, id=696564911035383929)
                await user.remove_roles(dyv, atomic=True)

    """
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        roles = []
        azoki = discord.utils.get(before.guild.roles, id=696565008758341662)
        child = discord.utils.get(before.guild.roles, id=696564684026806282)
        dyv = discord.utils.get(before.guild.roles, id=696564911035383929)
        roles.append(azoki)
        roles.append(child)
        roles.append(dyv)

        for role in roles:
            if role in after.roles:


        if (dyv and child in after.roles) or (child and azoki in after.roles) or (azoki and dyv in after.roles):
            await after.remove_roles(dyv)
            await after.remove_roles(child)
            await after.remove_roles(azoki)
            await after.send("Please select one role only")
    """

    @commands.command(hidden=True)
    @commands.is_owner()
    @checks.is_guild(guild=564974738716360724)
    async def reactions(self, ctx):
        msg = await ctx.message.channel.fetch_message(696840202630463548)
        await msg.add_reaction('<:gold:565007889207656458>')
        await msg.add_reaction('<:BEEG_YOSHI:683550277801869312>')
        await msg.add_reaction('<:1028_MCgoldenapple:565007885050970153>')


def setup(bot):
    bot.add_cog(Eshack(bot))
