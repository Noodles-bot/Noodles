import async_cleverbot as ac
import discord
from discord.ext import commands

CleverBot = ac.Cleverbot('n.C;AnAo^>%",?6sfq6l')
CleverBot.set_context(ac.DictContext(CleverBot))


class Chatbot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ask(self, ctx, *, question: str):
        response = await CleverBot.ask(question, ctx.author.id)
        await ctx.send(response.text)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 675542011457044512:
            return
        if (700024745348825199 == message.channel.id) or (700031126634364979 == message.channel.id) or (700033619283935252 == message.channel.id):
            if message.content.startswith("`"):
                return
            if len(message.content) >= 60:
                await message.channel.send(f"You are {len(message.content) - 60} over the limit")
                return
            message.content = message.content.lower().replace("noodles", "bot")
            response = await CleverBot.ask(message.content, message.author.id)
            await message.channel.send(f"**Reply to {message.author.name}:** " + response.text.replace("rachel", "noodles"))


def setup(bot):
    bot.add_cog(Chatbot(bot))
