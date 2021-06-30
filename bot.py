# -*- coding: utf-8 -*-
from discord.ext import commands
import discord
import os
import asyncio
import datetime
from discord_slash import SlashCommand
from modules import help, utils
from discord_components import DiscordComponents
import os
import threading

client = commands.Bot(command_prefix=commands.when_mentioned_or('.'), intents = discord.Intents().all(), allowed_mentions=discord.AllowedMentions.none(), case_insenstive = True)
slash = SlashCommand(client, sync_commands = True)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")
        print(f"{str(filename[:-3]).capitalize()} {'are' if filename[:-3].endswith('s') else 'is'} loaded.")

client.help_command = help.Help()

def voiceChatMain():
    os.system('cd DJFlame && node .')

t1 = threading.Thread(target=voiceChatMain)

@client.event
async def on_ready():
    t1.start()
    print(f"{client.user.name} is ready, logged on at {datetime.datetime.utcnow()}.")
    try:
        for guild in client.guilds:
            try:
                utils.add_guild_to_db(guild)
            except:
                continue
        DiscordComponents(client, change_discord_methods=True)
        while True:
            await asyncio.sleep(10)
            with open('spamdetect.txt', 'r+') as f:
                f.truncate(0)
    except Exception as e:
        print(e)

@client.command(help='Gives the ping of the bot!', aliases = ['clientping'])
async def botping(ctx):
    return await ctx.send(f"{round(client.latency * 1000)}ms")

@client.command()
async def feedback(ctx):
    try:
        await ctx.send(f'{ctx.author.mention}, thank you for using InfiniBot. Please state your feedback here:')

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        message = await client.wait_for('message', check=check, timeout=120)
        channel = client.get_channel(839951602168496149)
        fembed = discord.Embed(title=f"Feedback from {ctx.author} who is in the server **{ctx.guild.name}**",
                               description=f"{ctx.author.id} (User ID)\n{ctx.guild.id} (Guild ID)```" + message.content + "```",
                               color=discord.Color.blurple(), timestamp = datetime.datetime.utcnow())
        msg = await channel.send(embed=fembed)
        await msg.add_reaction(str('<:thumbsup:829860462966734898>'))
        await msg.add_reaction(str('<:thumbsdown:829860507125153795>'))
        await message.add_reaction(str('<:checked:829061772446531624>'))
        await ctx.send(str(f'{ctx.author.mention}, your feedback has been sent.'))
    except asyncio.TimeoutError:
        await ctx.reply("Timed out.", mention_author=False, delete_after=5)

@client.command(aliases = ['invite', 'botinvite'])
async def botinv(ctx):
    embed = discord.Embed(title="InfiniBot Invite Link",
                          description=r'https://discord.com/api/oauth2/authorize?client_id=829464107710677022&permissions=4294307063&scope=bot%20applications.commands',
                          color=discord.Color.blurple())
    embed.set_footer(text=f"InfiniBot Help | Requested by {ctx.author.name}")
    await ctx.reply(embed=embed)


import os
import discord
from discord.ext import commands
import DiscordUtils

bot = commands.AutoShardedBot(command_prefix="m ")
music = DiscordUtils.Music()


@bot.command()
async def join(ctx):
    await ctx.author.voice.channel.connect()
    await ctx.send('**Succsesfully Joined!!** Now Play Some Music <a:party:834824007860617270>')


@bot.command()
async def leave(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    if player: player.delete()
    await ctx.voice_client.disconnect()
    await ctx.send('All Good Things Must Come To An End <a:bye:834762050403172393>')


@bot.command()
async def play(ctx, *, url):
    await ctx.send('searching for the song........')
    player = music.get_player(guild_id=ctx.guild.id)
    if not player:
        player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
        await player.queue(url, search=True)
        song = await player.play()
        await ctx.send(f"Now Playing: **{song.name}** <a:np:834824012370149376>")
    else:
        song = await player.queue(url, search=True)
        await ctx.send(f"Queued: **{song.name}** <a:np:834824012370149376>")


@bot.command()
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    await ctx.send(f"Paused: **{song.name}** <a:remove:834824007604895764>")


@bot.command()
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    await ctx.send(f"Resumed: **{song.name}** <a:loading:834824007681179698> ")


@bot.command()
async def loop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        await ctx.send(f"Enabled loop for : **{song.name}** <a:loading:834824007681179698>")
    else:
        await ctx.send(f"Disabled loop for: **{song.name}** <a:loading:834824007681179698>")


@bot.command()
async def queue(ctx):
    embedVar = discord.Embed(title="Queue <a:loading:834824007681179698>", value=None, color=0x00ff00)
    player = music.get_player(guild_id=ctx.guild.id)
    i = 0
    for song in player.current_queue():
        embedVar.add_field(name=f'Song Number: {i}', value=f'{song.name}', inline=False)
        i += 1
    await ctx.send(embed=embedVar)


@bot.command()
async def np(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    await ctx.send('Now Playing : **' + song.name + '** <a:np:834824012370149376>')


@bot.command()
async def skip(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    data = await player.skip(force=True)
    await ctx.send(f"Skipped **{data[0].name}** <a:skip:834824011367972875>")


@bot.command()
async def remove(ctx, index):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.remove_from_queue(int(index))

    await ctx.send(f"Removed {song.name} from queue <a:remove:834824007604895764>")


with open('testbot.txt', 'r') as f:
    token = f.read()

client.run(token)