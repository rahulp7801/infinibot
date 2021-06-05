# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import os
import asyncio
import datetime
from discord_slash import SlashCommand
from modules import help, utils
from discord_components import DiscordComponents
import os.path
from os import path
import os
import json
import time

client = commands.Bot(command_prefix='.', intents = discord.Intents.all(), allowed_mentions=discord.AllowedMentions.none(), case_insenstive = True)
slash = SlashCommand(client, sync_commands = True)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")
        print(f"{str(filename[:-3]).capitalize()} {'are' if filename[:-3].endswith('s') else 'is'} loaded.")

client.help_command = help.Help()

@client.event
async def on_ready():
    print(f"{client.user.name} is ready, logged on at {datetime.datetime.utcnow()}.")
    for i in client.guilds:
        print(i.name + "->" + str(i.owner_id))
        try:
            utils.add_guild_to_db(i)
        except:
            continue
    DiscordComponents(client, change_discord_methods=True)
    while True:
        await asyncio.sleep(10)
        with open('spamdetect.txt', 'r+') as f:
            f.truncate(0)


def cache_init():
    if path.exists("cache/stats.json"):
        print('Cache Exists')
        cache = open('cache/stats.json')
        try:
            cache_json = json.loads(cache.read())
        except:
            cache.close()
            cache = open("cache/stats.json", "w")
            cache.write('{"guilds": []}')
            cache.close()
        if cache_json["guilds"] != None:
            print('Cache in Correct Format, Loading Data Complete')
            return cache_json["guilds"]
    else:
        print('Cache Does Not Exist, Creating Cache')
        os.mkdir('cache')
        cache = open("cache/stats.json", "w")
        cache.write('{"guilds": []}')
        cache.close()

cache = cache_init()

@client.event
async def on_message(message):
    if any(x for x in cache if x["guildID"] == message.guild.id):
        if message.author.bot:
            return ''
        for h in cache:
            if h["guildID"] == message.guild.id:
                h["messages"] += 1
                if any(p for p in h["engagedusers"] if p["uid"] == message.author.id):
                    for p in h["engagedusers"]:
                        if p["uid"] == message.author.id:
                            p["messagesSent"] += 1
                else:
                    h["engagedusers"].append({"username":message.author.name + '#' + message.author.discriminator, "uid": message.author.id, "messagesSent": 1, "vcsecs": 0, "activetime": [time.time()]})
                json_cache = open('cache/stats.json', 'w')
                json_str = '{"guilds":'+ json.dumps(cache)
                json_cache.write(json_str + '}')
    else:
        print(f"Cache Not Found for Guild {message.guild.id}, Writing it Now")
        cache.append({"guildID": message.guild.id, "messages": 1, "userdiff": 0, "vcsecdiff": 0, "engagedusers": [{"username":message.author.name + '#' + message.author.discriminator, "uid": message.author.id, "messagesSent": 1, "vcsecs": 0, "activetime": [time.time()]}]})
        json_cache = open('cache/stats.json', 'w')
        json_str = '{"guilds":'+ json.dumps(cache)
        json_cache.write(json_str + '}')

@client.command(help='Gives the ping of the bot!')
async def ping(ctx):
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


with open('testbot.txt', 'r') as f:
    token = f.read()

client.run(token)