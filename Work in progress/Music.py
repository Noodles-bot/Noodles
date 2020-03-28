import os
import shutil
import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get
from os import system


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.queues = {}

    @commands.command(pass_context=True, aliases=['j', 'joi'])
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await voice.disconnect()

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            print(f"Bot joined {channel}\n")

        await ctx.send(f'Joined {channel}')

    @commands.command(pass_context=True, aliases=['l', 'lea'])
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f"left {channel}")
            print(f'Bot left {channel}')
        else:
            await ctx.send(f'Not in channel')

    @commands.command(pass_context=True, aliases=['p', 'pla'])
    async def play(self, ctx, *, args):
        seperator = "_"
        # url = seperator.join(args)
        url = args

        def check_queue():
            Queue_infile = os.path.isdir("./cogs/Queue")
            if Queue_infile is True:
                DIR = os.path.abspath(os.path.realpath("Queue"))
                length = len(os.listdir(DIR))
                still_q = length - 1
                try:
                    first_file = os.listdir(DIR)[0]
                except:
                    print("No more queued songs")
                    queues.clear()
                    return
                main_location = os.path.dirname(os.path.realpath(__file__))
                song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
                if length != 0:
                    print("Song done, playing next queued")
                    print(f"Songs still in queue: {still_q}")
                    song_there = os.path.isfile("song.mp3")
                    if song_there:
                        os.remove("song.mp3")
                    shutil.move(song_path, main_location)
                    for file in os.listdir("../cogs/"):
                        if file.endswith(".mp3"):
                            os.rename(file, "song.mp3")

                    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 0.25  # verander volume hier

                else:
                    queues.clear()
                    return
            else:
                queues.clear()
                print("No songs in queued")

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                queues.clear()
                print("Removed old song")
        except PermissionError:
            Queue_infile = os.path.isdir("./Queue")
            if Queue_infile is False:
                os.mkdir("Queue")
            DIR = os.path.abspath(os.path.realpath("Queue"))
            q_num = len(os.listdir(DIR))
            q_num += 1
            add_queue = True
            while add_queue:
                if q_num in queues:
                    q_num += 1
                else:
                    add_queue = False
                    queues[q_num] = q_num

            queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'outtmpl': queue_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    print('Downloading audio....\n')
                    ydl.download([url])
            except:
                print("FALLBACK youtube-dl does not support this URL, using Spotdl")
                q_path = os.path.abspath(os.path.realpath("Queue"))
                system(f"spotdl -ff song{q_num} -f " + '"' + q_path + '"' + " -s " + url)

            await ctx.send(f"Added song {q_num} to queue")
            print("Song added to queue")

            return

        Queue_infile = os.path.isdir("./Queue")
        try:
            Queue_folder = "./Queue"
            if Queue_infile is True:
                print("Removed old queue Folder")
                shutil.rmtree(Queue_folder)
        except:
            print("No old Queue folder")

        await ctx.send("Getting everything ready....")

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print('Downloading audio....\n')
                ydl.download([url])
        except:
            print("FALLBACK youtube-dl does not support this URL, using Spotdl")
            c_path = os.path.dirname(os.path.realpath(__file__))
            system("spotdl -f " + '"' + c_path + '"' + " -s " + url)

        for file in os.listdir("../cogs/"):
            if file.endswith(".mp3"):
                name = file
                print(f"renamed file: {file}\n")
                os.rename(file, "song.mp3")

        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.25  # verander volume hiery

        try:
            nname = name.rsplit("-", 2)
            await ctx.send(f"Playing: {nname[0]}")
        except:
            await ctx.send(f"Playing: Song")

        print("playing...")

    @commands.command(pass_context=True, aliases=['pa', 'pau'])
    async def pause(self, ctx):
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("Music paused")
            voice.pause()
            await ctx.send("Music paused")
        else:
            print("No music playing")
            await ctx.send("No music playing, ERROR: Failed Pause")

    @commands.command(pass_context=True, aliases=['r', 'res'])
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            print("Music resumed")
            voice.resume()
            await ctx.send("Music resumed")
        else:
            print('Music is not paused')
            await ctx.send('Music is not paused')

    @bot.command(pass_context=True, aliases=['s', 'ski'])
    async def skip(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        queues.clear()

        if voice and voice.is_playing():
            print("Music skipped")
            voice.stop()
            await ctx.send("Music skipped")
        else:
            print('No music playing, ERROR: Unable to skip')
            await ctx.send('No music playing, ERROR: Unable to skip')

    queues = {}

    @bot.command(pass_context=True, aliases=['q', 'queu'])
    async def queue(self, ctx, url: str):
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is False:
            os.mkdir("Queue")
        DIR = os.path.abspath(os.path.realpath("Queue"))
        q_num = len(os.listdir(DIR))
        q_num += 1
        add_queue = True
        while add_queue:
            if q_num in queues:
                q_num += 1
            else:
                add_queue = False
                queues[q_num] = q_num

        queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': queue_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print('Downloading audio....\n')
                ydl.download([url])
        except:
            print("FALLBACK youtube-dl does not support this URL, using Spotdl")
            q_path = os.path.abspath(os.path.realpath("Queue"))
            system(f"spotdl -ff song{q_num} -f " + '"' + q_path + '"' + " -s " + url)

        await ctx.send(f"Added {q_num} to queue")
        print("Song added to queue")


def setup(bot):
    bot.add_cog(Music(bot))
