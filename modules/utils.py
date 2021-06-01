import discord
import asyncio
import datetime
from durations_nlp import Duration
from discord.ext import commands
from pymongo import MongoClient
import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

class ErrorMessage(Exception):
    pass

def tmts(string):
    try:
        string = string.strip().removeprefix('for')
        return int(Duration(string).to_seconds())
    except Exception as e:
        if 'contains an invalid token' in str(e).lower():
            raise ValueError('You need to specify a valid duration!')

def stringfromtime(t, accuracy=4):
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
    try:
        return ctx.prefix
    except Exception:
        name = f"GUILD{ctx.guild.id}"
        db = cluster[name]
        collection = db['config']
        results = collection.find({'_id': ctx.guild.id})
        for i in results:
            prefix = i['prefix']
        return prefix if prefix is not None else '%'
    except UnboundLocalError:
        return '%'

def messagetoembed(message:discord.Message):
    embed = discord.Embed()
    embed.description = message.content.strip()
    embed.set_author(name=message.author.name + "#" + message.author.discriminator, icon_url=message.author.avatar_url)
    embed.timestamp=message.created_at
    embed.colour = message.author.color
    if message.attachments:
        embed.set_image(url=message.attachments.proxy_url)
    return embed


def channelperms(channel: discord.TextChannel):
    if channel.is_nsfw():
        return False
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

def rolecheck(role:discord.Role):
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
    return True


def imgdraw(**kwargs):
    try:
        photo = Image.open(str(kwargs['photo']))
        print('hi1')
        font = ImageFont.truetype(kwargs['font'], int(kwargs['fontsize']))
        print('hi2')
        draw = ImageDraw.Draw(photo)
        print('hi3')
        draw.text(kwargs['xy'], kwargs['text'], kwargs['rgb'], font=font)
        print('hi4')
        photo.save(f'profile.{"png" if str(kwargs["photo"]).endswith("png") else "jpg"}')
        print('hi5')
        return photo
    except Exception as e:
        raise ErrorMessage(e)
