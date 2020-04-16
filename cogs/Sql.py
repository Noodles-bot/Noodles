import discord
from discord.ext import commands


class Sql(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def withdraw(self, amount, author_id, guild_id=None):
        if guild_id is not None:

            await self.bot.pg_con.execute('UPDATE users SET bal = bal - $1 WHERE user_id = $2 AND guild_id = $3',
                                          amount, author_id, guild_id)
        elif guild_id is None:
            await self.bot.pg_con.execute('UPDATE users SET bal = bal - $1 WHERE user_id = $2',
                                          amount, author_id)
        return

    async def deposit(self, amount, author_id, guild_id=None):
        if guild_id is not None:
            await self.bot.pg_con.execute('UPDATE users SET bal = bal + $1 WHERE user_id = $2 AND guild_id = $3',
                                          amount, author_id, guild_id)
        elif guild_id is None:
            await self.bot.pg_con.execute('UPDATE users SET bal = bal + $1 WHERE user_id = $2',
                                          amount, author_id)
        return

    async def get_balance(self, author_id, guild_id=None):
        if guild_id is not None:
            return await self.bot.pg_con.fetch("SELECT bal, user_id FROM users WHERE user_id = $1 AND guild_id = $2",
                                               author_id, guild_id)
        elif guild_id is None:
            return await self.bot.pg_con.fetch("SELECT bal, user_id FROM users WHERE user_id = $1",
                                               author_id)

    async def get_user(self, author_id, guild_id=None):
        if guild_id is not None:
            return await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id,
                                                  guild_id)
        elif guild_id is None:
            return await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1", author_id, )

    async def depbank(self, amount, author_id):
        await self.bot.pg_con.execute("UPDATE users SET bal = bal - $1 WHERE user_id = $2", amount, author_id)
        await self.bot.pg_con.execute("UPDATE users SET bank = bank + $1 WHERE user_id = $2", amount, author_id)

    async def withbank(self, amount, author_id):
        await self.bot.pg_con.execute("UPDATE users SET bal = bal + $1 WHERE user_id = $2", amount, author_id)
        await self.bot.pg_con.execute("UPDATE users SET bank = bank - $1 WHERE user_id = $2", amount, author_id)

    async def get_bank(self, author_id=None, guild_id=None):
        if guild_id is not None:
            return await self.bot.pg_con.fetch("SELECT bank FROM users WHERE user_id = $1 AND guild_id = $2", author_id,
                                               guild_id)
        if guild_id is None:
            return await self.bot.pg_con.fetch("SELECT bank FROM users WHERE user_id = $1", author_id)

    async def get_bank_all(self, guild_id):
        return await self.bot.pg_con.fetch("SELECT bank, user_id FROM users WHERE guild_id = $1", guild_id)

    async def bank_lvl(self, author_id):
        return await self.bot.pg_con.fetch("SELECT banklvl FROM bank WHERE user_id = $1", author_id)

    async def getbank(self, author_id):
        return await self.bot.pg_con.fetchrow("SELECT * FROM bank WHERE user_id = $1", author_id)

    async def bank_xp(self, author_id):
        return await self.bot.pg_con.fetch("SELECT bankxp FROM bank WHERE user_id = $1", author_id)

    async def create_bank(self, author_id):
        await self.bot.pg_con.execute("INSERT INTO bank (user_id, banklvl, bankxp) VALUES ($1, 1, 0)", author_id)

    async def get_lvl(self, user_id):
        i = await self.bot.pg_con.fetch("SELECT lvl, user_id FROM users WHERE user_id = $1", user_id)
        return i[0][0]

    async def bank_lvl_up(self, author_id):
        user = await self.bot.pg_con.fetchrow("SELECT * FROM bank WHERE user_id = $1", author_id)
        cur_xp = user['bankxp']
        cur_lvl = user['banklvl']

        if cur_xp >= round((4 * (cur_lvl ** 3)) / 12):
            await self.bot.pg_con.execute("UPDATE bank SET banklvl = $1 WHERE user_id  = $2",
                                          cur_lvl + 1, user['user_id'])
            return True
        else:
            return False

    async def bank_left(self, author_id):
        lvl = await self.bank_lvl(author_id=author_id)
        bank = await self.get_bank(author_id=author_id)
        return int(lvl[0][0]) * 523 - bank[0][0]

    async def bank_size(self, author_id):
        lvl = await self.bank_lvl(author_id=author_id)
        return int(lvl[0][0]) * 523


def setup(bot):
    bot.add_cog(Sql(bot))
