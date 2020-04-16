import discord
from discord.ext import commands
from asyncio import sleep


class Mod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} was kicked by {ctx.author.mention}. [{reason}]")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} was banned by {ctx.author.mention}. [{reason}]")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"{amount} messages got deleted")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, user: discord.Member, time: int = 5):
        time = time * 60
        if ctx.author == user:
            await ctx.send("You cannot mute yourself.")
        else:
            rolem = discord.utils.get(ctx.message.guild.roles, name='Muted')
            if rolem is None:
                try:
                    muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
                    for channel in ctx.guild.channels:
                        await channel.set_permissions(muted, send_messages=False,
                                                      read_message_history=False,
                                                      read_messages=False)
                except discord.Forbidden:
                    return await ctx.send("I have no permissions to make a muted role")
            elif rolem not in user.roles:
                embed = discord.Embed(title=f'User {user.name} has been successfully muted for {time / 60}m.',
                                      color=0xFFA500)
                embed.add_field(name="Shhh!", value="<:shut:689407119728181437>")
                embed.set_thumbnail(url=user.avatar_url)
                await ctx.send(embed=embed)
                await user.add_roles(rolem)
                await sleep(time)
                if rolem in user.roles:
                    try:
                        await user.remove_roles(rolem)
                        embed = discord.Embed(title=f'User {user.name} has been automatically unmuted.', color=0xFFA500)
                        embed.add_field(name="Welcome back!", value="Behave this time")
                        embed.set_thumbnail(url=user.avatar_url)
                        await ctx.send(embed=embed)
                    except Exception:
                        print(f'User {user.name} could not be unmuted!')
            else:
                await ctx.send(f'User {user.mention} is already muted.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, user: discord.Member):
        rolem = discord.utils.get(ctx.message.guild.roles, name='Muted')
        if rolem in user.roles:
            embed = discord.Embed(title=f'User {user.name} has been manually unmuted.', color=0xFFA500)
            embed.add_field(name="Welcome back!", value="Behave this time")
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)
            await user.remove_roles(rolem)
        else:
            await ctx.send("User is not muted")


def setup(bot):
    bot.add_cog(Mod(bot))
