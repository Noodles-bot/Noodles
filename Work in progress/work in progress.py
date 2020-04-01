def __init__(self, bot, last_time):
    self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content.startswith("I'm "):
            msg1 = message.content.lower()
            channel = message.channel
            msg = msg1.replace("I'm", "")
            await channel.send(f"Hi{msg}, I'm dad")
        if message.content.startswith("im "):
            msg1 = message.content.lower()
            channel = message.channel
            msg = msg1.replace("im", "")
            await channel.send(f"Hi{msg}, I'm dad")
        await asyncio.sleep(300)

    user1 = await economy.get_user(author_id=str(ctx.author.id), guild_id=str(ctx.guild.id))
    if user1['bal'] >= money >= 0:
        await economy.withdraw(amount=money, author_id=str(ctx.author.id), guild_id=str(ctx.guild.id))
        user = await economy.get_user(author_id=str(ctx.author.id), guild_id=str(ctx.guild.id))
        if coinflip() == 1:
            await economy.deposit(amount=money * 1.5, author_id=str(ctx.author.id), guild_id=str(ctx.guild.id))
            await ctx.send(f"Congrats you won, new balance is {user['bal'] + money * 1.5} ducc dollars")
        else:
            await ctx.send(f"Rip, you lost {money} ducc dollars, new balance is {user['bal']}")