import discord
from discord.ext import commands
import DiscordUtils
import youtube_dl
import urllib.request
from modules import utils
import re

music = DiscordUtils.Music()

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

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
                html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={query.strip().replace(' ', '+')}")
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
            embed.add_field(name='Duration', value=f"{dur}")
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