from __future__ import print_function
import asyncio
import datetime
import json
import math
import os
import random
import re
import sqlite3
from sqlite3.dbapi2 import paramstyle
import string
import sys
import threading
import disscord_interactions
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import dotenv
from dotenv import load_dotenv, find_dotenv
import logging
from urllib.parse import parse_qs
from prsaw import RandomStuff
import urllib.request
from decimal import Decimal
from io import BytesIO
import time
# import wikipedia
import aiofiles
import aiohttp
import discord
import discord.ext
import discord.ext.commands
import flask
import googleapiclient
import googletrans
import numpy
import pymongo
from discord_slash import SlashCommand, SlashContext
import pandas as pd
import praw             
import psutil
import pyfiglet
import pylast
import pyshorteners
import requests
import youtube_dl
from aiohttp import ClientSession, http
from discord import *
from discord import Spotify
from discord.ext import commands
from discord.ext.commands import ConversionError
from prsaw import RandomStuff
from googleapiclient import discovery
from googletrans import Translator
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pymongo import MongoClient
import pymongo

with open('praw.txt', 'r') as f:
    ff = f.read()
    creds = ff.split('\n')
    client_id = creds[0]
    client_secret = creds[1]
    username = creds[2]
    password = creds[3]
    user_agent = creds[4]

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     username=username,
                     password=password,
                     user_agent=user_agent,
                     check_for_async=False)
from discord.ext.commands import (Bot, BotMissingPermissions, bot,
                                  bot_has_permissions)

botversion = "1.0.0"
intents = discord.Intents().all()
with open('perspectiveapis.txt', 'r') as file:
    tokens = file.read()
    keys = tokens.split('\n')
PERSPECTIVE_KEYS = keys

with open('mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

# class MyBot(commands.Bot):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.ipc = ipc.Server(self, secret_key = "raycooldineshbot")
#
#     async def on_ready(self):
#         print("bot is online")
#     async def on_ipc_ready(self):
#         print('IPC is ready')
#
#     async def on_ipc_error(self, endpoint, error):
#         print(endpoint, "raised", error)

def get_prefix(client, msg):
    name = f"GUILD{msg.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': msg.guild.id})
    for i in user:
        prefix = i['prefix']
    return commands.when_mentioned_or(prefix)(client, msg)



client = commands.Bot(command_prefix=get_prefix, intents=intents, allowed_mentions=discord.AllowedMentions.none(), case_insenstive = True)
slash = SlashCommand(client, override_type = True)



client.remove_command('help')
rs = RandomStuff(async_mode=True)
translator = Translator()
TICKER_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
url_shortener = pyshorteners.Shortener()

# @client.ipc.route()
# async def get_guild_count(data):
#     return len(client.guilds)
#
# @client.ipc.route()
# async def get_guild_ids(data):
#     final = []
#     for y in client.guilds:
#         final.append(y.id)
#     return final

mainshop = [
    {"name": "Watch", "price": 100, "description": "Time"},
    {"name": "Laptop", "price": 1000, "description": "Work"},
    {"name": "PC", "price": 10000, "description": "Gaming"}
]

def voiceChatMain():
    os.system('cd DJFlame && node .')

t1 = threading.Thread(target=voiceChatMain)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="%help | InfiniBot Universe"))
    print('Bot is ready')
    t1.start()
    for i in client.guilds:
        print(i.name + "->" + str(i.owner_id))
    for guild in client.guilds:
        try:
            name = f"GUILD{guild.id}"
            db = cluster[name]
            collection = db['config']
            ping_cm = {
                "_id": guild.id,
                "name": guild.name,
                'prefix': '%',
                'welcomemsg': "",
                "welcomechannel": "",
                'priv_welcomemsg': "",
                'leavemsg': "",
                'captchaon': "",
                'muterole': "",
                'spamdetect': "",
                'logging': "",
                'logchannel': "",
                'levelups': "",
                'ghostpingon': "",
                'ghostcount':'',
                'blacklistenab': "",
                'mcip': "",
                'starchannel': '',
                'welcomenick': '',
                'welcomerole': ''
            }
            x = collection.insert_one(ping_cm)
            collection = db['levels']
            ping_cm = {
                "_id": guild.id,
                "name": guild.name
            }
            x = collection.insert_one(ping_cm)
            collection = db['afk']
            ping_cm = {
                "_id": guild.id,
                "name": guild.name,
                'afkstatus': "",
                'startafk': '',
                'preafknick': '',
                'afkid': ''
            }
            x = collection.insert_one(ping_cm)
            collection = db['commands']
            ping_cm = {
                "_id": guild.id,
                "name": guild.name,
                'commandname': "",
                'commandcount': '',
                'commandchannel': ''
            }
            x = collection.insert_one(ping_cm)
            collection = db['customcmnd']
            ping_cm = {
                "_id": guild.id,
                "name": guild.name,
                'commandname': ""
            }
            x = collection.insert_one(ping_cm)
            collection = db['warns']
            ping_cm = {
                "_id": guild.id,
                "name": guild.name,
                'reason': "",
                'time': '',
                'mod': '',
                'offender': ''
            }
            x = collection.insert_one(ping_cm)
            collection = db['serverstats']
            ping_cm = {
                "_id": guild.id,
                "name": guild.name,
                'vcsecs': "",
                'msgcount': ''
            }
            x = collection.insert_one(ping_cm)
            collection = db['messages']
            ping_cm = {
                "_id": guild.id,
                "name": guild.name,
                'author': "",
                'date': '',
                'channel': '',
                'count': ''
            }
            x = collection.insert_one(ping_cm)
            collection = db['typing']
            ping_cm = {
                "_id": guild.id,
                "name": guild.name,
                'uid': '',
                'date': "",
                'accuracy': '',
                'wpm': ''
            }
            x = collection.insert_one(ping_cm)
            await asyncio.sleep(0.5)
        except Exception:
            continue
    channel = client.get_channel(id=844611738133463121)
    desc = f"Logged on as {client.user.name} on {datetime.datetime.utcnow().strftime('%D')}\n" \
           f"Guild count: {len(client.guilds)}"
    embed = discord.Embed(description = desc, color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
    await channel.send(embed=embed)
    while True:
        await asyncio.sleep(10)
        with open('spamdetect.txt', 'r+') as f:
            f.truncate(0)

@client.check
def check_commands(ctx):
    db = cluster['BLACKLIST']
    collection = db['users']
    query = {"_id": ctx.author.id}
    if collection.count_documents(query) == 0:
        collection = db['guilds']
        query = {"_id": ctx.guild.id}
        if collection.count_documents(query) == 0:
            pass
        else:
            return False
    else:
        return False
    db = cluster['DONOTTRACK']
    collection = db['users']
    query = {"_id": ctx.author.id}
    if collection.count_documents(query) == 0:
        collection = db['guilds']
        query = {"_id": ctx.guild.id}
        if collection.count_documents(query) == 0:
            return True
        else:
            return False
    else:
        return False

@client.event
async def on_command_error(ctx, error):
    db = cluster['ERRORS']
    collection = db['boterrs']
    name = f"GUILD{ctx.guild.id}"
    if isinstance(error, commands.CommandOnCooldown):
        time = round(error.retry_after)
        desc = f"{ctx.author.mention}, wait `{time}` seconds to use the command again."
        embed = discord.Embed(title="Command on cooldown", description=desc, color=discord.Color.red(), timestamp = datetime.datetime.utcnow())
        embed.set_footer(text=f"Message Author: {ctx.author}")
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        return
    if isinstance(error, commands.MissingRole):
        return
    if isinstance(error, commands.NotOwner):
        return
    if isinstance(error, commands.NoPrivateMessage):
        return
    if isinstance(error, commands.MissingPermissions):
        return
    if isinstance(error, commands.PrivateMessageOnly):
        return
    if 'The global check functions for command' in str(error):
        return
    else:
        channel = client.get_channel(id = 840386258203312129)
        desc = f"{ctx.author.id} - Author ID\n{ctx.guild.id} - GUILD ID - **{ctx.guild.name}** - GUILD NAME\n\nCommand:{ctx.command.name}" \
                f"```{error}```"
        embed = discord.Embed(title = "Error", description = desc, color = discord.Color.red())
        await channel.send(embed=embed)
    try:
        ping_cm = {"name": name, 'time': datetime.datetime.utcnow(), 'error': str(error)}
        collection.insert_one(ping_cm)
    except:
        pass

@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            if channel.is_nsfw():
                continue
            else:
                await channel.send(
                f'**Thanks for adding InfiniBot to {guild.name}!**\n'
                f'I\'m InfiniBot and I hope our relationship can be infinite! To set me up please use `%setup` (limited to admins)\n'
                f'By using InfiniBot in {guild.name} you agree to the [terms of service](https://docs.google.com/document/d/1XHOKPspuyqUIS9a0d0BMcO5oKXT5Xe5KdN_olG9sGFc/edit?usp=sharing). Use `%tos` to find it again.\n\n'
                f'**---------------------**\n\n'
                f'`-` Use `%changeprefix <prefix>` to change the prefix.\n'
                f'`-` Use `%help` to see all commands.\n'
                f'If you have a specific question, visit my support server (Coming soon!)')
                break

    try:
        name = f"GUILD{guild.id}"
        db = cluster[name]
        collection = db['config']
        ping_cm = {
            "_id": guild.id,
            "name": guild.name,
            'prefix': '%',
            'welcomemsg': "",
            "welcomechannel": "",
            'priv_welcomemsg': "",
            'leavemsg': "",
            'captchaon': "",
            'muterole': "",
            'spamdetect': "",
            'logging': "",
            'logchannel': "",
            'levelups': "",
            'ghostpingon': "",
            'ghostcount' : '',
            'blacklistenab': "",
            'mcip': "",
            'starchannel': '',
            'welcomenick' : '',
            'welcomerole' : ''
        }
        x = collection.insert_one(ping_cm)
        collection = db['levels']
        ping_cm = {
            "_id": guild.id,
            "name": guild.name
        }
        x = collection.insert_one(ping_cm)
        collection = db['customcmnd']
        ping_cm = {
            "_id": guild.id,
            "name": guild.name,
            'commandname': ""
        }
        x = collection.insert_one(ping_cm)
        collection = db['afk']
        ping_cm = {
            "_id": guild.id,
            "name": guild.name,
            'afkstatus': "",
            'startafk': '',
            'preafknick': '',
            'afkid': ''
        }
        x = collection.insert_one(ping_cm)
        collection = db['serverstats']
        ping_cm = {
            "_id": guild.id,
            "name": guild.name,
            'vcsecs': "",
            'msgcount': ''
        }
        x = collection.insert_one(ping_cm)
        collection = db['commands']
        ping_cm = {
            "_id": guild.id,
            "name": guild.name,
            'commandname': "",
            'commandcount': '',
            'commandchannel': ''
        }
        x = collection.insert_one(ping_cm)
        collection = db['warns']
        ping_cm = {
            "_id": guild.id,
            "name": guild.name,
            'reason': "",
            'time': '',
            'mod': '',
            'offender': ''
        }
        x = collection.insert_one(ping_cm)
        collection = db['messages']
        ping_cm = {
            "_id": guild.id,
            "name": guild.name,
            'author': "",
            'date': '',
            'channel': '',
            'count': ''
        }
        x = collection.insert_one(ping_cm)
        collection = db['typing']
        ping_cm = {
            "_id": guild.id,
            "name": guild.name,
            'uid' : '',
            'date': "",
            'accuracy': '',
            'wpm': ''
        }
        x = collection.insert_one(ping_cm)
    except Exception:
        pass

@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if str(reaction) == "⭐":
        #make it work for images
        if reaction.count == 1:
            name = f"GUILD{reaction.message.guild.id}"
            db = cluster[name]
            collection = db['config']
            query = {"_id": reaction.message.guild.id}
            if collection.count_documents(query) == 0:
                return
            else:
                res = collection.find(query)
                for result in res:
                    starchannel = result['starchannel']
                try:
                    chan = client.get_channel(int(starchannel))
                except:
                    return
                if reaction.message.attachments:
                    desc = f"{f'[Jump to the message!]({reaction.message.jump_url})'}\n\n"
                    embed = discord.Embed(description = desc, color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
                    embed.set_image(url=reaction.message.attachments[0].url)
                    embed.set_author(name=reaction.message.author.name, icon_url=reaction.message.author.avatar_url)
                    await chan.send(f"{reaction.message.author.name}'s message in {reaction.message.channel.mention}!")
                    return await chan.send(embed=embed)
                desc = f"{f'[Jump to the message!]({reaction.message.jump_url})'}"
                embed = discord.Embed(description =f"{desc}\n\n{reaction.message.content}", color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
                embed.set_author(name=reaction.message.author.name, icon_url = reaction.message.author.avatar_url)
                embed.set_footer(text=f"Message ID: {reaction.message.id}")
                await chan.send(f"Sent by {reaction.message.author.name} in {reaction.message.channel.mention}!")
                await chan.send(embed=embed)

@client.event
async def on_command(ctx):
    db = cluster['COMMANDCOUNT']
    collection = db['commandcount']
    query = {"_id": ctx.guild.id}
    if collection.count_documents(query) == 0:
        ping_cm = {"_id": ctx.guild.id, "count": 1}
        collection.insert_one(ping_cm)
    else:
        user = collection.find(query)
        for result in user:
            count = result['count']
        count += 1
        collection.update_one({"_id": ctx.guild.id}, {"$set": {'count': count}})
    query = {"_id": client.user.id}
    if collection.count_documents(query) == 0:
        ping_cm = {"_id": client.user.id, "count": 1}
        collection.insert_one(ping_cm)
    else:
        user = collection.find(query)
        for result in user:
            count = result['count']
        count += 1
        collection.update_one({"_id": client.user.id}, {"$set": {'count': count}})


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author.system:
        return
    name = f"GUILD{message.guild.id}"
    db = cluster[name]
    collection = db['config']
    counter = 0
    with open('spamdetect.txt', 'r+') as f:
        for lines in f:
            if lines.strip("\n") == str(message.author.id):
                counter += 1

        f.writelines(f"{str(message.author.id)}\n")
        if counter > 8:
            user = collection.find({'_id': message.guild.id})
            for i in user:
                spamdetect = i['spamdetect']
                muterole = i['muterole']
            try:
                if message.author.guild_permissions.manage_messages:
                    pass
                if spamdetect.lower().strip() != 'on':
                    pass
                elif muterole == '':
                    pass
                else:
                    mute_role = discord.utils.get(message.author.guild.roles, name=muterole.strip())
                    await message.author.add_roles(mute_role)
                    await message.channel.send(f"{message.author.name} has been muted indefinitely for spamming.")
            except discord.Forbidden:
                pass
    #add option to blacklist channels for spam detection
    # try:
    #     j = discovery.build(
    #         "commentanalyzer",
    #         "v1alpha1",
    #         developerKey=random.choice(PERSPECTIVE_KEYS),
    #         discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    #         static_discovery=False,
    #     )

    #     analyze_request = {
    #         'comment': {'text': f'{message.content}'},
    #         'requestedAttributes': {'TOXICITY': {}}
    #     }

    #     response = j.comments().analyze(body=analyze_request).execute()
    #     tox = float(response['attributeScores']['TOXICITY']['summaryScore']['value']) * 100
    #     if int(float(response['attributeScores']['TOXICITY']['summaryScore']['value']) * 100) >= 85:
    #         cursor.execute(f"SELECT toxicitydetect from {name}")
    #         result72 = cursor.fetchone()
    #         if str(result72[0]).lower() == 'none' or str(result72[0]).lower() == '0':
    #             pass
    #         else:
    #             if message.author.guild_permissions.manage_guild:
    #                 pass
    #             else:
    #                 cursor.execute(f"SELECT toxicmsg from {name}")
    #                 result = cursor.fetchone()
    #                 if str(result[0]).lower() == 'none' or str(result[0]) == '1':
    #                     pass
    #                 else:
    #                     await message.delete()
    #                     embed = discord.Embed(
    #                         description=str(result[0]).format(member=message.author.mention, user=message.author.name,
    #                                                            guild=message.guild.name),
    #                         color=discord.Color.blurple(), timestamp=datetime.datetime.utcnow())
    #                     embed.set_footer(text=f"Toxicity rate : {tox}%")
    #                     embed.set_thumbnail(url=message.guild.icon_url)
    #                     await message.channel.send(embed=embed, delete_after = 30)
    # except Exception as e:
    #     pass

    if message.mentions:
        name = f"GUILD{message.guild.id}"
        db = cluster[name]
        collection = db['afk']
        userID = (message.mentions[0].id)
        query = {'_id': userID}
        if collection.count_documents(query) == 0:
            pass
        else:
            user = collection.find({'_id': userID})
            for i in user:
                status = i['status']
            user = message.mentions[0].name
            desc = f"Status: ```{status}```"
            embed = discord.Embed(description=desc, color=discord.Color.red())
            embed.set_thumbnail(url=message.guild.icon_url)
            embed.set_author(name=f"{user} is afk", icon_url=message.mentions[0].avatar_url)
            await message.reply(embed=embed, mention_author=False)

    name = f"GUILD{message.guild.id}"
    db = cluster[name]
    collection = db['afk']
    query = {'_id': message.author.id}
    if collection.count_documents(query) == 0:
        pass
    else:
        user = collection.find({'_id': message.author.id})
        for i in user:
            starttime = i['start']
        totime = int(float(time.time())) - int(float(starttime))
        if 60 <= totime:
            mins = int(totime) // 60
            desc = f"Away for {mins} minute{'' if math.floor(mins) == 1 else 's'}"
        if totime < 60:
            desc = f"Away for {int(totime)} second{'' if totime == 1 else 's'}"

        embed = discord.Embed(title="Welcome Back!", description=desc, color=discord.Color.green())
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        embed.set_thumbnail(url=message.author.avatar_url)
        await message.channel.send(embed=embed)
        member = collection.find({'_id': message.author.id})
        for i in member:
            prenick = i['display_name']
        try:
            await message.author.edit(nick=prenick)
        except discord.Forbidden:
            pass
        finally:
            collection.delete_one({'_id': message.author.id})
    x = datetime.datetime.utcnow().strftime('%b%e, %Y')
    name = f"GUILD{message.guild.id}"
    #add more messages params
    #maybe the author param can be the user_id
    collection = db['messages']
    query = {'_id': message.guild.id}
    if collection.count_documents(query) == 0:
        ping_cm = {
            "_id": message.guild.id,
            "name": message.guild.name,
            "count": 1
        }
        collection.insert_one(ping_cm)
    else:
        user = collection.find(query)
        for result in user:
            count = result['count']
        if count == '':
            count = 1
        else:
            count = int(count)
            count += 1
        collection.update_one({'_id':message.guild.id}, {'$set' : {'count' : str(count)}})
    # cursor.execute(f"SELECT msgcount from {name} WHERE user_id = {message.author.id} AND msgchannel_id = {message.channel.id} AND date = '{x}'")
    # result2 = cursor.fetchone()
    # if result2 is None:
    #     sql = (f"INSERT INTO {name}(msgcount, user_id, msgchannel_id, date) VALUES(?, ?, ?, ?)")
    #     val = (1, message.author.id, message.channel.id, f"{x}")
    # elif result2 is not None:
    #     cursor.execute(f"SELECT msgcount from {name} WHERE user_id = {message.author.id} AND msgchannel_id = {message.channel.id} AND date = '{x}'")
    #     result2 = cursor.fetchone()
    #     sql = (f"UPDATE {name} SET msgcount = ? WHERE user_id = ? AND msgchannel_id = ? AND date = ?")
    #     val = ((int(result2[0]) + 1), message.author.id, message.channel.id, f"{x}")
    # cursor.execute(sql, val)
    # name = f"GUILD{message.guild.id}"
    # cursor.execute(f"SELECT XP from {name} WHERE user_id = {int(message.author.id)} AND msgchannel_id = {int(message.channel.id)}")
    # result3 = cursor.fetchone()
    # print(result3)
    # if str(result3[0]) == 'None':
    #     print('here')
    #     sql = (f"UPDATE {name} SET XP = ? WHERE user_id = ? AND msgchannel_id = ?")
    #     val = (random.randint(10, 30), message.author.id, message.channel.id)
    # elif result3 is None:
    #     sql = (f"INSERT INTO {name}(XP, user_id, msgchannel_id) VALUES(?, ?, ?)")
    #     val = (random.randint(10, 30), message.author.id)
    # else:
    #     sql = (f"UPDATE {name} SET XP = ? WHERE user_id = ? AND msgchannel_id = ?")
    #     val = ((int(result3[0]) + (random.randint(10, 30))), message.author.id, message.channel.id)
    # cursor.execute(sql, val)
    # db.commit()
    # cursor.close()
    # db.close()
    await client.process_commands(message)

@client.group(invoke_without_command = True)
async def setup(ctx):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    #add help for each command
    desc = f"```welcomechannel, welcometext, privset, welcomerole, captcha, muterole, leavemsg, spamdetection, logs, ghostping```"
    embed = discord.Embed(title= "InfiniBot Setup Commands",description = desc, color = discord.Color.green())
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Use {prefix}setup <command> for these commands. For example, {prefix}setup welcomechannel")
    await ctx.send(embed=embed)

@setup.command()
async def list(ctx):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    embed = discord.Embed(title="Available Setup Commands for InfiniBot", color=discord.Color.greyple())
    embed.add_field(name=f"{prefix}setup welcomechannel <#channel>",
                    value="Set the server\'s welcome channel! All welcome messages will be sent to this channel.",
                    inline=False)
    embed.add_field(name=f"{prefix}setup welcometext <message>",
                    value="Set a custom welcome message to be sent in the specified welcome channel.\nAvailable parameters: {membercount}, {guild}, {user}, {mention}",
                    inline=False)
    embed.add_field(name=f"{prefix}setup privset <message>",
                    value="Set a custom welcome message to be sent in DMs to the new user. \nAvailable parameters: {members}, {guild}, {user}, {mention}",
                    inline=False)
    embed.add_field(name=f"{prefix}setup welcomerole <Role>",
                    value="Set a custom welcome role to be added to the new user. \n**NOTE: Role name is case-sensitive**",
                    inline=False)
    embed.add_field(name=f"{prefix}setup captcha <True or False>",
                    value=f"Set a captcha that the user has to solve before being verified. \n**NOTE: Role name MUST be set first using {prefix}setup welcomerole <Role>**",
                    inline=False)
    embed.add_field(name=f"{prefix}setup muterole <optional name>",
                    value="Create and set a muterole for the server.",
                    inline=False)
    embed.add_field(name=f"{prefix}setup leavemsg <message>",
                    value="Set a custom leave message that will be sent into the same channel as the welcome message.",
                    # add an option for changing the channel in the future.
                    inline=False)
    embed.add_field(name=f"{prefix}setup spamdetection <True or False>",
                    value="Set spam detection on, when if the user does not have the Manage Messages permission, they will be muted. \n**NOTE: Muterole must be set prior to usage of this command!**",
                    inline=False)
    embed.add_field(name=f"{prefix}setup logs <#channel> <True or False>",
                    value="Set up logs to a specific channel. **MAKE SURE I HAVE PERMISSION TO READ MESSAGES, SEND MESSAGES, AND EMBED LINKS. ",
                    inline=False)
    embed.add_field(name=f"{prefix}setup ghostping <True or False>",
                    value="Set up anti-ghost pinging. Works when the message is deleted or edited. Sends a message in the chat the ping was sent in.",
                    inline=False)
    embed.set_footer(text=f"InfiniBot Server Greetings Help | Requested by: {ctx.author.name}",
                     icon_url=client.user.avatar_url)
    await ctx.send(embed=embed)


@setup.command()
@commands.has_permissions(manage_messages = True)
async def welcomechannel(ctx, channel: discord.TextChannel = None):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if channel is None:
        desc = f"```{prefix}setup welcomechannel [channel ID or mention]```"
        embed = discord.Embed(title = "Incorrect Usage!", description = desc, color = discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    if ctx.message.author.guild_permissions.manage_messages:
        res = await channelperms(channel)
        print(res)
        if not res:
            return await ctx.send(
                f"Please give me permission to `View Channel`, `Send Messages`, and `Embed Links` in {channel.mention} before proceeding.")

        if channel.is_nsfw():
            return await ctx.send(f"{channel.mention} is marked as NSFW, so I cannot send welcome messages in this channel.")
        collection = db['config']
        query = {'_id': ctx.guild.id}
        if collection.count_documents(query) == 0:
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                "welcomechannel": channel.id
            }
            collection.insert_one(ping_cm)
            return await ctx.send(f"{channel.mention} has been set as the welcome channel for {ctx.guild.name}!")
        else:
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'welcomechannel': channel.id}})
            return await ctx.send(f"{channel.mention} has been updated as the welcome channel for {ctx.guild.name}!")
    else:
        await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
        return


@setup.command(aliases=['welcomemsg', 'welcomemessage'])
@commands.has_permissions(manage_messages = True)
async def welcometext(ctx, *, text : str = None):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if text is None:
        desc = f"```{prefix}setup welcometext [text]```"
        embed = discord.Embed(title = "Incorrect Usage!", description = desc, color = discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    membercount = ctx.guild.member_count
    member = ctx.author.mention
    user = ctx.author.name
    guild = ctx.guild.name
    if len(text) > 2000:
        return await ctx.send(f"I cannot send this message due to discord limitations.")
    if ctx.message.author.guild_permissions.manage_messages:
        collection = db['config']
        query = {'_id': ctx.guild.id}
        if collection.count_documents(query) == 0:
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                "welcomemsg": text.strip()
            }
            collection.insert_one(ping_cm)
        else:
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'welcomemsg': text.strip()}})
        embed = discord.Embed(
        description=str(text).format(members=membercount, member=member, user=user, guild=guild),
        color=discord.Color.blurple(), timestamp = datetime.datetime.utcnow())
        embed.set_author(name=f'{ctx.author.name} just joined the server!', icon_url=f'{ctx.author.avatar_url}')
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(content = f"Message has been set to {text}. EXAMPLE:", embed=embed)




@setup.command(aliases=['welcomenick', 'welconickname'])
@commands.has_permissions(manage_nicknames = True)
async def onjoinnick(ctx, *, nick = None):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if nick is None:
        desc = f"```{prefix}setup welcometext [text]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    if len(nick.strip()) > 20:
        return await ctx.send(f"I cannot set this nickname due to Discord limitations.")
    collection = db['config']
    query = {'_id': ctx.guild.id}
    if collection.count_documents(query) == 0:
        ping_cm = {
            "_id": ctx.guild.id,
            "name": ctx.guild.name,
            "welcomenick": nick.strip()
        }
        collection.insert_one(ping_cm)
        return await ctx.send(f"The welcomenick for {ctx.guild.name} has been set to {nick.strip()}")
    else:
        collection.update_one({'_id': ctx.guild.id}, {'$set': {'welcomenick': nick.strip()}})
        return await ctx.send(f"The welcomenick for {ctx.guild.name} has been updated to {nick.strip()}")

# @setup.command(aliases=['toxicitydetect'])
# async def toxicitydetection(ctx, enab:bool = None):
#     db = sqlite3.connect('main.sqlite')
#     cursor = db.cursor()
#     name = f"GUILD{ctx.guild.id}"
#     cursor.execute(f"SELECT prefix from {name} WHERE user_id = {ctx.guild.id}")
#     result = cursor.fetchone()
#     if str(result[0]) == "None":
#         result = ("%", "Hi")
#     if enab is None:
#         desc = f"```{result[0]}setup toxicitydetection [True or False]```"
#         embed = discord.Embed(title = "Incorrect Usage!", description = desc, color = discord.Color.red())
#         embed.set_footer(text="Parameters in [] are required and () are optional")
#         return await ctx.send(embed=embed)
#     if ctx.message.author.guild_permissions.manage_messages:
#         sql = (f"UPDATE {name} SET toxicitydetect = ? WHERE user_id = ?")
#         val = (enab, ctx.guild.id)
#         cursor.execute(sql, val)
#         db.commit()
#         if enab:
#             try:
#                 await ctx.send(f"Toxicity detection for {ctx.guild.name} has been enabled!")
#                 await asyncio.sleep(1)
#                 await ctx.send(f"{ctx.author.mention}, what would you like the message to be after detecting a message?\n"
#                                "```Params are: \n"
#                                "`-` {member} (mentions user who send message)\n"
#                                "`-` {user} (doesn't mention user who sent message, but prints their name.)\n"
#                                "`-` {guild} for the server the message was sent in.\n"
#                                "Example: {member}, here in {guild} we want to keep a welcoming environment.\n"
#                                "**NOTE:** Messages delete after 30 seconds.```")
#                 def check(m):
#                     return m.channel == ctx.channel and m.author == ctx.author
#                 msg = await client.wait_for('message', check=check, timeout = 60)
#                 if len(msg.content) > 1000:
#                     return await ctx.send(f"Please keep your message under 1000 characters.")
#                 name = f"GUILD{ctx.guild.id}"
#                 sql = (f"UPDATE {name} SET toxicmsg = ? WHERE user_id = ?")
#                 val = (msg.content, ctx.guild.id)
#                 cursor.execute(sql, val)
#                 db.commit()
#                 cursor.close()
#                 db.close()
#                 return await ctx.send(f"**{msg.content}** has been saved as the toxicity detection message for {ctx.guild.name},")
#             except asyncio.TimeoutError:
#                 return await ctx.send(f"This creation session has timed out, but toxicity detection has been enabled.")
#         else:
#             await ctx.send(f"Toxicity detection for {ctx.guild.name} has been disabled!")
#     else:
#         await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
#         return

@setup.command(aliases=['minecraftip'])
async def mcip(ctx, *, text:str = None):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if text is None:
        desc = f"```{prefix}setup mcip [ip]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    if ctx.message.author.guild_permissions.manage_messages:
        collection = db['config']
        query = {'_id': ctx.guild.id}
        if collection.count_documents(query) == 0:
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                "mcip": text.strip()
            }
            collection.insert_one(ping_cm)
            return await ctx.send(f"The Minecraft IP for {ctx.guild.name} has been set to {text.strip()}")
        else:
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'mcip': text.strip()}})
            return await ctx.send(f"The Minecraft IP for {ctx.guild.name} has been updated to {text.strip()}")
    else:
        await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
        return



@setup.command(aliases=['XP', 'levelups'])
async def levels(ctx, enab = True):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if str(enab).lower() not in ['true', 'false']:
        desc = f"```{prefix}setup levels [True or False]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    if ctx.message.author.guild_permissions.manage_messages:
        collection = db['config']
        query = {'_id': ctx.guild.id}
        if collection.count_documents(query) == 0:
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                "levelups": f"{'on' if enab else ''}"
            }
            collection.insert_one(ping_cm)
            return await ctx.send(f"Levelups have been toggled to `{'on' if enab else 'off'}` for {ctx.guild.name}!")
        else:
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'levelups': f"{'on' if enab else ''}"}})
            return await ctx.send(f"Levelups have been toggled to `{'on' if enab else 'off'}` for {ctx.guild.name}!")
    else:
        await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
        return



@setup.command(aliases=['antighostping', 'antighost'])
async def ghostping(ctx, enab=True):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if str(enab).lower() not in ['true', 'false']:
        desc = f"```{prefix}setup ghostping [True or False]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    if ctx.message.author.guild_permissions.manage_messages:
        collection = db['config']
        query = {'_id': ctx.guild.id}
        if collection.count_documents(query) == 0:
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                "ghostpingon": f"{'on' if enab else ''}"
            }
            collection.insert_one(ping_cm)
            return await ctx.send(f"Ghostpings have been toggled to `{'on' if enab else 'off'}` for {ctx.guild.name}!")
        else:
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'ghostpingon': f"{'on' if enab else ''}"}})
            return await ctx.send(f"Ghostpings have been toggled to `{'on' if enab else 'off'}` for {ctx.guild.name}!")
    else:
        await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
        return


@setup.command(aliases=['dmset', 'privmsg', 'privatemsg', 'privatemessage', 'dmmsg', 'dmsg'])
async def privset(ctx, *, text:str=None):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if text is None:
        desc = f"```{prefix}setup privset [text]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    membercount = ctx.guild.member_count
    mention = ctx.author.mention
    user = ctx.author.name
    guild = ctx.guild.name
    if ctx.message.author.guild_permissions.manage_messages:
        collection = db['config']
        query = {'_id': ctx.guild.id}
        if collection.count_documents(query) == 0:
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                "priv_welcomemsg": text.strip()
            }
            collection.insert_one(ping_cm)
        else:
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'priv_welcomemsg': text.strip()}})
        embed = discord.Embed(
        description=str(text).format(members=membercount, mention=mention, user=user, guild=guild),
        color=discord.Color.blurple(), timestamp = datetime.datetime.utcnow())
        embed.set_author(name=f'Welcome to {ctx.guild.name}!', icon_url=f'{ctx.guild.icon_url}')
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(content = f"Welcome DM has been updated to ```{text}```", embed = embed)
    else:
        await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
        return

@setup.command()
async def welcomerole(ctx, *, role : discord.Role = None):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if role is None:
        desc = f"```{prefix}setup welcomerole [Role Name]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)

    if ctx.message.author.guild_permissions.manage_messages:
        rolez = discord.utils.get(ctx.guild.roles, name=role.name)
        if rolez is None:
            return await ctx.send(f"`{role}` is not a valid role in **{ctx.guild.name}**.")
        if rolez >= ctx.guild.me.top_role:
            return await ctx.send(f"`{role}` is higher than or equal to my top role in **{ctx.guild.name}**. You must make my role higher than this for me to assign it.")
        if rolez.is_default():
            return await ctx.send(f"You cannot set the role to be `@everyone` because everyone has it by default.")
        if rolez.is_bot_managed():
            return await ctx.send(f"You cannot assign a role that is managed by a bot.")
        if rolez.is_integration():
            return await ctx.send(f"You cannot assign a role that is managed by an integration.")
        if rolez.is_premium_subscriber():
            return await ctx.send(f"You cannot assign a role that can only be assigned to server boosters.")
        if rolez >= ctx.author.top_role:
            if ctx.author.id == ctx.guild.owner_id:
                pass
            else:
                return await ctx.send("You cannot assign a role that is higher than your own.")
        collection = db['config']
        query = {'_id': ctx.guild.id}
        if collection.count_documents(query) == 0:
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                "welcomerole": role.id
            }
            collection.insert_one(ping_cm)
        else:
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'welcomerole': role.id}})
        desc = f'Welcome role: **{role.mention}**\n\n' \
               f'Make sure that **{role.mention}** is the exact name of the role, as it is case-sensitive. \nUse the command again if you wish to update.\n\n' \
               f'Also, please make my highest role higher than **{role.mention}** so I can assign it.'
        embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp = datetime.datetime.utcnow())
        embed.set_author(name=f'{client.user.name} Welcomer', icon_url=client.user.avatar_url)
        embed.set_footer(text="InfiniBot Welcomer")
        await ctx.reply(embed=embed)
        return
    else:
        await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
        return


@setup.command(aliases=['bl', 'blackl'])
async def blacklist(ctx, enab : bool = False):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if str(enab).lower() not in ['true', 'false']:
        desc = f"```{prefix}setup blacklist [True or False]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)

    if ctx.message.author.guild_permissions.manage_messages:
        collection = db['config']
        query = {'_id': ctx.guild.id}
        if collection.count_documents(query) == 0:
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                "blacklistenab": f"{'on' if enab else ''}"
            }
            collection.insert_one(ping_cm)
            return await ctx.send(f"Blacklist for {ctx.guild.name} has been toggled to {'on' if enab else 'off'}!")
        else:
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'blacklistenab': f"{'on' if enab else ''}"}})
            return await ctx.send(f"Blacklist for {ctx.guild.name} has been toggled to {'on' if enab else 'off'}!")
    else:
        await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
        return


@setup.command(aliases=['byemsg', 'leavemessage', 'leavemsg'])
async def goodbyemsg(ctx, *, text : str = None):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if text is None:
        desc = f"```{prefix}setup goodbyemsg [text]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)

    if ctx.message.author.guild_permissions.manage_messages:
        collection = db['config']
        query = {'_id': ctx.guild.id}
        if collection.count_documents(query) == 0:
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                "leavemsg": text.strip()
            }
            collection.insert_one(ping_cm)
            await ctx.send(f"The goodbye message for {ctx.guild.name} has been set to {text.strip()}! \nExample usage:")
        else:
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'leavemsg': text.strip()}})
            await ctx.send(f"The goodbye message for {ctx.guild.name} has been updated to {text.strip()}! \nExample Usage:")
        membercount = ctx.guild.member_count
        mention = ctx.author.mention
        user = ctx.author.name
        guild = ctx.guild.name
        embed = discord.Embed(
            description=str(text).format(members=membercount, mention=mention, user=user, guild=guild),
            color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=f'{ctx.author.avatar_url}')
        embed.set_author(name=f'{ctx.author.name} just left the server.', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text=f"User ID: {ctx.author.id}")
        await ctx.send(embed=embed)

    else:
        await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
        return


@setup.command(aliases=['starchannel', 'starchan'])
async def starboardchannel(ctx, channel: discord.TextChannel = None):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if channel is None:
        desc = f"```{prefix}setup starboardchannel [channel mention]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)

    if ctx.message.author.guild_permissions.manage_messages:
        res = await channelperms(channel)
        if not res:
            return await ctx.send(
                f"Please give me permission to `View Channel`, `Send Messages`, and `Embed Links` in {channel.mention} before proceeding.")
        collection = db['config']
        query = {'_id': ctx.guild.id}
        if collection.count_documents(query) == 0:
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                "starchannel": channel.id
            }
            collection.insert_one(ping_cm)
            await ctx.send(f"The starboard channel for {ctx.guild.name} has been set to {channel.mention}!")
        else:
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'starchannel': channel.id}})
            await ctx.send(
                f"The starboard channel for {ctx.guild.name} has been updated to {channel.mention}!")
    else:
        await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
        return

