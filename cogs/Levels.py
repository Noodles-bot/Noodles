import discord
from discord.ext import commands
from datetime import date


class Levels(commands.Cog):
    bot = commands

    def __init__(self, bot):
        self.bot = bot

    async def lvl_up(self, user):
        cur_xp = user['xp']
        cur_lvl = user['lvl']

        if cur_xp >= round((4 * (cur_lvl ** 3)) / 5):
            await self.bot.pg_con.execute("UPDATE users SET lvl = $1 WHERE user_id  = $2 AND guild_id = $3",
                                          cur_lvl + 1, user['user_id'], user['guild_id'])
            return True
        else:
            return False

    @bot.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.author.bot:
            return

        author_id = str(message.author.id)
        guild_id = str(message.guild.id)

        user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id,
                                           guild_id)

        today = date.today()
        dt = today.strftime("%b-%d-%Y")
        if not user:
            await self.bot.pg_con.execute(
                "INSERT INTO users (user_id, guild_id, lvl, xp, date) VALUES ($1, $2, 1, 0, $3)",
                author_id, guild_id, dt)

        user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id,
                                              guild_id)
        id = str(message.guild.id)
        await self.bot.pg_con.execute("UPDATE users SET xp = $1 WHERE user_id = $2 AND guild_id = $3", user['xp'] + 1,
                                      author_id, guild_id)

        if await self.lvl_up(user):
            channel = discord.utils.get(message.guild.channels, name="Levels")
            if "665249179496349716" in id:
                channel = self.bot.get_channel(676472980842479656)
                await channel.send(f"{message.author.display_name} is now secks level {user['lvl'] + 1}")
            elif "564974738716360724" in id:
                channel = self.bot.get_channel(618209942783918091)
                await channel.send(f"{message.author.display_name} is now level {user['lvl'] + 1}")
            elif "668213545909092354" in id:
                pass
            elif channel is not None:
                await channel.send(f"{message.author.display_name} is now level {user['lvl'] + 1}")
            else:
                channel = message.channel
                await channel.send(f"{message.author.display_name} is now level {user['lvl'] + 1}")

    @bot.command(aliases=['lvl'])
    async def level(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        author_id = str(member.id)
        guild_id = str(ctx.guild.id)

        user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id,
                                           guild_id)

        if not user:
            await ctx.send("Member doesn't have a level yet")
        else:
            embed = discord.Embed(color=member.color)

            embed.set_author(name=f"Level - {member}", icon_url=member.avatar_url)

            embed.add_field(name='Level', value=user[0]['lvl'])
            embed.add_field(name='XP', value=user[0]['xp'])
            embed.set_footer(text=f"XP needed to level up: {round(((4 * (user[0]['lvl'] ** 3)) / 5) - user[0]['xp'])}")

            await ctx.send(embed=embed)

    @bot.command()
    async def leaderboard(self, ctx):
        guild_id = str(ctx.guild.id)

        result = await self.bot.pg_con.fetch(
            "SELECT user_id, lvl FROM public.users WHERE guild_id = $1 ORDER BY lvl DESC LIMIT 5", guild_id)

        embed = discord.Embed(color=0xFFA500)
        embed.set_author(name="Top 5 levels")
        embed.add_field(name="#1", value=f"User: {ctx.guild.get_member(int(result[0][0]))} \n**lvl: {result[0][1]}**",
                        inline=False)
        embed.add_field(name="#2", value=f"User: {ctx.guild.get_member(int(result[1][0]))} \n**lvl: {result[1][1]}**",
                        inline=False)
        embed.add_field(name="#3", value=f"User: {ctx.guild.get_member(int(result[2][0]))} \n**lvl: {result[2][1]}**",
                        inline=False)
        embed.add_field(name="#4", value=f"User: {ctx.guild.get_member(int(result[3][0]))} \n**lvl: {result[3][1]}**",
                        inline=False)
        embed.add_field(name="#5", value=f"User: {ctx.guild.get_member(int(result[4][0]))} \n**lvl: {result[4][1]}**",
                        inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Levels(bot))
