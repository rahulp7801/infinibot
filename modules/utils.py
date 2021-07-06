from __future__ import print_function

import asyncio

from durations_nlp import Duration
from discord.ext import commands
from pymongo import MongoClient
from modules import help
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
import re
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import discord
from modules.exceptions import ClassroomError
import pandas as pd

with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

SCOPES = ['https://www.googleapis.com/auth/classroom.course-work.readonly', 'https://www.googleapis.com/auth/classroom.courses.readonly', 'https://www.googleapis.com/auth/classroom.announcements.readonly', 'https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly', 'https://www.googleapis.com/auth/classroom.coursework.me']
AUTHLINK = 'https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?response_type=code&client_id=250731096823-ic06oic089jcv0kgnck91dmhcn0jg0tf.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A55342%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fclassroom.course-work.readonly%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fclassroom.courses.readonly%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fclassroom.announcements.readonly%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fclassroom.courseworkmaterials.readonly%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fclassroom.coursework.me&state=X5AHIXL7KxCC27TcxbE8PM8BqNOyUE&access_type=offline&flowName=GeneralOAuthFlow'

class ErrorMessage(Exception):
    pass

def tmts(string):
    '''
    :param string:
    Formatted preferably in d, h, m, s
    :return:
    The value in seconds
    '''
    try:
        string = string.strip().removeprefix('for')
        return int(Duration(string).to_seconds())
    except Exception as e:
        if 'contains an invalid token' in str(e).lower():
            raise ValueError('You need to specify a valid duration!')