@setup.command(aliases = ['servercaptcha'])
async def captcha(ctx, text:bool=True):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if str(text).lower() not in ['true', 'false']:
        desc = f"```{prefix}setup captcha [True or False]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    if text is None:
        return
    if ctx.message.author.guild_permissions.manage_messages:
        collection = db['config']
        query = {'_id': ctx.guild.id}
        if collection.count_documents(query) == 0:
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                "captchaon": f"{'on' if text else ''}"
            }
            collection.insert_one(ping_cm)
            await ctx.send(f"Server captcha for {ctx.guild.name} has been toggled to {'on' if text else 'off'}!")
        else:
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'captchaon': f"{'on' if text else ''}"}})
            await ctx.send(
                f"Server captcha for {ctx.guild.name} has been toggled to {'on' if text else 'off'}!")
    else:
        await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
        return


@setup.command(aliases = ['spamdetect'])
async def spamdetection(ctx, text : bool =False):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if str(text).lower() not in ['true', 'false']:
        desc = f"```{prefix}setup spamdetection [True or False]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    if text is None:
        return
    if ctx.message.author.guild_permissions.manage_messages:
        collection = db['config']
        query = {'_id': ctx.guild.id}
        if collection.count_documents(query) == 0:
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                "spamdetect": f"{'on' if text else ''}"
            }
            collection.insert_one(ping_cm)
            await ctx.send(f"Spam detection for {ctx.guild.name} has been toggled to {'on' if text else 'off'}!")
        else:
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'spamdetect': f"{'on' if text else ''}"}})
            await ctx.send(
                f"Spam detection for {ctx.guild.name} has been toggled to {'on' if text else 'off'}!")
    else:
        await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
        return


@setup.command(aliases=['logs', 'log'])
async def logging(ctx, setup : bool = True, channel: discord.TextChannel = None):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if str(setup).lower() not in ['true', 'false']:
        desc = f"```{prefix}setup logging [True or False] [channel]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    if channel is None:
        if not setup:
            collection = db['config']
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                ping_cm = {
                    "_id": ctx.guild.id,
                    "name": ctx.guild.name,
                    "logging": f"{'on' if setup else ''}"
                }
                collection.insert_one(ping_cm)
                return await ctx.send(f"Logging for {ctx.guild.name} has been toggled to {'on' if setup else 'off'}!")
            else:
                collection.update_one({'_id': ctx.guild.id}, {'$set': {'logging': f"{'on' if setup else ''}"}})
                return await ctx.send(
                    f"Logging for {ctx.guild.name} has been toggled to {'on' if setup else 'off'}!")

        desc = f"```{prefix}setup logging [True or False] [channel]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)

    if ctx.message.author.guild_permissions.manage_messages:
        res = await channelperms(channel)
        if not res:
            return await ctx.send(
                f"Please give me permission to `View Channel`, `Send Messages`, and `Embed Links` in {channel.mention} before proceeding.")
        if channel.is_nsfw():
            return await ctx.send(f"{channel.mention} is an NSFW channel, so I cannot send log messages here.")
        collection = db['config']
        query = {'_id': ctx.guild.id}
        if collection.count_documents(query) == 0:
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                "logging": f"{'on' if setup else ''}"
            }
            collection.insert_one(ping_cm)
            await ctx.send(f"Logging for {ctx.guild.name} has been toggled to {'on' if setup else 'off'}!")
        else:
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'logging': f"{'on' if setup else ''}"}})
            await ctx.send(
                f"Logging for {ctx.guild.name} has been toggled to {'on' if setup else 'off'}!")
        collection = db['config']
        query = {'_id': ctx.guild.id}
        if collection.count_documents(query) == 0:
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                "logchannel": channel.id
            }
            collection.insert_one(ping_cm)
            return await ctx.send(f"Logging channel for {ctx.guild.name} has been set to {channel.mention}!")
        else:
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'logchannel': channel.id}})
            return await ctx.send(
                f"Logging channel for {ctx.guild.name} has been updated to {channel.mention}!")
    else:
        await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
        return

@setup.command()
async def muterole(ctx, *, name="Muted"):
    if len(name) > 20:
        return await ctx.send(f"Make sure that `{name}` is kept under 20 characters.")
    named = f"GUILD{ctx.guild.id}"
    db = cluster[named]
    if ctx.author.guild_permissions.manage_roles:
        message = await ctx.send("Updating channel overrides...")
        mutedRole = await ctx.guild.create_role(name=name)
        for channel in ctx.guild.channels:
            if str(channel.type).lower() == 'category':
                continue
            if str(channel.type).lower() == 'text':
                await channel.set_permissions(mutedRole, send_messages=False)
            if str(channel.type).lower() == 'voice':
                continue
        collection = db['config']
        query = {'_id': ctx.guild.id}
        if collection.count_documents(query) == 0:
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                "muterole": mutedRole.id
            }
            collection.insert_one(ping_cm)
            await ctx.send(f"The muterole for {ctx.guild.name} has been set to {mutedRole.mention}!")
        else:
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'muterole': mutedRole.id}})
            await ctx.send(
                f"The muterole for {ctx.guild.name} has been updated to {mutedRole.mention}!")
        # else:
        #     named = f"GUILD{ctx.guild.id}"
        #     cursor.execute(f"SELECT muterole from {named} where user_id = {ctx.guild.id}")
        #     result1 = cursor.fetchone()
        #     await ctx.send(
        #         f"There is already muterole {str(result1[0])} saved for server {ctx.guild.name}. Would you like to update it to {name}? \nPress `y` to confirm or anything else to cancel.")
        #     message = await client.wait_for('message', check=check, timeout=30)
        #     if message.content.lower() == 'y':
        #         for k in ctx.guild.roles:
        #             if str(k) == str(name):
        #                 rolez = discord.utils.get(ctx.guild.roles, name=name)
        #                 if rolez is None:
        #                     return await ctx.send(f"`{role}` is not a valid role in **{ctx.guild.name}**.")
        #                 if rolez >= ctx.guild.me.top_role:
        #                     return await ctx.send(
        #                         f"`{role}` is higher than or equal to my top role in **{ctx.guild.name}**. You must make my role higher than this for me to assign it.")
        #                 if rolez.is_default():
        #                     return await ctx.send(
        #                         f"You cannot set the role to be `@everyone` because everyone has it by default.")
        #                 if rolez.is_bot_managed():
        #                     return await ctx.send(f"You cannot assign a role that is managed by a bot.")
        #                 if rolez.is_integration():
        #                     return await ctx.send(f"You cannot assign a role that is managed by an integration.")
        #                 if rolez.is_premium_subscriber():
        #                     return await ctx.send(
        #                         f"You cannot assign a role that can only be assigned to server boosters.")
        #                 if rolez >= ctx.author.top_role:
        #                     if ctx.author.id == ctx.guild.owner_id:
        #                         pass
        #                     else:
        #                         return await ctx.send(f"You cannot assign a role that is higher than your own. ")
        #                 sql = ("UPDATE main SET muterole = ? WHERE guild_id = ?")
        # #                 val = (name, ctx.guild.id)
        # #                 cursor.execute(sql, val)
        # #                 db.commit()
        # #                 cursor.close()
        # #                 db.close()
        # #                 await ctx.send(f"Muterole role has been updated to `{name}`")
        #                 return
        #         sql = (f"UPDATE {named} SET muterole = ? WHERE user_id = ?")
        #         val = (name, ctx.guild.id)
        #         cursor.execute(sql, val)
        #         db.commit()
        #         cursor.close()
        #         db.close()
        #         message = await ctx.send("Updating channel overrides...")
        #         mutedRole = await ctx.guild.create_role(name=name)
        #         # role = discord.utils.get(guild.roles, name=muted)
        #         for channel in ctx.guild.channels:
        #             if str(channel.type).lower() == 'category':
        #                 continue
        #             if str(channel.type).lower() == 'text':
        #                 await channel.set_permissions(mutedRole, send_messages=False)
        #             if str(channel.type).lower() == 'voice':
        #                 continue
        #         await asyncio.sleep(2)
        #         await message.edit(
        #             content=f"Muterole `{name}` has been created and set as the muterole for **{ctx.guild.name}**.")
        #         return
        #     else:
        #         await ctx.send('Muterole setup has been cancelled.')
        #         return
        # cursor.execute(sql, val)
        # db.commit()
        # cursor.close()
        # db.close()

@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    name = f"GUILD{member.guild.id}"
    db = cluster[name]
    collection = db['config']
    res = collection.find({'_id': member.guild.id})
    for i in res:
        prefix = i['prefix']
        logenab = i['logging']
        logchannel = i['logchannel']
    if not before.channel and after.channel:
        collection = db['serverstats']
        ping_cm = {
            "_id": member.id,
            "name": member.name,
            "guild": member.guild.id,
            "gname": member.guild.name,
            "vcstart": datetime.datetime.utcnow()
        }
        x = collection.insert_one(ping_cm)
        if logenab == '' or logchannel == '':
            pass
        else:
            desc = f"{member.mention} joined `{after.channel.name}`"
            embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"{member.display_name} has joined a voice channel!", icon_url=member.avatar_url)
            embed.set_thumbnail(url=member.guild.icon_url)
            channel = client.get_channel(int(logchannel))
            return await channel.send(embed=embed)
    elif before.channel and after.channel:
        if before.channel == after.channel:
            return
        collection = db['serverstats']
        res = collection.find({'_id': member.id})
        for i in res:
            starttime = i['vcstart']
        collection.delete_one({'_id':member.id})
        x = pd.to_datetime(starttime)
        z = (abs(datetime.datetime.utcnow() - x))
        vcsecs = int(z.total_seconds())
        collection = db['serverstats']
        res = collection.find({'_id': member.guild.id})
        for i in res:
            vcmins = i['vcsecs']
        if vcmins == "":
            collection.update_one({'_id' : member.guild.id}, {"$set": {'vcsecs': vcsecs}})
        else:
            collection.update_one({'_id' : member.guild.id}, {"$set": {'vcsecs': (int(vcmins) + vcsecs)}})
        collection = db['serverstats']
        ping_cm = {
            "_id": member.id,
            "name": member.name,
            "guild": member.guild.id,
            "gname": member.guild.name,
            "vcstart": datetime.datetime.utcnow()
        }
        x = collection.insert_one(ping_cm)
        if logchannel == '' or logenab == '':
            pass
        else:
            desc = f"{member.mention} left `{before.channel.name}`"
            embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"{member.display_name} has left a voice channel!", icon_url=member.avatar_url)
            embed.set_thumbnail(url=member.guild.icon_url)
            channel = client.get_channel(int(logchannel))
            await channel.send(embed=embed)
            desc = f"{member.mention} joined `{after.channel.name}`"
            embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"{member.display_name} has joined a voice channel!", icon_url=member.avatar_url)
            embed.set_thumbnail(url=member.guild.icon_url)
            channel = client.get_channel(int(logchannel))
            await channel.send(embed=embed)
    elif before.channel and not after.channel:
        collection = db['serverstats']
        res = collection.find({'_id': member.id})
        for i in res:
            starttime = i['vcstart']
        collection.delete_one({'_id': member.id})
        x = pd.to_datetime(starttime)
        z = (abs(datetime.datetime.utcnow() - x))
        vcsecs = int(z.total_seconds())
        collection = db['serverstats']
        res = collection.find({'_id': member.guild.id})
        for i in res:
            vcmins = i['vcsecs']
        if vcmins == "":
            collection.update_one({'_id': member.guild.id}, {"$set": {'vcsecs': vcsecs}})
        else:
            collection.update_one({'_id': member.guild.id}, {"$set": {'vcsecs': (int(vcmins) + vcsecs)}})
        if logchannel == '' or logenab == '':
            pass
        else:
            desc = f"{member.mention} left `{before.channel.name}`"
            embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"{member.display_name} has left a voice channel!", icon_url=member.avatar_url)
            embed.set_thumbnail(url=member.guild.icon_url)
            channel = client.get_channel(int(logchannel))
            await channel.send(embed=embed)

@client.event
async def on_message_delete(message):
    if message.author.bot:
        return
    if message.author.system:
        return
    name = f"GUILD{message.guild.id}"
    db = cluster[name]
    collection = db['config']
    res = collection.find({'_id': message.guild.id})
    for i in res:
        ghostcount = i['ghostcount']
        ghostpingon = i['ghostpingon']
        logchannel = i['logchannel']
        logging = i['logging']

    if message.mentions:
        if str(ghostpingon) == "on":
            if str(ghostcount) == '':
                collection.update_one({'_id': message.guild.id}, {"$set": {'ghostcount': 1}})
            else:
                collection.update_one({'_id': message.guild.id}, {"$set": {'ghostcount': ghostcount + 1}})
            desc = f"**Ghost ping detected!!**\n\nMessage Author: {message.author.mention}\nMessage: {message.content}"
            embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp = datetime.datetime.utcnow())
            embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_footer(text=f"{message.guild.name} Anti-Ghost Ping")
            await message.channel.send(embed=embed)
        else:
            pass
    if '@everyone' in str(message.content.lower()) or "@here" in str(message.content.lower()):
        if str(ghostpingon) == "on":
            if str(ghostcount) == '':
                collection.update_one({'_id': message.guild.id}, {"$set": {'ghostcount': 1}})
            else:
                collection.update_one({'_id': message.guild.id}, {"$set": {'ghostcount': ghostcount + 1}})
            desc = f"**Ghost ping detected!!**\n\nMessage Author: {message.author.mention}\nMessage: {message.content}"
            embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp = datetime.datetime.utcnow())
            embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_footer(text=f"{message.guild.name} Anti-Ghost Ping")
            await message.channel.send(embed=embed)
        else:
            pass

    if message.role_mentions:
        if str(ghostpingon) == "on":
            if str(ghostcount) == '':
                collection.update_one({'_id': message.guild.id}, {"$set": {'ghostcount': 1}})
            else:
                collection.update_one({'_id': message.guild.id}, {"$set": {'ghostcount': ghostcount + 1}})
            desc = f"**Ghost ping detected!!**\n\nMessage Author: {message.author.mention}\nMessage: {message.content}"
            embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp = datetime.datetime.utcnow())
            embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_footer(text=f"{message.guild.name} Anti-Ghost Ping")
            await message.channel.send(embed=embed)
        else:
            pass

    # j = discovery.build(
    #     "commentanalyzer",
    #     "v1alpha1",
    #     developerKey=random.choice(PERSPECTIVE_KEYS),
    #     discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    #     static_discovery=False,
    # )
    #
    # # analyze_request = {
    # #     'comment': {'text': f'{message.content}'},
    # #     'requestedAttributes': {'TOXICITY': {}}
    # # }
    #
    # response = j.comments().analyze(body=analyze_request).execute()
    # title = f"Message deleted in #{message.channel.name}"
    # if (float(response['attributeScores']['TOXICITY']['summaryScore']['value']) * 100) > 85:
    #     cursor.execute(f"SELECT toxic from main WHERE guild_id = {message.guild.id}")
    #     result72 = cursor.fetchone()
    #     if str(result72[0]).lower() == 'none' or str(result72[0]) == '0':
    #         title = f"Message deleted in #{message.channel.name}"
    #     elif str(result72[0]) == '1':
    #         title = f"TOXIC message deleted in #{message.channel.name}"

    if str(logging) == '':
        return
    if str(logchannel) == '':
        return
    pfp = message.author.avatar_url
    author = message.author
    channel = client.get_channel(id=int(logchannel))
    mid = message.id
    deletedem = discord.Embed(title=f"Message deleted in #{message.channel.name}",
                              description=f"```{message.content}```", color=discord.Color.red(), timestamp = datetime.datetime.utcnow())
    deletedem.set_author(name=str(author), icon_url=pfp)
    deletedem.set_footer(text=f"Message ID: {mid}")
    await channel.send(embed=deletedem)
    return

@client.event
async def on_member_join(member):
    name = f"GUILD{member.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': member.guild.id})
    for i in results:
        welcomechannel = i['welcomechannel']
        welcomenick = i['welcomenick']
        logchannel = i['logchannel']
        logging = i['logging']
        welcomemsg = i['welcomemsg']
        privmsg = i['priv_welcomemsg']
        welcomerole = i['welcomerole']
        captchaon = i['captchaon']
    if str(welcomenick) == '':
        pass
    else:
        try:
            await member.edit(nick=str(welcomenick))
        except discord.Forbidden:
            pass
    membercount = member.guild.member_count
    mention = member.mention
    user = member.name
    guild = member.guild
    embed = discord.Embed(
        description=str(welcomemsg).format(members=membercount, member = mention, mention=mention, user=user, guild=guild),
        color=discord.Color.blurple(), timestamp = datetime.datetime.utcnow())
    embed.set_author(name=f'{member.name} just joined the server!', icon_url=f'{member.avatar_url}')
    embed.set_thumbnail(url=member.avatar_url)
    try:
        channel = client.get_channel(id=int(welcomechannel))
        await channel.send(embed=embed)
    except Exception:
        pass

    try:
        if privmsg == '':
            pass
        else:
            uembed = discord.Embed(
                description=str(privmsg).format(members=membercount, member=mention, mention=mention, user=user,
                                                guild=guild),
                color=discord.Color.green())
            uembed.set_author(name=f'Welcome to {member.guild.name}!', icon_url=f'{member.guild.icon_url}')
            await member.send(embed=uembed)
    except discord.Forbidden:
        pass

    if str(logging) == 'on':
        try:
            embed1 = discord.Embed(title="Member joined server", description=member.mention,
                                    color=discord.Color.green(), timestamp = datetime.datetime.utcnow())
            embed1.set_author(name=f"{member.guild.name}", icon_url=member.avatar_url)
            embed1.set_thumbnail(url=member.avatar_url)
            channel = client.get_channel(id=int(logchannel))
            await channel.send(embed=embed1)
        except discord.Forbidden:
            pass

    if str(captchaon) == "on":
        res = await servercaptcha(member)
        if res:
            await member.add_roles(discord.utils.get(member.guild.roles, id=int(welcomerole)))
        else:
            pass
    else:
        if str(welcomerole) == '':
            return
        await member.add_roles(discord.utils.get(member.guild.roles, id=int(welcomerole)))

@client.event
async def on_member_remove(member):
    name = f"GUILD{member.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': member.guild.id})
    for i in results:
        welcomechannel = i['welcomechannel']
        logchannel = i['logchannel']
        logging = i['logging']
        leavemsg = i['leavemsg']
    if str(welcomechannel) == '':
        return
    else:
        if str(leavemsg) == '':
            leavemsg = "{user} has left the server."
        membercount = member.guild.member_count
        mention = member.mention
        user = member.name
        guild = member.guild
        embed = discord.Embed(
            description=str(leavemsg).format(members=membercount, mention=mention, user=user, guild=guild),
            color=discord.Color.red(), timestamp = datetime.datetime.utcnow())
        embed.set_thumbnail(url=f'{member.avatar_url}')
        embed.set_author(name=f'{member.name} just left the server.', icon_url=f'{member.avatar_url}')
        embed.set_footer(text=f"User ID: {member.id}")
        channel = client.get_channel(id=int(welcomechannel))
        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass
        try:
            channel1 = client.get_channel(id=int(logchannel))
            embed1 = discord.Embed(title=f"{member} has left the server", color=discord.Color.greyple(), timestamp = datetime.datetime.utcnow())
            embed1.set_author(name=member.guild.name, icon_url=member.guild.icon_url)
            embed1.set_thumbnail(url=member.avatar_url)
            embed1.set_footer(text=f"User ID: {member.id}")
            await channel1.send(embed=embed1)
            return
        except discord.Forbidden:
            return


@client.command()
async def spam(ctx):
    await ctx.send('I will begin spam in 5 4 3 2 1')


@client.event
async def on_message_edit(before, after):
    if before.author == client.user:
        return
    if before.author.bot:
        return
    name = f"GUILD{before.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': before.guild.id})
    for i in results:
        ghostpingon = i['ghostpingon']
        ghostcount = i['ghostcount']
        logging = i['logging']
        logchannel = i['logchannel']
    if before.mentions and not after.mentions:
        if str(ghostpingon) == "on":
            if str(ghostcount) == '':
                collection.update_one({"_id": before.guild.id}, {"$set": {'ghostcount': 1}})
            else:
                collection.update_one({"_id": before.guild.id}, {"$set": {'ghostcount': int(ghostcount) + 1}})
            desc = f"**Ghost ping detected!!**\n\nMessage Author: {before.author.mention}\nMessage: {before.content}"
            embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp = datetime.datetime.utcnow())
            embed.set_author(name=before.author.name, icon_url=before.author.avatar_url)
            embed.set_thumbnail(url=before.author.avatar_url)
            embed.set_footer(text=f"{before.guild.name} Anti-Ghost Ping")
            await before.channel.send(embed=embed)
        else:
            pass
    if ('@everyone' in str(before.content.lower()) or "@here" in str(before.content.lower())):
        if ('@everyone' not in str(after.content.lower()) and "@here" not in str(after.content.lower())):
            if str(ghostpingon) == "on":
                if str(ghostcount) == '':
                    collection.update_one({"_id": before.guild.id}, {"$set": {'ghostcount': 1}})
                else:
                    collection.update_one({"_id": before.guild.id}, {"$set": {'ghostcount': int(ghostcount) + 1}})
                desc = f"**Ghost ping detected!!**\n\nMessage Author: {before.author.mention}\nMessage: {before.content}"
                embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp = datetime.datetime.utcnow())
                embed.set_author(name=before.author.name, icon_url=before.author.avatar_url)
                embed.set_thumbnail(url=before.author.avatar_url)
                embed.set_footer(text=f"{before.guild.name} Anti-Ghost Ping")
                await before.channel.send(embed=embed)
            else:
                pass    

    if before.role_mentions and not after.role_mentions:
        if str(ghostpingon) == "on":
            if str(ghostcount) == '':
                collection.update_one({"_id": before.guild.id}, {"$set": {'ghostcount': 1}})
            else:
                collection.update_one({"_id": before.guild.id}, {"$set": {'ghostcount': int(ghostcount) + 1}})
            desc = f"**Ghost ping detected!!**\n\nMessage Author: {before.author.mention}\nMessage: {before.content}"
            embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp = datetime.datetime.utcnow())
            embed.set_author(name=before.author.name, icon_url=before.author.avatar_url)
            embed.set_thumbnail(url=before.author.avatar_url)
            embed.set_footer(text=f"{before.guild.name} Anti-Ghost Ping")
            await before.channel.send(embed=embed)
        else:
            pass

    if str(logchannel) == '' or str(logging) == '':
        return
    pfp = before.author.avatar_url
    channel = client.get_channel(id=int(logchannel))
    desc = f"{before.author.mention} edited a message in {before.channel.mention}! \n\nOriginal: ```{before.content}```\nUpdated: ```{after.content}```"
    embed = discord.Embed(description=f"{desc}\n[Jump to message!]({after.jump_url})", color=discord.Color.red(), timestamp = datetime.datetime.utcnow())
    embed.set_author(name=f"{before.author.name}", icon_url=pfp)
    embed.set_footer(text=f"Message ID: {before.id}")
    await channel.send(embed=embed)


@client.event
async def on_member_update(before, after):
    name = f"GUILD{before.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': before.guild.id})
    for i in results:
        logging = i['logging']
        logchannel = i['logchannel']
    if str(logging) == '' or str(logchannel) == '':
        return
    if before.display_name != after.display_name:
        channel = client.get_channel(id=int(logchannel))
        desc = f"Before: ```{before.display_name}``` \nAfter: ```{after.display_name}```"
        embed = discord.Embed(description=desc, color=discord.Color.greyple(), timestamp = datetime.datetime.utcnow())
        embed.set_author(name=f"{before.name} has updated their nickname!", icon_url=before.avatar_url)
        embed.set_footer(text=f"User ID: {before.id}")
        await channel.send(embed=embed)

    if before.roles != after.roles:
        channel = client.get_channel(id=int(logchannel))
        if len(before.roles) < len(after.roles):
            newRole = next(role for role in after.roles if role not in before.roles)
            embed = discord.Embed(title="Role was added!", description=newRole.mention, color=discord.Color.greyple(), timestamp = datetime.datetime.utcnow())
            embed.set_author(name=f"{before}", icon_url=before.avatar_url)
            embed.set_footer(text=f"User ID: {before.id} | Server: {before.guild.name}")
            await channel.send(embed=embed)
        if len(before.roles) > len(after.roles):
            newRole = next(role for role in before.roles if role not in after.roles)
            embed = discord.Embed(title="Role was removed!", description=newRole.mention, color=discord.Color.greyple(), timestamp = datetime.datetime.utcnow())
            embed.set_author(name=f"{before}", icon_url=before.avatar_url)
            embed.set_footer(text=f"User ID: {before.id} | Server: {before.guild.name}")
            await channel.send(embed=embed)


@client.event
async def on_guild_remove(guild):
    name = f"GUILD{guild.id}"
    cluster.drop_database(name)



@client.event
#doesnt work
async def on_user_update(before, after):
    name = f"GUILD{before.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': before.guild.id})
    for i in results:
        logging = i['logging']
        logchannel = i['logchannel']
    if str(logchannel) == '' or str(logging) == '':
        return
    channel = client.get_channel(id=int(logchannel))
    if before.avatar != after.avatar:
        embed = discord.Embed(title="Avatar was updated!", description=before.name, color=discord.Color.greyple(), timestamp = datetime.datetime.utcnow())
        embed.set_author(name=f"{before}", icon_url=before.avatar_url)
        embed.set_thumbnail(url=after.avatar_url)
        embed.set_footer(text=f"User ID: {before.id}")
        await channel.send(embed=embed)


@client.event
async def on_guild_role_create(role):
    name = f"GUILD{role.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': role.guild.id})
    for i in results:
        logging = i['logging']
        logchannel = i['logchannel']
    if str(logging) == '' or str(logchannel)  == '':
        return
    channel = client.get_channel(id=int(logchannel))
    embed = discord.Embed(title="New role was created!", description=role.mention, color=discord.Color.greyple(), timestamp = datetime.datetime.utcnow())
    embed.set_author(name=f"{role.guild.name}", icon_url=role.guild.icon_url)
    embed.set_footer(text=f"Server: {role.guild.name}")
    await channel.send(embed=embed)


@client.event
async def on_guild_role_delete(role):
    name = f"GUILD{role.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': role.guild.id})
    for i in results:
        logging = i['logging']
        logchannel = i['logchannel']
    if str(logging) == '' or str(logchannel) == '':
        return
    channel = client.get_channel(id=int(logchannel))
    embed = discord.Embed(title="Role was deleted", description=f"@{role.name}", color=discord.Color.greyple(), timestamp = datetime.datetime.utcnow())
    embed.set_author(name=f"{role.guild.name}", icon_url=role.guild.icon_url)
    embed.set_footer(text=f"Server: {role.guild.name}")
    await channel.send(embed=embed)


@client.event
async def on_guild_role_update(before, after):
    # check the documentation for specifics
    name = f"GUILD{before.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': before.guild.id})
    for i in results:
        logging = i['logging']
        logchannel = i['logchannel']
    if str(logging) == '' or str(logchannel) == '':
        return
    channel = client.get_channel(id=int(logchannel))
    embed = discord.Embed(title="Role was updated!", description=after.mention, color=discord.Color.greyple(), timestamp = datetime.datetime.utcnow())
    embed.set_author(name=f"{before.guild.name}", icon_url=before.guild.icon_url)
    embed.set_footer(text=f"Server: {before.guild.name}")
    await channel.send(embed=embed)


@client.event
async def on_member_ban(guild, member):
    name = f"GUILD{guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': guild.id})
    for i in results:
        logging = i['logging']
        logchannel = i['logchannel']
    if str(logging) == '' or str(logchannel) == '':
        return
    channel = client.get_channel(id=int(logchannel))
    embed = discord.Embed(title=f"Member was banned from {guild.name}:", description=member.mention,
                          color=discord.Color.greyple(), timestamp = datetime.datetime.utcnow())
    embed.set_author(name=f"{guild.name}", icon_url=guild.icon_url)
    embed.set_footer(text=f"Server: {guild.name}")
    await channel.send(embed=embed)


@client.event
async def on_member_unban(guild, member):
    name = f"GUILD{guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': guild.id})
    for i in results:
        logging = i['logging']
        logchannel = i['logchannel']
    if str(logging) == '' or str(logchannel) == '':
        return
    channel = client.get_channel(id=int(logchannel))
    embed = discord.Embed(title=f"User was unbanned from {guild.name}:", description=member.mention,
                          color=discord.Color.greyple(), timestamp=datetime.datetime.utcnow())
    embed.set_author(name=f"{guild.name}", icon_url=guild.icon_url)
    embed.set_footer(text=f"Server: {guild.name}")
    await channel.send(embed=embed)


@client.event
async def on_guild_channel_update(before, after):
    name = f"GUILD{before.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': before.guild.id})
    for i in results:
        logging = i['logging']
        logchannel = i['logchannel']
    if str(logging) == '' or str(logchannel) == '':
        return
    if before.name != after.name:
        channel = client.get_channel(id=int(logchannel))
        desc = f"`{before.name}` --> `{after.name}`"
        embed = discord.Embed(title=f"Channel name was updated in {before.guild.name}:",
                              description=f"{after.mention} \n\n{desc}",
                              color=discord.Color.greyple(), timestamp = datetime.datetime.utcnow())
        embed.set_author(name=f"{before.guild.name}", icon_url=before.guild.icon_url)
        embed.set_footer(text=f"Server: {before.guild.name}")
        await channel.send(embed=embed)
    #channel topic i believe falls under here

@client.event
async def on_guild_channel_create(channel):
    name = f"GUILD{channel.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': channel.guild.id})
    for i in results:
        logging = i['logging']
        logchannel = i['logchannel']
    if str(logging) == '' or str(logchannel) == '':
        return
    channel1 = client.get_channel(id=int(logchannel))
    embed = discord.Embed(title=f"New channel created in {channel.guild.name}:",
                          description=channel.mention,
                          color=discord.Color.greyple(), timestamp = datetime.datetime.utcnow())
    embed.set_author(name=f"{channel.guild.name}", icon_url=channel.guild.icon_url)
    embed.set_footer(text=f"Server: {channel.guild.name}")
    await channel1.send(embed=embed)


@client.event
async def on_guild_channel_delete(channel):
    name = f"GUILD{channel.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': channel.guild.id})
    for i in results:
        logging = i['logging']
        logchannel = i['logchannel']
    if str(logging) == '' or str(logchannel) == '':
        return
    channel1 = client.get_channel(id=int(logchannel))
    embed = discord.Embed(title=f"Channel deleted in {channel.guild.name}:",
                          description=f"**{channel.name}**",
                          color=discord.Color.greyple(), timestamp = datetime.datetime.utcnow())
    embed.set_author(name=f"{channel.guild.name}", icon_url=channel.guild.icon_url)
    embed.set_footer(text=f"Server: {channel.guild.name}")
    await channel1.send(embed=embed)

#
#@client.event
#async def on_raw_reaction_add(payload):
    #get message ID from guildID or something
    #compare that to this
    #video link: https://www.youtube.com/watch?v=0Yr4ddt7vbI


@client.command()
async def rage(ctx):
    await ctx.send('I have turned into Babatunde rage monsta')


@client.command()
async def xceptzion(ctx):
    await ctx.send('Xceptzion is very godly')


@client.command()
async def taran(ctx):
    await ctx.send('Taran betta very smart indian boi')


@client.command()
async def ethan(ctx):
    await ctx.send('Ethan very stupid need to drink milk boi')


@client.command()
async def cuss(ctx):
    await ctx.send('Why u ask for cuzzing words man')


@client.command()
async def cussleet(ctx):
    await ctx.send('shiz dam fuc bish AAAAAA')


@client.command()
async def spamisyummy(ctx):
    await ctx.send(
        'efhiiiiifwfeiiiiiwuffhebcdddddddddddddddddddddwwhejjjjjjjjjjjjjjjjjjjjjjjjjjjjjfhbbbbbbbbbbbbbbbbbbbbbehdoqwqijxxxxxxxxxxxxxxxxxxx ffffeiiiw,ssssssssssssssssssssssssfebbbbbbbbbbjjjjjjjjjjjjjjjjjjjwooooooooooooooooodjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjwoqqqqqqqqqqqqqqqqqlwkkkkkkkkkkkkkkkdjjjjjjjjossssssssssw,,,,,,,,,,,,,diiiiiiiiiifbbbbbbbeiiiiiiiiiskkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkeibbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbdkkkkkkkkkkkkkkkkc9999999999999w dhruv so godly man iuuuuuuuuuuuuuuudhbbbbbbbbbbbbbuwwwwwwwww')

@client.command()
async def epic(ctx):
    await ctx.send('All rappers are african so rap music is african music')

@client.command()
async def test(ctx):
    await ctx.send(len(client.users))

@client.command()
async def owner(ctx):
    await ctx.send('Bow down to ur master glizzybeam u peasant')


@client.command()
async def potato(ctx):
    await ctx.send("Everything on earth is a potato and man likes potato so this man will eat u")

@client.command()
async def techhelp(ctx):
    await ctx.send(
        "Hello, my name is Rajesh from Tech Support, how may I assist u today? I think the error is an 1D10T error, please stay on the line.")


@client.command()
async def alldogs(ctx):
    await ctx.send("https://www.youtube.com/watch?v=kyPzl8M4yCE")


@client.command()
async def arnav(ctx):
    await ctx.send(
        "Boy u already asked me for chopsticks we r out man. Go into the kitchen and steal one of the cooks chopsticks who knows what they did with them")


@client.command(aliases=['cnick', 'unick', 'usernick', 'changenick'])
@commands.has_permissions(manage_nicknames = True)
@commands.bot_has_guild_permissions(manage_nicknames = True)
async def nick(ctx, member: discord.Member, *, nick):
    try:
        if ctx.author.top_role <= member.top_role:
            return await ctx.send(f"You can't use this on a member above you.")
        if len(nick) > 32:
            return await ctx.send(f"You cannot set a nickname above 32 characters. Yours is `{len(nick)}`. ")
        await member.edit(nick=nick)
        await ctx.send('Nickname was changed for ' + member.mention)
    except discord.errors.Forbidden:
        if member.id == ctx.guild.owner_id:
            return await ctx.send("You cannot take action on the server owner.")
        await ctx.send(
            "I don't have permission to change the nickname of this person. You can fix that by going into server settings and giving me the `Manage Nicknames` permission.")

@nick.error
async def nick_err(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}nick [member] [nickname]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)

    if isinstance(error, commands.MissingPermissions):
        return await ctx.send(f"{ctx.author.name}, you can't use that!")
    if isinstance(error, commands.BotMissingPermissions):
        return await ctx.send("I don't have permission to `Manage Nicknames`. ")

