import discord
import pylast
from discord.ext import commands
import modules
import youtube_dl
import urllib.request
from modules import utils
import re
import requests
import asyncio
import datetime
from pymongo import MongoClient
import lastpy
from modules.music import event

music = modules.music.Music()

with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

with open('lfapi.txt', 'r') as f:
    key = f.read()

SECRET = '3fc2809a9fc31fed3ea94864398cdd1b'

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @staticmethod
    @event.on("songstart")
    def _start_scrobble_song(ctx, song):
        loop = ctx.bot.loop
        embed = discord.Embed(color = discord.Color.blurple())
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        voice_channel = voice_client.channel
        count = 0
        for i in voice_channel.members:
            if not i.bot:
                db = cluster["LASTFM"]
                col = db["usernames"]
                if col.count_documents({'_id':i.id}) != 0:
                    count += 1
        if count == 0:
            return
        print((song.name).lower().replace(')', '').replace('(', '').replace('lyrics', '').replace('official', '').replace('video', '').replace('directed by cole bennett', '').replace('music', '').strip())
        params = {
            'limit': 1,
            'track': (song.name).lower().replace(')', '').replace('(', '').replace('lyrics', '').replace('official', '').replace('video', '').replace('directed by cole bennett', ''),   # lol
            'api_key': '35722626b405419c84e916787e6bf949',
            'method': 'track.search',
            'format': 'json'
        }
        data = requests.get(url='https://ws.audioscrobbler.com/2.0/', params=params)
        data = data.json()
        print(data)
        if int(data["results"]["opensearch:totalResults"]) != 0:
            embed.description = f"Scrobbling **{song.name}** for {count} user{'' if count == 1 else 's'}"
            loop.create_task(ctx.send(embed=embed))
        print("success")

    @staticmethod
    @event.on("songend") #event listener triggered from the module i modded
    def _scrobble_song(ctx, song):
        assert song.duration > 30 and song.duration != '', "Song not long enough to scrobble or is a live youtube video"
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        voice_channel = voice_client.channel
        params = {
            'limit': 1,
            'track': (song.name).lower().replace(')', '').replace('(', '').replace('lyrics', '').replace('official', '').replace('video', '').replace('directed by cole bennett', ''),   # lol
            'api_key': '35722626b405419c84e916787e6bf949',
            'method': 'track.search',
            'format': 'json'
        }
        data = requests.get(url='https://ws.audioscrobbler.com/2.0/', params=params)
        data = data.json()
        if int(data["results"]["opensearch:totalResults"]) == 0:
            return
        for i in voice_channel.members:
            if not i.bot:
                db = cluster["LASTFM"]
                col = db["usernames"]
                if col.count_documents({'_id':i.id}) != 0:
                    res = col.find({'_id':i.id})
                    for k in res:
                        try:
                            network = pylast.LastFMNetwork(
                                api_key=key,
                                api_secret=SECRET,
                                session_key=k["sessionkey"]
                            )
                            network.scrobble(title=data["results"]["trackmatches"]["track"][0]["name"],
                                             artist=data["results"]["trackmatches"]["track"][0]["artist"],
                                             timestamp=datetime.datetime.utcnow())
                        except Exception as e:
                            print(e)
                            continue




    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice.channel is None:
            return await ctx.send("You must be connected to a voice channel!")
        res = utils.vcperms(ctx.author.voice.channel)
        if not res:
            return await ctx.send(f"I am missing permissions to connect to {ctx.author.voice.channel.mention}")
        try:
            await ctx.author.voice.channel.connect()
        except discord.Forbidden:
            return await ctx.send("I cannot connect to this Voice Channel!")
        except Exception as e:
            print(e)

    @commands.command()
    async def leave(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            player.delete()
        await ctx.voice_client.disconnect()
        await ctx.message.add_reaction('👋🏽')

    @commands.command() #add lfm integration, should be pretty easy from here
    async def play(self, ctx, *, query):
        if not ctx.guild.me.voice:
            return await ctx.send("I am not in a voice channel!")
        embed = discord.Embed(color = discord.Color.green())
        try:
            await ctx.send('Searching for `{url}`...'.format(url=query.strip()))
            if ('www.' or '.be' or '.com' or 'youtu') not in query.lower():
                query = query.strip().replace(' ', '+').replace("'", '%27').replace('&', '%26').replace('^', '%5E').replace('%', '%25').replace(':', '%3A').replace(';', '%3B')
                html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={query}")
                vidid = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                query = (f"https://www.youtube.com/watch?v={vidid[0]}")
            player = music.get_player(guild_id=ctx.guild.id)
            if not player:
                player = music.create_player(ctx, ffmpeg_error_betterfix=True)
            if not ctx.voice_client.is_playing():
                await player.queue(query.strip(), search=True)
                song = await player.play()
                embed.set_author(name='Now Playing', icon_url=ctx.author.avatar_url)
            else:
                song = await player.queue(query.strip(), search=True)
                embed.set_author(name='Added to Queue', icon_url=ctx.author.avatar_url)
            dur = song.duration
            dur = utils.stringfromtime(int(dur))
            print(dur)
            embed.add_field(name='Duration', value=f"{dur if dur != '' else 'Live'}")
            embed.add_field(name='Channel', value=f"{song.channel}")
            embed.description = f"[{song.name}]({song.url})"
            embed.set_thumbnail(url=song.thumbnail)
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @commands.command()
    async def pause(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.pause()
        await ctx.send(f"Paused: **{song.name}**!")

    @commands.command()
    async def resume(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.resume()
        await ctx.send(f"Resumed: **{song.name}**")

    @commands.command()
    async def loop(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.toggle_song_loop()
        if song.is_looping:
            await ctx.send(f"Enabled loop for : **{song.name}**")
        else:
            await ctx.send(f"Disabled loop for: **{song.name}**")

    @commands.command()
    async def queue(self, ctx):
        q = []
        player = music.get_player(guild_id=ctx.guild.id)
        i = 0
        for song in player.current_queue():
            i += 1
            dur = song.duration
            dur = utils.stringfromtime(int(dur))
            q.append(f"{i}. {song.name} | {dur}")
        qlen = len(player.current_queue())
        fin = "\n"+ "\n".join(q) + f"\n\n{qlen} song{'' if qlen == 1 else 's'}"
        await ctx.send(f"```py"
                       f"{fin}```")

    @commands.command(aliases = ['nowplaying'])
    async def np(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = player.now_playing()
        await ctx.send('Now Playing : **' + song.name + '**')

    @commands.command()
    async def skip(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        data = await player.skip(force=True)
        await ctx.send(f"Skipped **{data[0].name}**.")

    @commands.command()
    async def remove(self, ctx, index):
        player = music.get_player(guild_id=ctx.guild.id)
        try:
            song = await player.remove_from_queue((int(index) - 1))
        except:
            return await ctx.send("Are you sure you specified a correct number?")
        await ctx.send(f"Removed {song.name} from queue!")


def setup(client):
    client.add_cog(Music(client))