def stringfromtime(t, accuracy=4):
    '''
    :param t: more often than not the output from the tmts function
    :param accuracy: How accurate, for example do we want days, seconds, hours?
    :return:
    a string of <days>, <hours>, <minutes>, <seconds>
    '''
    try:
        m, s = divmod(t, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        components = []
        if d > 0:
            components.append(f"{int(d)} day" + ("s" if d != 1 else ""))
        if h > 0:
            components.append(f"{int(h)} hour" + ("s" if h != 1 else ""))
        if m > 0:
            components.append(f"{int(m)} minute" + ("s" if m != 1 else ""))
        if s > 0:
            components.append(f"{int(s)} second" + ("s" if s != 1 else ""))

        return " ".join(components[:accuracy])
    except Exception as e:
        print(e)

def serverprefix(ctx):
    '''
    :param ctx: Context from message
    :return: Returns the prefix from the context, if that doesn't work then scrapes the MongoDB
    '''
    try:
        return ctx.prefix
    except Exception:
        db = cluster['CONFIGURATON']
        collection = db['guilds']
        results = collection.find({'_id': ctx.guild.id})
        for i in results:
            prefix = i['prefix']
        return "%" if prefix is None else prefix
    except UnboundLocalError:
        return '%'

def messagetoembed(message:discord.Message):
    '''
    :param message: Message ID or referenced message to convert
    :return:
    An embed of the message, (starchannel, logging, and fun commands)
    '''
    embed = discord.Embed()
    embed.description = message.content.strip()
    embed.set_author(name=message.author.name + "#" + message.author.discriminator, icon_url=message.author.avatar_url)
    embed.timestamp=message.created_at
    embed.colour = message.author.color
    if message.attachments:
        embed.set_image(url=message.attachments.proxy_url)
    return embed


def channelperms(channel: discord.TextChannel):
    '''
    :param channel: The text channel that we are getting perms for
    :return:
    True if the bot has sufficient perms, or False and a reason if the Bot does not
    '''
    if channel.is_nsfw():
        print('her3')
        return False
    if channel.guild.me.guild_permissions.administrator:
        print('here2')
        return True
    y = channel.overwrites_for(channel.guild.default_role)
    if not y.send_messages or not y.read_messages or not y.embed_links:
        print('here4')
        pass
    else:
        print('here7')
        return True
    for role in channel.guild.me.roles:
        print('here8')
        x = channel.overwrites_for(role)
        if not x.send_messages or not x.read_messages or not x.embed_links:
            if role == channel.guild.default_role:
                print('nruj')
                pass
            else:
                print('here9')
                pass
        else:
            print('here10')
            return True
        break

    z = channel.overwrites_for(channel.guild.me)
    if not z.send_messages or not z.read_messages or not z.embed_links:
        print('here1')
        return False

def rolecheck(role:discord.Role, ctx):
    '''
    :param role: A role in a server, (welcomerole, muterole, ...)
    :return:
    True if the bot has permission to manage this role, or False and a reason.
    '''
    rolez = discord.utils.get(role.guild.roles, name=role.name)
    if rolez is None:
        return False, f"`{role}` is not a valid role in **{role.guild.name}**."
    if rolez >= role.guild.me.top_role:
        return False, f"{role.mention} is above my highest role!"
    if rolez.is_default():
        return False, f"{role.mention} is given to everybody, so I cannot assign this role."
    if rolez.is_bot_managed():
        return False, f"{role.mention} is managed by a bot."
    if rolez.is_integration():
        return False, f"{role.mention} is managed by an integration."
    if rolez.is_premium_subscriber():
        return False, f"{role.mention} is only given to server boosters and cannot be manually assigned."
    if rolez >= ctx.author.top_role:
        if ctx.author.id == ctx.guild.owner_id:
            pass
        else:
            return False, f"{role.mention} is above your highest role."
    return True


def imgdraw(**kwargs):
    '''
    :param kwargs: Args from the input
    :return:
    An edited image with PIL, to shorten code (6 lines v 1 line)
    '''
    try:
        photo = Image.open(str(kwargs['photo']))
        font = ImageFont.truetype(kwargs['font'], int(kwargs['fontsize']))
        draw = ImageDraw.Draw(photo)
        draw.text(kwargs['xy'], kwargs['text'], kwargs['rgb'], font=font)
        photo.save(f'profile.{"png" if str(kwargs["photo"]).endswith("png") else "jpg"}')
        return photo
    except Exception as e:
        raise ErrorMessage(e)

def errmsg(ctx):
    '''
    :param ctx: Context of the command
    :return:
    an embed explaining proper usage.
    '''
    desc = getcmnduse(ctx)
    embed = discord.Embed(title="Incorrect Usage!", description=f"```{desc}```", color=discord.Color.red())
    embed.set_footer(text="Parameters in <> are required and [] are optional")
    return embed

async def tomember(ctx, user):
    '''
    :param ctx: Context
    :param user: The user to convert, preferably with an ID or with name+discrim
    :return: A discord.Member object
    '''
    try:
        return await commands.MemberConverter().convert(ctx, user)
    except commands.errors.BadArgument as e:
        raise ErrorMessage(e)

def boolint(val:bool):
    '''
    :param val: The value (boolean)
    :return:
    1 (True) or 0 (False)
    '''
    try:
        return 1 if val else 0
    except:
        raise ValueError(f'{val} is not a boolean!')

def intbool(val:int):
    '''
    :param val: The value (integer)
    :return:
    True if the value is not None or 0 otherwise False
    '''
    return True if val != (0 or None) else False

def getcmnduse(ctx):
    return f"{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}"

async def send_bot_help(ctx):
    await ctx.bot.help_command.send_bot_help()

async def send_cog_help(ctx, cog):
    await ctx.bot.help_command.send_cog_help(cog)

async def send_command_help(ctx):
    await ctx.send_help(ctx.command)
#create help function here that maps from help.py

async def send_group_help(ctx, group):
    await ctx.bot.help_command.send_group_help(group)

def get_classes(ctx, limit :int= 10):
    '''
    :param ctx: Context of the message
    :param limit: The limit of classes we want to retrieve information from
    :return:
    Information of all classes returned in a list
    '''
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(f'./temp/token{ctx.guild.id}-{ctx.author.id}.json'):
        creds = Credentials.from_authorized_user_file(f'./temp/token{ctx.guild.id}-{ctx.author.id}.json', SCOPES)
    else:
        return False, "Not authorized to view classes for this server."
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            return False, "Invalid credentials, please try logging in again."

    service = build('classroom', 'v1', credentials=creds)
    # Call the Classroom API
    results = service.courses().list(pageSize=(int(limit) if limit < 15 else 15)).execute()
    courses = results.get('courses', [])
    if not courses:
        raise ClassroomError("No courses found!")
    else:
        arr = []
        for i in courses:
            arr.append(i) #appending all information
        return arr, service

def add_member_cah(member:discord.Member):
    embed = discord.Embed(description=f'{member.mention} was added to the game!', color=discord.Color.blue())
    return embed

def priv_cah_msg(channel:discord.TextChannel):
    embed = discord.Embed(
        description=f"You have joined a Cards Against Humanity game in {channel.mention} in **{channel.guild.name}**.",
        color=discord.Color.blue())
    return embed

def current_tzar(index:int, arr):
    embed = discord.Embed(description=f"The current czar is {arr[index]}! Wait until the other players have submitted their cards, then choose the best one.",
                                color=discord.Color.blue())
    current_admin = arr[index]
    return embed, current_admin

# def add_guild_to_db(guild:discord.Guild):
#     '''
#     :param guild: The guild (server) we need to add to the database.
#     :return:
#     add the guild to the database, but if it already exists just pass (we don't need duplicates)
#     '''
#     try:
#         db = cluster[name]
#         collection = db['config']
#         ping_cm = {
#             "_id": guild.id,
#             "name": guild.name,
#             'prefix': '%',
#             'welcomemsg': "",
#             "welcomechannel": "",
#             'priv_welcomemsg': "",
#             'leavemsg': "",
#             'captchaon': "",
#             'muterole': "",
#             'spamdetect': "",
#             'logging': "",
#             'logchannel': "",
#             'levelups': "",
#             'ghostpingon': "",
#             'ghostcount': '',
#             'blacklistenab': "",
#             'mcip': "",
#             'starchannel': '',
#             'welcomenick': '',
#             'welcomerole': ''
#         }
#         x = collection.insert_one(ping_cm)
#         collection = db['levels']
#         ping_cm = {
#             "_id": guild.id,
#             "name": guild.name
#         }
#         x = collection.insert_one(ping_cm)
#         collection = db['customcmnd']
#         ping_cm = {
#             "_id": guild.id,
#             "name": guild.name,
#             'commandname': ""
#         }
#         x = collection.insert_one(ping_cm)
#         collection = db['reactionroles']
#         ping_cm = {
#             "name": 'placeholder',
#             'commandname': ""
#         }
#         x = collection.insert_one(ping_cm)
#         collection = db['afk']
#         ping_cm = {
#             "_id": guild.id,
#             "name": guild.name,
#             'afkstatus': "",
#             'startafk': '',
#             'preafknick': '',
#             'afkid': ''
#         }
#         x = collection.insert_one(ping_cm)
#         collection = db['serverstats']
#         ping_cm = {
#             "_id": guild.id,
#             "name": guild.name,
#             'vcsecs': "",
#             'msgcount': ''
#         }
#         x = collection.insert_one(ping_cm)
#         collection = db['commands']
#         ping_cm = {
#             "_id": guild.id,
#             "name": guild.name,
#             'commandname': "",
#             'commandcount': '',
#             'commandchannel': ''
#         }
#         x = collection.insert_one(ping_cm)
#         collection = db['warns']
#         ping_cm = {
#             "_id": guild.id,
#             "name": guild.name,
#             'reason': "",
#             'time': '',
#             'mod': '',
#             'offender': ''
#         }
#         x = collection.insert_one(ping_cm)
#         collection = db['messages']
#         ping_cm = {
#             "_id": guild.id,
#             "name": guild.name,
#             'author': "",
#             'date': '',
#             'channel': '',
#             'count': ''
#         }
#         x = collection.insert_one(ping_cm)
#         collection = db['typing']
#         ping_cm = {
#             "_id": guild.id,
#             "name": guild.name,
#             'uid': '',
#             'date': "",
#             'accuracy': '',
#             'wpm': ''
#         }
#         x = collection.insert_one(ping_cm)
#         collection = db['starboard']
#         ping_cm = {
#             "_id": guild.id
#         }
#         x = collection.insert_one(ping_cm)
#     except Exception:
#         pass

def add_guild_to_db(guild:discord.Guild):
    '''
    :param guild: The guild (server) we need to add to the database.
    :return:
    add the guild to the database, but if it already exists just pass (we don't need duplicates)
    '''
    try:
        db = cluster['CONFIGURATION']
        col = db['guilds']
        query = {'_id':guild.id}
        if col.count_documents(query) != 0:
            pass
        else:
            payload = {
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
                'ghostcount': '',
                'blacklistenab': "",
                'mcip': "",
                'starchannel': '',
                'welcomenick': '',
                'welcomerole': '',
                'enablestats': True
            }
            col.insert_one(payload)
        db = cluster['LEVELING']
        col = db['guilds']
        if col.count_documents({'_id':guild.id}) != 0:
            pass
        else:
            payload = {
                "_id": guild.id,
                "name": guild.name
            }
            col.insert_one(payload)
        db = cluster['CUSTOMCMND']
        col = db['guilds']
        if col.count_documents({'_id':guild.id}) != 0:
            pass
        else:
            payload = {
                "_id": guild.id,
                "name": guild.name,
                'commandname': ""
            }
            col.insert_one(payload)
        db = cluster['STATS']
        col = db['guilds']
        if col.count_documents({'_id':guild.id}) != 0:
            pass
        else:
            payload = {
                '_id':guild.id,
                'name':guild.name,
                'vcsecs': 0,
                'msgcount': 0
            }
            col.insert_one(payload)
        db = cluster['COMMANDCOUNT']
        col = db['commandcount']
        if col.count_documents({'_id':guild.id}) != 0:
            pass
        else:
            payload = {
                "_id": guild.id,
                "name": guild.name,
                'commandname': "",
                'commandcount': '',
                'commandchannel': ''
            }
            col.insert_one(payload)
        db = cluster['MESSAGES']
        col = db['guilds']
        if col.count_documents({'_id':guild.id}) != 0:
            pass
        else:
            payload = {
                "_id": guild.id,
                "name": guild.name,
                'author': "",
                'date': '',
                'channel': '',
                'count': ''
            }
            col.insert_one(payload)

    except Exception:
        pass

separators = [" ", " ", " ", "  ", "  ", " "]
font = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ1234567890"

def obfuscate(text):
    while " " in text:
        text = text.replace(" ", random.choice(separators), 1)
    letter_dict = dict(zip("abcdefghijklmnopqrstuvwxyz1234567890", font))
    return "".join(letter_dict.get(letter, letter) for letter in text)

def anticheat(message):
    remainder = "".join(
        set(message.content).intersection(font + "".join(separators))
    )
    return remainder != ""

def clean_string(string):
    string = re.sub('@', '@\u200b', string)
    string = re.sub('#', '#\u200b', string)
    return string

def force_reset_guild_db(guild):
    name = f"GUILD{guild.id}"
    cluster.drop_database(name)
    add_guild_to_db(guild)
    print(f"Success, force resetted {guild.name} ({guild.id})'s information")

def check_if_starboard_message_exists(message:discord.Message):
    db = cluster[f"GUILD{message.guild.id}"]
    collection = db['starboard']
    query = {'ogmsg': message.id}
    if collection.count_documents(query) == 0:
        return False
    return True

async def clear_guild_starboard_messages(guild:discord.Guild):
    name = f"GUILD{guild.id}"
    db = cluster[name]
    collection = db['config']
    query = {"_id": guild.id}
    if collection.count_documents(query) == 0:
        return False, "This guild has not been indexed, contact the developers immediately."
    else:
        res = collection.find(query)
        for result in res:
            starchannel = result['starchannel']
        if starchannel == '':
            return False, "Starboard channel does not exist in the database!"
        try:
            chan = guild.get_channel(int(starchannel))
        except Exception:
            return False, "I cannot access the starboard channel anymore!"
        try:
            await chan.purge(limit = 10000)
        except:
            pass
    collection = db['starboard']
    db.drop_collection(collection)
    ping_cm = {
        "_id": guild.id
    }
    x = collection.insert_one(ping_cm)
    return True

def add_message_to_starboard(message:discord.Message, ogmsg:discord.Message, channel:discord.TextChannel):
    name = f"GUILD{message.guild.id}"
    db = cluster[name]
    collection = db['starboard']
    ping_cm = {
        "_id": message.id,
        'gid' : message.guild.id,
        'ogmsg' : ogmsg.id,
        'starboardchannel': channel.id,
        'ogchannel': ogmsg.channel.id
    }
    collection.insert_one(ping_cm)

def fetch_starboard_message(message:discord.Message):
    name = f"GUILD{message.guild.id}"
    db = cluster[name]
    collection = db['starboard']
    query = {'ogmsg':message.id, 'gid':message.guild.id}
    result = collection.find(query)
    for i in result:
        msg = i['_id']
        channel = i['starboardchannel']

    return int(msg), int(channel)

async def set_classroom_class(ctx:discord.ext.commands.Context):
    try:
        print('here1')
        res, service = get_classes(ctx)
        print(res, service)
        if not res:
            return (False, service)
        print(res, service)
        return (True, res)

    except Exception as e:
        print(e)

def vcperms(channel:discord.VoiceChannel):
    if channel.guild.me.guild_permissions.administrator:
        return True

    if len(channel.members) >= channel.user_limit != 0:
        return False, "The max number of people are already in VC!"

    y = channel.overwrites_for(channel.guild.default_role)
    if not y.speak or not y.view_channel or not y.connect:
        pass
    else:
        return True
    for role in channel.guild.me.roles:
        x = channel.overwrites_for(role)
        if not x.speak or not x.view_channel or not x.connect:
            if role == channel.guild.default_role:
                pass
            else:
                pass
        else:
            return True
        break

    z = channel.overwrites_for(channel.guild.me)
    if not z.speak or not z.view_channel or not z.connect:
        return False
    return True

def determine_timeframe(param):
    if param.lower() == ('w' or 'week'):
        param = '7day'
        phrase = 'weekly'
    elif param.lower() == ('m' or 'month'):
        param = '1month'
        phrase = 'monthly'
    elif param.lower() == ('3m' or '3month'):
        param = '3month'
        phrase = '3 monthly'
    elif param.lower() == ('h' or '6m' or 'hy'):
        param = '6month'
        phrase = 'half-yearly'
    elif param.lower() == ('y' or 'year'):
        param = '12month'
        phrase = 'yearly'
    elif param.lower() == ('a' or 'alltime' or 'overall'):
        param = 'overall'
        phrase = 'overall'
    else:
        param = '7day'
        phrase = 'weekly'
    return param, phrase

def auth_classroom(ctx:discord.ext.commands.Context):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(f'./temp/token{ctx.guild.id}-{ctx.author.id}.json'):
        creds = Credentials.from_authorized_user_file(f'./temp/token{ctx.guild.id}-{ctx.author.id}.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            AUTHLINK = flow.run_discord()
            print('here bruh')
            embed = discord.Embed(color=discord.Color.green())
            embed.description = f"Please sign in [here]({AUTHLINK.replace('Please visit this URL to authorize this application:', '')})\n\nPlease enter the code that you receive after logging in."
            return embed

def save_class_creds(ctx:discord.ext.commands.Context, code):
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.discord_auth(code)
    with open(f'./temp/token{ctx.guild.id}-{ctx.author.id}.json', 'w') as token:
        token.write(creds.to_json())
    return

def classroomlogout(ctx:discord.ext.commands.Context):
    if os.path.exists(f'./temp/token{ctx.guild.id}-{ctx.author.id}.json'):
        os.remove(f'./temp/token{ctx.guild.id}-{ctx.author.id}.json')
        return (True, "nice")
    return (False, "No classes set for this user in this server.")