@client.group(invoke_without_command =True)
async def help(ctx):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    embed = discord.Embed(color = discord.Color.green())
    embed.set_author(name=f"{client.user.name}'s Help Menu", icon_url = client.user.avatar_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    #add individual help for each command
    embed.set_footer(text=f"Made by glizzybeam7801#8196 and kidsonfilms#4635")
    #add some example commands
    embed.add_field(name="🛠️ Setup", value = f"Setup InfiniBot For {ctx.guild.name}!\n`{prefix}setup`")
    embed.add_field(name="🎮 Games", value = f"Play games with InfiniBot!\n`{prefix}help games`")
    embed.add_field(name="📣 Moderation", value = f"Moderate your server or take a step back and let InfiniBot moderate for you!\n`{prefix}help moderation`")
    embed.add_field(name="❓ Miscellaneous", value = f"These commands aren't sorted right now, but include everything.\n`{prefix}help misc`")
    embed.add_field(name="💰 Economy", value = f"Participate in an economy system! (Currently in development). \n`{prefix}help economy`")
    embed.add_field(name="📈 Server Stats",
                    value=f"See server stats for {ctx.guild.name} \n`{prefix}help serverstats`")
    embed.add_field(name="About Us!",value=f"[Invite Link](https://discord.com/api/oauth2/authorize?client_id=829464107710677022&permissions=4294307063&scope=bot%20applications.commands) - [Support Server](https://discord.gg/4VnUA8ZXyH)\nSend the devs feedback by using `{prefix}feedback`!" ,inline = False)
    await ctx.send(embed=embed)

@help.command(aliases = ['game'])
async def games(ctx):
    #fix this menu, its unclear
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    desc = f"Available Commands: ```play madlibs, play numberguess, talk, meme, joke, fight, reverse, typing, topwpm, servertopwpm, servertopstats, flip, rps```\n**NOTE:** Make sure you use the entire command to access. For example, `{prefix}play numberguess`, but it is only `{prefix}rps`."
    embed = discord.Embed(title = "🎮 Games Help", description= desc, color=discord.Color.green())
    embed.set_author(name=f"{client.user.name}'s Help Menu", icon_url=client.user.avatar_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Game Help | Requested by {ctx.author.name}")
    await ctx.send(embed=embed)


@help.command(aliases = ['mod', 'moderate'])
async def moderation(ctx):
    #check all commands
    desc = "Available Commands: ```nick, clear, ban, kick, unban, softban, tempmute, mute, lockdown, warn, warns, tempban, openticket, deleterole```"
    embed = discord.Embed(title="📣 Moderation Help", description=desc, color=discord.Color.green())
    embed.set_author(name=f"{client.user.name}'s Help Menu", icon_url=client.user.avatar_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Moderation Help | Requested by {ctx.author.name}")
    await ctx.send(embed=embed)


@help.command(aliases = ['misc'])
async def miscellaneous(ctx):
    #check all commands
    desc = "Available Commands: ```cinv, emojify, urban, passwordgenerator, makeuppercase, makelowercase, mimic, poll, clap, urlshorten, fakeconvo, membercount, truemembercount, echo, feedback, servercount, avatar, afk, afk clear, afk clearall, botinv, serverinfo, ascii, asciitext, ping```"
    embed = discord.Embed(title="❓ Miscellaneous Help", description=desc, color=discord.Color.green())
    embed.set_author(name=f"{client.user.name}'s Help Menu", icon_url=client.user.avatar_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Miscellaneous Help | Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@help.command(aliases = ['econ'])
async def economy(ctx):
    #check all commands
    desc = "Available Commands: ```balance, rob, withdraw, deposit, give, slots, highlow, leaderboard``` \n(More commands in progress)"
    embed = discord.Embed(title="❓ Economy Help", description=desc, color=discord.Color.green())
    embed.set_author(name=f"{client.user.name}'s Help Menu", icon_url=client.user.avatar_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Economy Help | Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@help.command(aliases = ['stats'])
async def serverstats(ctx):
    desc = "Available Commands: ```serverstats, servericon, levels, XP, messages, ghostpings, tcc, vcc, mcip``` \n(More commands in progress)"
    embed = discord.Embed(title="📈 Server Stats Help", description=desc, color=discord.Color.green())
    embed.set_author(name=f"{client.user.name}'s Help Menu", icon_url=client.user.avatar_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Server Stats Help | Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@help.command()
async def list(ctx):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    embed = discord.Embed(color=discord.Color.blurple(), title="Setup")
    embed1 = discord.Embed(color=discord.Color.blurple(), title="Games")
    embed2 = discord.Embed(color=discord.Color.blurple(), title="Moderation")
    embed3 = discord.Embed(color=discord.Color.blurple(), title="Miscellaneous")
    embed4 = discord.Embed(color=discord.Color.blurple(), title="Economy")
    pages = [embed, embed1, embed2, embed3, embed4]
    embed.set_thumbnail(url=client.user.avatar_url)
    embed1.set_thumbnail(url=client.user.avatar_url)
    embed2.set_thumbnail(url=client.user.avatar_url)
    embed3.set_thumbnail(url=client.user.avatar_url)
    embed4.set_thumbnail(url=client.user.avatar_url)
    embed.set_author(name="InfiniBot Commands List", icon_url=client.user.avatar_url)
    embed1.set_author(name="InfiniBot Commands List", icon_url=client.user.avatar_url)
    embed2.set_author(name="InfiniBot Commands List", icon_url=client.user.avatar_url)
    embed3.set_author(name="InfiniBot Commands List", icon_url=client.user.avatar_url)
    embed4.set_author(name="InfiniBot Commands List", icon_url=client.user.avatar_url)
    embed.add_field(name=f"{prefix}setup",
                    value=f"Use this command to get a more detailed help menu to setup InfiniBot for {ctx.guild.name}!")
    embed1.add_field(name=f'{prefix}play <game>',
                     value="Play a game! Current supported game modes are `madlibs` and `numberguess`. More coming soon!!",
                     inline=False)
    embed1.add_field(name=f'{prefix}talk', value="Talk with InfiniBot using AI!!", inline=False)
    embed1.add_field(name=f'{prefix}meme <optional sub>',
                     value="Returns a meme from the specified subreddit. Defaults to r/memes.", inline=False)
    embed1.add_field(name=f'{prefix}joke',
                     value="Returns a joke from r/jokes.", inline=False)
    embed1.add_field(name=f'{prefix}fight <user>', value="Fight a user in your server! See who prevails.", inline=False)
    embed1.add_field(name=f'{prefix}reverse <text>', value="Reverse inputted text!!", inline=False)
    embed1.add_field(name=f'{prefix}typing',
                     value="Test your typing speed with two different modes! Returns accuracy and WPM.", inline=False)
    embed1.add_field(name=f'{prefix}topwpm <optionalUser>',
                     value="Returns the top 5 WPM scores for a user.", inline=False)
    embed1.add_field(name=f'{prefix}servertopwpm',
                     value="Returns the top WPM scores achieved with 100% accuracy in the current server.",
                     inline=False)
    embed1.add_field(name=f'{prefix}servertopstats',
                     value="Returns the server's highest WPM typer, highest accuracy member.", inline=False)
    embed1.add_field(name=f'{prefix}flip', value="Flip a coin!", inline=False)
    embed1.add_field(name=f'{prefix}rps <optional user ID or @mention>',
                     value="Play a rock-paper-scissors match against a friend!", inline=False)
    embed2.add_field(name=f"{prefix}nick <@mention> <newnick>", value="Change the nickname of a member.", inline=False)
    embed2.add_field(name=f"{prefix}clear <amount>", value="Clears <amount> messages off the chat. By default clears 5.",
                     inline=False)
    embed2.add_field(name=f"{prefix}ban <@mention> <reason>", value="Bans a user and has reason.", inline=False)
    embed2.add_field(name=f"{prefix}kick <@mention> <reason>", value="Kicks a user and reason.", inline=False)
    embed2.add_field(name=f"{prefix}unban <user ID  or @mention>", value="Unbans a user.", inline=False)
    embed2.add_field(name=f"{prefix}softban <user ID or @mention>", value="Bans a user then unbans to delete messages.",
                     inline=False)
    embed2.add_field(name=f"{prefix}tempmute <@mention> <duration> <unit> <reason>", value="Mutes a user for a specified time.",
                     inline=False)
    embed2.add_field(name=f"{prefix}mute <@mention> <reason>", value="Mutes user indefinetely with reason.", inline=False)
    embed2.add_field(name=f"{prefix}lockdown", value="Disables `Send Message` permission for everyone in the channel.",
                     inline=False)
    embed2.add_field(name=f"{prefix}unlock",
                     value=f"To be used after `{prefix}lockdown`, gives everyone back their `Send Messages` permissions.",
                     inline=False)
    embed2.add_field(name=f"{prefix}ot or {prefix}openticket",
                     value="Opens a support ticket between admins and the creator of ticket. Use `ct` or `closeticket` inside of it to close.",
                     inline=False)
    embed2.add_field(name=f'{prefix}deleterole <@role>',
                     value="Deletes the mentioned role.", inline=False)
    embed3.add_field(name=f"{prefix}cinv <server name>",
                     value=f"Generates an invite to the server. If you would like your server to have a custom invite, use {prefix}feedback and provide a **PERMANENT** invite link.",
                     inline=False)
    embed3.add_field(name=f"{prefix}membercount", value="Counts total members in the server.", inline=False)
    embed3.add_field(name=f"{prefix}msgcount", value="Counts messages sent in a certain channel.", inline=False)
    embed3.add_field(name=f"{prefix}echo <channel> <content>", value="Echos your message in a specified channel.", inline=False)
    embed3.add_field(name=f"{prefix}feedback", value="Send your feedback to the developers!", inline=False)
    embed3.add_field(name=f"{prefix}servercount", value="I return how many servers I am in!", inline=False)
    embed3.add_field(name=f"{prefix}avatar <Optional @mention>", value="Return the avatar of the mentioned user!", inline=False)
    embed3.add_field(name=f"{prefix}afk <optionalstatus> ",
                     value="Set an afk status that members will see when they mention you! Removed when you send a message.",
                     inline=False)
    embed3.add_field(name=f"{prefix}afk clear <userID> ",
                     value="Clears an afk status for specified user.",
                     inline=False)
    embed3.add_field(name=f"{prefix}afk clearall",
                     value="Clears the afk statuses for all members in a server.",
                     inline=False)
    embed3.add_field(name=f"{prefix}botinv", value="Get the bot\'s invite link.", inline=False)
    embed3.add_field(name=f"{prefix}serverinfo", value="Get the presets for the server.", inline=False)
    embed3.add_field(name=f"{prefix}ascii <text>", value="Get the ASCII code for the inputted text.", inline=False)
    embed3.add_field(name=f"{prefix}ping", value="Get your ping in milliseconds!", inline=False)
    embed4.add_field(name=f"{prefix}bal <optional @mention or User ID>", value="Check your balance!", inline=False)
    embed4.add_field(name=f"{prefix}rob <@mention or User ID> ", value="Rob a user", inline=False)
    embed4.add_field(name=f"{prefix}with <amount>", value="Withdraw coins from your bank!", inline=False)
    embed4.add_field(name=f"{prefix}dep <amount> ", value="Deposit coins into the bank.", inline=False)
    embed4.add_field(name=f"{prefix}send <@mention or ID> <amount> or {prefix}give <@mention or ID> <amount>",
                     value="Give a user specified amount of coins!", inline=False)
    embed4.add_field(name=f"{prefix}slots <amount> ",
                     value="Try your luck with slots! Attempt to get 100x or even 1000x your gamble or lose it all.",
                     inline=False)
    embed4.add_field(name=f"{prefix}highlow", value="Attempt to guess a number for coins. No loss even if you get it wrong.",
                     inline=False)
    embed.set_footer(text="InfiniBot • Help Menu | Requested by: " + ctx.author.name + " | Page 1/" + str(len(pages)))
    embed1.set_footer(text="InfiniBot • Help Menu | Requested by: " + ctx.author.name + " | Page 2/" + str(len(pages)))
    embed2.set_footer(text="InfiniBot • Help Menu | Requested by: " + ctx.author.name + " | Page 3/" + str(len(pages)))
    embed3.set_footer(text="InfiniBot • Help Menu | Requested by: " + ctx.author.name + " | Page 4/" + str(len(pages)))
    embed4.set_footer(text="InfiniBot • Help Menu | Requested by: " + ctx.author.name + " | Page 5/" + str(len(pages)))
    try:
        message = await ctx.send(embed=embed)
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in ['⬅️', '➡️']
    except:
        await ctx.send("Please give me the `Embed Links` and `Attach Files` permissions for this channel.")
        return
    try:
        i = 0
        reaction, user = await client.wait_for('reaction_add', timeout=30, check=check)
        while True:
            if reaction.emoji == '➡️':
                if i < (len(pages) - 1):
                    i += 1
                    try:
                        await message.edit(embed=pages[i])
                        reaction, user = await client.wait_for('reaction_add', timeout=30, check=check)
                        await message.remove_reaction(reaction, user)
                    except discord.errors.Forbidden:
                        await ctx.send(
                            "Please give me the `Edit Messages` and `Add Reactions` permissions in this channel.")
                        return

            elif reaction.emoji == '⬅️':
                if i > -1:
                    i -= 1
                    try:
                        await message.edit(embed=pages[i])
                        reaction, user = await client.wait_for('reaction_add', timeout=30, check=check)
                        await message.remove_reaction(reaction, user)
                    except discord.errors.Forbidden:
                        await ctx.send(
                            "Please give me the `Edit Messages` and `Add Reactions` permissions in this channel.")
                        return
    except asyncio.TimeoutError:
        await ctx.reply("Timed out.", mention_author=False, delete_after=5)
        return
    except UnboundLocalError:
        return

@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await asyncio.sleep(2)
    await ctx.send("Cleared `" + str(amount) + "` messages.", delete_after=3)

@clear.error
async def clear_err(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send("You can't use that!")
    if isinstance(error, commands.CommandInvokeError):
        return await ctx.send("I do not have the `Manage Messages` permission. You can fix that by going into Server Settings and giving my role that permission.")

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member, *, reason="No reason given"):
    try:
        pfp = member.avatar_url
        author = member
        # message = f"You have been banned from {ctx.guild.name} for {reason}"
        ban = discord.Embed(description=f"Reason: ```{reason}```\nBy: {ctx.author.mention}",
                            color=discord.Color.dark_red())
        ban.set_author(name=str(author) + " has been banned.", icon_url=pfp)
        uban = discord.Embed(title=f"You were banned from **{ctx.guild.name}**",
                                description=f"Reason: ```{reason}```", color=discord.Color.blurple())
        uban.set_footer(text="If you believe this is in error, please contact an Admin.")
        try:
            if member.top_role >= ctx.author.top_role:
                if member.id == ctx.guild.owner_id:
                    pass
                else:
                    await ctx.send(f"You can only use this moderation on a member below you.")
                    return
        except AttributeError:
            return

        if not member.bot:
            await ctx.guild.ban(member, reason=reason)
            await ctx.channel.send(embed=ban)
            try:
                await member.send(embed=uban)
            except:
                await ctx.send(f'A reason could not be sent to `{member}` as they had their dms off.')
        else:
            await ctx.guild.ban(member, reason=reason)
            ban = discord.Embed(
                                description=f"Reason: ```{reason}```\nBy: {ctx.author.mention}")
            ban.set_author(name=f"{member.name} was banned", icon_url = member.avatar_url)
            await ctx.channel.send(embed=ban)
    except discord.errors.Forbidden:
        if member.id == ctx.guild.owner_id:
            await ctx.send(f"You cannot take any action on the server owner.")
            return
        if member.id == client.user.id:
            return await ctx.send("Bruh")
        await ctx.send(
            "I do not have the `Ban Members` permission. You can fix that by going into Server Settings and giving my role that permission.\nOr my role is not high enough.")


@ban.error
async def ban_err(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}ban [member] (reason)```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send(f"{ctx.author.mention}, you can't use that!")



@client.command()
@commands.has_permissions(ban_members = True)
async def tempban(ctx, member: discord.Member, duration=1, unit="h", *, reason="No reason given"):
    if unit == "s":
        dur = str(duration) + " seconds"
    elif unit == "m":
        dur = str(duration) + " minutes"
    elif unit == "h":
        dur = str(duration) + " hours"
    try:
        pfp = member.avatar_url
        author = member
        if unit not in ["s", "m", "h"]:
            await ctx.send("Please enter a correct unit. `(s)`, `(m)`, or `(h)`")
            return
        embed = discord.Embed(description=f"For reason: ```{reason}```", color=discord.Color.dark_red())
        embed.set_author(name=str(author) + f" has been banned for {dur}.", icon_url=pfp)
        uembed = discord.Embed(title=f"You have been banned in {ctx.guild.name}",
                               description=f"For reason: ```{reason}```", color=discord.Color.blurple())
        uembed.set_footer(text="If you believe this is in error, please contact an Admin.")
        if member.top_role >= ctx.author.top_role:
            await ctx.send(f"You can only use this moderation on a member below you.")
            return
        else:
            if not member.bot:
                await ctx.guild.ban(member, reason=reason)
                await ctx.send(embed=embed)
                try:
                    await member.send(embed=uembed)
                except:
                    await ctx.send(f'A reason could not be sent to `{member}` as they had their dms off.')
            else:
                await ctx.guild.ban(member, reason=reason)
                await ctx.send(embed=embed)
                try:
                    await member.send(embed=uembed)
                except:
                    await ctx.send(f'A reason could not be sent to {member} as they had their dms off.')
            if unit == "s":
                await asyncio.sleep(duration)
                await ctx.guild.unban(user=member)
            elif unit == "m":
                await asyncio.sleep(duration * 60)
                await ctx.guild.unban(user=member)
            elif unit == "h":
                await asyncio.sleep(duration * 60 * 60)
                await ctx.guild.unban(user=member)
    except AttributeError as e:
        print(e)
        await ctx.reply("An error has occured. The devs have been notified and will look into it.")
        return
    except discord.errors.Forbidden:
        if member.id == ctx.guild.owner_id:
            await ctx.send(f"You cannot take any action on the server owner.")
            return
        await ctx.send(
            "I do not have the `Ban Members` permission. You can fix that by going into Server Settings and giving my role that permission.\nOr my role is not high enough.")
        return

@tempban.error
async def tempban_err(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}tempban [member] (duration) (unit) (reason)```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send(f"{ctx.author.mention}, you can't use that!")
    if isinstance(error, commands.MemberNotFound):
        return await ctx.reply("Please mention someone to ban.")


@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason="No reason given"):
    try:
        pfp = member.avatar_url
        author = member
        desc = f'Reason: ```{reason}```'
        kick = discord.Embed(description=str(desc), color=discord.Color.blurple())
        kick.set_author(name=str(author) + " has been kicked.", icon_url=pfp)
        ukick = discord.Embed(title=f"You were kicked from **{ctx.guild.name}**",
                                description=f"Reason: ```{reason}```", color=discord.Color.blurple())
        ukick.set_footer(text="If you believe this is in error, please contact an Admin.")
        if member.top_role >= ctx.author.top_role:
            if ctx.author.id == ctx.guild.owner_id:
                pass
            else:
                await ctx.send(f"You can only use this moderation on a member below you.")
                return

        else:
            if not member.bot:
                await ctx.guild.kick(member, reason=reason.strip())
                await ctx.channel.send(embed=kick)
                try:
                    await member.send(embed=ukick)
                except discord.Forbidden:
                    await ctx.send(f'A reason could not be sent to `{member}` as they had their dms off.')
            else:
                await ctx.guild.kick(member, reason=reason.strip())
                await ctx.channel.send(embed=kick)
    except discord.errors.Forbidden:
        if member.id == ctx.guild.owner_id:
            await ctx.send(f"You cannot take any action on the server owner.")
            return
        if member.id == client.user.id:
            return await ctx.send(f"Unfortunately, {ctx.author.mention}, I cannot kick myself.")
        await ctx.send(
            "I do not have the `Kick Members` permission. You can fix that by going into Server Settings and giving my role that permission.\nOr my role is not high enough.")

@kick.error
async def kick_err(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}kick [member] (reason)```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send("You don't have permissions!")


@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, user: discord.User):
    try:
        pfp = user.avatar_url
        author = user
        embed = discord.Embed(color=discord.Color.red())
        embed.set_author(name=str(author) + " is now unbanned", icon_url=pfp)
        guild = ctx.guild
        await guild.unban(user=user)
        await ctx.send(embed=embed)
    except discord.errors.Forbidden:
        await ctx.send(
            "I do not have the `Ban Members` permission. You can fix that by going into Server Settings and giving my role that permission.\nOr my role is not high enough.")


@unban.error
async def unban_err(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}unban [user]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    if isinstance(error, commands.UserNotFound):
        nban = discord.Embed(color=discord.Color.red())
        nban.set_author(name=f"User is not banned or doesn\'t exist!")
        await ctx.send(embed=nban)



@client.command()
@commands.has_permissions(manage_roles = True)
async def tempmute(ctx, member: discord.Member, duration=1, unit="h", *, reason="No reason given"):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
        muterole = i['muterole']
    if unit.lower() == "s":
        dur = str(duration) + " seconds"
    elif unit.lower() == "m":
        dur = str(duration) + " minutes"
    elif unit.lower() == "h":
        dur = str(duration) + " hours"
    try:
        pfp = member.avatar_url
        author = member
        if unit.lower() not in ["s", "m", "h"]:
            await ctx.send("Please enter a correct unit. `(s)`, `(m)`, or `(h)`")
            return
        embed = discord.Embed(description=f"For reason: ```{reason}```", color=discord.Color.dark_red())
        embed.set_author(name=str(author) + f" has been muted for {dur}.", icon_url=pfp)
        uembed = discord.Embed(title=f"You have been muted in {ctx.guild.name}",
                               description=f"For reason: ```{reason}```", color=discord.Color.blurple())
        uembed.set_footer(text="If you believe this is in error, please contact an Admin.")
        if str(muterole) == '':
            await ctx.send(
                f"This server doesn\'t have a muterole set up! Use `{prefix}setup muterole <Optionalname>` to set it up.")
            return
        role = discord.utils.get(ctx.guild.roles, id=int(muterole))
        if member.top_role >= ctx.author.top_role:
            await ctx.send(f"You can only use this moderation on a member below you.")
            return
        elif role in member.roles:
            await ctx.send(f"`{member}` is already muted.")
            return
        elif reason != None:
            await member.add_roles(role)
            await ctx.send(embed=embed)
            try:
                await member.send(embed=uembed)
            except:
                await ctx.send(f'A reason could not be sent to {member} as they had their dms off.')
            if unit.lower() == "s":
                await asyncio.sleep(duration)
                await member.remove_roles(role)
            elif unit.lower() == "m":
                await asyncio.sleep(duration * 60)
                await member.remove_roles(role)
            elif unit.lower() == "h":
                await asyncio.sleep(duration * 60 * 60)
                await member.remove_roles(role)
        elif reason is None:
            await ctx.reply("Please provide a reason for tempmute.")
    except AttributeError as e:
        print(e)
        return await ctx.reply(f"This server does not have a mute role. Use `{prefix}muterole` to create the muterole.")
    except discord.errors.Forbidden:
        if member.id == ctx.guild.owner_id:
            await ctx.send(f"You cannot take any action on the server owner.")
            return

@tempmute.error
async def tempmute_err(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}tempmute [member] (duration) (unit) (reason)```\nUnits: `s`, `m`, `h`"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    if isinstance(error, commands.CommandInvokeError):
        return await ctx.send("I do not have the `Manage Roles` permission. You can fix that by going into Server Settings and giving my role that permission.\nOr my role is not high enough.")

    if isinstance(error, commands.MissingPermissions):
        return await ctx.send(f"{ctx.author.name}, you can't use that!")


@client.command()
@commands.has_permissions(manage_roles = True)
async def mute(ctx, member: discord.Member, *, reason="No reason given."):
    if member == client.user:
        await ctx.send("I can't mute myself.")
        return
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
        muterole = i['muterole']
    try:
        pfp = member.avatar_url
        author = member
        embed = discord.Embed(description=f"For reason: ```{reason}```", color=discord.Color.red())
        embed.set_author(name=str(author) + " has been muted indefintely.", icon_url=pfp)
        uembed = discord.Embed(title=f"You have been muted in {ctx.guild.name}",
                               description=f"For reason: ```{reason}```", color=discord.Color.blurple())
        uembed.set_footer(text="If you believe this is in error, please contact an Admin.")
        if str(muterole) == '':
            await ctx.send(
                f"This server doesn\'t have a muterole set up! Use `{prefix}setup muterole <Optionalname>` to set it up.")
            return
        role = discord.utils.get(ctx.guild.roles, id=int(muterole))
        if role in member.roles:
            await ctx.send(f"`{member}` is already muted.")
            return
        elif reason != None:
            if ctx.author.top_role >= member.top_role:
                await member.add_roles(role)
                await ctx.send(embed=embed)
                try:
                    await member.send(embed=uembed)
                except:
                    await ctx.send(f'A reason could not be sent to {member} as they had their dms off.')
            else:
                await ctx.send(f"You can only use this moderation on a member below yourself.")
                return
        else:
            await ctx.send(
                ctx.author.mention + ", you do not have the `Manage Roles` permission, so you cannot use this command. ")
    except AttributeError as e:
        return await ctx.send(f"This server does not have a mute role. Use `{prefix}muterole` to create the muterole.")
    except discord.errors.Forbidden:
        if member.id == ctx.guild.owner_id:
            await ctx.send(f"You cannot take any action on the server owner.")
            return
        await ctx.send(
            "I do not have the `Manage Roles` permission. You can fix that by going into Server Settings and giving my role that permission.\nOr my role is not high enough.")

@mute.error
async def mute_err(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}mute [member] (reason)```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    if isinstance(error, commands.MemberNotFound):
        return await ctx.reply(error, mention_author = False)
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send(f"{ctx.author.name}, you can't use that!")


@client.command()
@commands.has_permissions(manage_roles = True)
async def unmute(ctx, member: discord.Member):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        muterole = i['muterole']
    pfp = member.avatar_url
    author = member
    role = discord.utils.find(lambda r: r.id == int(muterole), ctx.message.guild.roles)
    await member.remove_roles(role)
    embed = discord.Embed(color=discord.Color.green())
    embed.set_author(name=str(author) + " has been unmuted.", icon_url=pfp)
    await ctx.send(embed=embed)


@unmute.error
async def unmute_err(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}unmute [member]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send("You can't use that!")



# @client.command()
# async def msgcount(ctx, channel: discord.TextChannel = None):
#     if channel is None:
#         channel = ctx.channel
#     await ctx.send("Please be patient, this process may take a while...")
#     count = 0
#     async for i in channel.history(limit=None):
#         count += 1
#     await ctx.reply(f"There were `{count}` messages in {channel.mention}")


@client.group()
async def cinv(ctx, server=None):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if server is None:
        invite = await ctx.channel.create_invite(max_age=604800)
        await ctx.send(f"Here is an invite to **{ctx.guild.name}**: \n{invite}")
        num = random.randint(1, 10)
        if num == 2:
            await ctx.send(
                f'{ctx.author.mention}, if you would like your server to have a custom invite intro, please use the {prefix}feedback command to request.')
            return
        return

@cinv.command()
async def gamers(ctx):
    message = 'Welcome to Gamers!\n\nWe are a Minecraft Multiverse Community with fun gameplay for everyone.  We have a Faction Minecraft Server and a Vanilla Economy Minecraft Server.\n\nOUR FACTION SERVER HAS:\n' \
                '-Killing players and raiding bases\n-Clans\n-Secret Bases\n-Griefing\n\n' \
                'OUR ECONOMY MINECRAFT SERVER HAS:\n\n' \
                '-Pure Survival\n-Fun for everyone\n-Economy\n-Shops\n\n' \
                'OUR CREATIVE SERVER HAS:\n\n' \
                '-General Building\n-Chill Hangout Area\n- A place to show off your builds\n\n' \
                'Discord Link: https://discord.gg/xFZdxfwpuT\n\n' \
                'Website Link: COMING SOON!!\n\n' \
                'Minecraft IP: 192.99.233.197:25580\n\n' \
                'JOIN NOW FOR ALL THE FUN!!'
    await ctx.send(message)


@client.command(aliases=['tusers', 'mc'])
async def membercount(ctx):
    await ctx.send(f'There are `{ctx.guild.member_count}` members in **{ctx.guild.name}**.')


@client.command()
@commands.has_permissions(manage_channels = True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    desc = str("<:locked:829732789917974588>") + ctx.channel.mention + "**is now in lockdown.**"
    embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp = datetime.datetime.utcnow())
    embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
    await ctx.send(embed=embed)

@lockdown.error
async def lockdown_err(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send(f"{ctx.author.mention}, you do not have the `Manage Channels` permission.")
    if isinstance(error, commands.CommandInvokeError):
        return await ctx.send("I don't have the Manage Channel permission for that channel.")


@client.command()
@commands.has_permissions(manage_channels = True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    desc = (str("<:unlocked:829732807601029150>") + ctx.channel.mention + " ***has been unlocked.***")
    embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp = datetime.datetime.utcnow())
    embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
    await ctx.send(embed=embed)

@unlock.error
async def unlock_err(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send("You can't use that!")
    if isinstance(error, commands.CommandInvokeError):
        return await ctx.send("I don't have the Manage Channel permission for that channel.")

# @client.command()
# async def botping(ctx):
#     if ctx.author.id == 759245009693704213:
#         ping = round(client.latency * 1000)
#         embed = discord.Embed(title="Dinesh Bot Latency:", description=str(ping) + "ms", color=discord.Color.blurple())
#         await ctx.send(embed=embed)
#     else:
#         await ctx.reply(f'{ctx.author.mention}, this command is limited to the developers of Dinesh Bot.',
#                         mention_author=False)


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


@client.command(aliases=['sc', 'botguildcount'])
async def servercount(ctx):
    await ctx.send("I'm in `" + str(len(client.guilds)) + "` servers!")


# @client.command()
# async def join(ctx):
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#     try:
#         connected = ctx.author.voice
#         channel = ctx.author.voice.channel
#     except AttributeError:
#         await ctx.send(f"{ctx.author.mention}, you are not connected to a voice channel.")
#         return
#     if connected:
#         try:
#             await connected.channel.connect()
#             await ctx.send(f"Connected to `{channel.name}`.")
#             return channel.name
#         except discord.errors.Forbidden:
#             await ctx.send(f"I don't have permission to connect to {channel.name}!")
#         except ClientException:
#             if voice.channel == channel:
#                 pass
#             else:
#                 return await ctx.send("I am already connected to a vc!")
#     else:
#         await ctx.send("You must be connected to a voice channel!")
#         return False

# @client.command(aliases = ['dc', 'disconnect'])
# @commands.has_permissions(manage_guild = True)
# async def leave(ctx):
#     voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
#     if voice is None:
#         return await ctx.send("I am not connected to a Voice Channel!")
#     if voice.is_connected():
#         await voice.disconnect()
#         await ctx.message.add_reaction('👋🏽')

# @client.command()
# async def pause(ctx):
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#     if voice.is_playing():
#         voice.pause()
#         await ctx.message.add_reaction('⏸️')
#     else:
#         await ctx.send("Currently no audio is playing.")

# @client.command(aliases = ['unpause'])
# async def resume(ctx):
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#     if voice.is_paused():
#         voice.resume()
#         await ctx.message.add_reaction('▶️')
#     else:
#         await ctx.send("The audio is not paused.")

# @client.command()
# async def stop(ctx):
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#     voice.stop()

# @client.command()
# async def ytdownload(ctx, *, song: str):
#     if ('www.' or '.com' or '.be') in song.lower():
#         url = song
#     else:
#         print(song)
#         x = song.split()
#         arr = []
#         for i in x:
#             arr.append(i.strip())
#         z = "+".join(arr)
#         print(arr)
#         print(z)     
#         html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={z}")
#         vidid = re.findall(r"watch\?v=(\S{11})", html.read().decode())
#         url = (f"https://www.youtube.com/watch?v={vidid[0]}")
#     await ctx.send(f"Searching for `{song}`...")
        
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#     } 
#     print('hi')
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         info_dict = ydl.extract_info(url, download=False)
#         ydl.download([url])
#         vidtitle = (info_dict['title'])
#         print(info_dict)
#     for file in os.listdir("./"):
#         if file.endswith('.mp3'):
#             os.rename(file, 'song.mp3')
#     await ctx.send(file=discord.File('song.mp3'))


# @ytdownload.error
# async def play_error(ctx, error):
#     db = sqlite3.connect('main.sqlite')
#     cursor = db.cursor()
#     cursor.execute(f"SELECT prefix from main WHERE guild_id = {ctx.guild.id}")
#     result = cursor.fetchone()
#     if str(result[0]) == "None":
#         result = ("%", "Hi")
#     if isinstance(error, commands.MissingRequiredArgument):
#         desc = f"```{result[0]}ytdownload [song]```"
#         embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
#         embed.set_footer(text="Parameters in [] are required and () are optional")
#         return await ctx.send(embed=embed)





@client.command()
async def echo(ctx, chanel: discord.TextChannel, *, message="Echo"):
    channel = chanel.id
    schannel = client.get_channel(channel)
    await schannel.send(content = message, allowed_mentions = AllowedMentions.none())
    await ctx.message.add_reaction(str('<:checked:829061772446531624>'))
    await asyncio.sleep(2)
    await ctx.message.delete()

    
@echo.error
async def ech_err(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}echo [channel] (message)```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    if isinstance(error, BotMissingPermissions):
        return await ctx.send("I do not have permission this channel to `Read Messages` and `Send Messages`.")
    if isinstance(error, commands.CommandInvokeError):
        return await ctx.send("I cannot access this channel.")


@client.command()
async def play(ctx, game=None):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if game is None:
        desc = f"```{prefix}play [game]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    elif game.lower() == 'numberguess':
        await ctx.send(ctx.author.mention + " is gonna be guessing today. Are you sure? Reply with `y` or `n`")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            message = await client.wait_for('message', check=check, timeout=30)
            if message.content.lower() == "y":
                i = random.randint(0, 100)
                print(i)
                lives = 0
                limit = ""
                await ctx.send(
                    "Ok " + ctx.author.mention + ", we are gonna be playing a guessing game! Try to get the integer between 0 and 100 to win. Type `cancel` to end your game.")
                await asyncio.sleep(1)
                await ctx.send(ctx.author.mention + ", would you like `easy`, `medium`, or `hard` level?")
                message = await client.wait_for('message', check=check, timeout=30)
                await message.add_reaction(str('<:checked:829061772446531624>'))
                if message.content.lower() == "easy":
                    limit = 20
                    await ctx.send(" Great, you get " + str(limit) + " tries.")
                    await asyncio.sleep(1)
                    await ctx.send("Make ur first guess now: ")
                elif message.content.lower() == "medium":
                    limit = 10
                    await ctx.send(" Great, you get " + str(limit) + " tries.")
                    await asyncio.sleep(1)
                    await ctx.send("Make ur first guess now: ")
                elif message.content.lower() == "hard":
                    limit = 5
                    await ctx.send(" Great, you get " + str(limit) + " tries.")
                    await asyncio.sleep(1)
                    await ctx.send("Make ur first guess now: ")
                elif message.content.lower() not in ["easy", "medium", "hard"]:
                    await ctx.send(
                        ctx.author.mention + ", `" + message.content + "` was not either `easy`, `medium`, or `hard`. Please use the command again to play again.")
                    pass
                while lives < limit:
                    try:
                        message = await client.wait_for('message', check=check, timeout=30)
                        if int(message.content) == i:
                            await ctx.send(
                                "<:checked:829061772446531624> Good job " + ctx.author.mention + "! You've gotten the number!")
                            break
                        else:
                            lives += 1
                            if int(message.content) > i:
                                if lives == (limit - 1):
                                    await ctx.send(
                                        ctx.author.mention + ", `" + message.content + "` is above the number. You have " + str(
                                            limit - lives) + " life left.")
                                else:
                                    await ctx.send(
                                        ctx.author.mention + ", `" + message.content + "` is above the number. You have " + str(
                                            limit - lives) + " lives left.")
                            else:
                                if lives == (limit - 1):
                                    await ctx.send(
                                        ctx.author.mention + ", `" + message.content + "` is below the number. You have " + str(
                                            limit - lives) + " life left.")
                                else:
                                    await ctx.send(
                                        ctx.author.mention + ", `" + message.content + "` is below the number. You have " + str(
                                            limit - lives) + " lives left.")
                    except ValueError:
                        if message.content.lower() == "cancel":
                            await message.add_reaction(str('<:checked:829061772446531624>'))
                            await ctx.send(ctx.author.mention + ", you have ended the game.")
                            break
                        else:
                            lives += 1
                            await ctx.send(
                                ctx.author.mention + ", `" + message.content + "` is not an integer. You have lost 1 life. You have " + str(
                                    limit - lives) + " lives left.")
                if lives >= limit:
                    await ctx.send("You have run out of guesses. Tsk tsk. The actual number was `" + str(i) + "`")


            elif message.content.lower() == "n":
                await ctx.send("Ok " + ctx.author.mention + ", why did u use the command if u weren't gonna play lmao?")
            elif message.content.lower() not in ["y", "n"]:
                await ctx.send(
                    ctx.author.mention + ", please use ur brain and read the question again. It says use `y` or `n`, not " + "`" + message.content + "`")
        except asyncio.TimeoutError:
            await ctx.send(
                ctx.author.mention + " ite imma ignore you now lmao. If you want to start another game use the command again.")

    elif game.lower() == 'madlibs':
        await ctx.send(
            ctx.author.mention + " wants to play madlibs!! Type `y` to confirm or `n` to cancel. If you take too long I will ignore you.")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            message = await client.wait_for('message', check=check, timeout=30)
            if message.content.lower() == 'y':
                choices = []
                for file in os.listdir('./Discord Bot/MadLibs'):
                    if file.endswith(".txt"):
                        choices.append(file)
                    if len(choices) == 0:
                        # No madlibs...
                        msg = 'I\'m not configured for MadLibs yet...'
                        await ctx.send(msg)
                        return
                await ctx.send(
                    ctx.author.mention + " Fill out the madlib and laugh at the end :D (or cringe it's up to you tho). If you take longer than 30 seconds to respond or type `cancel`, your game will end.")
                try:
                    randnum = random.randint(0, (len(choices) - 1))
                    randLib = choices[randnum]
                    with open("./Discord Bot/MadLibs/{}".format(randLib),
                              'r') as myfile:
                        data = myfile.read()
                        d2 = data.split()
                        lent = []
                        print(d2)
                        for pos in d2:
                            if pos.isupper():
                                if pos == "I":
                                    continue
                                else:
                                    lent.append(pos)
                        await asyncio.sleep(1)
                        await ctx.send("This MadLib has `" + str(len(lent)) + "` inputs.")
                        await asyncio.sleep(1)
                        for index, pos in enumerate(d2):
                            if "ADJ" in pos:
                                await ctx.send("Enter an adjective: ")
                                message = await client.wait_for('message', check=check, timeout=30)
                                if message.content.lower() == 'cancel':
                                    return await ctx.send(f"Come back soon!")
                                d2[index] = message.content
                                await message.add_reaction(str('<:checked:829061772446531624>'))
                            elif "NOUN" in pos:
                                await ctx.send("Enter a noun: ")
                                message = await client.wait_for('message', check=check, timeout=30)
                                if message.content.lower() == 'cancel':
                                    return await ctx.send(f"Come back soon!")
                                d2[index] = message.content
                                await message.add_reaction(str('<:checked:829061772446531624>'))
                            elif "ADVERB" in pos:
                                await ctx.send("Enter an adverb: ")
                                message = await client.wait_for('message', check=check, timeout=30)
                                if message.content.lower() == 'cancel':
                                    return await ctx.send(f"Come back soon!")
                                d2[index] = message.content
                                await message.add_reaction(str('<:checked:829061772446531624>'))
                            elif "V3RB" in pos:
                                await ctx.send("Enter a verb: ")
                                message = await client.wait_for('message', check=check, timeout=30)
                                if message.content.lower() == 'cancel':
                                    return await ctx.send(f"Come back soon!")
                                d2[index] = message.content
                                await message.add_reaction(str('<:checked:829061772446531624>'))
                            elif "VERBPT" in pos:
                                await ctx.send("Enter a past-tense verb: ")
                                message = await client.wait_for('message', check=check, timeout=30)
                                if message.content.lower() == 'cancel':
                                    return await ctx.send(f"Come back soon!")
                                d2[index] = message.content
                                await message.add_reaction(str('<:checked:829061772446531624>'))
                            elif "PN" in pos:
                                await ctx.send("Enter a plural noun: ")
                                message = await client.wait_for('message', check=check, timeout=30)
                                if message.content.lower() == 'cancel':
                                    return await ctx.send(f"Come back soon!")
                                d2[index] = message.content
                                await message.add_reaction(str('<:checked:829061772446531624>'))
                            elif "NUM" in pos:
                                await ctx.send("Enter a number: ")
                                message = await client.wait_for('message', check=check, timeout=30)
                                if message.content.lower() == 'cancel':
                                    return await ctx.send(f"Come back soon!")
                                d2[index] = message.content
                                await message.add_reaction(str('<:checked:829061772446531624>'))
                            elif "AEST" in pos:
                                await ctx.send("Enter an adjective that ends in -est: ")
                                message = await client.wait_for('message', check=check, timeout=30)
                                if message.content.lower() == 'cancel':
                                    return await ctx.send(f"Come back soon!")
                                d2[index] = message.content
                                await message.add_reaction(str('<:checked:829061772446531624>'))
                            elif "VING" in pos:
                                await ctx.send("Enter a verb that ends in -ing: ")
                                message = await client.wait_for('message', check=check, timeout=30)
                                if message.content.lower() == 'cancel':
                                    return await ctx.send(f"Come back soon!")
                                d2[index] = message.content
                                await message.add_reaction(str('<:checked:829061772446531624>'))
                            elif "NAME" in pos:
                                await ctx.send("Enter a name: ")
                                message = await client.wait_for('message', check=check, timeout=30)
                                if message.content.lower() == 'cancel':
                                    return await ctx.send(f"Come back soon!")
                                d2[index] = message.content
                                await message.add_reaction(str('<:checked:829061772446531624>'))
                            elif "EXC" in pos:
                                await ctx.send("Enter an exclamation: ")
                                message = await client.wait_for('message', check=check, timeout=30)
                                if message.content.lower() == 'cancel':
                                    return await ctx.send(f"Come back soon!")
                                d2[index] = message.content
                                await message.add_reaction(str('<:checked:829061772446531624>'))
                            elif "SND" in pos:
                                await ctx.send("Enter a sound: ")
                                message = await client.wait_for('message', check=check, timeout=30)
                                if message.content.lower() == 'cancel':
                                    return await ctx.send(f"Come back soon!")
                                d2[index] = message.content
                                await message.add_reaction(str('<:checked:829061772446531624>'))
                            else:
                                continue

                        fin = (' '.join(d2))
                        print(fin)
                        await ctx.send(fin)
                        await asyncio.sleep(1)
                        await ctx.send(
                            f'{ctx.author.mention}, that was fun! If you want to play again, just use the command again!!!')

                    if message.content.lower() == "cancel":
                        await ctx.send(ctx.author.mention + " ok see u later")
                except asyncio.TimeoutError as e:
                    print(e)
                    await ctx.send(
                        ctx.author.mention + " ite imma ignore you now lmao. If you want to start another game use the command again.")


            elif message.content.lower() not in ['y', 'n']:
                await ctx.send(
                    ctx.author.mention + " can u read lmao it says `say 'y' or 'n'` not" + " `" + message.content + "`")
                return
            elif message.content.lower() == "n":
                await ctx.send("Ok " + ctx.author.mention + ", why did u use the command if u weren't gonna play lmao?")
                return


        except asyncio.TimeoutError as e:
            print(e)
            await ctx.send(
                ctx.author.mention + " ite imma ignore you now lmao. If you want to start another game use the command again.")

    elif game.lower() == "cah":
        await ctx.send(
            f'{ctx.author.mention}, by playing this game you acknowledge that **there may be NSFW content** (no images). Do you wish to proceed? Respond with `y` or `n`.')

        try:
            authID = ctx.author.id
            authMen = ctx.author.mention

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            message = await client.wait_for('message', check=check, timeout=30)
            if message.content.lower() == "y":
                choices = []
                channel = message.channel.id
                schannel: discord.TextChannel
                schannel = client.get_channel(channel)
                for file in os.listdir('./Discord Bot/CAH cards/White Cards'):
                    if file.endswith(".txt"):
                        choices.append(file)
                randnum = random.randint(0, (len(choices) - 1))
                randLib = choices[randnum]
                with open("./Discord Bot/CAH cards/White Cards/{}".format(randLib),
                          'r') as myfile:
                    data = myfile.read()
                    d2 = data.split(". ")
                    startembed = discord.Embed(title=f"{ctx.author} is starting a Cards Against Humanity game!",
                                               description=f"Type `join` to join in the next 120 seconds.\n\n {ctx.author.mention}, type `start` to begin once everyone has joined.",
                                               color=discord.Color.blue())
                    invokeembed = discord.Embed(description=f'{ctx.author.mention} was added to the game!',
                                                color=discord.Color.blue())
                    await ctx.send(embed=startembed)
                    await ctx.send(embed=invokeembed)
                    username = []
                    username.append(authMen)
                    t_end = time.time() + 120
                    while time.time() < t_end:
                        playerlist = []
                        playerlist.append(authID)
                        print(playerlist)
                        playerlist.append(message.author.id)
                        message = await client.wait_for('message', timeout=120)
                        playerembed = discord.Embed(description=f"{message.author.mention} was added to the game!",
                                                    color=discord.Color.blue())
                        # print(playerlist)
                        if message.content.lower() not in ["start", "join"]:
                            continue
                        if message.content.lower() == "join":
                            if message.author.id == authID:
                                await ctx.send(f'{message.author.mention}, you are already joined.', delete_after=2)
                                await asyncio.sleep(2)
                                await message.delete()
                            else:
                                if message.author.id not in playerlist:
                                    usernames = message.author.mention
                                    # print(usernames)
                                    username.append(usernames)

                                    await message.delete()
                                    await ctx.send(embed=playerembed)
                                    try:
                                        uembed = discord.Embed(
                                            description=f"You have joined a Cards Against Humanity game in {schannel.mention} in **{ctx.guild.name}**.",
                                            color=discord.Color.blue())
                                        await message.author.send(embed=uembed)
                                    except:
                                        username.remove(usernames)
                                        await ctx.send(
                                            f"{message.author.mention}, please turn on your DMs, or this game will not work properly.")
                                        await ctx.send(
                                            f'{authMen}, use the command again when {message.author.mention} has turned on their DMs.')
                                        return
                                else:
                                    await ctx.send(f"{message.author.mention}, you are already joined.", delete_after=2)
                                    await asyncio.sleep(2)
                                    await message.delete()

                        if message.content.lower() == "start":
                            if message.author.id == authID:
                                if len(username) < 2:
                                    doneembed = discord.Embed(title=f"**Time\'s up!**",
                                                              description="Not enough people joined the game!",
                                                              color=discord.Color.blue())
                                    gameoverem = discord.Embed(title=f'Game over!',
                                                               description="Use the command to play again.",
                                                               color=discord.Color.green())
                                    await ctx.send(embed=doneembed)
                                    await ctx.send(embed=gameoverem)
                                    return
                                else:
                                    users = ", ".join(username)
                                    print(users)
                                    # await ctx.send("Hello")
                                    break
                                    # ONTO game code itself...
                    bgnembed = discord.Embed(title="**Time\'s up!**", description=str(users) + ' joined the game.',
                                             color=discord.Color.blue())
                    await ctx.send(embed=bgnembed)
                    await ctx.send("The next round will begin in 5 seconds.")
                    flename = str(authID) + str(random.randint(0, 199394))
                    print(flename)
                    # with open(f"{flename}.txt", "w") as fle:
                    #    for user in username:
                    #      fle.write(f'{user}: 0\n')
                    currentczar = discord.Embed(description="The current czar is " + str(username[
                                                                                             1]) + "! Wait until the other players have submitted their cards, then choose the best one.",
                                                color=discord.Color.blue())
                    tz = random.randint(0, (len(username) - 1))
                    cardtzar = str(username[tz])
                    await ctx.send(embed=currentczar)
                    bchoices = []
                    for file1 in os.listdir('./Discord Bot/CAH cards/Black Cards'):
                        if file1.endswith(".png"):
                            bchoices.append(file1)
                        if len(bchoices) == 0:
                            # No black cards...
                            msg = 'I\'m not configured for Cards Against Humanity yet...'
                            await ctx.send(msg)
                            return
                    # while loop
                    randnum1 = random.randint(0, (len(bchoices) - 1))
                    randLib1 = bchoices[randnum1]
                    # with open("C:/Users/Rahul/Documents/Personal/Discord Bot/CAH Cards/Black Cards/{}".format(randLib1),
                    #         'r') as myfile1:
                    #  gameembed = discord.Embed(title="**This round\'s black card**")
                    #  gameembed.set_image(url="attachment://(randLib1)")
                    #  await ctx.send(embed=gameembed)
                    gameembed = discord.Embed(title=f"*This round\'s black card*", color=discord.Color.blue())
                    gamefile = discord.File(
                        f"./Discord Bot/CAH Cards/Black Cards/{randLib1}",
                        filename="image.png")
                    gameembed.set_image(url="attachment://image.png")
                    gameembed.set_footer(text="InfiniBot | Game Mode")
                    await ctx.send(file=gamefile, embed=gameembed)
                    # while loop here as well (no user has 5 correct)
                    newL = []
                    for k in username:
                        newL.append(k + "<:cancel:830613286642909194> Not submitted.")
                    lDesc = " \n".join(newL)
                    substat = discord.Embed(title="*Submission Status*", description=lDesc, color=discord.Color.red())
                    await ctx.send(embed=substat)
                    with open('./Discord Bot/CAH Cards/White Cards/whitecards.txt',
                              'r') as myfile2:
                        data = myfile2.read()
                        print(data)
                        d2 = data.split(". ")
                        print(d2)
                        wordlist = []
                        uslist = []
                    # while loop here for while not everyone has submitted.
                    for index, k in enumerate(playerlist):
                        user = client.get_user(int(k))
                        if user == client.user:
                            await ctx.send("Something went wrong, please try again later.")
                            return
                        print(user)
                        await user.send("View your hand and select a card.")
                        listsk = []
                        count = 0
                        for i in range(0, 10):
                            count += 1
                            listsk.append("**" + str(count) + "**: " + str(random.choice(d2)) + ".")
                        listskj = " \n".join(listsk)
                        wordlist.append(listsk)
                        couned = str(user)
                        uslist.append(couned)
                        # print(uslist)
                        # usword = " ".join(uslist)

                        # usercount = []
                        # usercount.append(uslist)
                        gembed = discord.Embed(title="**Cards Against Humanity - Your Current Hand**", description=(
                                                                                                                       listskj) + f"\n\nEnter the number next to the card in the channel {schannel.mention} to select it. You need to select 1 card.",
                                               color=discord.Color.dark_blue())
                        await user.send(embed=gembed)
                    # FIGURE OUT HOW TO GET The initiall array index from the user that inputted.

                    # get the (index-1) of given value for inputted value, https://www.geeksforgeeks.org/python-get-the-string-after-occurrence-of-given-substring/ use partition
                    print(wordlist)
                    print(uslist)
                    # while not everyone submit and not timeout:
                    message = await client.wait_for('message')
                    mauth = str(message.author)
                    print(mauth)
                    answers = []
                    try:
                        if any(mauth in s for s in uslist):
                            await message.delete()
                            print("Yes")
                            ans = (uslist.index(mauth))
                            ans2 = (wordlist[ans][int(message.content) - 1])
                            res = ans2.partition(": ")[2]
                            answers.append(res)
                            answord = " \n".join(answers)
                            msg = ""
                            for i, c in enumerate(answers):
                                j = answers.index(c)
                                msg += str(i + 1) + ": " + str(answers[j]) + "\n"
                            sembed = discord.Embed(title="Choose the best card, Card Czar", description=msg)
                            await ctx.send(embed=sembed)
                            # print(res)

                        # return
                        choice = int(message.content)
                        await ctx.send("youdwaefge")
                        # print(uslist[0][4])
                    except ValueError as e:
                        print(e)
                        await message.reply(f"Please input a number.")
                        # continue
                        pass
                # for ki in uslist:
                # print(int(ki[-1]))
                # now, iterate throuh the contents of the uslist and get the Last character of each string (in da iteration) by using the [-1] index.
                # then, take the integer value of that number and take wordslist[(integer value of last character)][INPUT(which is the message command right after.)]
                # save that as input and await everyone to submit :)

                # print(str(random.choice(d2)) + ".\n")
                # await user.send(listskj)

                # with open(str(flename) + ".txt") as f:
                #     contents = f.readline()
                #      while contents:
                #           contents = f.readline()
                #           substat.add_field(name = contents, value=contents)
                #       await ctx.send(embed=substat)

            elif message.content.lower() == "n":
                await ctx.send(f'{ctx.author.mention}, why did you use the command if you weren\'t gonna play?')
                return
        except asyncio.TimeoutError:
            await ctx.reply("This game has timed out.")


@client.command()
async def talk(ctx):
    if ctx.author.bot:
        return
    try:
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send(
            f'{ctx.author.mention}, before I start I\'d like to go over a few things. When you wish to end the chat session, type `bye`. \n'
            f'I only wait for 30 seconds between messages. If you don\'t respond, I will end the session on my own.\n'
            f'Finally, press `y` to confirm you want to talk. Anything else, and the chat session ends.')
        message = await client.wait_for('message', check=check, timeout=30)
        if message.content.lower() == 'y':
            await ctx.send(f"Great {ctx.author.mention}, let's get to it. What's on your mind?")
            while message.content.lower() != "bye":
                message = await client.wait_for('message', check=check, timeout=30)
                response = await rs.get_ai_response(message.content)
                await message.reply(response)
                if message.content.lower() == 'bye':
                    await ctx.send(f'{ctx.author.mention}, we will meet again soon')
                    return

        else:
            await ctx.send(f'{ctx.author.mention}, we will meet again soon')
            return
    except asyncio.TimeoutError:
        await ctx.reply("Your chat session has timed out. Use the command again to chat.")
        return


@client.command()
async def botinv(ctx):
    embed = discord.Embed(title="InfiniBot Invite Link",
                          description=r'https://discord.com/api/oauth2/authorize?client_id=829464107710677022&permissions=4294307063&scope=bot%20applications.commands',
                          color=discord.Color.blurple())
    embed.set_footer(text=f"InfiniBot Help | Requested by {ctx.author.name}")
    await ctx.reply(embed=embed)


@client.command()
async def meme(ctx, *, sub="memes"):
    all_subs = []
    try:
        subreddit = reddit.subreddit("memes")
        top = subreddit.hot(limit=30)
        for sub in top:
            all_subs.append(sub)

        random_sub = random.choice(all_subs)

        name = random_sub.title
        url = random_sub.url
        suburl = "https://www.reddit.com" + random_sub.permalink
        scr = random_sub.score
        com = random_sub.num_comments
        em = discord.Embed(title=name, url=suburl, color=discord.Color.green())
        em.set_image(url=url)
        em.set_footer(text="👍 " + str(scr) + " | 💬 " + str(com))

        await ctx.send(embed=em)
    except Exception as e:
        print(e)
        await ctx.reply(f'`{sub}` is not a valid subreddit.', mention_author=False)


@client.command()
# still in dev
async def joke(ctx):
    all_subs = []
    subreddit = reddit.subreddit('jokes')
    top = subreddit.hot(limit=30)
    for sub in top:
        all_subs.append(sub)

    random_sub = random.choice(all_subs)
    name = random_sub.title
    tex = random_sub.selftext
    url = random_sub.url
    suburl = "https://www.reddit.com" + random_sub.permalink
    scr = random_sub.score
    com = random_sub.num_comments
    em = discord.Embed(title=name, description=tex, url=suburl, color=discord.Color.green())
    em.set_footer(text="👍 " + str(scr) + " | 💬 " + str(com))
    await ctx.send(embed=em)


@client.command()
async def fight(ctx, member: discord.Member):
    if member == ctx.author:
        await ctx.send("You can\'t fight yourself lmao")
        return
    if member == client.user:
        await ctx.send("You cannot fight me because I am all-powerful.")
        return
    if member.bot:
        await ctx.send("You can\'t fight a bot lmao")
        return
    else:
        choices = []
        global memHP
        global userHP
        memHP = 100
        userHP = 100
        global upnow
        global upnext
        global memprot
        global userprot
        memprot = 1
        userprot = 1
        upnow = ctx.author
        upnext = member
        for file in os.listdir('./Discord Bot/Fighting'):
            if file.endswith(".txt"):
                choices.append(file)
            if len(choices) == 0:
                # Should never happen lol
                msg = 'I\'m not configured for fighting yet...'
                await ctx.send(msg)
                return
            randnum = random.randint(0, (len(choices) - 1))
            randLib = choices[randnum]
            with open("./Discord Bot/Fighting/{}".format(randLib),
                      'r') as myfile:
                data = myfile.read()
                d2 = data.split(" ")
                print(d2)
        try:
            await ctx.send(
                f'{ctx.author.mention}, what do you want to do? `punch`, `defend`, or `end`? \nType your choice out in the chat as it\'s displayed!')

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            players = []
            players.append(ctx.author.id)
            players.append(member.id)
            print(players)

            async def punch():
                global memHP
                global userHP
                global upnow
                global upnext
                global userprot
                global memberprot
                if memHP > 0 and userHP > 0:
                    randadj = random.randint(0, (len(d2) - 1))
                    dama = random.randint(1, 75)
                    adj = d2[randadj]
                    if upnow == ctx.author:
                        dama1 = round((dama * userprot), 2)
                        userHP -= int(dama1)
                        if userHP > 0:
                            await ctx.send(
                                f"**{upnow.name}** lands a " + adj + f" punch on **{upnext.name}** dealing **{dama}** damage!\n"
                                                                     f"**{upnext.name}** is left with {userHP} HP!")
                        else:
                            await ctx.send(
                                f"**{upnow.name}** lands a " + adj + f" punch on **{upnext.name}** dealing **{dama}** damage!\n"
                                                                     f"**{upnext.name}** is left with 0 HP!")
                        upnow = member
                        upnext = ctx.author
                        print(upnow, upnext)
                        return
                    else:
                        dama1 = round((dama * memprot), 2)
                        memHP -= int(dama1)
                        if memHP > 0:
                            await ctx.send(
                                f"**{upnow.name}** lands a " + adj + f" punch on **{upnext.name}** dealing **{dama}** damage!\n"
                                                                     f"**{upnext.name}** is left with {memHP} HP!")
                        else:
                            await ctx.send(
                                f"**{upnow.name}** lands a " + adj + f" punch on **{upnext.name}** dealing **{dama}** damage!\n"
                                                                     f"**{upnext.name}** is left with 0 HP!")
                        upnow = ctx.author
                        upnext = member
                        print(upnow, upnext)
                        return

            async def defend():
                global upnow
                global upnext
                global memprot
                global userprot
                if memHP > 0 and userHP > 0:
                    if upnow == ctx.author:
                        if float(memprot) < 0.75:
                            await ctx.send(f"{message.author.mention}, you have already reached max protection level!")
                            upnow = member
                            upnext = ctx.author
                            return
                        rate = random.randint(1, 9)
                        rate1 = rate / 10
                        memprot *= rate1
                        await ctx.send(
                            f"**{message.author.name}** has increased their protection level by {10 - rate}!")
                        upnow = member
                        upnext = ctx.author
                        print(upnow, upnext)
                        return
                    else:
                        if float(userprot) < 0.75:
                            await ctx.send(f"{message.author.mention}, you have already reached max protection level!")
                            upnow = ctx.author
                            upnext = member
                            return
                        rate = random.randint(1, 9)
                        rate1 = rate / 10
                        userprot *= rate1
                        await ctx.send(
                            f"**{message.author.name}** has increased their protection level by {10 - rate}!")
                        upnow = ctx.author
                        upnext = member
                        print(upnow, upnext)
                        return

            async def end():
                await ctx.send(f'**{message.author.name}** has ended the game, what a wimp')
                return

            async def errorc():
                await message.reply(f"{message.content} isn\'t a valid option lmao", mention_author=False)
                return

            message = await client.wait_for('message', check=check, timeout=30)
            try:
                while memHP > 0 and userHP > 0:
                    if message.author == upnow:
                        if message.content.lower() == "punch":
                            await punch()
                            if memHP > 0 and userHP > 0:
                                await ctx.send(
                                    f"**{upnow.mention}**, what do you want to do? `punch`, `defend`, or `end`?")
                                message = await client.wait_for('message', timeout=30)
                        if message.content.lower() == 'defend':
                            await defend()
                            if memHP > 0 and userHP > 0:
                                await ctx.send(
                                    f"**{upnow.mention}**, what do you want to do? `punch`, `defend`, or `end`?")
                                message = await client.wait_for('message', timeout=30)
                        if message.content.lower() == 'end':
                            await end()
                            return
                        if message.content.lower() not in ['end', 'punch', 'defend']:
                            await errorc()
                            if memHP > 0 and userHP > 0:
                                # await ctx.send(f"**{upnow}**, what do you want to do? `punch`, `defend`, or `end`?")
                                message = await client.wait_for('message', timeout=30)

                    else:
                        message = await client.wait_for('message', timeout=30)
                        continue
                if memHP <= 0:
                    await ctx.send(
                        f'Holy heck! **{member.name}** totally memed **{ctx.author.name}**, winning with just `{userHP}` HP left!')
                    return
                elif userHP <= 0:
                    await ctx.send(
                        f'Holy heck! **{ctx.author.name}** totally memed **{member.name}**, winning with just `{memHP}` HP left!')
                return
            except asyncio.TimeoutError:
                await ctx.send(f"No one was talking, so this fight has ended.")
                return




        except asyncio.TimeoutError:
            await ctx.send(f"No one was talking, so this fight has ended.")
            return

@fight.error
async def fight_err(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}fight [member]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)


@client.command(aliases = ['quickpoll'])
async def poll(ctx, *, pollc):
    try:
        author = ctx.message.author
        pfp = author.avatar_url
        embed = discord.Embed(description=pollc, color=discord.Color.red(), timestamp = datetime.datetime.utcnow())
        embed.set_author(name=author, icon_url=pfp)
        message = await ctx.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        return
    except asyncio.TimeoutError:
        await ctx.reply(
            "This poll-creation session has timed out. Please use the command again to generate another poll.")
        return

@poll.error
async def poll_errq(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}poll [text]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)

@client.command(aliases=['multiplechoicepoll', 'choice', 'createpoll'])
@commands.cooldown(5, 25, commands.BucketType.user)
async def choicepoll(ctx):
    #how much time would you like it to run for?
    #dm creator on timeup
    try:
        await ctx.reply(f"What would you like the title of the poll to be?", mention_author = False)
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        message = await client.wait_for('message', check=check, timeout = 30)
        if len(message.content) > 50:
            return await message.reply("Your title cannot be longer than 50 characters.", mention_author = False)
        title = message.content.strip()
        await message.reply(f"Great, I have saved the title. Now enter the options split by a \"|\" in this format:\n"
                       f"```coke | pepsi | sprite | fanta```", mention_author = False)
        message = await client.wait_for('message', check=check, timeout = 120)
        if "|" not in message.content:
            return await message.reply(f"You must specify at least two options.", mention_author = False)
        x = message.content.split("|")
        if len(x) > 9:
            return await message.reply(f"The maximum amount of options a poll can have is 9.", mention_author = False)
        descarr = []
        numarr = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        for i, k in enumerate(x):
            descarr.append(f":{numarr[i]}: --> {k.strip()}")
        desc = "\n".join(descarr)
        embed = discord.Embed(title = title, description = desc, color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
        embed.set_author(name=ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        message = await ctx.send(embed=embed)
        emoji_numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        for i, k in enumerate(x):
            await message.add_reaction(f"{emoji_numbers[i]}")
    except asyncio.TimeoutError:
        return await ctx.reply("Unfortunately, this poll creation session has timed out.", mention_author = False)



@client.command(aliases=['av'])
async def avatar(ctx, member: discord.Member = None):
    try:
        if member is None:
            author = ctx.message.author
            pfp = author.avatar_url
            embed = discord.Embed(title="**Avatar**")
            embed.set_author(name=author, icon_url=pfp)
            embed.set_image(url=pfp)
            await ctx.send(embed=embed)
            return
        else:
            author = member
            pfp = author.avatar_url
            embed = discord.Embed(title="**Avatar**")
            embed.set_author(name=str(author), icon_url=pfp)
            embed.set_image(url=pfp)
            await ctx.send(embed=embed)
            return
    except discord.ext.commands.errors.MemberNotFound:
        await ctx.reply(f'{member} is either not real or is not in this server.')
        return


@client.command(aliases=['flip', 'cf'])
async def coinflip(ctx):
    outcomes = ['heads', 'tails']
    final = random.choice(outcomes)
    await ctx.reply(f"{final}", mention_author=False)
    return


@client.command()
async def ping(ctx):
    time_1 = time.perf_counter()
    await ctx.trigger_typing()
    time_2 = time.perf_counter()
    ping = round((time_2 - time_1) * 1000)
    await ctx.reply(f"Pong! 🏓 `{ping}ms`", mention_author=False)
    return


@client.group(invoke_without_command=True)
async def typing(ctx):
    await ctx.send(
        f"{ctx.author.mention}, we are going to be testing your typing speed! Press `y` to confirm. Anything else, and we will end the session.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    message = await client.wait_for('message', check=check, timeout=30)
    if message.content.lower() == 'y':
        await ctx.send(
            f'Great, we will be calculating your typing speed.')
        await asyncio.sleep(1)
        await ctx.send(
            f"{ctx.author.mention} Excellent! A test will be available in 5 seconds. Type out the entire sentence in one go.")
        choices = []
        for file in os.listdir('./Discord Bot/Typing Test'):
            if file.endswith(".txt"):
                choices.append(file)
            if len(choices) == 0:
                # No typing tests... should never happen
                msg = 'I\'m not configured for typing test yet...'
                await ctx.send(msg)
                return
        try:
            randnum = random.randint(0, (len(choices) - 1))
            randLib = choices[randnum]
            with open("./Discord Bot/Typing Test/{}".format(randLib),
                        'r') as myfile:
                data = myfile.read()
                d2 = data.split()
                x = " ".join(d2)
                print(x)
            await asyncio.sleep(2)
            await ctx.send("Start typing as soon as the words show up.")
            await asyncio.sleep(2)
            await ctx.send(f'```{x}```')
            start = time.time()
            message = await client.wait_for('message', check=check, timeout=180)
            end = time.time()
            timtot = (end - start)
            inp = message.content.split()
            wpm = round((len(d2) / timtot) * 60)
            words = len(d2)
            timetaken = round(timtot)
            acc = 0
            for index, k in enumerate(inp):
                # print(index, k)
                try:
                    if k == d2[index]:
                        # print("yes")
                        acc += 1
                    else:
                        # print("no")
                        continue
                except IndexError:
                    break
            perccorr = round((acc / len(d2)) * 100)
            if message.content == x:
                if wpm >= 300:
                    await message.reply(f"{ctx.author.mention}, did you copy paste it smh", mention_author=False)
                    return
                await message.reply("Wow, you got it exactly right!", mention_author=False)
                await asyncio.sleep(1)
                name = f"GUILD{ctx.guild.id}"
                db = cluster[name]
                collection = db['typing']
                ping_cm = {
                    "name": ctx.guild.name,
                    "date": datetime.datetime.utcnow(),
                    'uid': ctx.author.id,
                    'accuracy': 100,
                    'wpm' : wpm
                }
                collection.insert_one(ping_cm)
                # cursor.execute(f"SELECT msgchannel_id from {name} WHERE user_id = {ctx.author.id}")
                # result232 = cursor.fetchone()
                # print('ok')
                # if result232 is not None:
                #     if int(result232[0]) < wpm:   
                #         sql = (f"UPDATE {name} SET wpm = ?, wpmtestdate = ?, accuracy = ? WHERE user_id = ? AND msgchannel_id = ?")
                #         val = (wpm, str(datetime.datetime.utcnow()), int(perccorr), ctx.author.id, ctx.channel.id)
                #         await ctx.send(f"You beat your Personal Best in {ctx.guild.name}!")
                #         cursor.execute(sql, val)
                #         db.commit()
                #     elif int(result232[0]) == wpm:
                #         await ctx.send(f"You tied your personal best in {ctx.guild.name}!")
                # elif str(result232[0]) == 'None':
                #     sql = (f"INSERT INTO {name}(user_id, wpm, wpmtestdate, accuracy, msgchannel_id) VALUES(?, ?, ?, ?, ?)")
                #     val = (ctx.author.id, wpm, str(datetime.datetime.utcnow()), int(perccorr), ctx.channel.id)
                #     cursor.execute(sql, val)
                #     db.commit()

                collection = db['typing']
                results = collection.find({'_id': ctx.guild.id})
                for i in results:
                    topscore = i['wpm']
                query = {'_id': ctx.guild.id}
                if collection.count_documents(query) == 0:
                    ping_cm = {
                        "_id": ctx.guild.id,
                        "name": ctx.guild.name,
                        "wpm": wpm,
                        'date': datetime.datetime.utcnow(),
                        'uid': ctx.author.id,
                        'accuracy': 100
                    }
                    collection.insert_one(ping_cm)
                    await ctx.send(f"🎉 With {wpm} WPM, you are now first place on the server WPM leaderboard! 🎉 ")
                elif topscore == '':
                    collection.update_one({"_id": ctx.guild.id}, {"$set": {'wpm': wpm, 'accuracy':100, 'uid':ctx.guild.id, 'date':datetime.datetime.utcnow(), 'name': ctx.guild.name}})
                    await ctx.send(f"🎉 With {wpm} WPM, you are now first place on the server WPM leaderboard! 🎉")
                else:
                    if int(topscore) < int(wpm):
                        collection.update_one({"_id": ctx.guild.id}, {
                            "$set": {'wpm': wpm, 'accuracy': 100, 'uid': ctx.author.id,
                                     'date': datetime.datetime.utcnow(), 'name': ctx.guild.name}})
                        await ctx.send(f"🎉 With {wpm} WPM, you are now first place on the server WPM leaderboard! 🎉")
                    elif int(topscore) == int(wpm):
                        collection.update_one({"_id": ctx.guild.id}, {
                            "$set": {'wpm': wpm, 'accuracy': 100, 'uid': ctx.author.id,
                                     'date': datetime.datetime.utcnow(), 'name': ctx.guild.name}})
                        await ctx.send(f"🎉 With {wpm} WPM, you tied first place on the server WPM leaderboard! 🎉 ")
                    else:
                        pass
                pfp = ctx.author.avatar_url
                author = ctx.author
                embed = discord.Embed(color=discord.Color.blurple(), timestamp = datetime.datetime.utcnow())
                embed.set_author(name=f'{author}\'s typing report', icon_url=pfp)
                embed.add_field(name="Accuracy:", value="100%")
                embed.add_field(name="Speed:", value=str(wpm) + " WPM", inline=False)
                embed.add_field(name="Words Typed:", value=str(words) + " words", inline=False)
                embed.add_field(name="Time Taken:", value=str(timetaken) + " seconds", inline=False)
                embed.set_footer(text=f"InfiniBot Typing Test | Requested by: {ctx.author}")
                await ctx.send(embed=embed)
                return
            elif message.content != x:
                if (end - start) <= 10:
                    await message.reply(
                        f"{ctx.author.mention}, lmao you copy pasted but still couldn\'t get it right.",
                        mention_author=False)
                    return
                await message.reply("Unfortunately this wasn\'t 100% accurate.", mention_author=False)
                perccorr = round((acc / len(d2)) * 100)
                pfp = ctx.author.avatar_url
                name = f"GUILD{ctx.guild.id}"
                db = cluster[name]
                collection = db['typing']
                query = {'_id': ctx.guild.id}
                if collection.count_documents(query) == 0:
                    ping_cm = {
                        "_id": ctx.guild.id,
                        "name": ctx.guild.name,
                        "wpm": 0,
                        'date': datetime.datetime.utcnow(),
                        'uid': ctx.author.id,
                        'accuracy': 100
                    }
                    collection.insert_one(ping_cm)
                else:
                    ping_cm = {
                        "name": ctx.guild.name,
                        "wpm": wpm,
                        'date': datetime.datetime.utcnow(),
                        'uid': ctx.author.id,
                        'accuracy': perccorr
                    }
                    collection.insert_one(ping_cm)
                # await ctx.send(f"Channel has been set to {channel.mention}.")
                author = ctx.author
                words = len(d2)
                timetaken = round(timtot)
                embed = discord.Embed(color=discord.Color.blurple(), timestamp = datetime.datetime.utcnow())
                embed.set_author(name=f'{author}\'s typing report', icon_url=pfp)
                embed.add_field(name="Accuracy:", value=str(perccorr) + "%")
                embed.add_field(name="Speed:", value=str(wpm) + "WPM", inline=False)
                embed.add_field(name="Words Typed:", value=str(words) + " words", inline=False)
                embed.add_field(name="Time Taken:", value=str(timetaken) + " seconds", inline=False)
                embed.set_footer(text=f"InfiniBot Typing Test | Requested by: {ctx.author}")
                await asyncio.sleep(1)
                await ctx.send(embed=embed)
                # await ctx.send(f'{ctx.author.mention}, you were {perccorr}% accurate.')
                return

        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention}, your typing test has timed out.")
            return

@client.command(aliases=['bal'])
async def balance(ctx, member: discord.Member = None):
    if member is None:
        user = ctx.author
    else:
        user = member
    await open_account(user)

    users = await get_bank_data()
    t = time.localtime()
    current_time = time.strftime(r"%I:%M %p", t)

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]
    embed = discord.Embed(title=f"{user.name}'s balance",
                          description=f'**Wallet**: {wallet_amt} coins \n**Bank**: {bank_amt} coins',
                          color=discord.Color.red(), timestamp = datetime.datetime.utcnow())
    embed.set_footer(text=f'😏 • {current_time}')
    await ctx.send(embed=embed)


@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def beg(ctx):
    # add a .txt file with stupid quotes to make the description of embed
    choices = []
    for file in os.listdir('./Discord Bot/Economy/Beg Command/Celebrities'):
        if file.endswith(".txt"):
            choices.append(file)
        if len(choices) == 0:
            # No list... should never happen
            msg = 'I\'m not configured for begging yet...'
            await ctx.send(msg)
            return
        randnum = random.randint(0, (len(choices) - 1))
        randLib = choices[randnum]
        with open("./Discord Bot/Economy/Beg Command/Celebrities/{}".format(randLib),
                  'r') as myfile:
            data = myfile.read()
            d2 = data.split(", ")
            randNUM = random.randint(0, (len(d2) - 1))

    await open_account(ctx.author)

    users = await get_bank_data()
    user = ctx.author

    earnings = random.randrange(101)
    # here create a .txt file with random names, and randomly select one.
    em = discord.Embed(color=discord.Color.green())

    await ctx.send(f'**{d2[randNUM]}** has donated {earnings} coins to {ctx.author.mention}!')
    users[str(user.id)]["wallet"] += earnings
    with open("mainbank.json", "w") as f:
        json.dump(users, f)


@client.command(aliases=['with'])
async def withdraw(ctx, amount=None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.reply("Please specify the amoun\'t you\'d like to withdraw.", mention_author=False)
        return

    bal = await update_bank(ctx.author)
    if amount.lower() == 'all':
        amount = bal[1]

    amount = int(amount)
    if amount == 0:
        await ctx.reply("There is nothing in your bank to withdraw.", mention_author=False)
        return
    if amount > bal[1]:
        await ctx.reply(f"You don\'t have {amount} coins.", mention_author=False)
        return
    if amount < 0:
        await ctx.reply(f'{amount} is not a positive number.')
        return

    await update_bank(ctx.author, amount, "wallet")
    await update_bank(ctx.author, -1 * amount, "bank")
    await ctx.reply(f'You withdrew {amount} coins!')


@client.command(aliases=['dep'])
async def deposit(ctx, amount=None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.reply("Please specify the amoun\'t you\'d like to deposit.", mention_author=False)
        return

    bal = await update_bank(ctx.author)
    if amount.lower() == 'all':
        amount = bal[0]

    amount = int(amount)
    if amount == 0:
        await ctx.reply("There is nothing in your wallet.", mention_author=False)
        return
    if amount > bal[0]:
        await ctx.reply(f"You don\'t have {amount} coins.", mention_author=False)
        return
    if amount < 0:
        await ctx.reply(f'{amount} is not a positive number.')
        return

    await update_bank(ctx.author, amount, "bank")
    await update_bank(ctx.author, -1 * amount, "wallet")
    await ctx.reply(f'You deposited **{amount}** coins!')


@client.command(aliases=['give'])
async def send(ctx, member: discord.Member = None, amount=None):
    if member == None:
        await ctx.reply("Please specify who you would like to send coins to!", mention_author=False)
        return
    await open_account(ctx.author)
    await open_account(member)

    if amount == None:
        await ctx.reply("Please specify the amoun\'t you\'d like to send.", mention_author=False)
        return

    bal = await update_bank(ctx.author)
    if amount.lower() == 'all':
        amount = bal[0]

    amount = int(amount)
    if amount == 0:
        await ctx.reply("You don\'t have any coins in your wallet.", mention_author=False)
        return

    if amount > bal[0]:
        await ctx.reply(f"You don\'t have **{amount}** coins.", mention_author=False)
        return
    if amount < 0:
        await ctx.reply(f'**{amount}** is not a positive number.')
        return

    await update_bank(ctx.author, -1 * amount, "wallet")
    await update_bank(member, amount, "wallet")
    await ctx.reply(f'Success! You gave `{amount}` coins to **{member.name}**!!')


@client.command(aliases=['steal'])
@commands.cooldown(1, 15, commands.BucketType.user)
async def rob(ctx, member: discord.Member = None):
    # add something here so that there is a 75-25 chance of not succeeding
    if member == None:
        await ctx.reply("Please specify who you would like to rob from!", mention_author=False)
        return

    await open_account(ctx.author)
    await open_account(member)
    bal1 = await update_bank(ctx.author)

    bal = await update_bank(member)

    if bal[0] < 100:
        await ctx.reply(f"**{member.name}** doesn\'t have enough coins, it\'s not worth it.", mention_author=False)
        return

    if bal1[0] < 5000:
        await ctx.reply(
            f"{ctx.author.mention}, you don\'t have enough money in your wallet to rob people. You need 5000 coins.",
            mention_author=False)
        return

    earnings = random.randrange(0, bal[0])
    if earnings > 0:
        randd = random.randint(1, 4)
        if randd == 1:
            if earnings > 20000:
                earnings = 15882
            else:
                if earnings < 500:
                    earnings = 1000
                else:
                    earnings = earnings
        else:
            earnings = 0

    if earnings == 0:
        await update_bank(ctx.author, -5000)
        await update_bank(member, 5000, "bank")
        pfp = ctx.author.avatar_url
        author = ctx.author.name
        embd = f"Status: FAILED! You\'ve been caught in the act robbing from **{member.name}**!! You\'ve given them 5,000 coins from your wallet to their bank."
        embed = discord.Embed(description=embd, color=discord.Color.red())
        embed.set_author(name=f'{author}\'s robbery of {member.name}', icon_url=pfp)
        await ctx.send(embed=embed)
        return

    await update_bank(ctx.author, earnings)
    await update_bank(member, -1 * earnings)
    pfp = ctx.author.avatar_url
    author = ctx.author.name
    embd = f"Status: Success! You\'ve robbed {earnings} coins from **{member.name}**."
    embed = discord.Embed(description=embd, color=discord.Color.green())
    embed.set_author(name=f'{author}\'s robbery of {member.name}', icon_url=pfp)
    await ctx.send(embed=embed)


# await ctx.reply(f'Success! You robbed `{earnings}` coins from **{member.name}**!!', mention_author = False)

@client.command(aliases=['slot', 'slotmachine'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def slots(ctx, amount=None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.reply("Please specify the amount you\'d like to gamble.", mention_author=False)
        return

    bal = await update_bank(ctx.author)

    if amount.lower() == 'all':
        amount = bal[0]

    amount = int(amount)
    if amount < 0:
        await ctx.reply(
            f'**{ctx.author.name}**, {amount} is not a positive number. What are they teaching you at school smh.',
            mention_author=False)
        return
    if amount < 500:
        await ctx.reply(f"**{ctx.author.name}**, don\'t be a wimp. Please gamble 500 coins or more.",
                        mention_author=False)
        return
    if amount > bal[0]:
        await ctx.reply(f"You don\'t have {amount} coins.", mention_author=False)
        return

    final = []
    for i in range(3):
        a = random.choice(
            ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
             "V", "W", "X", "Y", "Z"])
        final.append(a)

    x = " ".join(final)
    # await ctx.send(f'{ctx.author.name}, your three letters are as follows:')
    # for k in (x):
    # msg = await ctx.send(k)
    #  await asyncio.sleep(2)
    # await msg.edit(text = f" {k}")

    await ctx.send(f'{ctx.author.name}, your slot machine is spinning, be patient...')
    await asyncio.sleep(2)
    print(x)
    pfp = ctx.author.avatar_url
    if final[0] == final[1] == final[2]:
        await asyncio.sleep(1)
        await update_bank(ctx.author, int(1000 * amount))
        embd = ">**" + x + f"**< \n\n You won **{int(amount * 1000)}** coins! \nYou now have **{bal[0] + int(amount * 1000)}** coins."
        embed = discord.Embed(description=embd, color=discord.Color.green())
        embed.set_author(name=f'{ctx.author.name}\'s slot machine', icon_url=pfp)
        await ctx.send(embed=embed)
        return
    if final[0] == final[1] or final[0] == final[2] or final[1] == final[2]:
        await asyncio.sleep(1)
        await update_bank(ctx.author, int(100 * amount))
        embd = ">**" + x + f"**< \n\n You won **{int(amount * 100)}** coins! \nYou now have **{bal[0] + int(amount * 100)}** coins."
        embed = discord.Embed(description=embd, color=discord.Color.green())
        embed.set_author(name=f'{ctx.author.name}\'s slot machine', icon_url=pfp)
        await ctx.send(embed=embed)
        return
    else:
        await update_bank(ctx.author, int(-1 * amount))
        await asyncio.sleep(1)
        embd = ">**" + x + f"**< \n\n You lost **{int(amount)}** coins. \nYou now have **{bal[0] - int(amount * 1)}** coins."
        embed = discord.Embed(description=embd, color=discord.Color.red())
        embed.set_author(name=f'{ctx.author.name}\'s slot machine', icon_url=pfp)
        await ctx.send(embed=embed)
        # await ctx.send(f"You lost {amount} coins :(")


@client.command(aliases=['store'])
async def shop(ctx):
    embed = discord.Embed(title="Store", color=discord.Color.blue())
    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        embed.add_field(name=name, value=f'{price} coins | {desc}', inline=False)
    await ctx.send(embed=embed)


@client.command()
async def buy(ctx, item, amount=1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            await ctx.reply(f"`{item}` isn\'t in the shop!!", mention_author=False)
            return
        if res[1] == 2:
            await ctx.send(f'You don\'t have enough money in your wallet to buy {amount} of {item}')
            return

    item_name = item.lower()
    name_ = None
    price = None
    for itemz in mainshop:
        name = itemz["name"].lower()
        if name == item_name:
            name_ = name
            price = itemz['price']
            break
    tprice = amount * price
    pfp = ctx.author.avatar_url
    saleconf = f'{ctx.author.mention} bought {amount} **{item}{"" if amount == 1 else "s"}** and paid `{tprice}` coins.'
    embed = discord.Embed(description=saleconf, color=discord.Color.orange(), timestamp = datetime.datetime.utcnow())
    embed.set_author(name=f"Successful {item} purchase", icon_url=pfp)
    embed.set_footer(text=f"InfiniBot Economy | Requested by: {ctx.author}")
    await ctx.reply(embed=embed, mention_author=False)
    # await ctx.send(f'You just bought {amount} {item}{"" if amount == 1 else "s"}!')


@client.command(aliases=['inv', 'inventory'])
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]['bag']
    except:
        bag = []

    embed = discord.Embed(title="Bag")
    for item in bag:
        name = item['item']
        amount = item['amount']

        embed.add_field(name=name, value=amount)
    await ctx.send(embed=embed)


async def buy_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item['price']
            break

    if name_ == None:
        return [False, 1]

    cost = price * amount
    users = await get_bank_data()
    bal = await update_bank(user)

    if bal[0] < cost:
        return [False, 2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]['bag']:
            n = thing['item']
            if n == item_name:
                old_amt = thing['amount']
                new_amt = old_amt + amount
                users[str(user.id)]['bag'][index]['amount'] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]['bag'].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]['bag'] = [obj]

    with open('mainbank.json', 'w') as f:
        json.dump(users, f)

    await update_bank(user, cost * -1, "wallet")

    return [True, "Worked"]


@client.command()
async def sell(ctx, item, amount=1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author, item, amount)
    if not res[0]:
        if res[1] == 1:
            await ctx.reply(f"{item} isn\'t in the shop!", mention_author=False)
            return
        if res[1] == 2:
            await ctx.reply(
                f'You don\'t have {"a" if amount == 1 else f"{amount}"} {item}{"" if amount == 1 else "s"} in your inventory.',
                mention_author=False)
            return
        if res[1] == 3:
            await ctx.reply(f'You don\'t have a(n) {item} in your inventory.', mention_author=False)
            return
    pfp = ctx.author.avatar_url
    price = None
    item_name = item.lower()
    for itemz in mainshop:
        name = itemz["name"].lower()
        if name == item_name:
            name_ = name
            if price == None:
                price = int(0.75 * itemz['price'])
            break
    # price = int(0.75 * item['price'])
    tprice = amount * price
    saleconf = f'You just sold {amount} **{item}{"**" if amount == 1 else "s**"} for `{tprice}` coins.'
    embed = discord.Embed(description=saleconf, color=discord.Color.orange(), timestamp = datetime.datetime.utcnow())
    embed.set_author(name=f"Successful {item} sale", icon_url=pfp)
    embed.set_footer(text=f"InfiniBot Economy | Requested by: {ctx.author}")
    await ctx.reply(embed=embed, mention_author=False)
    return
    # await ctx.reply(f'You just sold {amount} {item}{"" if amount == 1 else "s"}.', mention_author = False)


async def sell_this(user, item_name, amount, price=None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price == None:
                price = int(0.75 * item['price'])
            break

    if name_ == None:
        return [False, 1]
    cost = price * amount
    users = await get_bank_data()
    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]['bag']:
            n = thing['item']
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False, 2]
                users[str(user.id)]['bag'][index]['amount'] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            return [False, 3]
    except:
        return [False, 3]

    with open('mainbank.json', 'w') as f:
        json.dump(users, f)

    await update_bank(user, cost, 'wallet')

    return [True, cost]


@client.command(aliases=['lb'])
async def leaderboard(ctx, x=5):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]['wallet'] + users[user]['bank']
        leader_board[total_amount] = name
        total.append(total_amount)
    total = sorted(total, reverse=True)
    embed = discord.Embed(title=f'Top {x} Richest People', description="Highest Net Worth Members:",
                          color=discord.Color.green(), timestamp = datetime.datetime.utcnow())
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        embed.add_field(name=f'{index}. {name}', value=f'{amt}', inline=False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed=embed)


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users


async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal


@client.command(aliases=['hl'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def highlow(ctx):
    num = random.randint(1, 100)
    hint = random.randint(1, 100)
    print(num)
    pfp = ctx.author.avatar_url
    author = ctx.author
    desc = f"A number secret between 1-100 has been chosen. Your hint is **{hint}**. \n" \
           f"Respond with \"high\", \"low\", or \"jackpot\"."
    embed = discord.Embed(description=desc, color=discord.Color.blurple())
    embed.set_author(name=f'{author}\'s high-low game', icon_url=pfp)
    embed.set_footer(text="Choose whether you think the hidden number is higher, lower, or the same number as the hint")
    await ctx.reply(embed=embed, mention_author=False)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        message = await client.wait_for('message', check=check, timeout=30)
        if message.content.lower() not in ['high', 'low', 'jackpot']:
            await message.reply(
                f"{ctx.author.mention} Hey your options to respond are \"high\", \"low\", and \"jackpot\". Run the command again with more brain cells next time. (Number was {num} btw)",
                mention_author=False)
            return
        if message.content.lower() == 'high':
            if num > hint:
                await update_bank(ctx.author, 500)
                pfp = ctx.author.avatar_url
                author = ctx.author
                desc = f"You won **500** coins! \n\nYour hint was **{hint}**. The hidden number was **{num}**."
                embed = discord.Embed(description=desc, color=discord.Color.green())
                embed.set_author(name=f'{author}\'s winning high-low game', icon_url=pfp)
                embed.set_footer(text=f"InfiniBot High-Low Game | Requested by: {ctx.author}")
                await ctx.send(embed=embed)
                return
            else:
                pfp = ctx.author.avatar_url
                author = ctx.author
                desc = f"**You lost!** \n\nYour hint was **{hint}**. The hidden number was **{num}**."
                embed = discord.Embed(description=desc, color=discord.Color.red())
                embed.set_author(name=f'{author}\'s losing high-low game', icon_url=pfp)
                embed.set_footer(text=f"InfiniBot High-Low Game | Requested by: {ctx.author}")
                await ctx.send(embed=embed)
                return
        if message.content.lower() == "low":
            if num < hint:
                await update_bank(ctx.author, 500)
                pfp = ctx.author.avatar_url
                author = ctx.author
                desc = f"You won **500** coins! \n\nYour hint was **{hint}**. The hidden number was **{num}**."
                embed = discord.Embed(description=desc, color=discord.Color.green())
                embed.set_author(name=f'{author}\'s winning high-low game', icon_url=pfp)
                embed.set_footer(text=f"InfiniBot High-Low Game | Requested by: {ctx.author}")
                await ctx.send(embed=embed)
                return
            else:
                pfp = ctx.author.avatar_url
                author = ctx.author
                desc = f"**You lost!** \n\nYour hint was **{hint}**. The hidden number was **{num}**."
                embed = discord.Embed(description=desc, color=discord.Color.red())
                embed.set_author(name=f'{author}\'s losing high-low game', icon_url=pfp)
                embed.set_footer(text=f"InfiniBot High-Low Game | Requested by: {ctx.author}")
                await ctx.send(embed=embed)
                return
        if message.content.lower() == 'jackpot':
            if num == hint:
                await update_bank(ctx.author, 1000000)
                pfp = ctx.author.avatar_url
                author = ctx.author
                desc = f"You won **1,000,000** coins! \n\nYour hint was **{hint}**. The hidden number was **{num}**."
                embed = discord.Embed(description=desc, color=discord.Color.green())
                embed.set_author(name=f'{author}\'s winning high-low game', icon_url=pfp)
                embed.set_footer(text=f"InfiniBot High-Low Game | Requested by: {ctx.author}")
                await ctx.send(embed=embed)
                return
            else:
                pfp = ctx.author.avatar_url
                author = ctx.author
                desc = f"**You lost!** \n\nYour hint was **{hint}**. The hidden number was **{num}**."
                embed = discord.Embed(description=desc, color=discord.Color.red())
                embed.set_author(name=f'{author}\'s losing high-low game', icon_url=pfp)
                embed.set_footer(text=f"InfiniBot High-Low Game | Requested by: {ctx.author}")
                await ctx.send(embed=embed)
                return

    except asyncio.TimeoutError:
        await ctx.send(f'{ctx.author.mention}, your high-low game has timed out.')
        return


@client.command(aliases=['pm'])
#in dev
async def postmemes(ctx):
    await ctx.send(
        f'**{ctx.author.mention}, what type of meme do you wan\'t to post?**\n`f` ■ Fresh Meme\n `r` ■ Reposted Meme \n`i` ■ Intellectual Meme\n`c` ■ Copypasta \n`k` ■ Kind Meme')

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        message = await client.wait_for('message', check=check, timeout=30)
        if message.content.lower() not in ['f', 'r', 'i', 'c', 'k']:
            await ctx.reply(f"{ctx.author.name}, that is not a valid option.", mention_author=False)
            return
        if message.content.lower() == 'f':
            await ctx.reply(f'{ctx.author.mention}, glizzybeam7801 is finishing this ASAP.')
            return
    except asyncio.TimeoutError:
        await ctx.reply(f'{ctx.author.mention}, your use of this command has timed out.', mention_author=False)
        return


@client.command(aliases=['ui'])
# ADD THE PERMISSIONS FIELD FOR THE EMBED, ADD USER ID and TIME REQUEST IN THE FOOTER
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    acc = client.get_user(member.id)
    create = acc.created_at.strftime("%b %d, %Y @ %H:%M:%S %p UTC")
    gjoin = member.joined_at.strftime("%b %d, %Y @ %H:%M:%S %p UTC")
    pfp = member.avatar_url
    author = member
    roles = []
    for role in member.roles:
        if role.name == "@everyone":
            continue
        else:
            roles.append(role.name)

    rolestr = ", ".join(reversed(roles))
    embed = discord.Embed(description=member.mention, color=discord.Color.blurple(), timestamp = datetime.datetime.utcnow())
    embed.set_author(name=author, icon_url=pfp)
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="Display Name", value = f"```{member.display_name}```")
    embed.add_field(name="User ID", value = f"```{member.id}```")
    embed.add_field(name="Joined", value=f"```{gjoin}```", inline = False)
    embed.add_field(name="Registered", value=f"```{create}```")
    embed.add_field(name=f"Roles [{len(roles)}]", value=f"```{rolestr if len(roles) != 0 else 'None'}```", inline=False)
    embed.set_footer(text=f"ID: {member.id}")
    await ctx.send(embed=embed)


@client.command(aliases=['rockpaperscissors'])
async def rps(ctx, member: discord.Member = None):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    if member == ctx.author:
        await ctx.reply(f'{ctx.author.name}, you can\'t play rock paper scissors against yourself lol.',
                        mention_author=False)
        return

    # if member.bot:
    #     print(member.name)
    #     await ctx.reply(f'{ctx.author.name}, you cannot play rock paper scissors against a bot.', mention_author = False)
    #     return

    try:
        if member is None:
            # ownerid = client.owner_id
            # owner = await client.get_user(ownerid)
            # print(owner)
            print(ctx.author.mention)
            print('yes')
            await ctx.reply(
                f'**{ctx.author.name}**, since you didn\'t mention a user to go against, you will go against an AI copy of my owner.',
                mention_author=False)
            await asyncio.sleep(1)
            pfp = ctx.author.avatar_url
            auth = ctx.author.name
            desc = f'**{ctx.author.name}**, type either `rock`, `paper`, or `scissors` into the chat below!'
            embed = discord.Embed(description=desc, color=discord.Color.blurple())
            embed.set_author(name=f'{auth}\'s Rock-Paper-Scissors game', icon_url=pfp)
            embed.set_footer(text=f"InfiniBot Rock Paper Scissors Match | Requested by {ctx.author.name}")
            await ctx.send(embed=embed)
            # await ctx.send(f'{ctx.author.name}, say `rock`, `paper`, or `scissors`.')
            randomword = random.choice(["Rock", "Paper", "Scissors"])
            message = await client.wait_for('message', check=check, timeout=30)
            if message.content.lower() not in ['rock', 'paper', 'scissors']:
                await ctx.reply(
                    f'`{message.content}` is not either `rock`, `paper`, or `scissors`. Use the command next time with more brain cells.',
                    mention_author=False)
                return
            if message.content.lower() == 'rock':
                if randomword == 'Paper':
                    desc = f'{ctx.author.mention}\'s word: **{message.content}**\n<@759245009693704213>\'s word: **{randomword}**'
                    fembed = discord.Embed(description=desc, color=discord.Color.red())
                    fembed.set_author(name=f'{auth}\'s losing match', icon_url=pfp)
                    fembed.set_footer(text=f"InfiniBot Rock Paper Scissors Match | Requested by {ctx.author.name}")
                    await ctx.reply(embed=fembed, mention_author=False)
                    await ctx.send(f"GG {ctx.author.mention}, but <@759245009693704213> wins this match.")
                    return
                else:
                    if message.content.lower() == randomword.lower():
                        desc = f'{ctx.author.mention}\'s word: **{message.content}**\n<@759245009693704213>\'s word: **{randomword}**'
                        fembed = discord.Embed(description=desc, color=discord.Color.greyple())
                        fembed.set_author(name=f'{auth}\'s tying match', icon_url=pfp)
                        fembed.set_footer(text=f"InfiniBot Rock Paper Scissors Match | Requested by {ctx.author.name}")
                        await ctx.reply(embed=fembed, mention_author=False)
                        await ctx.send(
                            f"{ctx.author.mention}, you and <@759245009693704213> TIED! Use the command to go again.")
                        return
                    desc = f'{ctx.author.mention}\'s word: **{message.content}**\n<@759245009693704213>\'s word: **{randomword}**'
                    fembed = discord.Embed(description=desc, color=discord.Color.green())
                    fembed.set_author(name=f'{auth}\'s winning match', icon_url=pfp)
                    fembed.set_footer(text=f"InfiniBot Rock Paper Scissors Match | Requested by {ctx.author.name}")
                    await ctx.reply(embed=fembed, mention_author=False)
                    await ctx.send(
                        f"{ctx.author.mention}, congratulations, you WON! Use the command to go again.")
                    return
                    # await ctx.reply(f'{randomword}! Aww, you win this match.', mention_author = False)
                    # return
            if message.content.lower() == 'paper':
                if randomword == 'Scissors':
                    desc = f'{ctx.author.mention}\'s word: **{message.content}**\n<@759245009693704213>\'s word: **{randomword}**'
                    fembed = discord.Embed(description=desc, color=discord.Color.red())
                    fembed.set_author(name=f'{auth}\'s losing match', icon_url=pfp)
                    fembed.set_footer(text=f"InfiniBot Rock Paper Scissors Match | Requested by {ctx.author.name}")
                    await ctx.reply(embed=fembed, mention_author=False)
                    await ctx.send(
                        f"GG {ctx.author.mention}, but <@759245009693704213> wins this match! Use the command to go again.")
                    return
                    # await ctx.send(f"{randomword}! I win this match.", mention_author=False)
                else:
                    if message.content.lower() == randomword.lower():
                        desc = f'{ctx.author.mention}\'s word: **{message.content}**\n<@759245009693704213>\'s word: **{randomword}**'
                        fembed = discord.Embed(description=desc, color=discord.Color.greyple())
                        fembed.set_author(name=f'{auth}\'s tying match', icon_url=pfp)
                        fembed.set_footer(text=f"InfiniBot Rock Paper Scissors Match | Requested by {ctx.author.name}")
                        await ctx.reply(embed=fembed, mention_author=False)
                        await ctx.send(
                            f"Wow {ctx.author.mention}, you and <@759245009693704213> tied this match! Use the command to go again.")
                        return

                    desc = f'{ctx.author.mention}\'s word: **{message.content}**\n<@759245009693704213>\'s word: **{randomword}**'
                    fembed = discord.Embed(description=desc, color=discord.Color.green())
                    fembed.set_author(name=f'{auth}\'s winning match', icon_url=pfp)
                    fembed.set_footer(text=f"InfiniBot Rock Paper Scissors Match | Requested by {ctx.author.name}")
                    await ctx.reply(embed=fembed, mention_author=False)
                    await ctx.send(
                        f"GG {ctx.author.mention}, you win! Use the command to go again.")
                    # await ctx.reply(f'{randomword}! Aww, you win this match.', mention_author = False)
                    return
            if message.content.lower() == 'scissors':
                if randomword == 'Rock':
                    desc = f'{ctx.author.mention}\'s word: **{message.content}**\n<@759245009693704213>\'s word: **{randomword}**'
                    fembed = discord.Embed(description=desc, color=discord.Color.red())
                    fembed.set_author(name=f'{auth}\'s losing match', icon_url=pfp)
                    fembed.set_footer(text=f"InfiniBot Rock Paper Scissors Match | Requested by {ctx.author.name}")
                    await ctx.reply(embed=fembed, mention_author=False)
                    await ctx.send(
                        f"GG {ctx.author.mention}, but <@759245009693704213> wins this match! Use the command to go again.")
                    # await ctx.reply(f"{randomword}! I win this match.", mention_author=False)
                    return
                else:
                    if message.content.lower() == randomword.lower():
                        desc = f'{ctx.author.mention}\'s word: **{message.content}**\n<@759245009693704213>\'s word: **{randomword}**'
                        fembed = discord.Embed(description=desc, color=discord.Color.greyple())
                        fembed.set_author(name=f'{auth}\'s tying match', icon_url=pfp)
                        fembed.set_footer(text=f"InfiniBot Rock Paper Scissors Match | Requested by {ctx.author.name}")
                        await ctx.reply(embed=fembed, mention_author=False)
                        await ctx.send(
                            f"Lol {ctx.author.mention}, you and <@759245009693704213> tied! Use the command to go again.")
                        return
                    desc = f'{ctx.author.mention}\'s word: **{message.content}**\n<@759245009693704213>\'s word: **{randomword}**'
                    fembed = discord.Embed(description=desc, color=discord.Color.red())
                    fembed.set_author(name=f'{auth}\'s winning match', icon_url=pfp)
                    fembed.set_footer(text=f"InfiniBot Rock Paper Scissors Match | Requested by {ctx.author.name}")
                    await ctx.reply(embed=fembed, mention_author=False)
                    await ctx.send(
                        f"GG {ctx.author.mention}, you win this match! Use the command to go again.")
                    # await ctx.reply(f'{randomword}! Aww, you win this match.', mention_author=False)
                    return
        else:
            await ctx.send(
                f"{member.mention}, {ctx.author.mention} wants to play rock-paper-scissors with you! To confirm, press `y`. Else, press anything else. Respond in 30 seconds.")

            def check(m):
                return m.author == member and m.channel == ctx.channel

            message = await client.wait_for('message', check=check, timeout=30)
            if message.content.lower() != 'y':
                await ctx.send(
                    f"{ctx.author.mention}, it looks like **{message.author.name}** doesn\'t want to play right now.")
                return
            mem = member
            auth = ctx.author
            mempfp = mem.avatar_url
            authpfp = ctx.author.avatar_url
            memid = member.id
            authID = ctx.author.id
            idlist = []
            idlist.append(memid)
            idlist.append(authID)
            print(idlist)
            submitted = 0
            noticemem = f"**{mem.name}**, type your answer into this DM:"
            noticeauth = f"**{auth.name}**, type your answer into this DM:"
            membed = discord.Embed(description=f"Paper\nRock\nScissors\n\n{noticemem}", color=discord.Color.greyple())
            authembed = discord.Embed(description=f"Paper\nRock\nScissors\n\n{noticeauth}",
                                      color=discord.Color.greyple())
            membed.set_author(name=f"{member.name}'s options:", icon_url=mempfp)
            authembed.set_author(name=f'{ctx.author.name}\'s options:', icon_url=authpfp)
            try:
                await mem.send(embed=membed)
                await auth.send(embed=authembed)
            except discord.Forbidden:
                return await ctx.send("Someone's Dms were off, this game will not work otherwise.")
            anslist = []
            while submitted < 2:
                message = await client.wait_for('message', timeout=30)
                if message.author.id in idlist:
                    submitted += 1
                    msg = message.content
                    authmen = (idlist.index(message.author.id))
                    # listans = message.author.mention + msg
                    ans = f'{message.author.mention}: {msg}'
                    anslist.append(ans)
                    # print(ans)
                else:
                    pass
            # x = "\n".join(anslist)
            us = []
            # await ctx.send(x)
            for k in anslist:
                if 'rock' in k.lower():
                    print(anslist.index(k))
                    us.append(k.split(":"))
                    # print(us.index('rock'))
                    print(us)
                    # await ctx.send('hi')
                if 'paper' in k.lower():
                    print(anslist.index(k))
                    us.append(k.split(":"))
                    print(us)
                    # await ctx.send('hi')
                if 'scissors' in k.lower():
                    print(anslist.index(k))
                    us.append(k.split(":"))
                    print(us)
                    # await ctx.send('hi')
            if 'rock' in us[0][1].lower():
                if 'paper' in us[1][1].lower():
                    # pfp = us[1][0]
                    desc = f"{us[0][0]}'s word: **{us[0][1]}** \n{us[1][0]}\'s word: **{us[1][1]}**"
                    membed = discord.Embed(description=f"{desc}", color=discord.Color.greyple())
                    membed.set_author(name=f"Results:")
                    await ctx.send(embed=membed)
                    await ctx.send(f"GG {us[0][0]}, but {us[1][0]} wins!")
                    return
                else:
                    if 'rock' in us[1][1].lower():
                        desc = f"{us[0][0]}'s word: **{us[0][1]}** \n{us[1][0]}\'s word: **{us[1][1]}**"
                        membed = discord.Embed(description=f"{desc}", color=discord.Color.greyple())
                        membed.set_author(name=f"Results:")
                        await ctx.send(embed=membed)
                        await ctx.send(f"Wow! Both {us[1][0]} and {us[0][0]} said the same thing! It\'s a tie!")
                        return
                    desc = f"{us[0][0]}'s word: **{us[0][1]}** \n{us[1][0]}\'s word: **{us[1][1]}**"
                    membed = discord.Embed(description=f"{desc}", color=discord.Color.greyple())
                    membed.set_author(name=f"Results:")
                    await ctx.send(embed=membed)
                    await ctx.send(f"GG {us[1][0]}, but {us[0][0]} wins!")
                    # await ctx.send(f'{us[0][0]} wins!')
                    return
            if 'paper' in us[0][1].lower():
                if 'scissors' in us[1][1].lower():
                    desc = f"{us[0][0]}'s word: **{us[0][1]}** \n{us[1][0]}\'s word: **{us[1][1]}**"
                    membed = discord.Embed(description=f"{desc}", color=discord.Color.greyple())
                    membed.set_author(name=f"Results:")
                    await ctx.send(embed=membed)
                    await ctx.send(f"GG {us[0][0]}, but {us[1][0]} wins!")
                    # await ctx.send(f'{us[1][0]} wins!')
                    return
                else:
                    if 'paper' in us[1][1].lower():
                        desc = f"{us[0][0]}'s word: **{us[0][1]}** \n{us[1][0]}\'s word: **{us[1][1]}**"
                        membed = discord.Embed(description=f"{desc}", color=discord.Color.greyple())
                        membed.set_author(name=f"Results:")
                        await ctx.send(embed=membed)
                        await ctx.send(f"Wow! Both {us[1][0]} and {us[0][0]} said the same thing! It\'s a tie!")
                        return
                    desc = f"{us[0][0]}'s word: **{us[0][1]}** \n{us[1][0]}\'s word: **{us[1][1]}**"
                    membed = discord.Embed(description=f"{desc}", color=discord.Color.greyple())
                    membed.set_author(name=f"Results:")
                    await ctx.send(embed=membed)
                    await ctx.send(f"GG {us[1][0]}, but {us[0][0]} wins!")
                    # await ctx.send(f'{us[0][0]} wins!')
                    return
            if 'scissors' in us[0][1].lower():
                if 'rock' in us[1][1].lower():
                    desc = f"{us[0][0]}'s word: **{us[0][1]}** \n{us[1][0]}\'s word: **{us[1][1]}**"
                    membed = discord.Embed(description=f"{desc}", color=discord.Color.greyple())
                    membed.set_author(name=f"Results:")
                    await ctx.send(embed=membed)
                    await ctx.send(f"GG {us[0][0]}, but {us[1][0]} wins!")
                    # await ctx.send(f'{us[1][0]} wins!')
                    return
                else:
                    if 'scissors' in us[1][1].lower():
                        desc = f"{us[0][0]}'s word: **{us[0][1]}** \n{us[1][0]}\'s word: **{us[1][1]}**"
                        membed = discord.Embed(description=f"{desc}", color=discord.Color.greyple())
                        membed.set_author(name=f"Results:")
                        await ctx.send(embed=membed)
                        await ctx.send(f"Wow! Both {us[1][0]} and {us[0][0]} said the same thing! It\'s a tie!")
                        return
                    desc = f"{us[0][0]}'s word: **{us[0][1]}** \n{us[1][0]}\'s word: **{us[1][1]}**"
                    membed = discord.Embed(description=f"{desc}", color=discord.Color.greyple())
                    membed.set_author(name=f"Results:")
                    await ctx.send(embed=membed)
                    await ctx.send(f"GG {us[1][0]}, but {us[0][0]} wins!")
                    # await ctx.send(f'{us[0][0]} wins!')
                    return
    except asyncio.TimeoutError:
        await ctx.send(f'{ctx.author.mention}, your rock paper scissors match has ended due to inactivity.')
        return


@client.command(aliases=['ot'])
async def openticket(ctx):
    await ctx.message.delete()
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
        ctx.message.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    num = random.randint(0000, 1002222384031)
    name = f"open-ticket-{num}"
    channel = await ctx.message.guild.create_text_channel(name, overwrites=overwrites)
    await channel.send(f"{ctx.author.mention}, you have opened a support ticket.")
    desc = f"Someone will be here to assist you shortly.\nWhile you are here, please state your issue/problem."
    embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp = datetime.datetime.utcnow())
    embed.set_footer(text=f"InfiniBot Ticketing Tool | Ticket Created by {ctx.author.name}")
    await channel.send(embed=embed)
    try:
        while 1 == 1:
            message = await client.wait_for('message')
            if message.content.lower() == 'ct' or message.content.lower() == 'closeticket':
                await ctx.trigger_typing()
                msg = await message.reply(
                    f"{message.author.mention}, if you would like to save this channel, react with the ✅, otherwise react with the :no_entry: emoji to delete this channel.",
                    mention_author=False)
                await msg.add_reaction("✅")
                await msg.add_reaction('⛔')

                def check(reaction, user):
                    return user == message.author and str(reaction.emoji) in ["✅", '⛔']

                reaction, user = await client.wait_for('reaction_add', check=check, timeout=30)
                print('yes')
                if reaction.emoji == '⛔':
                    print('hi')
                    await ctx.trigger_typing()
                    await message.channel.send('This channel will be deleted shortly...')
                    await asyncio.sleep(3)
                    await channel.delete()
                    return
                if reaction.emoji == ("✅"):
                    print("yes")
                    await ctx.trigger_typing()
                    overwrites = {
                        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        ctx.guild.me: discord.PermissionOverwrite(read_messages=False),
                        # ctx.message.author: discord.PermissionOverwrite(send_messages=True)
                        ctx.message.author: discord.PermissionOverwrite(read_messages=True, send_messages=False)
                    }
                    await message.channel.send('Great, this channel will be saved. Updating overwrites now...')
                    await asyncio.sleep(3)
                    newname = f"closed-ticket-{num}"
                    await channel.edit(overwrites=overwrites, name=newname)
                    return
            else:
                continue
    except asyncio.TimeoutError:
        await channel.send(f"Since no one responded, I am going to delete the channel automatically in 5 seconds.")
        await asyncio.sleep(5)
        await channel.delete(name)


# @client.command()
# async def cleantickets(ctx)
# for every channel that contains 'tickets' in it will be deleted

async def servercaptcha(member:discord.Member):
    name = f"GUILD{member.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': member.guild.id})
    for i in results:
        welcomerole = i['welcomerole']
    choices = []
    for file in os.listdir('./Discord Bot/Server Captcha'):
        if file.endswith(".png"):
            choices.append(file)
    randnum = random.randint(0, (len(choices) - 1))
    randLib = choices[randnum]
    icon_url = member.guild.icon_url
    desc = f"Please send the captcha code into this DM.\n\nHey there! Before joining **{member.guild.name}**, you are required by the admins" \
           f" to succesfully complete a captcha before you can get verified.\nThis is to protect the server against bot attacks and raids.\n" \
           f"\n**Note: Make sure your captcha response is exactly the same, as the captcha is case-sensitive. You will get 3 tries.\n\n **ANSWER WITHIN 5 MINUTES!"
    gameembed = discord.Embed(title=f"Welcome to {member.guild.name}!", description=desc, color=discord.Color.blue(), timestamp = datetime.datetime.utcnow())
    gamefile = discord.File(f"./Discord Bot/Server Captcha/{randLib}",
                            filename="image.png")
    gameembed.set_image(url="attachment://image.png")
    gameembed.set_author(name=f'{member.guild.name}', icon_url=icon_url)
    gameembed.set_footer(text="InfiniBot | Server Verification")
    await member.send(file=gamefile, embed=gameembed)
    d2 = randLib.split(".")

    def check(m):
        return m.author == member and isinstance(m.channel, discord.DMChannel)

    try:
        t_end = time.time() + 300
        tries = 0
        while time.time() < t_end and tries < 3:
            msg = await client.wait_for('message', check=check, timeout=300)
            if msg.content == d2[0]:
                try:
                    role = discord.utils.get(member.guild.roles, id=int(welcomerole))
                    user = member
                    await user.add_roles(role)
                    confembed = discord.Embed(title=f"Thank you for verifying!",
                                              description=f'You have been verified in the server **{member.guild.name}**!',
                                              color=discord.Color.green(), timestamp = datetime.datetime.utcnow())
                    confembed.set_footer(text="InfiniBot Server Verification")
                    await msg.channel.send(embed=confembed)
                    return True
                except AttributeError:
                    confembed = discord.Embed(title=f"Thank you for verifying!",
                                              description=f'You have been verified in the server **{member.guild.name}**!',
                                              color=discord.Color.green(), timestamp = datetime.datetime.utcnow())
                    confembed.set_footer(text="InfiniBot Server Verification")
                    await msg.channel.send(embed=confembed)
                    return True
            else:
                tries += 1
                await msg.reply(
                    f"**{msg.author.name}**, that\'s not correct. You have {3 - tries} attempt{'' if tries == 2 else 's'} left.",
                    mention_author=False)
                continue

        await asyncio.sleep(1)
        dessc = f"{member.mention}, you failed to get the CAPTCHA within three guesses, so you must ask a server moderator to manually give you a role."
        embed = discord.Embed(title="STATUS: FAILED", description=dessc, color=discord.Color.red(), timestamp = datetime.datetime.utcnow())
        embed.set_author(name=member.guild.name + "'s CAPTCHA Verification", icon_url=icon_url)
        await member.send(embed=embed)
        return False
    except asyncio.TimeoutError:
        await member.send(
            f"{member.name}, you did not answer within 5 minutes, so you must ask a server moderator to manually give you a role.")
        return False


@client.command(aliases=['serverconfig', 'serverconfiguration'])
@commands.has_permissions(manage_guild = True)
async def serverinfo(ctx):
    await ctx.trigger_typing()
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
        welcomechannel = i['welcomechannel']
        welcomemsg = i['welcomemsg']
        privmsg = i['priv_welcomemsg']
        welcomerole = i['welcomerole']
        captchaon = i['captchaon']
        muterole = i['muterole']
        spamdetect = ['spamdetect']
        logging = i['logging']
        logchannel = i['logchannel']
        ghostpingon = i['ghostpingon']
        leavemsg = i['leavemsg']
        welcomenick = i['welcomenick']
    try:
        welcomechannel = client.get_channel(int(welcomechannel))
    except:
        welcomechannel = None
    try:
        logchannel = client.get_channel(int(logchannel))
    except:
        logchannel = None
    try:
        muterole = discord.utils.get(ctx.guild.roles, id=int(muterole))
    except:
        muterole = None
    try:
        welcomerole= discord.utils.get(ctx.guild.roles, id=int(welcomerole))
    except:
        welcomerole = None
    try:
        embed = discord.Embed(color=discord.Color.blurple())
        embed.set_author(name=f"{ctx.guild.name}'s InfiniBot Config", icon_url=ctx.guild.icon_url)
        embed.add_field(name="Welcome Message:", value=f"{welcomemsg if welcomemsg != '' else 'None'}", inline=False)
        embed.add_field(name="Private Welcome Message: ", value=f"{privmsg if privmsg != '' else 'None'}", inline=False)
        embed.add_field(name="Welcome Message Channel:",
                        value=f"{'Not specified' if welcomechannel is None else welcomechannel.mention}", inline=False)
        embed.add_field(name="On Member Join Role:",
                        value=f'{"Not specified" if welcomerole is None else welcomerole.mention}', inline=False)
        embed.add_field(name="Goodbye Message: ",
                        value=f"{'Not specified' if str(leavemsg) == '' else str(leavemsg)}", inline=False)
        embed.add_field(name="Captcha Enabled: ", value=f"{'Yes' if str(captchaon) == 'on' else 'No'}", inline=False)
        embed.add_field(name="Muterole:", value=f"{'Not specified' if muterole is None else muterole.mention}",
                        inline=False)
        embed.add_field(name="Spam Detection Enabled: ", value=f"{'Yes' if str(spamdetect) == 'on' else 'No'}",
                        inline=False)
        embed.add_field(name="Logging Enabled: ", value=f"{'Yes' if str(logging) == 'on' else 'No'}", inline=False)
        embed.add_field(name="Logging Channel:",
                        value=f"{logchannel.mention if logchannel is not None else 'Not specified'}", inline=False)
        embed.add_field(name="Ghost Ping Detection Enabled: ", value=f"{'Yes' if str(ghostpingon) == 'on' else 'No'}",
                        inline=False)
        embed.add_field(name="Server Prefix: ", value=f"{prefix}",
                        inline=False)
        embed.add_field(name = "Welcome Nickname", value = f"{'None' if str(welcomenick) == '' else welcomenick}")
        embed.set_footer(text=f"InfiniBot Server Information | Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    except Exception as e:
        print(e)
        await ctx.send('Something went wrong, try again later.')

    # await ctx.send(f'{result1[0], result2[0], result[0], result3[0], result4[0]}')


# @client.command()
# async def hack(ctx, member:discord.Member = None):
#     if member == None:
#         await ctx.reply("Use the command again, but make sure to mention a user this time.", mention_author = False)
#         return
#     else:


@client.command()
@commands.has_permissions(ban_members = True)
async def softban(ctx, member: discord.Member = None, *, reason = "To delete messages"):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if member is None:
        desc = f"```{prefix}softban [member] (reason)```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    if ctx.author.guild_permissions.ban_members:
        try:
            pfp = member.avatar_url
            author = member
            embed = discord.Embed(description=f"For reason: ```{reason}```", color=discord.Color.dark_red())
            embed.set_author(name=f"{str(author.name)} has been softbanned.", icon_url=pfp)
            await ctx.send(embed=embed)
            await ctx.guild.ban(member, reason="To delete messages")
            await ctx.guild.unban(user=member)
            return
        except discord.Forbidden:
            await ctx.send(f'I don\'t have the required permissions to softban **{member.name}**')
            return


@client.command(aliases=['ASCII'])
async def ascii(ctx, *, text = None):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if text is None:
        desc = f"```{prefix}ascii [text]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)

    x = [ord(c) for c in text]
    await ctx.reply("".join(str(v) for v in x))


@client.command(aliases=['rev'])
async def reverse(ctx, *, text:str):
    await ctx.send(text[::-1])

@reverse.error
async def rev_err(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}reverse [text]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)


@client.group()
# in development
async def crypto(ctx, coin = None, pair="USDT", interval="1h", limit: int = 50):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if coin is None:
        desc = f"```{prefix}crypto [coin] (pair)```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)


    symbol = (coin + pair).upper()
    async with aiohttp.ClientSession() as session:
        url = "https://api.binance.com/api/v3/klines"
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        async with session.get(url, params=params) as response:
            data = await response.json()

    current_price = Decimal(data[-1][4]).normalize()
    print(current_price)
    desc = f"{symbol}: ${current_price} USD"
    embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp = datetime.datetime.utcnow())
    embed.set_author(name=f"{ctx.author.name}'s crypto outlook", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
# in dev
async def trivia(ctx, questions = 10):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://opentdb.com/api.php?amount=50&type=multiple") as response:
            r = await response.json()
    if str(r['response_code']) != "0":
        return await ctx.send(f"Something went wrong while accessing the trivia questions.")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.message.channel

    try:
        score = 0
        quesnum = int(questions)
        await ctx.send(f"There will be {quesnum} question{'' if quesnum == 1 else 's'}.")
        for m in range(0, quesnum):
            randnum = random.randint(0, 49)
            quest = r['results'][randnum]['question']
            j = str(quest).replace("&#039;", "'")
            k = str(j).replace("&quot;", '"')
            print(k)
            title = f"Question #{m + 1}"
            choicearr = []
            choicearr.append(r['results'][randnum]['correct_answer'])
            for i in range(0, 3):
                choicearr.append(r['results'][randnum]['incorrect_answers'][i])

            random.shuffle(choicearr)
            fin = []
            print(choicearr)
            for i in range(len(choicearr)):
                fin.append(f"{i + 1}. {choicearr[i]}")
            desc = "\n".join(fin)
            print(desc)
            answer = r['results'][randnum]['correct_answer']
            embed = discord.Embed(title = title, description = f"Category: **{r['results'][randnum]['category']}**\n\n{k}\n\n{desc} \n\n **RESPOND WITH THE PHRASE!**", color = discord.Color.greyple())
            embed.set_author(name=f"{ctx.author.name}'s trivia game", icon_url = ctx.author.avatar_url)
            embed.set_thumbnail(url = ctx.guild.icon_url)
            embed.set_footer(text=f"Type cancel to end | Requested by {ctx.author.name}")
            await ctx.send(embed=embed)
            message = await client.wait_for('message', check=check, timeout = 30)
            if message.content.lower() == 'cancel':
                embed = discord.Embed(description = f"{ctx.author.name} has ended the trivia match. They got {score} out of {m + 1} correct before stopping.", color = discord.Color.red())
                return await ctx.send(embed = embed)
            if message.content.lower() == answer.lower():
                embed = discord.Embed(description = f"{ctx.author.mention}, that was correct!\n\nNext question in 5 seconds...",color = discord.Color.green())
                embed.set_author(name=f"{ctx.author.name}'s correct answer", icon_url = ctx.author.avatar_url)
                score += 1
                await ctx.send(embed=embed)
                await asyncio.sleep(1)
            elif message.content.lower() not in (z.lower() for z in choicearr):
                embed = discord.Embed(
                    description=f"{ctx.author.mention}, `{message.content}` was not an option!\n\nNext question in 5 seconds...",
                    color=discord.Color.red())
                embed.set_author(name=f"{ctx.author.name}'s confused answer", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f"{ctx.author.mention}, sorry but your answer was incorrect. The correct answer was **{answer}**.\n\nNext question in 5 seconds...",
                                      color=discord.Color.red())
                embed.set_author(name=f"{ctx.author.name}'s incorrect answer", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                await asyncio.sleep(5)

        desc = f"Wow {ctx.author.mention}, you were able to get **{score}** out of {quesnum} questions correct!"
        embed = discord.Embed(description = desc, color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
        embed.set_author(name=f"{ctx.author.name}'s trivia results", icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text=f"Trivia Test completed by: {ctx.author.name}")
        return await ctx.send(embed = embed)
    except asyncio.TimeoutError:
        return await ctx.reply("This match has timed out.")



# @typing.command()
# async def topwpm(ctx, member: discord.Member = None, num=5):
#     if member is None:
#         member = ctx.author
#     db = sqlite3.connect('main.sqlite')
#     name = f"GUILD{ctx.guild.id}"
#     cursor = db.cursor()
#     cursor.execute(
#         f"""
#         SELECT wpm
#         FROM typingtest
#         WHERE user_id = {member.id}
#         """
#     )
#     result = cursor.fetchall()
#     topwpm = []
#     for k in result:
#         topwpm.append(str(k[0]))

#     if len(topwpm) == 0:
#         await ctx.send(f"{member.mention} doesn't have any typing tests saved!")
#         return

#     x = sorted(topwpm, reverse=True)
#     print(x)
#     index = 1
#     embed = discord.Embed(title=f"Top {num} WPM all-time for {member.name}", color=discord.Color.green(), timestamp = datetime.datetime.utcnow())
#     embed.set_thumbnail(url=member.avatar_url)

#     for i, amt in enumerate(x):
#         if i > (num - 1):
#             break

#             # add date too
#         embed.add_field(name=f"{i + 1}.", value=f"{x[i]} WPM", inline=False)
#         print(0)

#     await ctx.send(embed=embed)
#     # y = " \n".join(x)
#     # await ctx.send(y)


# # print(result)

@typing.command(aliases=['stwpm', 'stopwpm'])
async def highscore(ctx):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['typing']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        topwpm = i['wpm']
        uid = i['uid']
        date = i['date']
    if topwpm == '':
        await ctx.send(
            f"{ctx.author.mention}, it looks like no one in **{ctx.guild.name}** has completed a typing test with InfiniBot.")
        return
    uid = int(uid)

    # x = sorted(topwpm, reverse=True)
    # print(x)
    # index = 1
    # embed = discord.Embed(title=f"Top 10 WPM all-time for {ctx.guild.name}", color=discord.Color.green(), timestamp = datetime.datetime.utcnow())
    # embed.set_thumbnail(url=ctx.guild.icon_url)
    # embed.set_footer(text="Typing Test | Server Statistics")
    # for i, amt in enumerate(x):
    #     if i > (11):
    #         break
    #         # add date too
    #     user = client.get_user(int(x[i][1]))
    #     embed.add_field(name=f"{i + 1}. {user.name}", value=f"{x[i][0]} WPM", inline=False)
    #     print(0)
    # embed.set_thumbnail(url=ctx.guild.avatar_url)
    topuser = client.get_user(uid)
    print(topuser)
    topdate = pd.to_datetime(date)
    await ctx.send(content=f"The highest WPM recorded in {ctx.guild.name} is {topwpm} WPM by {topuser.mention} on {topdate.strftime('%D')}!!!")


# @typing.command(aliases=['serverinfo'])
# async def servertopstats(ctx):
#     db = sqlite3.connect('main.sqlite')
#     cursor = db.cursor()
#     cursor.execute(
#         f"""
#                 SELECT wpm, user_id
#                 FROM typingtest
#                 WHERE guild_id = {ctx.guild.id}
#                 """
#     )
#     result = cursor.fetchmany(5)
#     cursor.execute(
#         f"""
#                     SELECT accuracy, user_id
#                     FROM typingtest
#                     WHERE guild_id = {ctx.guild.id}
#                     """
#     )
#     result1 = cursor.fetchmany(5)
#     print(result1)
#     topwpm = []
#     topacc = []
#     for k in result:
#         topwpm.append((k))

#     for i in result1:
#         topacc.append(i)

#     if len(topwpm) == 0 or len(topacc) == 0:
#         await ctx.send(
#             f"{ctx.author.mention}, it looks like no one in **{ctx.guild.name}** has completed a typing test with InfiniBot.")
#         return

#     x = sorted(topwpm, reverse=True)
#     y = sorted(topacc, reverse=True)
#     embed = discord.Embed(title=f"Top Server Stats for {ctx.guild.name}", color=discord.Color.green(), timestamp = datetime.datetime.utcnow())
#     embed.set_thumbnail(url=ctx.guild.icon_url)
#     embed.set_footer(text="Typing Test | Server Statistics")
#     for i, amt in enumerate(x):
#         if i >= 1:
#             break
#             # add date too
#         user = client.get_user(int(x[i][1]))
#         embed.add_field(name=f"Top WPM: {user.name}", value=f"{x[i][0]} WPM", inline=False)

#     print('hi')
#     for i, amt in enumerate(y):
#         if i >= 1:
#             break
#             # add date too
#         user = client.get_user(int(y[i][1]))
#         embed.add_field(name=f"Top Accuracy: {user.name}", value=f"{y[i][0]}% accuracy", inline=False)

#     await ctx.send(embed=embed)


@client.command(aliases=['deleterole'])
async def delrole(ctx, role: discord.Role = None):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if role is None:
        desc = f"```{prefix}delrole [role]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)

    if ctx.author.top_role >= role:
        try:
            await role.delete()
            await ctx.send(f"**{role.name}** has been deleted.")
            return
        except discord.Forbidden:
            await ctx.reply(f"I am missing permissions to delete {role.mention}.")
            return
    await ctx.reply(f"{ctx.author.mention}, you can't use that.")


@client.group(invoke_without_command=True)
async def afk(ctx, *, message="Away"):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['afk']
    cnick = ctx.author.display_name
    member = ctx.author
    ping_cm = {
        "_id": ctx.author.id,
        "name": ctx.author.name,
        "display_name": cnick,
        "member": ctx.author.name,
        'start': time.time(),
        'status': message
    }
    x = collection.insert_one(ping_cm)
    desc = f"Your afk status has been successfully updated to: ```{message}```"
    embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp = datetime.datetime.utcnow())
    embed.set_author(name=f"{ctx.author.name} is now afk", icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text="The AFK setting has been saved.")
    await ctx.send(embed=embed)

    try:
        await member.edit(nick = f"[AFK] {cnick}")
    except discord.Forbidden:
        pass


@afk.command()
@commands.has_permissions(manage_guild = True)
async def clear(ctx, member: discord.Member = None):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if member is None:
        desc = f"```{prefix}afk clear [member]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    if ctx.author.guild_permissions.manage_messages:
        collection = db['afk']
        query = {'_id': member.id}
        if collection.count_documents(query) == 0:
            return await ctx.send(f"{member.mention} hasn't set an AFK status in {ctx.guild.name}.")
        else:
            results = collection.find({'_id': member.id})
            for i in results:
                nick = i['display_name']
            collection.delete_one({'_id':member.id})
            try:
                await member.edit(nick=nick)
            except discord.Forbidden:
                pass
            finally:
                await ctx.send(f"AFK status for {member.mention} has been removed.")
    else:
        await ctx.send(f"{ctx.author.mention}, you don't have permission.")


@afk.command()
@commands.has_permissions(manage_guild = True)
@commands.cooldown(1, 300, commands.BucketType.guild)
async def clearall(ctx):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['afk']
    db.drop_collection(collection)
    collection = db['afk']
    ping_cm = {
        "_id": ctx.guild.id,
        "name": ctx.guild.name,
        'afkstatus': "",
        'startafk': '',
        'preafknick': '',
        'afkid': ''
    }
    x = collection.insert_one(ping_cm)
    return await ctx.send(f"All afk statuses for {ctx.guild.name} have been cleared.")

# @afk.command()
# @commands.has_guild_permissions(manage_guild = True)
# async def list(ctx):
#     name = f"GUILD{ctx.guild.id}"
#     db = cluster[name]
#     collection = db['config']
#     if len(result) == 0:
#         await ctx.send(f"It looks like nobody in **{ctx.guild.name}** have set an AFK status.")
#         return
#     print(result)
#     embed = discord.Embed(title=f"AFK Statuses", color = discord.Color.greyple())
#     embed.set_thumbnail(url=ctx.guild.icon_url)
#     embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
#     counter = 0
#     for i, k in enumerate(result):
#         if counter >= 10:
#             embed.set_footer(text = f"There are more results, but only ten are visible due to Discord limitations. Just mention them if you wish to see.")
#             break
#         user = client.get_user(int(result[i][0]))
#         embed.add_field(name = str(user), value = f"```{result[i][1]}```", inline = False)
#         counter += 1
#     await ctx.send(embed = embed)


@client.command()
async def serverstats(ctx):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['messages']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        msgcount = i['count']
    if msgcount == '':
        msgcount = 0
    collection = db['serverstats']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        vcsecs = i['vcsecs']
    if vcsecs == '':
        vcsecs = 0

    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        ghostcount = i['ghostcount']
    if ghostcount == '':
        ghostcount = 0
    x = ctx.guild.created_at
    y = x.strftime("%b %d %Y %H:%S")
    print(y)
    z = datetime.datetime.utcnow() - x
    lm = str(abs(z))
    print(lm)
    q = lm.split(", ")
    a = q[0]
    desc = f"This is only from when I joined **{ctx.guild.name}**. Anything before that has not been documented."
    embed = discord.Embed(description = desc, color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
    embed.add_field(name="Channels:", value = f"```{str(len(ctx.guild.channels))}```", inline = True)
    embed.add_field(name="Users:", value=f"```{ctx.guild.member_count}```", inline = True)
    embed.add_field(name="Messages Sent:", value = f"```{msgcount}```", inline = True)
    # embed.add_field(name=f"In #{ctx.channel.name}:", value = f"```{smsgcfount}```", inline = True)
    # embed.add_field(name=f"By {ctx.author.name}:", value = f"```{smsgcount}```", inline = True)
    # embed.add_field(name=f"In #{ctx.channel.name} by {ctx.author.name}:", value=f"```{result3[0]}```", inline = False)
    embed.add_field(name="Seconds in Voice Channels", value = f"```{vcsecs}```", inline = True)
    embed.add_field(name=f"Server Creation Date:", value = f"```{f'{y} ({a} ago)' if lm[0:6] != '1 day,' else 'Today'}```", inline = True)
    # embed.add_field(name=f"Most active text channel in **{ctx.guild.name}**: ", value = f"```#{topchannel.name} with {smsgcffount} messages.```", inline = False)
    #figure out most active VC
    ownerser = client.get_user(ctx.guild.owner_id)
    embed.add_field(name=f"Number of Ghost Pings", value=f"```{ghostcount}```", inline = False)
    embed.add_field(name="Server Owner:", value = ownerser.mention, inline = False)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_author(name=f"{ctx.guild.name}'s Statistics", icon_url = ctx.guild.icon_url)
    embed.set_footer(text=f"Server ID: {ctx.guild.id}")
    await ctx.send(embed=embed)
    #add graphs https://www.tutorialspoint.com/graph-plotting-in-python


#user specific stats next


@client.command(aliases = ['passwordgen', 'passgen', 'passwordgenerate'])
#add to help menu
@commands.cooldown(2, 15, commands.BucketType.user)
async def passwordgenerator(ctx, lent = 10):
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation
    if lent > 20:
        await ctx.send(f"Since your specified value was greater than 20 characters, we are shortening it to 20.")
    combined = lower + upper + num + symbols
    temp=random.sample(combined, lent)
    channel = ctx.channel
    desc = f'{"".join(temp)}'
    desc2 = f"\nYou requested this in {channel.mention} in the server **{ctx.guild.name}**"
    await ctx.message.add_reaction('✅')
    embed = discord.Embed(description = f"```{desc}```{desc2}", color = discord.Color.green())
    embed.set_author(name=f"{ctx.author.name}'s randomly generated password", icon_url = ctx.author.avatar_url)
    embed.set_footer(text="InfiniBot Password Generator")
    await ctx.author.send(embed = embed)

@client.command()
async def asciitext(ctx, *, text="Next time put text you want converted lol"):
    if len(text) > 2000:
        await ctx.send("Your message was too long!")
        return
    result = pyfiglet.figlet_format(f"{text}")
    await ctx.send(f"```{result}```")


@client.command()
#helpmenu addition !!!
async def servericon(ctx):
    embed = discord.Embed(color = discord.Color.green())
    embed.set_author(name=ctx.author.name, icon_url = ctx.author.avatar_url)
    embed.set_image(url=ctx.icon_url)
    embed.set_footer(text=f"{ctx.name} Server Icon | Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@client.command()
async def emojify(ctx, *, text):
    if len(text) > 2000:
        await ctx.send("Keep your message under 2000 characters.")
        return
    try:
        new = []
        for i in str(text):
            if i == " ":
                new.append("         ")
                continue
            if not i.isalpha():
                continue
            else:
                new.append(f":regional_indicator_{i.lower()}:")
                continue

        await ctx.send("".join(new))
    except:
        await ctx.send("Something went wrong, next time make sure to use only letters.")

@emojify.error
async def emojify_err(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}emojify [text]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)


@client.command()
async def urban(ctx, *, text):
    with open('urbanapi.txt', 'r') as f:
        apikey = f.read()
    try:
        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        querystring = {"term": text.strip()}
        headers = {
            'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
            'x-rapidapi-key': apikey
            }
        async with ClientSession() as session:
            async with session.get(url, headers=headers, params=querystring) as response:
                r = await response.json()
                definition = r['list'][0]['definition']
                desc = str(definition)
                if r['list'][0]['example'] == "":
                    r['list'][0]['example'] = "..."
                embed = discord.Embed(title=f"Urban Dictionary Definition of {text}", url = r['list'][0]['permalink'], description = desc, color = discord.Color.green())
                embed.add_field(name="Example Sentence:", value = r['list'][0]['example'], inline = False)
                embed.add_field(name="👍🏽", value = r['list'][0]['thumbs_up'])
                embed.add_field(name="👎🏽", value=r['list'][0]['thumbs_down'])
                embed.set_footer(text=f"Author: {r['list'][0]['author']} on {r['list'][0]['written_on'][0:10]}")
                embed.set_thumbnail(url=ctx.guild.icon_url)
                await ctx.send(embed=embed)
    except IndexError:
        return await ctx.send(f"Error! The search term **{text}** could not be found.")


@urban.error
async def urban_error(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}urban [term]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)



@client.command(aliases=['truemc', 'truemembercount'])
async def tmc(ctx):
    true_member_count = len([m for m in ctx.guild.members if not m.bot])
    return await ctx.send(f"There are {true_member_count} humans in the server **{ctx.guild.name}**")


# @client.command(aliases = ['level', "xp"])
# async def XP(ctx, member: discord.Member = None):
#     if member is None:
#         member = ctx.author
#     db = sqlite3.connect('main.sqlite')
#     cursor = db.cursor()
#     name = f"GUILD{ctx.guild.id}"
#     cursor.execute(f"SELECT XP from {name} WHERE user_id = {member.id} AND XP IS NOT NULL")
#     result = cursor.fetchall()
#     if result is None:
#         await ctx.send(f"**{member.name}** has not sent any messages in **{ctx.guild.name}**")
#         return
#     countr = 0
#     for i in result:
#         countr += int(i[0])
#     await ctx.send(f"**{member.name}** has {countr} XP in the server **{ctx.guild.name}**.")

@client.command(aliases = ['xplb', 'xpleaderboard'])
@commands.cooldown(1, 30, commands.BucketType.user)
async def levels(ctx):
    return await ctx.send("Discontinued command, will be supported when we move to the dashboard.")
    #link to dashboard
    # await ctx.trigger_typing()
    # db = sqlite3.connect('main.sqlite')
    # cursor = db.cursor()
    # name = f"GUILD{ctx.guild.id}"
    # cursor.execute(f"SELECT XP, user_id from {name} WHERE XP IS NOT NULL AND user_id IS NOT NULL")
    # result = cursor.fetchall()
    # if result is None:
    #     await ctx.send("Something went wrong. Try again later.")
    #     return
    # x = sorted(result, reverse=True)
    # cursor.execute(f"SELECT prefix from main WHERE guild_id = {ctx.guild.id}")
    # result = cursor.fetchone()
    # if str(result[0]) == "None":
    #     result = ("%", "Hi")
    # embed = discord.Embed(color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
    # embed.set_author(name=f"Most Active Members in {ctx.guild.name}", icon_url=ctx.guild.icon_url)
    # embed.set_thumbnail(url=ctx.guild.icon_url)
    # embed.set_footer(text=f"If you aren't in this list, use the {result[0]}xp command to see your xp.")
    # count = 1

    # for i in x:
    #     if count == 11:
    #         break
    #     else:
    #         print(count)
    #         try:
    #             person = client.get_user(i[1])
    #             embed.add_field(name=f"{count}. {person}", value=f"{i[0]} XP", inline=False)
    #             count += 1
    #         except:
    #             continue


    # await ctx.send(embed=embed)

@client.command()
#add to help menu
async def ghostpings(ctx, member: discord.Member = None):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        ghostcount = i['ghostcount']
    # if member is not None:
    #     cursor.execute(f"SELECT ghostcount from {name} WHERE user_id = {member.id} AND ghostcount IS NOT NULL")
    #     result = cursor.fetchall()
    #     if len(result) == 0:
    #         return await ctx.send(f"Looks like **{member.name}** has not ghost pinged in **{ctx.guild.name}** since I was added!")
    #     else:
    #         countr = 0
    #         for i in result:
    #             countr += int(i[0])
    #     return await ctx.send(f"**{member.name}** has ghost pinged {countr} time{'' if countr == 1 else 's'} in **{ctx.guild.name}**.")
    if ghostcount == '':
        return await ctx.send(f"Looks like **{ctx.guild.name}** has been free of ghost pings since I was added!")
    else:
        await ctx.send(f"There {'was' if int(ghostcount) == 1 else 'were'} {ghostcount} ghost ping{'' if int(ghostcount) == 1 else 's'} in **{ctx.guild.name}** since I have joined.")


@client.command()
@commands.has_permissions(manage_guild = True)
async def warn(ctx, member: discord.Member, *, reason = "No reason given."):
    if member.id == ctx.author.id:
        return await ctx.send("You cannot warn yourself.")
    if ctx.author.top_role <= member.top_role:
        if ctx.author.id == ctx.guild.owner_id:
            pass
        else:
            return await ctx.send("You can only use this moderation on a member below you.")
    if member.id == ctx.guild.owner_id:
        return await ctx.send("You cannot take any action on the server owner.")
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['warns']
    ping_cm = {
        "name": member.name,
        'guild': ctx.guild.id,
        "reason": reason.strip(),
        "time": datetime.datetime.now().strftime('%D'),
        'mod': ctx.author.id,
        'offender': member.id
    }
    collection.insert_one(ping_cm)
    query = {'offender': member.id}
    x = collection.count_documents(query)
    desc = f"For reason: ```{reason}```"
    embed = discord.Embed(description = desc, color = discord.Color.red(), timestamp = datetime.datetime.utcnow())
    embed.set_author(name=f"{member.name} has been warned", icon_url = member.avatar_url)
    embed.set_footer(text=f"Warning number {x} for {member.name}")
    uembed = discord.Embed(description = desc, color = discord.Color.red())
    uembed.set_author(name=f"You have been warned in the server **{ctx.guild.name}**", icon_url = ctx.guild.icon_url)
    uembed.set_footer(text="If you believe this is an error, please contact an Admin.")
    await ctx.send(embed=embed)
    await member.send(embed=uembed)

@warn.error
async def warn_err(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}warn [member] (reason)```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)

    if isinstance(error, commands.MissingPermissions):
        return await ctx.send(f"You cannot use this!")

@client.command()
@commands.has_permissions(manage_guild = True)
async def warns(ctx, member: discord.Member = None):
    await ctx.trigger_typing()
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if member is None:
        if ctx.author.guild_permissions.manage_roles:
            if member is None:
                collection = db['warns']
                query = {'guild':ctx.guild.id}
                if collection.count_documents(query) == 0:
                    return await ctx.send(f"There have been no documented warns in **{ctx.guild.name}**.")
                else:
                    results = collection.find(query)
                embed = discord.Embed(color=discord.Color.green())
                embed.set_author(name=f"{ctx.guild.name}'s warns", icon_url=ctx.guild.icon_url)
                embed.set_thumbnail(url=ctx.guild.icon_url)
                embed.set_footer(text=f"I cannot send all of the warn cases due to Discord limitations. use `{prefix}warns <@user>` to see warns for a specific user.")
                countr = 0
                for i in results:
                    if countr >= 10:
                        break
                    mod = client.get_user(int(i['mod']))
                    mem = client.get_user(int(i['offender']))
                    embed.add_field(name=f"Warn case #{countr + 1}:",
                                    value=f"Responsible Moderator: **{mod.mention}**\n\nOffender: {mem.mention}\n\nTime: {i['time']} \n\n Reason:```{i['reason']}```")
                    countr += 1
                return await ctx.send(embed=embed)
    collection = db['warns']
    query = {'offender': member.id}
    if collection.count_documents(query) == 0:
        return await ctx.send(f"**{member.mention}** does not have any warns in **{ctx.guild.name}**")
    else:
        results = collection.find(query)
    embed = discord.Embed(color = discord.Color.green())
    embed.set_author(name=f"{member.name}'s warns", icon_url = member.avatar_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    countr = 0
    for i in results:
        if countr >= 15:
            break
        mod = client.get_user(int(i['mod']))
        embed.add_field(name = f"Warn case #{countr + 1}:", value = f"Responsible Moderator: **{mod.mention}**\n\nTime: {i['time']} \n\n Reason:```{i['reason']}```")
        countr += 1
    await ctx.send(embed = embed)

@client.command()
#add to help menu
async def tcc(ctx):
    counter = 0
    for i in ctx.guild.text_channels:
        counter +=1
    return await ctx.send(f"There are {counter} text channels in **{ctx.guild.name}**.")

@client.command()
#add to help menu
async def vcc(ctx):
    counter = 0
    for i in ctx.guild.voice_channels:
        counter +=1
    return await ctx.send(f"There are {counter} voice channels in **{ctx.guild.name}**.")

@client.command(aliases=['mcip'])
async def ip(ctx):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        ip = i['mcip']
    if ip == '':
        return await ctx.send(f"{ctx.guild.name} has not set a Minecraft IP.")
    await ctx.send(str(ip))

@client.command(aliases=['makeupper'])
#help manu
async def makeuppercase(ctx, *, text):
    await ctx.reply(f"{text.strip().upper()}", mention_author = False)

@makeuppercase.error
async def makeuppercase_err(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}makeupper [text]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)



@client.command(aliases=['makelower'])
async def makelowercase(ctx, *, text):
    await ctx.reply(f"{text.lower()}", mention_author = False)

@makelowercase.error
async def makelow_err(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}makelower [text]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)



@client.command(aliases=['makepropercase'])
async def makeproper(ctx, *, text):
    await ctx.reply(f"{text.strip().capitalize()}", mention_author = False)

@makeproper.error
async def prper_err(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}makeproper [text]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)

@client.command()
async def botinfo(ctx):
    db = cluster['COMMANDCOUNT']
    collection = db['commandcount']
    results = collection.find({'_id' : client.user.id})
    for i in results:
        countr = i['count']
    cpusage = psutil.cpu_percent()
    RAMuse = psutil.virtual_memory().percent
    embed = discord.Embed(color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
    embed.add_field(name="Version:", value = f"```{botversion}```")
    embed.add_field(name="Python Version: ", value = "```3.9.5```")
    embed.set_footer(text="Developed by glizzybeam7801#8196 and kidsonfilms#4635")
    embed.add_field(name="Commands run:", value = f"```{countr + 1}```", inline = False)
    embed.add_field(name="Servers:", value = f"```{len(client.guilds)}```")
    embed.add_field(name="CPU Usage:", value = f"```{cpusage}%```", inline = False)
    embed.add_field(name="RAM Usage:", value=f"```{RAMuse}%```")
    embed.add_field(name="Client Latency:", value = f"```{round(client.latency * 1000)}ms```", inline = False)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.set_author(name=f"InfiniBot Statistics", icon_url = client.user.avatar_url)
    await ctx.send(embed=embed)

@client.command(aliases = ['mimick'])
@commands.cooldown(1, 180, commands.BucketType.user)
async def mimic(ctx, member: discord.Member = None, *, text = "Hi"):
    if member is None:
        member = ctx.author
    webhook = await ctx.channel.create_webhook(name=member.name)
    await webhook.send(text, username = member.display_name, avatar_url = member.avatar_url)
    await webhook.delete()

@client.command()
async def clap(ctx, *, text):
    arr = []
    for i in text:
        if i == " ":
            arr.append("    ")
        else:
            arr.append(i)

    x = ":clap:".join(arr)
    await ctx.send(x)

@clap.error
async def clap_error(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}clap [text]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)


@client.command(aliases = ['tinyurl'])
@commands.cooldown(1, 60, commands.BucketType.user)
async def urlshorten(ctx, url):
    try:
        x = url_shortener.tinyurl.short(url)
        return await ctx.send(x)
    except Exception as e:
        print(e)
        return await ctx.send("Something went wrong. Make sure after the command invocation you are only putting the URL link.")

@urlshorten.error
async def url_error(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}tinyurl [url]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)


@client.command(aliases = ['fakeconvo'])
@commands.cooldown(1, 900, commands.BucketType.guild)
async def pos(ctx):
    #delete b4 verification!!!
    memlist = []
    for m in ctx.guild.members:
        memlist.append(m)

    words = ['Hey what\'s up?', 'I\'m gonna go eat dinner now guys', 'Guys that test in aphug was super hard. I\'m glad I studied!!!!',
             'Guys want to go biking sometime soon?', 'Wassup guys', 'Guys get on vc lets talk', 'Hi everyone! I just had dinner.',
             'I just came back from Disney World!!!', 'Finally this COVID is done', 'Let\'s go to Russell Ranch to play basketball',
             'OMG that new BLACKPINK song was so good!!', 'Hi wassup?', 'I like to read']

    randnum = random.choice(memlist)
    x = client.get_user(randnum.id)
    webhook = await ctx.channel.create_webhook(name=x.name)

    for i in range(0, 25):
        x = client.get_user(randnum.id)
        randnum = random.choice(memlist)
        y = random.choice(words)
        await webhook.send(y, username = x.display_name, avatar_url = x.avatar_url)
        await asyncio.sleep(2)

    await webhook.delete()

# @client.command(aliases=['msgs'])
# @commands.cooldown(1, 20, commands.BucketType.user)
'''DEPRECATED COMMAND, FIX IT AFTER DB MIGRATION!'''
# async def messages(ctx, member: discord.Member = None):
#     if member is None:
#         member = ctx.author
#     db = sqlite3.connect('main.sqlite')
#     cursor = db.cursor()
#     name = f"GUILD{ctx.guild.id}"
#     cursor.execute(f"SELECT msgcount from {name} WHERE user_id = {ctx.guild.id} AND msgcount IS NOT NULL")
#     result = cursor.fetchall()
#     count = 0
#     for k in result:
#         count += int(k[0])
#
#     if result is None:
#         return await ctx.send(f"{member.name} has not sent any messages in **{ctx.guild.name}**!!")
#     elif str(result[0]) == 'None':
#         return await ctx.send(f"{member.name} has not sent any messages in **{ctx.guild.name}**!!")
#     desc = f"**{member.name}** has sent {count} {'message' if count == 1 else 'messages'} in **{ctx.guild.name}**!"
#     embed = discord.Embed(description = desc, color = discord.Color.blurple(), timestamp = datetime.datetime.utcnow())
#     embed.set_author(name=member.name, icon_url = member.avatar_url)
#     embed.set_thumbnail(url=ctx.guild.icon_url)
#     await ctx.send(embed = embed)

@client.group(invoke_without_command = True)
async def fm(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    await ctx.trigger_typing()
    db = cluster['LASTFM']
    collection = db['usernames']
    query = {"_id": member.id}
    if collection.count_documents(query) == 0:
        return await ctx.send(f"**{member.name}** has not set their Last FM profile with InfiniBot!")
    else:
        user = collection.find(query)
        for result in user:
            username = result['username']
    with open('lfapi.txt', 'r') as f:
        key = f.read()
    params = {
        'user': f'{username}',
        'api_key': key,
        'method': 'user.getrecenttracks',
        'format': 'json',
        'limit': 1
    }
    async with aiohttp.ClientSession() as session:
        url = 'https://ws.audioscrobbler.com/2.0/'
        async with session.get(url, params=params) as response:
            data = await response.json()
    x = (data['recenttracks']['track'])
    if not x:
        return await ctx.send(f"**{member.name}** has not listened to any tracks!")

    username = data['recenttracks']['@attr']['user']
    track = x[0]['name']
    trackurl = x[0]['url']
    album = x[0]['album']['#text']
    artist = x[0]['artist']['#text']
    thumbnail = x[0]['image'][-1]['#text']
    try:
        timestamp = x[0]['date']['#text']
        z = pd.to_datetime(timestamp)
        desc = f"{f'[{track}]({trackurl})'} \n**{artist}** | *{album}*"
        embed = discord.Embed(description = desc, color = discord.Color.green(), timestamp = z)
        embed.set_author(name=f"{username}'s last track:", icon_url=member.avatar_url)
        embed.set_thumbnail(url = str(thumbnail))
        embed.set_footer(text=f"{member.name} has {data['recenttracks']['@attr']['total']} total scrobbles | Last scrobble: ")
    except KeyError:
        z = datetime.datetime.utcnow()
        desc = f"{f'[{track}]({trackurl})'} \n**{artist}** | *{album}*"
        embed = discord.Embed(description = desc, color = discord.Color.green(), timestamp = z)
        embed.set_author(name=f"{username}'s currently playing track:", icon_url=member.avatar_url)
        embed.set_thumbnail(url = str(thumbnail))
        embed.set_footer(text=f"{member.name} has {data['recenttracks']['@attr']['total']} total scrobbles")
    message = await ctx.send(embed=embed)
    await message.add_reaction("👍🏽")
    await message.add_reaction("👎🏽")
    # text = json.dumps(r.json(), sort_keys=True, indent = 4)
    # #print(text)

@fm.command()
async def set(ctx, username):
    db = cluster['LASTFM']
    collection = db['usernames']
    query = {"_id": ctx.author.id}
    with open('lfapi.txt', 'r') as f:
        key = f.read()
    if collection.count_documents(query) == 0:
        params = {
            'user': f'{username.strip()}',
            'api_key': key,
            'method': 'user.getinfo',
            'format': 'json',
            'limit': 1
        }
        async with aiohttp.ClientSession() as session:
            url = 'https://ws.audioscrobbler.com/2.0/'
            async with session.get(url, params=params) as response:
                data = await response.json()
                try:
                    if data['error'] == 6:
                        desc = f"❌ User `{username.strip()}` was not found in the Last FM database."
                        embed = discord.Embed(description=desc, color=discord.Color.red(),
                                              timestamp=datetime.datetime.utcnow())
                        return await ctx.send(embed=embed)
                except Exception as e:
                    print(e)
                    pass
        ping_cm = {
            "_id": ctx.author.id,
            "username": username.strip()
        }
        try:
            x = collection.insert_one(ping_cm)
        except Exception:
            return
        imgurl = (data['user']['image'][-1]['#text'])
        desc = f"Success! Your Last FM username has been set as `{username}`!"
        embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=imgurl)
        embed.set_author(name=f"Your profile has been saved!", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        params = {
            'user': f'{username.strip()}',
            'api_key': key,
            'method': 'user.getinfo',
            'format': 'json',
            'limit': 1
        }
        async with aiohttp.ClientSession() as session:
            url = 'https://ws.audioscrobbler.com/2.0/'
            async with session.get(url, params=params) as response:
                data = await response.json()
                print(data)
                try:
                    if data['error'] == 6:
                        desc = f"❌ User `{username}` was not found in the Last FM database."
                        embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp = datetime.datetime.utcnow())
                        return await ctx.send(embed=embed)
                except Exception as e:
                    print(e)
                    pass
        collection.update_one({"_id": ctx.author.id}, {"$set": {'username': username}})
        imgurl = (data['user']['image'][-1]['#text'])
        desc = f"Success! Your Last FM username has been updated to `{username}`!"
        embed = discord.Embed(description = desc, color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
        embed.set_thumbnail(url=imgurl)
        embed.set_author(name=f"Your profile has been saved!", icon_url = ctx.author.avatar_url)
        await ctx.send(embed=embed)

@set.error
async def set_error(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}fm set [username]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)


@fm.command(aliases = ['remove'])
async def unset(ctx):
    db = cluster['LASTFM']
    collection = db['usernames']
    query = {'_id' : ctx.author.id}
    if collection.count_documents(query) == 0:
        return await ctx.send("You haven't set your LASTFM profile with InfiniBot!")
    collection.delete_one({'_id' : ctx.author.id})
    desc = f"You have removed your Last FM username from InfiniBot."
    embed = discord.Embed(description = desc, color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
    await ctx.send(embed = embed)


@fm.command(aliases = ['ta'])
async def topartists(ctx, member: discord.Member = None):
    #add a time period param
    await ctx.trigger_typing()
    if member is None:
        member = ctx.author
    db = cluster['LASTFM']
    collection = db['usernames']
    query = {"_id": member.id}
    if collection.count_documents(query) == 0:
        return await ctx.send(f"**{member.name}** has not set their Last FM profile with InfiniBot!")
    user = collection.find(query)
    for result in user:
        username = result['username']
    with open('lfapi.txt', 'r') as f:
        key = f.read()
    params = {
        'user': f'{username}',
        'api_key': key,
        'method': 'user.gettopartists',
        'format': 'json',
        'limit': 10,
        'period': '12month'
    }
    async with aiohttp.ClientSession() as session:
        url = 'https://ws.audioscrobbler.com/2.0/'
        async with session.get(url, params=params) as response:
            data = await response.json()
    counter = 0

    descarr = []
    for i in range (0, 10):
        descarr.append(f"{counter + 1}. {data['topartists']['artist'][counter]['name']} - {data['topartists']['artist'][counter]['playcount']} plays")
        counter +=1

    x = "\n".join(descarr)
    #img = data['topartists']['artist'][0]['image'][-1]['#text']
    embed = discord.Embed(description = x, color=discord.Color.green())
    embed.set_author(name=f"{member.name}'s top 10 yearly artists", icon_url = member.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@fm.command(aliases=['tt'])
async def toptracks(ctx, member: discord.Member = None):
    # add a time period param
    await ctx.trigger_typing()
    if member is None:
        member = ctx.author
    db = cluster['LASTFM']
    collection = db['usernames']
    query = {"_id": member.id}
    if collection.count_documents(query) == 0:
        return await ctx.send(f"**{member.name}** has not set their Last FM profile with InfiniBot!")
    user = collection.find(query)
    for result in user:
        username = result['username']
    with open('lfapi.txt', 'r') as f:
        key = f.read()
    params = {
        'user': f'{username}',
        'api_key': key,
        'method': 'user.gettoptracks',
        'format': 'json',
        'limit': 10,
        'period': '12month'
    }
    async with aiohttp.ClientSession() as session:
        url = 'https://ws.audioscrobbler.com/2.0/'
        async with session.get(url, params=params) as response:
            data = await response.json()
    counter = 0

    descarr = []
    for i in range(0, 10):
        descarr.append(
            f"{counter + 1}. {data['toptracks']['track'][counter]['name']} - {data['toptracks']['track'][counter]['artist']['name']} - **{data['toptracks']['track'][counter]['playcount']} plays**")
        counter += 1

    x = "\n".join(descarr)
    # img = data['topartists']['artist'][0]['image'][-1]['#text']
    embed = discord.Embed(description=x, color=discord.Color.green())
    embed.set_author(name=f"{member.name}'s top 10 yearly tracks", icon_url=member.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@fm.command(aliases=['talb', 'topalb'])
async def topalbums(ctx, member: discord.Member = None):
    # add a time period paramom {name} WHERE user_id = {ctx.guild.id}")
    await ctx.trigger_typing()
    if member is None:
        member = ctx.author
    db = cluster['LASTFM']
    collection = db['usernames']
    query = {"_id": member.id}
    if collection.count_documents(query) == 0:
        return await ctx.send(f"**{member.name}** has not set their Last FM profile with InfiniBot!")
    user = collection.find(query)
    for result in user:
        username = result['username']
    with open('lfapi.txt', 'r') as f:
        key = f.read()
    params = {
        'user': f'{username}',
        'api_key': key,
        'method': 'user.gettopalbums',
        'format': 'json',
        'limit': 10,
        'period': '12month'
    }
    async with aiohttp.ClientSession() as session:
        url = 'https://ws.audioscrobbler.com/2.0/'
        async with session.get(url, params=params) as response:
            data = await response.json()
    counter = 0

    descarr = []
    for i in range(0, 10):
        descarr.append(
            f"{counter + 1}. {data['topalbums']['album'][counter]['name']} - **{data['topalbums']['album'][counter]['artist']['name']}** - {data['topalbums']['album'][counter]['playcount']} plays")
        counter += 1

    x = "\n".join(descarr)
    # img = data['topartists']['artist'][0]['image'][-1]['#text']
    embed = discord.Embed(description=x, color=discord.Color.green())
    embed.set_author(name=f"{member.name}'s top 10 yearly albums", icon_url=member.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@fm.command(aliases=['artinfo', 'artistinfo'])
async def artist(ctx, *, name):
    with open('lfapi.txt', 'r') as f:
        key = f.read()
    params = {
        'api_key': key,
        'method': 'artist.getinfo',
        'format': 'json',
        'autocorrect': 1,
        'lang': 'eng',
        'artist': f'{name}'
    }
    async with aiohttp.ClientSession() as session:
        url = 'https://ws.audioscrobbler.com/2.0/'
        async with session.get(url, params=params) as response:
            data = await response.json()
            print(data)

    artt = data["artist"]["name"]
    artlink = data['artist']['url']
    learnmore = f"**{f'[{artt}]({artlink})'}**"
    listeners = data['artist']['stats']['listeners']
    playscount = data['artist']['stats']['playcount']
    img = data['artist']['image'][-1]['#text']
    similarart = f"[{data['artist']['similar']['artist'][0]['name']}]({data['artist']['similar']['artist'][0]['url']})"
    print(data['artist']['similar']['artist'][1]['name'])
    similarart1 = f"[{data['artist']['similar']['artist'][1]['name']}]({data['artist']['similar']['artist'][1]['url']})"
    print(similarart1)
    embed = discord.Embed(title = f"Information about {name}", color=discord.Color.green())
    embed.set_thumbnail(url=img)
    embed.add_field(name="Similar Artists:", value = f"{similarart}, \n{similarart1}")
    embed.set_footer(text=f"{listeners} listeners | {playscount} plays")
    await ctx.send(embed=embed)

@artist.error
async def art_error(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}fm artist [artist]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)

@fm.command(aliases=['cta'])
async def charttopartista(ctx):
    with open('lfapi.txt', 'r') as f:
        key = f.read()
    params = {
        'api_key': key,
        'method': 'chart.gettopartists',
        'limit': 10,
        'format': 'json',
    }
    async with aiohttp.ClientSession() as session:
        url = 'https://ws.audioscrobbler.com/2.0/'
        async with session.get(url, params=params) as response:
            data = await response.json()
            print(data)
    counter = 0

    descarr = []
    for i in range(0, 10):
        descarr.append(
            f"{counter + 1}. {data['artists']['artist'][counter]['name']} - **{data['artists']['artist'][counter]['listeners']} listeners** - {data['artists']['artist'][counter]['playcount']} plays")
        counter += 1

    x = "\n".join(descarr)
    # img = data['topartists']['artist'][0]['image'][-1]['#text']
    embed = discord.Embed(description=x, color=discord.Color.green())
    embed.set_author(name="Last FM's top 10 artists", icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@client.command()
async def pp(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    x = random.randint(0, 12)
    lent = "=" * x
    desc = f"8{lent}D"
    embed = discord.Embed(description = desc, color = discord.Color.green())
    embed.set_author(name=f"{member.name}'s pp", icon_url = member.avatar_url)
    embed.set_footer(text=f"{'' if member == ctx.author else f'Requested by: {ctx.author.name}'}")
    await ctx.send(embed = embed)

@client.command()
async def gayrate(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    x = random.randint(0, 100)
    desc = f"{member.mention} is {x}% gay"
    embed = discord.Embed(description=desc, color=discord.Color.green())
    embed.set_author(name=f"{member.name}'s gayrate", icon_url=member.avatar_url)
    embed.set_footer(text=f"{'' if member == ctx.author else f'Requested by: {ctx.author.name}'}")
    await ctx.send(embed=embed)

# @client.command()
# async def textchannelstats(ctx, channel: discord.TextChannel):
'''DEPRECATED COMMAND, FIX WHEN CREATING CLASSES/COGS'''
#     db = sqlite3.connect('main.sqlite')
#     cursor = db.cursor()
#     name = f"GUILD{ctx.guild.id}"
#     try:
#         res = await channelperms(channel)
#         if not res:
#             return await ctx.send(
#                 f"Please give me permission to `View Channel`, `Send Messages`, and `Embed Links` in {channel.mention} before proceeding.")
#         cursor.execute(f"SELECT msgcount from {name} where msgchannel_id = {channel.id} AND msgcount IS NOT NULL")
#         result = cursor.fetchall()
#         cursor.execute(f"SELECT msgcount from {name} where msgchannel_id = {channel.id} AND user_id = {ctx.author.id} AND msgcount IS NOT NULL")
#         result1 = cursor.fetchall()
#         tmc = 0
#         umc = 0
#         print(result)
#         if result is None:
#             result = (0, False)
#         else:
#             for k in result:
#                 tmc += int(k[0])
#         if result1 is None:
#             result1 = (0, False)
#         else:
#             for k in result1:
#                 umc += int(k[0])
#
#
#         x = channel.created_at
#         y = x.strftime("%b %d %Y %H:%S")
#         print(y)
#         z = datetime.datetime.utcnow() - x
#         lm = str(abs(z))
#         print(lm)
#         embed = discord.Embed(color=discord.Color.green(), timestamp = datetime.datetime.utcnow())
#         embed.set_thumbnail(url=ctx.guild.icon_url)
#         embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
#         embed.add_field(name="Channel name", value=f"```{channel.name}```")
#         embed.add_field(name="Channel ID", value=f"```{channel.id}```")
#         embed.add_field(name="Channel Topic", value=f'```{channel.topic}```', inline=False)
#         embed.add_field(name="Messages Sent", value=f"```{tmc}```")
#         embed.add_field(name=f"By {ctx.author.name}", value=f"```{umc}```")
#         if len(lm) == 14:
#             a = lm[0]
#             b = lm[2:4]
#             embed.add_field(name="Created on", value = f"```{y} (Today)```", inline = False)
#         else:
#             if lm[0:6] == '1 day,':
#                 a = lm[0:5]
#                 embed.add_field(name="Created on", value=f"```{y} ({a} ago)```", inline=False)
#             else:
#                 q = lm.split(", ")
#                 a = q[0]
#                 embed.add_field(name="Created on", value = f"```{y} ({a} ago)```", inline = False)
#             print(a)
#
#
#         #embed.add_field(name=f"Created at", value = f"```{y} ({lm})```", inline = False)
#         await ctx.send(embed=embed)
#     except Exception as e:
#         print(e)
#         return await ctx.send("Something went wrong, try again later.")

# @textchannelstats.error
# async def text_error(ctx, error):
#     db = sqlite3.connect('main.sqlite')
#     cursor = db.cursor()
#     name = f"GUILD{ctx.guild.id}"
#     cursor.execute(f"SELECT prefix from {name} WHERE user_id = {ctx.guild.id}")
#     result = cursor.fetchone()
#     if str(result[0]) == "None":
#         result = ("%", "Hi")
#     if isinstance(error, commands.MissingRequiredArgument):
#         desc = f"```{result[0]}textchannelstats [channel mention or ID]```"
#         embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
#         embed.set_footer(text="Parameters in [] are required and () are optional")
#         return await ctx.send(embed=embed)


@client.group(invoke_without_command = True)
async def youtube(ctx, *, query):
    html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={query}")
    vidid = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    await ctx.send(f"https://www.youtube.com/watch?v={vidid[0]}")

@youtube.error
async def youtube_error(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f'```{prefix}youtube [query]```'
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)

# @youtube.command()
# async def channel(ctx, *, channelname = None):
#     # if channelname is None:
#     #     return print('Incorrect usage')
#     search_channel_name = 'atgoogletalks'
#     channels_response = youtube.channels().list(
#         type = 'channel',
#         q=search_channel_name,
#         part="id, snippet, statistics, contentDetails, topicDetails"
#     ).execute()
#     print(channels_response)

    # youtube = build('youtube', 'v3', developerKey=ytapi)
    # print('bro')
    # request = youtube.channels().list(
    #     part='statistics',
    #     id=""
    # )
    # print('hi')
    # response = request.execute()
    # print(response)

#
# @client.command()
# async def hoi(ctx):
#





    #add another param to warns table
#increment a counter, so warn case 4, then 5, and so on.
#removing warns by %removewarn 4

@client.command()
@commands.guild_only()
@commands.has_permissions(manage_guild = True)
async def changeprefix(ctx, prefix):
    if len(prefix) > 10:
        return await ctx.reply(f"The prefix `{prefix}` is larger than 10 characters.", mention_author = False)
    if prefix == "":
        return await ctx.reply("You must specify a prefix!", mention_author = False)
    if prefix.startswith(" "):
        return await ctx.reply(f"The prefix `{prefix}` starts with a space. Rerun the command, and don't put a space next time.", mention_author = False)
    try:
        prefix = prefix.lstrip()
    except Exception as e:
        print(e)
        pass

    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    collection.update_one({"_id": ctx.guild.id}, {"$set": {'prefix': str(prefix)}})
    prefixz = Image.open('./Images/prefiximg.png')
    font = ImageFont.truetype('arial.ttf', 15)
    draw = ImageDraw.Draw(prefixz)
    draw.text((75,45), f"{prefix}tinyurl https://www.youtube.com/watch?v=dQw4w9WgXcQ", (255, 255, 255), font=font)
    prefixz.save('profile.png')
    desc = f"Prefix for **{ctx.guild.name}** has been updated to `{prefix}`. \n\n**NOTE:** If you want a word prefix with a space after it, you must surround it in quotes due to a Discord limitation.\n\nEXAMPLE: {prefix}changeprefix \"yo \""
    embed = discord.Embed(description = desc, color = discord.Color.green())
    embed.set_thumbnail(url = ctx.guild.icon_url)
    file = discord.File("./profile.png", filename='image.png')
    embed.set_image(url='attachment://image.png')
    await ctx.send(file=file, embed=embed)


@changeprefix.error
async def changeprefix_error(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f'```{prefix}changeprefix [prefix]```\n**NOTE: If you want a word prefix, surround the word in quotes and a space.** \nExample: {prefix}changeprefix "yo "'
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)



@client.group(aliases = ['reactionrole', 'reactionroles'], invoke_without_command = True)
async def rr(ctx):
    #help menu
    pass

# @rr.command()
# @commands.has_permissions(manage_guild = True)
# async def create(ctx):
'''DEPRECATED COMMAND, FIX WHEN CREATING COGS/CLASSES'''
#     #add support for new system
#     #add permission checks
#     db = sqlite3.connect('main.sqlite')
#     cursor = db.cursor()
#     name = f"GUILD{ctx.guild.id}"
#     cursor.execute(f"SELECT prefix from {name} WHERE user_id = {ctx.guild.id}")
#     result = cursor.fetchone()
#     if str(result[0]) == "None":
#         result = ("%", "Hi")
#     await ctx.send(f"Hey **{ctx.author.name}**, which channel would you like this to be in?")
#     def check(m):
#         return m.author == ctx.author and m.channel == ctx.message.channel
#
#     message = await client.wait_for('message', check=check, timeout = 30)
#     try:
#         benz = message.channel_mentions[0].id
#         print(benz)
#     except IndexError:
#         return await ctx.send(f"Channel `{message.content.lower()}` couldn't be found. Make sure I have permission to view the channel.")
#     channel = client.get_channel(int(benz))
#     if str(channel.type) == 'voice':
#         return await ctx.send(f"Unfortunately, you can't set a voice channel to be the reaction channel.")
#     elif str(channel.type) == 'category':
#         return await ctx.send(f"Unfortunately, you can't set a category channel to be the reaction channel.")
#     if channel is None:
#         return await ctx.send(f"Channel `{message.content.lower()}` couldn't be found. Re-use the command to try again.")
#     res = await channelperms(channel)
#     if not res:
#         return await ctx.send(
#             f"Please give me permission to `View Channel`, `Send Messages`, and `Embed Links` in {channel.mention} before proceeding.")
#     cursor.execute(f"SELECT channel_id from reactionroles WHERE guild_id = {ctx.guild.id}")
#     result1 = cursor.fetchone()
#     def check(m):
#         return m.channel.id == ctx.message.channel.id and m.author.id == ctx.author.id
#     if result1 is None:
#         sql = ("INSERT INTO reactionroles(guild_id, channel_id) VALUES(?, ?)")
#         val = (ctx.guild.id, channel.id)
#         cursor.execute(sql, val)
#         db.commit()
#         desc = f"Role channel for **{ctx.guild.name}** has been set to {channel.mention}."
#         embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp = datetime.datetime.utcnow())
#         await ctx.reply(embed=embed, mention_author=False)
#     else:
#         try:
#             chan = client.get_channel(int(result1[0]))
#             desc = f"{chan.mention} has already been set as the role channel for **{ctx.guild.name}**. Would you like to update it to {channel.mention}? Respond with `yes` or `no`."
#             embed = discord.Embed(description = desc, color = discord.Color.red(), timestamp = datetime.datetime.utcnow())
#             await ctx.send(embed=embed)
#             message = await client.wait_for('message', check=check, timeout = 45)
#             if message.content.lower() == "yes":
#                 # cursor.execute(f"DELETE FROM reactionroles WHERE guild_id = {ctx.guild.id}")
#                 # sql = ("INSERT INTO reactionroles(guild_id, channel_id) VALUES(?, ?)")
#                 # val = (ctx.guild.id, channel.id)
#                 # cursor.execute(sql, val)
#                 # db.commit()
#                 # cursor.close()
#                 # db.close()
#                 desc = f"Updated role channel has been set to {channel.mention}!"
#                 embed = discord.Embed(title = "Success!", description = desc, color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
#                 await ctx.send(embed = embed)
#             else:
#                 await ctx.send(f"Great, we will keep our reaction channel as {chan.mention}.")
#                 await asyncio.sleep(1)
#         except asyncio.TimeoutError:
#             return await ctx.send("Role setup has been ended due to inactivity.")
#
#
#     desc = f"What should the message content be? Use this format:\n" \
#            f"```Title | Message Content```"
#     embed = discord.Embed(description = desc, color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
#     await ctx.send(embed=embed)
#     message = await client.wait_for('message', check=check, timeout = 300)
#     if "|" not in message.content:
#         return await ctx.send(f"It looks like {message.content} has been formatted incorrectly.")
#
#     z = message.content.split("|")
#     #add the option for custom description
#     await ctx.send(f"Your title and description have been saved.\nThe embed will look like this:")
#     embed = discord.Embed(title = str(z[0]).strip(), description=str(z[1]).strip(), color = discord.Color.green())
#     await ctx.send(embed=embed)
#     await ctx.send(f"Great. Now it is time to assign roles. The format is the name of the emoji"
#                    f" and then the name of the role. Unfortunately, we are currently limited to default emojis, "
#                    f"not any custom ones. **CASE SENSITIVE!** Example:```:sunglasses: cool kid```")
#     cursor.execute(f"SELECT reaction from reactionroles WHERE guild_id = {ctx.guild.id}")
#     result = cursor.fetchall()
#     print(result)
#     if len(result) >= 50:
#         return await ctx.send(f"{ctx.guild.name} has reached its limit for reaction roles!")
#     lim = 50 - len(result)
#     print(lim)
#     identifier = random.randint(000000, 23721372831921)
#     while lim > 0:
#         print('we back')
#         message = await client.wait_for('message', check=check, timeout = 180)
#         print('gotcah')
#         if message.content.lower() == 'done':
#             break
#         args = message.content.split()
#         emoji = (args[0].replace(':', '').strip())
#         xz = discord.utils.get(ctx.guild.roles, name=f"{args[1].strip()}")
#         print('mhm')
#         sql = ("INSERT INTO reactionroles(guild_id, channel_id, reaction, role_id, identify) VALUES(?, ?, ?, ?, ?)")
#         val = (ctx.guild.id, channel.id, emoji, xz.id, identifier)
#         print('ok')
#         cursor.execute(sql, val)
#         print('yessir')
#         db.commit()
#
#         await message.add_reaction("👍🏽")
#         lim -= 1
#     cursor.execute(f"SELECT reaction, role_id from reactionroles WHERE guild_id = {ctx.guild.id} AND identify = {identifier}")
#     result = cursor.fetchall()
#     arr = []
#     for i in result:
#         role = discord.utils.get(ctx.guild.roles, id=int(i[1]))
#         arr.append(f"{i[0]}: {role.mention}")
#     x = '\n'.join(arr)
#     embed = discord.Embed(title = f"{str(z[0]).strip()}", description = f"{x}", color = discord.Color.green())
#     message = await channel.send(embed=embed)
#     for i in result:
#         await message.add_reaction(str(i[0]))
#         #continue onto raw reaction add event
#     print('ok')
#     cursor.close()
#     db.close()



#
# @rr.command()
# @commands.has_permissions(manage_guild = True)
# async def message(ctx, msgID: int = None):
#     #add support for new version
#     db = sqlite3.connect('main.sqlite')
#     cursor = db.cursor()
#     name = f"GUILD{ctx.guild.id}"
#     cursor.execute(f"SELECT prefix from {name} WHERE user_id = {ctx.guild.id}")
#     result = cursor.fetchone()
#     if str(result[0]) == "None":
#         result = ("%", "Hi")
#     print('hi')
#     if msgID is None:
#         desc = f"```{result[0]}rr message [message ID]```"
#         embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
#         embed.set_footer(text="Parameters in [] are required and () are optional")
#         return await ctx.reply(embed=embed, mention_author = False)
#     cursor.execute(f"SELECT channel_id from reactionroles WHERE guild_id = {ctx.guild.id}")
#     result1 = cursor.fetchone()
#     print(result1)
#     if result1 is None:
#         return await ctx.send(f"There is no set role channel for **{ctx.guild.name}**.")
#     cham = client.get_channel(int(result1[0]))
#     print(cham)
#     try:
#         msg = await cham.fetch_message(int(msgID))
#     except Exception as e:
#         print(e)
#         msg = None
#
#     if msg.channel.id == int(result1[0]):
#         print('yessir')
#     else:
#         print('noooo')

@client.command()
async def spotify(ctx, user: discord.Member = None):
    try:
        if user is None:
            user = ctx.author
        if user.activities:
            print(user.activities)
            for i in user.activities:
                if isinstance(i, Spotify):
                    x = i.artist.split("; ")
                    desc = f"{i.title}\n**{x[0]}** | *{i.album}*\n\nDuration: {str(i.duration)[0:7]}"
                    embed = discord.Embed(description = desc, color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
                    embed.set_author(name=f"Now playing for {user.name}", icon_url = user.avatar_url)
                    embed.set_thumbnail(url=i.album_cover_url)
                    message = await ctx.send(embed=embed)
                    await message.add_reaction("👍🏽")
                    await message.add_reaction("👎🏽")
        else:
            return await ctx.send(f"**{user.name}** isn't listening to anything at the moment.")
    except Exception as e:
        print(e)
        return await ctx.send("Something went wrong, try again later.")

@client.command()
async def whois(ctx, member: discord.User = None):
    if member is None:
        member = ctx.author
    try:
        desc = f"Bot: {'⛔' if not member.bot else '✅'}\n" \
               f"User ID: {member.id}\n" \
               f"Created: {member.created_at.strftime('%D')}\n" \
               f"Username: {member.name}#{member.discriminator}\n" \
               f"Is Discord System: {'⛔' if not member.system else '✅'}"
        embed = discord.Embed(description = desc, color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=f"About {member.name}", icon_url = member.avatar_url)
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)



@client.command(aliases = ['terms', 'termsofservice', 'privacypolicy'])
@commands.cooldown(1, 15, commands.BucketType.user)
async def tos(ctx):
    desc = '**View my User Agreement [here](https://docs.google.com/document/d/1XHOKPspuyqUIS9a0d0BMcO5oKXT5Xe5KdN_olG9sGFc/edit?usp=sharing).**\n' \
           '\nThank you for using InfiniBot!'
    embed = discord.Embed(title = "InfiniBot User Agreement", description = desc, color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
    embed.set_thumbnail(url=client.user.avatar_url)
    await ctx.author.send(embed=embed)

async def channelperms(channel: discord.TextChannel):
    if channel.guild.me.guild_permissions.administrator:
        return True
    y = channel.overwrites_for(channel.guild.default_role)
    if not y.send_messages or not y.read_messages or not y.embed_links:
        pass
    else:
        return True
    for role in channel.guild.me.roles:
        x = channel.overwrites_for(role)
        if not x.send_messages or not x.read_messages or not x.embed_links:
            continue
        else:
            return True

    z = channel.overwrites_for(channel.guild.me)
    if not z.send_messages or not z.read_messages or not z.embed_links:
        return False

@client.command()
@commands.cooldown(2, 15, commands.BucketType.user)
async def wanted(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    wanted = Image.open('./images/wantedposter.jpg')

    asset = member.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((519,539))
    wanted.paste(pfp, (160, 420))
    wanted.save('profile.jpg')

    await ctx.send(file=discord.File('profile.jpg'))

@client.command()
async def president(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    picture = Image.open('./images/presidentold.jpg')

    asset = member.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((140, 130))
    picture.paste(pfp, (295, 145))
    picture.save('profile.jpg')
    await ctx.send(file=discord.File('profile.jpg'))

@client.command()
async def polog(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    picture = Image.open('./images/polog.jpeg')

    asset = member.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((877, 775))
    picture.paste(pfp, (359, 53))
    picture.save('profile.jpg')
    await ctx.send(file=discord.File('profile.jpg'))

@client.command(aliases = ['tweet'])
async def twitter(ctx, member: discord.Member = None, *, text = "Next time put text you want converted lol"):
    if member is None:
        member = ctx.author

    if len(text) > 2000:
        return await ctx.reply("This message is too long.", mention_author = False)
    picture = Image.open('./images/twittertemp.png')
    font = ImageFont.truetype('arial.ttf', 39)
    draw = ImageDraw.Draw(picture)
    draw.text((187,69), member.display_name, (0, 0, 0), font=font)
    font = ImageFont.truetype('arial.ttf', 30)
    draw.text((187, 120), f"@{member.name}", (128,128,128), font=font)
    font = ImageFont.truetype('arial.ttf', 45)
    draw.text((55, 190), text, (0, 0, 0), font=font)
    font = ImageFont.truetype('arial.ttf', 30)
    t = time.localtime()
    current_time = time.strftime(r"%I:%M %p", t)
    current_date = time.strftime(r"%d %B %Y")
    draw.text((82, 420), current_time, (128,128,128), font=font)
    draw.text((210, 420), f"  -  {current_date}", (128,128,128), font=font)
    asset = member.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((117, 117))
    picture.paste(pfp, (55, 48))
    picture.save('profile.png')
    await ctx.send(file=discord.File('profile.png'))
    #add blacklisting for users who spam!


@client.command()
@commands.is_owner()
async def broadcast(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    await ctx.send(f"Type message now....")
    await client.wait_for('message', check=check)
    for k in client.guilds:
        for channel in k.text_channels:
            if k.permissions_for(k.me).send_messages:
                await channel.send(message.content)
                break


# @client.command(aliases=['msgraph', 'msggraph'])
# @commands.cooldown(1, 20, commands.BucketType.user)
# async def messagegraph(ctx):
'''DEPRECATED COMMAND, FIX WHEN COGS/CLASSES'''
#     db = sqlite3.connect('main.sqlite')
#     cursor = db.cursor()
#     name = f"GUILD{ctx.guild.id}"
#     cursor.execute(f"SELECT date, msgcount from {name} WHERE msgcount IS NOT NULL")
#     result = cursor.fetchall()
#     dictz = {}
#     for i in (result):
#         if str(i[0]) == 'None':
#             continue
#         else:
#             n_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days = 7)
#             print(pd.to_datetime(i[0]))
#             print(n_days_ago)
#             if pd.to_datetime(i[0]) > n_days_ago:
#                 print('yea')
#                 if pd.to_datetime(i[0]).strftime('%b%e, %Y') not in dictz.keys():
#                     dictz.__setitem__(pd.to_datetime(i[0]).strftime('%b%e, %Y'), i[1])
#                 else:
#                     x = (dictz[pd.to_datetime(i[0]).strftime('%b%e, %Y')])
#                     print(x)
#                     dictz[pd.to_datetime(i[0]).strftime('%b%e, %Y')] = x + int(i[1])
#                     print('done')
#     xv = []
#     yv = []
#     for i, k in enumerate(dictz.values()):
#         print(i, k)
#         xv.append(i + 1)
#         yv.append(k)
#
#     plt.plot(xv, yv, '-o')
#     plt.ylabel('Messages')
#     plt.xlabel('Last 7 Days')
#     plt.title(f"Messages in {ctx.guild.name}")
#     plt.savefig('bro.png')
#     await ctx.send(file=discord.File('bro.png'))
#     plt.close()

# @client.command()
# @commands.cooldown(1, 25, commands.BucketType.user)
'''DEPRECATED COMMAND, FIX WHEN CLASSES/COGS'''
# async def rank(ctx, member: discord.Member = None):
#     return await ctx.send("This command is being revamped, check back soon.")
#     await ctx.trigger_typing()
#     if member is None:
#         member = ctx.author
#     picture = Image.open('./images/rankup.png')
#     font = ImageFont.truetype('arial.ttf', 75)
#     draw = ImageDraw.Draw(picture)
#     async def getxp(member: discord.Member):
#         db = sqlite3.connect('main.sqlite')
#         cursor = db.cursor()
#         name = f"GUILD{ctx.guild.id}"
#         cursor.execute(f"SELECT XP, user_id from {name} WHERE XP IS NOT NULL")
#         result = cursor.fetchall()
#         if result is None:
#             await ctx.send("Something went wrong. Try again later.")
#             return False
#         elif len(result) == 0:
#             await ctx.send("Something went wrong. Try again later.")
#             return False
#         x = sorted(result, reverse=True)
#         countr = 0
#         for i, k in enumerate(x):
#             if int(k[1]) == member.id:
#                 return i, k[0]
#
#     x = await getxp(member)
#     if not x:
#         return
#
#     try:
#         draw.text((675, 58), f"{member.name}#{member.discriminator}", (255, 255, 255), font=font)
#         font = ImageFont.truetype('arial.ttf', 50)
#         draw.text((675, 209), f"XP: {x[1]}", (255, 255, 255), font=font)
#         draw.text((675, 330), f"Rank: {x[0] + 1}", (255, 255, 255), font=font)
#     except Exception as e:
#         print(e)
#     asset = member.avatar_url_as(size=128)
#     data = BytesIO(await asset.read())
#     pfp = Image.open(data)
#     pfp = pfp.resize((522, 522))
#     picture.paste(pfp, (25, 47))
#     picture.save('profile.png')
#     await ctx.send(file=discord.File('profile.png'))

@client.command(aliases = ['8ball'])
async def eightball(ctx, *, question):
    message = await ctx.reply(f"🎱 Please wait, the magic 8ball is thinking ... 🎱", mention_author = False)
    choices = [
        'Outlook not so good.',
        'It is decidedly so.',
        'Without a doubt.',
        'It is certain.',
        'You may rely on it.',
        'As I see it, yes.',
        'Outlook good.',
        'Signs point to yes.',
        'Reply hazy try again.',
        'Ask again later.',
        'Better not tell you now!',
        'Cannot predict now.',
        'Concentrate and ask again.',
        'Don\'t count on it.',
        'My reply is no.',
        'My sources say no.',
        'Outlook not so good.',
        'Very doubtful.'
    ]
    response = random.choice(choices)
    await asyncio.sleep(1)
    await message.edit(content = response, mention_author = False)

@eightball.error
async def eightball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        name = f"GUILD{ctx.guild.id}"
        db = cluster[name]
        collection = db['config']
        user = collection.find({'_id': ctx.guild.id})
        for i in user:
            prefix = i['prefix']
        desc = f"```{prefix}eightball [question]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.reply(embed=embed, mention_author = False)

@client.command()
async def gamewith(ctx, member: discord.Member, game):
    try:
        await ctx.send(f"{member.mention}, {ctx.author.mention} wants to play `{game}` with you. Do you accept?\nRespond within three minutes.")
        def check(m):
            return m.channel == ctx.channel and m.author == member
        msg = await client.wait_for('message', check=check, timeout = 180)
        if msg.content.lower() in ['y', 'yes']:
            return await ctx.send(f"Great, **{member.name}** and **{ctx.author.name}** are gonna play `{game}`!")
        elif msg.content.lower() in ['n', 'no']:
            return await ctx.send(f"Welp {ctx.author.mention}, it looks like **{member.name}** doesn't want to play `{game}` right now.")
        else:
            return await ctx.send(f"**{member.name}** gave an invalid response.")

    except asyncio.TimeoutError:
        return await ctx.send(f"{ctx.author.name}, your gamewith session has ended due to inactivity.")

@gamewith.error
async def gamewith_error(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}gamewith [member] [game]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.reply(embed=embed, mention_author = False)
    if isinstance(error, commands.MemberNotFound):
        await ctx.reply(error, mention_author = False)

@client.command()
async def guessingame(ctx):
    await ctx.send(f"**{ctx.author.name}** wants to play the guessing game! Are you sure you want to play?\nRespond with `y` or `n`.")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
        
    try:
        msg = await client.wait_for('message', check=check, timeout = 45)
        if msg.content.lower() not in ['y', 'yes']:
            return await ctx.send(f"Aw man, come back soon!")
        await ctx.send(f"Great. The rules of the game are as follows:")
        await asyncio.sleep(2)
        await ctx.send(f"You will get three guesses to guess the word. A word list will pop up shortly.")
        await asyncio.sleep(2)
        await ctx.send("You get 30 seconds between each guess. Any longer, and the game will automatically end.")
        await asyncio.sleep(2)
        await ctx.send(f"Word bank: `babatunde`, `hehe`, `epic`, `monke`, `kermit`, `wata`.\n**NOTE:** Capitalization doesn't matter.")
        await asyncio.sleep(2)
        await ctx.send(f"Start guessing now.")
        count = 0
        bank = [
            'babatunde',
            'hehe',
            'epic',
            'monke',
            'kermit',
            'wata'
        ]
        word = random.choice(bank)
        while count < 3:
            msg = await client.wait_for('message', check=check, timeout = 30)
            if msg.content.lower() == word.lower() and count == 0:
                return await ctx.send(f"Wow, {ctx.author.mention}! You were able to get it on your first try!")
            elif msg.content.lower() == word.lower():
                return await ctx.send(f"You guessed the word. It was `{word}`. You only took {count + 1} guesse{'' if count == 1 else 's'} to get it!")
            else:
                count += 1
                if count == 3:
                    break
                await ctx.send("That wasn't it, try again...")
                
                continue

        return await ctx.send(f'Aw man, you ran out of guesses! The word was `{word}`. Use the command to play again!')


    except asyncio.TimeoutError:
        return await ctx.send(f"**{ctx.author.name}**, you took too long. ")


@client.command()
async def choose(ctx, *, args = None):
    if args is None:
        name = f"GUILD{ctx.guild.id}"
        db = cluster[name]
        collection = db['config']
        user = collection.find({'_id': ctx.guild.id})
        for i in user:
            prefix = i['prefix']
        desc = f"```{prefix}choose [arg1] [arg2] ...```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.reply(embed=embed, mention_author = False)
    if "," not in args:
        return await ctx.reply("It looks like your message is incorrectly formatted. Split your arguments with a comma.\nEXAMPLE: Sprite, Coke, Beer, Water", mention_author = False)
    x = args.split(",")
    if len(x) < 2:
        return await ctx.reply("I need at least two arguments, split by a comma. \nEXAMPLE: Sprite, Coke, Beer, Water", mention_author = False)
    if len(x) > 20:
        return await ctx.reply(f"I cannot choose between more than 20 options!", mention_author = False)
    choice = random.choice(x)
    if len(choice) > 1000:
        return await ctx.reply("Make sure your arguments are less than 1000 characters in length!", mention_author = False)
    await ctx.reply(f"I choose `{choice.strip()}`!", mention_author = False) 
            
@client.command()
async def slowmode(ctx, channel: discord.TextChannel = None, duration:int = None):
    await channel.edit(reason='Bot Slowmode Command', slowmode_delay=(duration))
    await ctx.send(f"Slowmode for {channel.mention} has been toggled to on! Delay: {duration} seconds")

@slowmode.error
async def slowmode_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(f"I do not have permission to set slowmode for this channel! Please give me the `Read Messages`, `Send Messages`, and `Manage Channel` permissions. ")
        return
    if isinstance(error, commands.BadArgument):
        name = f"GUILD{ctx.guild.id}"
        db = cluster[name]
        collection = db['config']
        user = collection.find({'_id': ctx.guild.id})
        for i in user:
            prefix = i['prefix']
        desc = f"```{prefix}slowmode [channel mention] [duration]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        if str(error).strip() == 'Converting to "int" failed for parameter "duration".':
            error = 'Make sure the duration parameter is a number!'
        embed.set_footer(text="Parameters in [] are required and () are optional")
        await ctx.reply(embed=embed, content = error, mention_author = False)
        return
    if isinstance(error, BotMissingPermissions):
        await ctx.send(error)

@client.command()
async def slowmodeoff(ctx, channel: discord.TextChannel = None):
    if channel is None:
        channel = ctx.message.channel
    await channel.edit(reason='Bot Slowmode Command', slowmode_delay=0)
    await ctx.send(f"Slowmode for {channel.mention} has been toggled to off!")

@slowmodeoff.error
async def slowmodeoff_error(ctx, error):
    if isinstance(error, AttributeError):
        return await ctx.reply(f"You must mention a channel to remove slowmode from!", mention_author = False)
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(f"I do not have permission to set slowmode for this channel! Please give me the `Read Messages`, `Send Messages`, and `Manage Channel` permissions. ")
        return
    if isinstance(error, commands.BadArgument):
        name = f"GUILD{ctx.guild.id}"
        db = cluster[name]
        collection = db['config']
        user = collection.find({'_id': ctx.guild.id})
        for i in user:
            prefix = i['prefix']
        desc = f"```{prefix}slowmodeoff (channel mention)```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        await ctx.reply(embed=embed, mention_author = False)
        return
    if isinstance(error, BotMissingPermissions):
        return await ctx.send(error)
    

@client.command()
@commands.has_permissions(ban_members = True)
async def hackban(ctx, user: discord.User, reason = "No reason given"):
    ban = discord.Embed(description=f"Reason: ```{reason}```\nBy: {ctx.author.mention}",
                            color=discord.Color.dark_red())
    ban.set_author(name=f"{user.name} has been banned.", icon_url=user.avatar_url)
    try:
        await ctx.guild.ban(user, reason=reason)
        await ctx.channel.send(embed=ban)    
    except discord.Forbidden:
        return await ctx.send("I do not have proper permissions to ban this person!")

@hackban.error
async def hackban_err(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}slowmode [channel mention] [duration]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send("You can't use this!")


@client.command()
async def vchelp(ctx):
    pass

@client.command()
async def vcjoin(ctx):
    pass

@client.command()
async def vcleave(ctx):
    await ctx.message.add_reaction('👋🏽')

@client.command()
async def vcplay(ctx):
    pass

@client.command()
async def vcgenre(ctx):
    pass

@client.command()
async def vcrandom(ctx):
    pass

@client.command()
async def vcpause(ctx):
    pass

@client.command()
async def vcresume(ctx):
    pass

@client.command()
async def vcskip(ctx):
    pass

@client.command()
async def vcshuffle(ctx):
    pass

@client.command()
async def vcfavorite(ctx):
    pass

@client.command()
async def vcunfavorite(ctx):
    pass

@client.command()
async def vcfavorites(ctx):
    pass

@client.command()
async def vcgenres(ctx):
    pass

@client.command()
async def vclist(ctx):
    pass

@client.command()
async def vcclear(ctx):
    pass

@client.command()
async def vcqueue(ctx):
    pass


@client.command()
async def translate(ctx, language, *, phrase,):
    translator = Translator()
    newphrase = translator.translate(phrase, dest=language)
    print(newphrase)
    await ctx.send(f'Your phrase is: "{newphrase.text}"')

@client.command()
async def songlyrics(ctx):
    async with aiohttp.ClientSession() as session:
        url = 'http://api.genius.com/search'
        headers = {
            'Authorization': 'Bearer DhwDlvQfh5nupt0BxXKGxLAxc-Sv6gubjXH_PlDR-HBFEcw6Kj0vMExjp5zasnoE'
        }
        song_title = 'Life is Good'
        artist_name = 'Playboi Carti'
        params = {'q': song_title}
        async with session.get(url, headers=headers, params=params) as response:
            data = await response.json()
            print(data)

@slash.slash(name='test', description="Test")
async def test(ctx: SlashContext):
    await ctx.send('hi')

@slash.slash(name='emojify', description='Emojify a phrase')
async def emojify(ctx: SlashContext, *, text):
    if len(text) > 2000:
        await ctx.send("Keep your message under 2000 characters.")
        return
    try:
        new = []
        for i in str(text):
            if i == " ":
                new.append("         ")
                continue
            if not i.isalpha():
                continue
            else:
                new.append(f":regional_indicator_{i.lower()}:")
                continue

        await ctx.send(" ".join(new))
    except:
        await ctx.send("Something went wrong, next time make sure to use only letters.")

@slash.slash(name='8ball', description="Ask the 8ball a question!")
async def _eightball(ctx:SlashContext, *, question):
    choices = [
        'Outlook not so good.',
        'It is decidedly so.',
        'Without a doubt.',
        'It is certain.',
        'You may rely on it.',
        'As I see it, yes.',
        'Outlook good.',
        'Signs point to yes.',
        'Reply hazy try again.',
        'Ask again later.',
        'Better not tell you now!',
        'Cannot predict now.',
        'Concentrate and ask again.',
        'Don\'t count on it.',
        'My reply is no.',
        'My sources say no.',
        'Outlook not so good.',
        'Very doubtful.'
    ]
    response = random.choice(choices)
    await asyncio.sleep(1)
    embed = discord.Embed(title = f"{question.strip()}{'' if question.strip().endswith('?') else '?'}", description = response, color = discord.Color.green())
    await ctx.send(embed=embed)

import wikipedia as wk

@client.command()
async def wikipedia(ctx, *, query):
    print(query.strip())
    info = wk.summary(query.strip(), 1)
    print(info)

@slash.slash(name='asciitext', description='Convert a string into ASCII Binary!')
async def _asciitext(ctx: SlashContext, *, text):
    x = [ord(c) for c in text]
    await ctx.send(f"{text.strip()} -> {''.join(str(v) for v in x)}")

@slash.slash(name='servericon', description='Get this server\'s icon!')
async def _servericon(ctx:SlashContext):
    embed = discord.Embed(color = discord.Color.green())
    embed.set_author(name=ctx.author.name, icon_url = ctx.author.avatar_url)
    embed.set_image(url=ctx.guild.icon_url)
    embed.set_footer(text=f"{ctx.guild.name} Server Icon | Requested by {ctx.author.name}")
    await ctx.send(embed=embed)


@slash.slash(name='joke', description='Get a joke from r/jokes!')
async def _joke(ctx:SlashContext):
    all_subs = []
    subreddit = reddit.subreddit('jokes')
    top = subreddit.hot(limit=30)
    for sub in top:
        all_subs.append(sub)

    random_sub = random.choice(all_subs)
    name = random_sub.title
    tex = random_sub.selftext
    url = random_sub.url
    suburl = "https://www.reddit.com" + random_sub.permalink
    scr = random_sub.score
    com = random_sub.num_comments
    em = discord.Embed(title=name, description=tex, url=suburl, color=discord.Color.green())
    em.set_footer(text="👍 " + str(scr) + " | 💬 " + str(com))
    await ctx.send(embed=em)

@slash.slash(name='flip', description='Flips a coin!')
async def _flip(ctx:SlashContext):
    choices = ['heads', 'tails']
    res = random.choice(choices)
    return await ctx.send(res)

@slash.slash(name="reverse", description='Reverses text')
async def _reverse(ctx:SlashContext, *, text):
    return await ctx.send(f"{text.strip()} -> {text[::-1].strip()}")

@slash.slash(name='cinv', description='Generates an invite link to the server')
async def _cinv(ctx:SlashContext):
    invite = await ctx.channel.create_invite(max_age=604800)
    await ctx.send(f"Here is an invite to **{ctx.guild.name}**: \n{invite}")

@slash.slash(name='tinyurl', description='Creates a shortened URL from the given URL!')
async def _tinyurl(ctx:SlashContext, url):
    try:
        x = url_shortener.tinyurl.short(url)
        await ctx.author.send(x)
        await ctx.send("Check your dms!")
    except Exception as e:
        print(e)
        return await ctx.send("Something went wrong. Make sure after the command invocation you are only putting the URL link.")

@slash.slash(name='tmc', description='Returns the number of HUMANS in a server.')
async def _tmc(ctx:SlashContext):
    true_member_count = len([m for m in ctx.guild.members if not m.bot])
    return await ctx.send(f"There are {true_member_count} humans in the server **{ctx.guild.name}**")

@slash.slash(name='afk', description='Sets an AFK status globally')
async def _afk(ctx:SlashContext, *, message = 'Away'):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['afk']
    cnick = ctx.author.display_name
    member = ctx.author
    ping_cm = {
        "_id": ctx.author.id,
        "name": ctx.author.name,
        "display_name": cnick,
        "member": ctx.author.name,
        'start': time.time(),
        'status': message
    }
    try:
        x = collection.insert_one(ping_cm)
    except Exception:
        return await ctx.send("You are already afk!")
    desc = f"Your afk status has been successfully updated to: ```{message}```"
    embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
    embed.set_author(name=f"{ctx.author.name} is now afk", icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text="The AFK setting has been saved.")
    await ctx.send(embed=embed)

    try:
        await member.edit(nick=f"[AFK] {cnick}")
    except discord.Forbidden:
        pass

@slash.slash(name='membercount', description="Returns count of members in the server!")
async def memcount(ctx:SlashContext):
    await ctx.send(f'There are `{ctx.guild.member_count}` members in **{ctx.guild.name}**.')

@slash.slash(name='asciiart', description='Convert text into ASCII art!')
async def _asciitext(ctx:SlashContext, *, text):
    if len(text) > 2000:
        await ctx.send("Your message was too long!")
    result = pyfiglet.figlet_format(f"{text}")
    await ctx.send(f"```{result}```")


@slash.slash(name='clap', description='Insert claps between words!')
async def _clap(ctx:SlashContext, *, text):
    arr = []
    for i in text:
        if i == " ":
            arr.append("    ")
        else:
            arr.append(i.strip())

    x = ":clap:".join(arr)
    await ctx.send(x)

@slash.slash(name='urban', description='Search the urban dictionary!')
async def _urban(ctx:SlashContext, *, text):
    with open('urbanapi.txt', 'r') as f:
        key = f.read()
    try:
        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        querystring = {"term": text}
        headers = {
            'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
            'x-rapidapi-key': key
            }
        async with ClientSession() as session:
            async with session.get(url, headers=headers, params=querystring) as response:
                r = await response.json()
                definition = r['list'][0]['definition']
                desc = str(definition)
                if r['list'][0]['example'] == "":
                    r['list'][0]['example'] = "..."
                embed = discord.Embed(title=f"Urban Dictionary Definition of {text}", url = r['list'][0]['permalink'], description = desc, color = discord.Color.green())
                embed.add_field(name="Example Sentence:", value = r['list'][0]['example'], inline = False)
                embed.add_field(name="👍🏽", value = r['list'][0]['thumbs_up'])
                embed.add_field(name="👎🏽", value=r['list'][0]['thumbs_down'])
                embed.set_footer(text=f"Author: {r['list'][0]['author']} on {r['list'][0]['written_on'][0:10]}")
                embed.set_thumbnail(url=ctx.guild.icon_url)
                await ctx.send(embed=embed)
    except IndexError:
        return await ctx.send(f"Error! The search term **{text}** could not be found.")

@slash.slash(name='avatar', description='Returns the avatar of said user!')
async def _avatar(ctx:SlashContext, member:discord.User = None):
    try:
        if member is None:
            author = ctx.author
            pfp = author.avatar_url
            embed = discord.Embed(title="**Avatar**")
            embed.set_author(name=author, icon_url=pfp)
            embed.set_image(url=pfp)
            await ctx.send(embed=embed)
            return
        else:
            author = member
            pfp = author.avatar_url
            embed = discord.Embed(title="**Avatar**")
            embed.set_author(name=str(author), icon_url=pfp)
            embed.set_image(url=pfp)
            await ctx.send(embed=embed)
            return
    except discord.ext.commands.errors.MemberNotFound:
        await ctx.reply(f'Couldn\'t find member -> {member.strip()}')
        return

@slash.slash(name='feedback', description = 'Send feedback to the developers!')
async def _feedback(ctx:SlashContext, *, text):
    channel = client.get_channel(839951602168496149)
    fembed = discord.Embed(title=f"Feedback from {ctx.author} who is in the server **{ctx.guild.name}**",
                            description=f"{ctx.author.id} (User ID)\n{ctx.guild.id} (Guild ID)```" + text + "```",
                            color=discord.Color.blurple(), timestamp = datetime.datetime.utcnow())
    msg = await channel.send(embed=fembed)
    await msg.add_reaction(str('👍🏽'))
    await msg.add_reaction(str('👎🏽'))
    await ctx.send(str(f'Thank you for using InfiniBot!'))

@slash.slash(name='quickpoll', description='Create a poll with two options!')
async def _quickpoll(ctx:SlashContext, opt1, opt2):
    author = ctx.author
    pfp = author.avatar_url
    embed = discord.Embed(description=f"{opt1} or {opt2}", color=discord.Color.red(), timestamp = datetime.datetime.utcnow())
    embed.set_author(name=author, icon_url=pfp)
    message = await ctx.send(embed=embed)
    await message.add_reaction("👍")
    await message.add_reaction("👎")
    return

@slash.slash(name='choicepoll', description='Create a multiple choice poll!')
async def _choicepoll(ctx:SlashContext, title, arg1, arg2, arg3, arg4 = None, arg5 = None, arg6 = None, arg7 = None, arg8 = None, arg9 = None):
        if len(title) > 50:
            return await ctx.send("Your title cannot be longer than 50 characters.")
        title = title.strip()
        descarr = []
        numarr = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        x = []
        x.append(arg1)
        x.append(arg2)
        x.append(arg3)
        if arg4 is not None:
            x.append(arg4)
        if arg5 is not None:
            x.append(arg5)
        if arg6 is not None:
            x.append(arg6)
        if arg7 is not None:
            x.append(arg7)
        if arg8 is not None:
            x.append(arg8)
        if arg9 is not None:
            x.append(arg9)

        for i, k in enumerate(x):
            descarr.append(f":{numarr[i]}: --> {k.strip()}")
        desc = "\n".join(descarr)
        embed = discord.Embed(title = title, description = desc, color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
        embed.set_author(name=ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        message = await ctx.send(embed=embed)
        emoji_numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        for i, k in enumerate(x):
            await message.add_reaction(f"{emoji_numbers[i]}")

@slash.slash(name='botinfo', description='Get stats about the bot!')
async def _botinfo(ctx:SlashContext):
    db = cluster['COMMANDCOUNT']
    collection = db['commandcount']
    results = collection.find({'_id': client.user.id})
    for i in results:
        countr = i['count']
    cpusage = psutil.cpu_percent()
    RAMuse = psutil.virtual_memory().percent
    embed = discord.Embed(color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Version:", value=f"```{botversion}```")
    embed.add_field(name="Python Version: ", value="```3.9.5```")
    embed.set_footer(text="Developed by glizzybeam7801#8196 and kidsonfilms#4635")
    embed.add_field(name="Commands run:", value=f"```{countr + 1}```", inline=False)
    embed.add_field(name="Servers:", value=f"```{len(client.guilds)}```")
    embed.add_field(name="CPU Usage:", value=f"```{cpusage}%```", inline=False)
    embed.add_field(name="RAM Usage:", value=f"```{RAMuse}%```")
    embed.add_field(name="Client Latency:", value=f"```{round(client.latency * 1000)}ms```", inline=False)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.set_author(name=f"InfiniBot Statistics", icon_url=client.user.avatar_url)
    await ctx.send(embed=embed)

@slash.slash(name='botinvite', description='Get InfiniBot\'s invite link!')
async def _botinv(ctx):
    embed = discord.Embed(title="InfiniBot Invite Link",
                          description=r'https://discord.com/api/oauth2/authorize?client_id=829464107710677022&permissions=4294307063&scope=bot%20applications.commands',
                          color=discord.Color.blurple())
    embed.set_footer(text=f"InfiniBot Help | Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

# @slash.slash(name='messagegraph', description='Generates a graph showing progression of messages')
# async def _messagegraph(ctx):
'''DEPRECATED COMMAND'''
#     db = sqlite3.connect('main.sqlite')
#     cursor = db.cursor()
#     name = f"GUILD{ctx.guild.id}"
#     cursor.execute(f"SELECT date, msgcount from {name} WHERE msgcount IS NOT NULL")
#     result = cursor.fetchall()
#     dictz = {}
#     for i in (result):
#         if str(i[0]) == 'None':
#             continue
#         else:
#             n_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days = 7)
#             print(pd.to_datetime(i[0]))
#             print(n_days_ago)
#             if pd.to_datetime(i[0]) > n_days_ago:
#                 print('yea')
#                 if pd.to_datetime(i[0]).strftime('%b%e, %Y') not in dictz.keys():
#                     dictz.__setitem__(pd.to_datetime(i[0]).strftime('%b%e, %Y'), i[1])
#                 else:
#                     x = (dictz[pd.to_datetime(i[0]).strftime('%b%e, %Y')])
#                     print(x)
#                     dictz[pd.to_datetime(i[0]).strftime('%b%e, %Y')] = x + int(i[1])
#                     print('done')
#     xv = []
#     yv = []
#     for i, k in enumerate(dictz.values()):
#         print(i, k)
#         xv.append(i + 1)
#         yv.append(k)
#
#     plt.plot(xv, yv, '-o')
#     plt.ylabel('Messages')
#     plt.xlabel('Last 7 Days')
#     plt.title(f"Messages in {ctx.guild.name}")
#     plt.savefig('bro.png')
#     await ctx.send(file=discord.File('bro.png'))
#     plt.close()
@slash.slash(name='passwordgenerator', description='Creates a random string!')
async def _passgen(ctx, length:int=10):
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation
    if length > 20:
        await ctx.send(f"Since your specified value was greater than 20 characters, we are shortening it to 20.")
    combined = lower + upper + num + symbols
    temp=random.sample(combined, length)
    channel = ctx.channel
    desc = f'{"".join(temp)}'
    desc2 = f"\nYou requested this in {channel.mention} in the server **{ctx.guild.name}**"
    await ctx.send("Check your dms!")
    embed = discord.Embed(description = f"```{desc}```{desc2}", color = discord.Color.green())
    embed.set_author(name=f"{ctx.author.name}'s randomly generated password", icon_url = ctx.author.avatar_url)
    embed.set_footer(text="InfiniBot Password Generator")
    await ctx.author.send(embed = embed)
    
@slash.slash(name='fm', description='Get your currently playing track from Last.fm!')
async def _fm(ctx, member:discord.Member = None):
    if member is None:
        member = ctx.author
    db = cluster['LASTFM']
    collection = db['usernames']
    query = {"_id": member.id}
    if collection.count_documents(query) == 0:
        return await ctx.send(f"**{member.name}** has not set their Last FM profile with InfiniBot!")
    else:
        user = collection.find(query)
        for result in user:
            username = result['username']
    with open('lfapi.txt', 'r') as f:
        key = f.read()
    params = {
        'user': f'{username}',
        'api_key': key,
        'method': 'user.getrecenttracks',
        'format': 'json',
        'limit': 1
    }
    async with aiohttp.ClientSession() as session:
        url = 'https://ws.audioscrobbler.com/2.0/'
        async with session.get(url, params=params) as response:
            data = await response.json()
    x = (data['recenttracks']['track'])
    if not x:
        return await ctx.send(f"**{member.name}** has not listened to any tracks!")

    username = data['recenttracks']['@attr']['user']
    track = x[0]['name']
    trackurl = x[0]['url']
    album = x[0]['album']['#text']
    artist = x[0]['artist']['#text']
    thumbnail = x[0]['image'][-1]['#text']
    try:
        timestamp = x[0]['date']['#text']
        z = pd.to_datetime(timestamp)
        desc = f"{f'[{track}]({trackurl})'} \n**{artist}** | *{album}*"
        embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=z)
        embed.set_author(name=f"{username}'s last track:", icon_url=member.avatar_url)
        embed.set_thumbnail(url=str(thumbnail))
        embed.set_footer(
            text=f"{member.name} has {data['recenttracks']['@attr']['total']} total scrobbles | Last scrobble: ")
    except KeyError:
        z = datetime.datetime.utcnow()
        desc = f"{f'[{track}]({trackurl})'} \n**{artist}** | *{album}*"
        embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=z)
        embed.set_author(name=f"{username}'s currently playing track:", icon_url=member.avatar_url)
        embed.set_thumbnail(url=str(thumbnail))
        embed.set_footer(text=f"{member.name} has {data['recenttracks']['@attr']['total']} total scrobbles")
    message = await ctx.send(embed=embed)
    await message.add_reaction("👍🏽")
    await message.add_reaction("👎🏽")


@client.command()
async def prefix(ctx):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    prefix = Image.open('./Images/prefiximg.png')
    font = ImageFont.truetype('arial.ttf', 15)
    draw = ImageDraw.Draw(prefix)
    draw.text((75,45), f"{prefix}tinyurl https://www.youtube.com/watch?v=dQw4w9WgXcQ", (255, 255, 255), font=font)
    prefix.save('profile.png')
    desc = f"Prefix for **{ctx.guild.name}** is {prefix}. \n\n**NOTE:** If you want a word prefix with a space after it, you must surround it in quotes due to a Discord limitation.\n\nEXAMPLE: {prefix}changeprefix \"yo \""
    embed = discord.Embed(description = desc, color = discord.Color.green())
    embed.set_thumbnail(url = ctx.guild.icon_url)
    file = discord.File("./profile.png", filename='image.png')
    embed.set_image(url='attachment://image.png')
    await ctx.send(file=file, embed=embed)


@slash.slash(name='prefix', description='Returns the prefix for your server!')
async def _prefix(ctx:SlashContext):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefixd = i['prefix']
    prefix = Image.open('./Images/prefiximg.png')
    font = ImageFont.truetype('arial.ttf', 15)
    draw = ImageDraw.Draw(prefix)
    draw.text((75, 45), f"{prefixd}tinyurl https://www.youtube.com/watch?v=dQw4w9WgXcQ", (255, 255, 255), font=font)
    prefix.save('profile.png')
    desc = f"Prefix for **{ctx.guild.name}** is {prefixd}. \n\n**NOTE:** If you want a word prefix with a space after it, you must surround it in quotes due to a Discord limitation.\n\nEXAMPLE: {prefixd}changeprefix \"yo \""
    embed = discord.Embed(description=desc, color=discord.Color.green())
    embed.set_thumbnail(url=ctx.guild.icon_url)
    file = discord.File("./profile.png", filename='image.png')
    embed.set_image(url='attachment://image.png')
    await ctx.send(file=file, embed=embed)


@client.command()
@commands.has_permissions(manage_guild = True)
async def vckick(ctx, member: discord.Member):
    await member.edit(voice_channel = None)
    await ctx.send(f"**{member.name}** has been successfully kicked from VC!")

@vckick.error
async def vck_err(ctx, error):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    if isinstance(error, commands.MissingRequiredArgument):
        desc = f"```{prefix}vckick [member]```"
        embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
        embed.set_footer(text="Parameters in [] are required and () are optional")
        return await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send(f"{ctx.author.mention}, you can't use that!")

@slash.slash(name='serverstats', description='Get some basic server statistics!')
async def _serverstats(ctx:SlashContext):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['messages']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        msgcount = i['count']
    if msgcount == '':
        msgcount = 0
    collection = db['serverstats']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        vcsecs = i['vcsecs']
    if vcsecs == '':
        vcsecs = 0

    collection = db['config']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        ghostcount = i['ghostcount']
    if ghostcount == '':
        ghostcount = 0
    x = ctx.guild.created_at
    y = x.strftime("%b %d %Y %H:%S")
    print(y)
    z = datetime.datetime.utcnow() - x
    lm = str(abs(z))
    print(lm)
    q = lm.split(", ")
    a = q[0]
    desc = f"This is only from when I joined **{ctx.guild.name}**. Anything before that has not been documented."
    embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Channels:", value=f"```{str(len(ctx.guild.channels))}```", inline=True)
    embed.add_field(name="Users:", value=f"```{ctx.guild.member_count}```", inline=True)
    embed.add_field(name="Messages Sent:", value=f"```{msgcount}```", inline=True)
    # embed.add_field(name=f"In #{ctx.channel.name}:", value = f"```{smsgcfount}```", inline = True)
    # embed.add_field(name=f"By {ctx.author.name}:", value = f"```{smsgcount}```", inline = True)
    # embed.add_field(name=f"In #{ctx.channel.name} by {ctx.author.name}:", value=f"```{result3[0]}```", inline = False)
    embed.add_field(name="Seconds in Voice Channels", value=f"```{vcsecs}```", inline=True)
    embed.add_field(name=f"Server Creation Date:",
                    value=f"```{f'{y} ({a} ago)' if lm[0:6] != '1 day,' else 'Today'}```", inline=True)
    # embed.add_field(name=f"Most active text channel in **{ctx.guild.name}**: ", value = f"```#{topchannel.name} with {smsgcffount} messages.```", inline = False)
    # figure out most active VC
    ownerser = client.get_user(ctx.guild.owner_id)
    embed.add_field(name=f"Number of Ghost Pings", value=f"```{ghostcount}```", inline=False)
    embed.add_field(name="Server Owner:", value=ownerser.mention, inline=False)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_author(name=f"{ctx.guild.name}'s Statistics", icon_url=ctx.guild.icon_url)
    embed.set_footer(text=f"Server ID: {ctx.guild.id}")
    await ctx.send(embed=embed)

@client.command()
async def vcseconds(ctx):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['serverstats']
    results = collection.find({'_id': ctx.guild.id})
    for i in results:
        vcsecs = i['vcsecs']
    if vcsecs == '':
        vcsecs = 0
    return await ctx.send(f"The people of **{ctx.guild.name}** have spent a cumulative {vcsecs} second{'' if int(vcsecs) == 1 else 's'} in VC!")

@client.command(aliases = ['clear_server_data', 'clearguilddata', 'clear_guild_data'])
@commands.has_permissions(manage_guild = True)
@commands.guild_only()
@commands.cooldown(1, 900, commands.BucketType.guild)
async def clearserverdata(ctx):
    await ctx.message.delete()
    name = f"GUILD{ctx.guild.id}"
    desc = f"Here at {client.user.name}, we take your privacy seriously. By clearing this data you acknowledge that ALL information pertaining to {ctx.guild.name}, such as message counts and server configuration settings, WILL BE LOST. THIS IS AN IRREVERSIBLE ACTION! \n\nTo confirm clearing **{ctx.guild.name}'s** information, react with the ✅. \n\nIf you would like to cancel, react with ⛔."
    embed = discord.Embed(description = desc, color = discord.Color.red())
    def check(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) in ['✅', '⛔']
    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')
    await message.add_reaction('⛔')
    try:
        reaction, user = await client.wait_for('reaction_add', check=check, timeout = 120)
        if reaction.emoji == '✅':
            cluster.drop_database(name)
            name = f"GUILD{ctx.guild.id}"
            db = cluster[name]
            collection = db['config']
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                'prefix': '%',
                'welcomemsg': "",
                "welcomechannel": "",
                'priv_welcomemsg': "",
                'leavemsg': "",
                'captchaon': "",
                'muterole': "",
                'spamdetect': "",
                'logging': "",
                'logchannel': "",
                'levelups': "",
                'ghostpingon': "",
                'ghostcount': '',
                'blacklistenab': "",
                'mcip': "",
                'starchannel': '',
                'welcomenick': '',
                'welcomerole': ''
            }
            x = collection.insert_one(ping_cm)
            collection = db['afk']
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                'afkstatus': "",
                'startafk': '',
                'preafknick': '',
                'afkid': ''
            }
            x = collection.insert_one(ping_cm)
            collection = db['serverstats']
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                'vcsecs': "",
                'msgcount': ''
            }
            x = collection.insert_one(ping_cm)
            collection = db['levels']
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name
            }
            x = collection.insert_one(ping_cm)
            collection = db['customcmnd']
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                'commandname': ""
            }
            x = collection.insert_one(ping_cm)
            collection = db['commands']
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                'commandname': "",
                'commandcount': '',
                'commandchannel': ''
            }
            x = collection.insert_one(ping_cm)
            collection = db['warns']
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                'reason': "",
                'time': '',
                'mod': '',
                'offender': ''
            }
            x = collection.insert_one(ping_cm)
            collection = db['messages']
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                'author': "",
                'date': '',
                'channel': '',
                'count': ''
            }
            x = collection.insert_one(ping_cm)
            collection = db['typing']
            ping_cm = {
                "_id": ctx.guild.id,
                "name": ctx.guild.name,
                'uid': '',
                'date': "",
                'accuracy': '',
                'wpm': ''
            }
            x = collection.insert_one(ping_cm)
            await message.clear_reactions()
            desc = f"All server data for {ctx.guild.name} has successfully been cleared from the database."
            embed = discord.Embed(description = desc, color = discord.Color.green())
            await message.edit(embed = embed)
        elif (reaction.emoji) == '⛔':
            await message.clear_reactions()
            desc = f"Session has been cancelled."
            embed = discord.Embed(description = desc, color = discord.Color.red())
            return await message.edit(embed=embed)
    except asyncio.TimeoutError:
        await message.clear_reactions()
        desc = "Session has ended due to inactivity, data has not been cleared."
        embed = discord.Embed(description = desc, color = discord.Color.red())
        return message.edit(embed=embed)


