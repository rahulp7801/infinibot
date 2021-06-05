import discord
import asyncio
from discord.ext import commands
from pymongo import MongoClient
import time
from modules import utils
import os
import os.path
from os import path
import os
import json
import time

with open('mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

class Stats(commands.Cog):
    def __init__(self, client, cache):
        self.client = client
        self.cache = cache

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild is False:
            return ''
        if any(x for x in cache if x["guildID"] == message.guild.id):
            for h in cache:
                print('Found Server Stats')
                if h["guildID"] == message.guild.id:
                    h["messages"] += 1
                    if any(p for p in h["engagedusers"] if p["uid"] == message.author.id):
                        for p in h["engagedusers"]:
                            if p["uid"] == message.author.id:
                                p["messagesSent"] += 1
                    else:
                        h["engagedusers"].append({"username":message.author.name + '#' + message.author.discriminator, "uid": message.author.id, "messagesSent": 1, "vcsecs": 0, "activetime": [time.time()]})
                    print(cache)
                    json_cache = open('cache/stats.json', 'w')
                    json_str = '{"guilds":'+ json.dumps(cache)
                    json_cache.write(json_str + '}')
        else:
            print(f"Cache Not Found for Guild {message.guild.id}, Writing it Now")
            cache.append({"guildID": message.guild.id, "messages": 1, "userdiff": 0, "vcsecdiff": 0, "engagedusers": [{"username":message.author.name + '#' + message.author.discriminator, "uid": message.author.id, "messagesSent": 1, "vcsecs": 0, "activetime": [time.time()]}]})
            json_cache = open('cache/stats.json', 'w')
            json_str = '{"guilds":'+ json.dumps(cache)
            json_cache.write(json_str + '}')
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print('New Member, Adding to Stats')
        if any(x for x in cache if x["guildID"] == member.guild.id):
            if member.bot:
                print('New Member is Bot, Escaping')
                return ''
            for h in cache:
                if h["guildID"] == member.guild.id:
                    h["userdiff"] += 1
                    json_cache = open('cache/stats.json', 'w')
                    json_str = '{"guilds":'+ json.dumps(cache)
                    json_cache.write(json_str + '}')
        else:
            print(f"Cache Not Found for Guild {member.guild.id}, Writing it Now")
            cache.append({"guildID": member.guild.id, "messages": 0, "userdiff": 1, "vcsecdiff": 0, "engagedusers": []})
            json_cache = open('cache/stats.json', 'w')
            json_str = '{"guilds":'+ json.dumps(cache)
            json_cache.write(json_str + '}')
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print('Member Left, Adding to Stats')
        if any(x for x in cache if x["guildID"] == member.guild.id):
            if member.bot:
                print('Member is Bot, Escaping')
                return ''
            for h in cache:
                if h["guildID"] == member.guild.id:
                    h["userdiff"] -= 1
                    json_cache = open('cache/stats.json', 'w')
                    json_str = '{"guilds":'+ json.dumps(cache)
                    json_cache.write(json_str + '}')
        else:
            print(f"Cache Not Found for Guild {member.guild.id}, Writing it Now")
            cache.append({"guildID": member.guild.id, "messages": 0, "userdiff": -1, "vcsecdiff": 0, "engagedusers": []})
            json_cache = open('cache/stats.json', 'w')
            json_str = '{"guilds":'+ json.dumps(cache)
            json_cache.write(json_str + '}')

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

def setup(client):
    client.add_cog(Stats(client, cache))