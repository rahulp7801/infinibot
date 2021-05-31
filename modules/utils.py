import discord
import asyncio
import datetime
from durations_nlp import Duration
from discord.ext import commands
from pymongo import MongoClient

with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

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
        name = f"GUILD{ctx.guild.id}"
        db = cluster[name]
        collection = db['config']
        results = collection.find({'_id': ctx.guild.id})
        for i in results:
            prefix = i['prefix']
        return prefix if prefix is not None else '%'
    except UnboundLocalError:
        return '%'