@clearserverdata.error
async def clr_err(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        return await ctx.send(f"Data for **{ctx.guild.name}** has recently been cleared. Please try again later.")

@client.command()
async def inviteinfo(ctx, invite:discord.Invite):
    try:
        embed = discord.Embed(color = discord.Color.green())
        embed.add_field(name = "Inviter", value = f"```{invite.inviter}```")
        embed.add_field(name = "Code", value = f"```{invite.code}```")
        embed.add_field(name = "Server", value = f"```{invite.guild}```")
        embed.add_field(name = "URL", value = f"```{invite.url}```", inline = False)
        embed.add_field(name = "Uses", value = f"```{invite.uses}```", inline = False)
        await ctx.send(embed=embed)
    except Exception as e:
        if str(e).strip() == 'Invite is invalid or expired.':
            return await ctx.reply(e, mention_author = False)

# @client.command()
# async def ping1(ctx):
#     mongo_url = "mongodb+srv://infinibot:jTGQE2m44bsWNnLM@infinibot.f381p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
#     cluster = MongoClient(mongo_url)
#     db = cluster['GUILD830158413408239646']
#     collection = db['prefix']
#     query = {"_id": ctx.author.id}
#     if collection.count_documents(query) == 0:
#         ping_cm = {"_id": ctx.author.id, "score": 1}
#         collection.insert_one(ping_cm)
#     else:
#         user = collection.find(query)
#         for result in user:
#             score = result['score']
#         score += 1
#         collection.update_one({"_id": ctx.author.id}, {"$set": {'score': score}})
#
#     await ctx.send("DoNE!")

# @client.command()
# async def rahul(ctx):
#     mongo_url = "mongodb+srv://infinibot:jTGQE2m44bsWNnLM@infinibot.f381p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
#     cluster = MongoClient(mongo_url)
#     name = f"GUILD{ctx.guild.id}"
#     db = cluster[name]
#     collection =  db['prefix']
#     query = {"_id": ctx.author.id}
#     if collection.count_documents(query) == 0:
#         ping_cm = {"_id": ctx.author.id, "name": 'Test', 'address': 'Joe Mama'}
#         collection.insert_one(ping_cm)
#     else:
#         
#         dict = {'$set': {
#             "name" : 'Test',
#             'address': 'Joe Mama'
#             }
#         }
#         x = collection.update_one(query, dict)
#     # dblist = (cluster.list_database_names())
#     # if name in dblist:
#     #     print(name)
#     await ctx.send("Success!")


@client.command()
@commands.cooldown(1, 90000, commands.BucketType.user)
async def dntu(ctx):
    desc = f"{ctx.author.mention}, by requesting not to track your data, you understand that you will not be allowed to run commands with {client.user.name} from this point on. " \
           f"Do you still wish to proceed? React with the ✅ if yes, or with the ⛔ to cancel.\n\n**NOTE: TO UNDO THIS ACTION, YOU MUST CONTACT THE DEVELOPERS OR JOIN THE SUPPORT SERVER**"
    embed = discord.Embed(description = desc, color = discord.Color.red())
    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')
    await message.add_reaction('⛔')
    def check(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) in ['✅', '⛔']
    reaction, user = await client.wait_for('reaction_add', check=check, timeout=120)
    if reaction.emoji == '✅':
        db = cluster['DONOTTRACK']
        collection = db['users']
        query = {"_id": ctx.author.id}
        if collection.count_documents(query) == 0:
            ping_cm = {"_id": ctx.author.id, "name": ctx.author.name, 'time': datetime.datetime.utcnow().strftime('%D')}
            collection.insert_one(ping_cm)
        else:
            results = collection.find(query)
            for i in results:
                date = i['time']
            desc = f"You have already requested not to track your data. \nLAST REQUESTED: {date}"
            embed = discord.Embed(description = desc, color = discord.Color.red())
            await message.edit(embed=embed)
            return await message.clear_reactions()
        desc = f"Success! From this point on, all data pertaining to {ctx.author.mention} will now be deleted.\n\nTo undo this action, please visit the support server."
        embed = discord.Embed(description = desc, color = discord.Color.green())
        await message.edit(embed=embed)
        return await message.clear_reactions()

@client.command()
@commands.guild_only()
@commands.has_guild_permissions(manage_guild = True)
async def dntg(ctx):
    db = cluster['DONOTTRACK']
    collection = db['guilds']
    query = {"_id": ctx.guild.id}
    if collection.count_documents(query) == 0:
        ping_cm = {"_id": ctx.guild.id, "name": ctx.guild.name, 'time': datetime.datetime.utcnow()}
        collection.insert_one(ping_cm)
    else:
        return await ctx.send(f"{ctx.guild.name} has already requested to not track its data.")
    # dblist = (cluster.list_database_names())
    # if name in dblist:
    #     print(name)
    await ctx.send("Success!")


@slash.slash(name = "Help", description="Retrieves InfiniBot's help menu!")
async def _help(ctx):
    name = f"GUILD{ctx.guild.id}"
    db = cluster[name]
    collection = db['config']
    user = collection.find({'_id': ctx.guild.id})
    for i in user:
        prefix = i['prefix']
    embed = discord.Embed(color=discord.Color.green())
    embed.set_author(name=f"{client.user.name}'s Help Menu", icon_url=client.user.avatar_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    # add individual help for each command
    embed.set_footer(text=f"Made by glizzybeam7801#8196 and kidsonfilms#4635")
    # add some example commands
    embed.add_field(name="🛠️ Setup", value=f"Setup InfiniBot For {ctx.guild.name}!\n`{prefix}setup`")
    embed.add_field(name="🎮 Games", value=f"Play games with InfiniBot!\n`{prefix}help games`")
    embed.add_field(name="📣 Moderation",
                    value=f"Moderate your server or take a step back and let InfiniBot moderate for you!\n`{prefix}help moderation`")
    embed.add_field(name="❓ Miscellaneous",
                    value=f"These commands aren't sorted right now, but include everything.\n`{prefix}help misc`")
    embed.add_field(name="💰 Economy",
                    value=f"Participate in an economy system! (Currently in development). \n`{prefix}help economy`")
    embed.add_field(name="📈 Server Stats",
                    value=f"See server stats for {ctx.guild.name} \n`{prefix}help serverstats`")
    embed.add_field(name="About Us!",
                    value=f"[Invite Link](https://discord.com/api/oauth2/authorize?client_id=829464107710677022&permissions=4294307063&scope=bot%20applications.commands) - [Support Server](https://discord.gg/4VnUA8ZXyH)\nSend the devs feedback by using `{prefix}feedback`!",
                    inline=False)
    await ctx.send(embed=embed)


async def is_dev(ctx):
    return ctx.author.id in [645388150524608523, 759245009693704213]

@client.group(invoke_without_command = True)
@commands.check(is_dev)
async def sudo(ctx):
    return await ctx.author.send("Available params are `--shutdown` and `--restart`.")

@sudo.command(name = '--restart')
@commands.check(is_dev)
async def _restart(ctx):
    channel = client.get_channel(id=844611738133463121)
    desc = f"Restart requested by {ctx.author.mention} on {datetime.datetime.utcnow().strftime('%D')}. \nAttempting restart..."
    embed = discord.Embed(title = "Bot restarting --force restart activated", description = desc, color = discord.Color.red(), timestamp = datetime.datetime.utcnow())
    message = await channel.send(embed=embed)
    await ctx.message.add_reaction('✅')
    try:
        await client.close()
    except Exception as e:
        print(e)
        await ctx.author.send("Something went wrong while attempting a restart.")
        pass
    finally:
        os.system('python main.py')


@sudo.command(name = '--shutdown')
@commands.check(is_dev)
async def _shutdown(ctx):
    channel = client.get_channel(id=844611738133463121)
    desc = f"Shutdown requested by {ctx.author.mention} on {datetime.datetime.utcnow().strftime('%D')}. \nAttempting shutdown..."
    embed = discord.Embed(title = "Bot shutting down --force shutdown activated", description = desc, color = discord.Color.red(), timestamp = datetime.datetime.utcnow())
    message = await channel.send(embed=embed)
    await ctx.message.add_reaction('✅')
    try:
        await client.close()
        print('Client closed')
    except Exception as e:
        print(e)
        await ctx.author.send("Something went wrong while shutting down.")

@client.command()
async def gc(ctx):
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']
    # if os.path.exists('token.json'):

@client.command()
async def test1(ctx):
    AUTH_URL = 'https://api.spotify.com/v1/'
    access_token = 'BQA8xYDai1rHrbVisv-5261qw7edCbXbQjEhEkJWEjXXYK5qw7is1_b2SjOGjrA159NxnEJ1I6zuaFTeNCU'
    track_id = '0sci7ppTZFm4mjcH3nu8yO?si=efc14ad1bb1e4a9e'
    async with ClientSession() as session:
        headers = {
            'Authorization': "Bearer {token}".format(token=access_token)
        }
        url = AUTH_URL + 'audio/features/' + track_id
        async with session.get(url=url, headers=headers) as response:
            print('hi')
            data = await response.json()
            print(data)



with open('token.txt', 'r') as f:
    TOKEN = f.read()

client.run(TOKEN)



# from PIL import Image

# im1 = Image.open('image/path/1.png')
# im2 = Image.open('image/path/2.png')
# area = (40, 1345, 551, 1625)  
# im1.paste(im2, area)
#                    l>(511+40) l>(280+1345)
#          |    l> From 0 (move, 1345px down) 
#           -> From 0 (top left, move 40 pixels right)
