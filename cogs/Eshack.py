import discord
from discord.ext import commands


class Eshack(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Server Moderator")
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
    async def on_message(self, message):
        msg = message.content.lower()
        if '564974738716360724' in str(message.guild.id):
            if '618960977664147477' == str(message.channel.id):
                return
            if '675215762645975045' == str(message.channel.id):
                return
            if '675493012733952046' in str(message.channel.id):
                ign = message.content
                channel = self.bot.get_channel(675215762645975045)
                await channel.send(f"Whitelist add {ign}")
                await message.delete()
                gen = self.bot.get_channel(675103763656343552)
                role = discord.utils.get(message.author.guild.roles, id=589586005602992140)
                await message.author.add_roles(role, atomic=True)
                await gen.send(
                    f'{message.author.mention} you have been added to the whitelist under the name `{ign}`. Please ping an moderator if this is an mistake. Enjoy your stay at E-Shack')
            if 'tiktok' in msg:
                if message.author == self.bot.user:
                    return
                await message.delete()
                channel = message.channel
                await channel.send(
                    f'{message.author.mention} the usage of `tiktok` is not allowed in this server, take this as an warning')
            if 'owo' in msg:
                if message.author == self.bot.user:
                    return
                await message.delete()
                channel = message.channel
                await channel.send(
                    f'{message.author.mention} the usage of `owo` is not allowed in this server, take this as an warning')
            if 'uwu' in msg:
                if message.author == self.bot.user:
                    return
                await message.delete()
                channel = message.channel
                await channel.send(
                    f'{message.author.mention} the usage of `uwu` is not allowed in this server, take this as an warning')
            if 'tik tok' in msg:
                if message.author == self.bot.user:
                    return
                await message.delete()
                channel = message.channel
                await channel.send(
                    f'{message.author.mention} the usage of `tiktok` is not allowed in this server, take this as an warning')

        @commands.Cog.listener()
        async def on_member_remove(self, member):
            people = []
            for user in member.guild.members:
                people.append(user)
            id = str(member.guild.id)
            if "564974738716360724" in id:
                members = self.bot.get_channel(689476024723177488)
                await members.edit(name=f'Members: {len(people)}')


def setup(bot):
    bot.add_cog(Eshack(bot))
