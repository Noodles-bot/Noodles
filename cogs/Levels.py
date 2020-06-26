import discord
from discord.ext import commands


class Levels(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def lvl_up(self, user, guild_id: str):
        cur_xp = user['lvl'][guild_id]['xp']
        cur_lvl = user['lvl'][guild_id]['lvl']

        if cur_xp >= round((4 * (cur_lvl ** 3)) / 5):
            await self.bot.conn.users.update_one({"user_id": user["user_id"]},
                                                 {'$set': {'lvl': {guild_id: {"lvl": cur_lvl + 1}}}})
            return True
        else:
            return False

    @commands.guild_only()
    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.author == self.bot.user) or message.author.bot:
            return

        author_id = str(message.author.id)
        guild_id = str(message.guild.id)

        user = await self.bot.conn.users.find_one({"user_id": author_id})
        if not user:
            document = {
                "user_id": author_id,
                "economy": {
                    "balance": {"pocket": 0, "bank": 500},
                    "bank": {"xp": 0, "lvl": 2}
                },
                "waifu": {
                    "price": 100,
                    "owned_by": None
                },
                "misc": {
                    "donator": False,
                    "tester": False
                }
            }
            await self.bot.conn.users.insert_one(document)

    @commands.command(aliases=['lvl'])
    async def level(self, ctx, member: discord.Member = None):
        member = ctx.author or member
        author_id = str(member.id)
        guild_id = str(ctx.guild.id)

        user = await self.bot.conn.users.find_one({"user_id": author_id})

        if not user:
            await ctx.send("Member doesn't have a level yet")
        else:
            embed = discord.Embed(color=member.color)

            embed.set_author(name=f"Level - {member}", icon_url=member.avatar_url)

            embed.add_field(name='Level', value=user['lvl'][guild_id]['lvl'])
            embed.add_field(name='XP', value=user['lvl'][guild_id]['xp'])
            embed.set_footer(
                text=f"XP needed to level up: {round(((4 * (user['lvl'][guild_id]['lvl'] ** 3)) / 5) - user['lvl'][guild_id]['xp'])}")

            await ctx.send(embed=embed)
            """
            xp = user[0]['xp']
            xp_total = (4 * (user[0]['lvl'] ** 3)) / 5
            width = 590
            x = (xp / xp_total) * width
            im = Image.open(
                BytesIO(requests.get('https://i.imgur.com/pHnwUqz.png').content)
            ).convert("RGB")
            draw = ImageDraw.Draw(im)
            color = (255, 165, 0)

            x, y, diam = x, 8, 34
            draw.ellipse([x, y, x + diam, y + diam], fill=color)

            ImageDraw.floodfill(im, xy=(14, 24), value=color, thresh=40)

            arr = BytesIO()
            im.save(arr, format="PNG")
            arr.seek(0)
            file = discord.File(arr, filename="lvl.png")
            await ctx.send(file=file)
            """


def setup(bot):
    bot.add_cog(Levels(bot))
