import discord
import asyncio
from discord.ext import commands, tasks
from matplotlib import use
from pymongo import MongoClient
import time
from modules import utils
import os
import os.path
from os import path
import os
import json
import time
import datetime
import plotly
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import datetime
import math

with open('mongourl.txt', 'r') as file:
    url = file.read()

async def is_dev(ctx):
    return ctx.author.id in [645388150524608523, 759245009693704213]

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

def seconds_until(hours, minutes):
    given_time = datetime.time(hours, minutes)
    now = datetime.datetime.now()
    future_exec = datetime.datetime.combine(now, given_time)
    if (future_exec - now).days < 0:  # If we are past the execution, it will take place tomorrow                future_exec = datetime.datetime.combine(now + datetime.timedelta(days=1), given_time) # days always >= 0
        return (future_exec - now).total_seconds()
    return (future_exec - now).total_seconds()
        
def round_up_to_even(f):
    return math.ceil(f / 2.) * 2

class Stats(commands.Cog):

    def __init__(self, client, cache):
        self.client = client
        self.cache = cache

    def cog_unload(self):
        self.update_database_stats.cancel()

    def seconds_until(self, hours, minutes):
        given_time = datetime.time(hours, minutes)
        now = datetime.datetime.now()
        future_exec = datetime.datetime.combine(now, given_time)
        if (future_exec - now).days < 0:  # If we are past the execution, it will take place tomorrow
            future_exec = datetime.datetime.combine(now + datetime.timedelta(days=1), given_time) # days always >= 0

        return (future_exec - now).total_seconds()

            
    @tasks.loop(hours=2)
    async def update_database_stats(self):
        print(f'Uploading Stats to Database: LOG TIME: {datetime.datetime.utcnow()}')
        for g in cache:
            name = "GUILD" + str(g["guildID"])
            db = cluster[name]
            collection = db['serverstats']
            collection.insert_one({
                "messages": g["messages"],
                "userdiff": g["userdiff"],
                "vcsecdiff": g["vcsecdiff"],
                "engagedusers": g["engagedusers"],
                "timestamp": time.time()
            })
        cacheF = open("cache/stats.json", "w")
        cacheF.write('{"guilds": []}')
        cacheF.close()
        self.cache = {"guilds": []}
    
    @update_database_stats.before_loop
    async def beforedbupate(self):
        await self.client.wait_until_ready()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild is False:
            return ''
        if any(x for x in cache if x["guildID"] == message.guild.id):
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
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
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
        if any(x for x in cache if x["guildID"] == member.guild.id):
            if member.bot:
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
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        name = f"GUILD{member.guild.id}"
        db = cluster[name]
        collection = db['config']
        res = collection.find({'_id': member.guild.id})
        if before.channel and after.channel:
            if before.channel == after.channel:
                return
        elif before.channel and not after.channel:
            collection = db['serverstats']
            res = collection.find({'_id': member.id})
            vcsecs = 0
            for i in res:
                starttime = i['vcstart']
                x = pd.to_datetime(starttime)
                z = (abs(datetime.datetime.utcnow() - x))
                vcsecs = int(z.total_seconds())
            collection = db['serverstats']
            res = collection.find({'_id': member.guild.id})
            for i in res:
                vcmins = i['vcsecs']
            if vcmins == "":
                if any(x for x in cache if x["guildID"] == member.guild.id):
                    for h in cache:
                        if h["guildID"] == member.guild.id:
                            h["vcsecdiff"] += vcsecs
                            json_cache = open('cache/stats.json', 'w')
                            json_str = '{"guilds":'+ json.dumps(cache)
                            json_cache.write(json_str + '}')
                else:
                    print(f"Cache Not Found for Guild {member.guild.id}, Writing it Now")
                    cache.append({"guildID": member.guild.id, "messages": 0, "userdiff": 0, "vcsecdiff": vcsecs, "engagedusers": []})
                    json_cache = open('cache/stats.json', 'w')
                    json_str = '{"guilds":'+ json.dumps(cache)
                    json_cache.write(json_str + '}')
            else:
                if any(x for x in cache if x["guildID"] == member.guild.id):
                    for h in cache:
                        if h["guildID"] == member.guild.id:
                            h["vcsecdiff"] += int(vcmins) + vcsecs
                            json_cache = open('cache/stats.json', 'w')
                            json_str = '{"guilds":'+ json.dumps(cache)
                            json_cache.write(json_str + '}')
                else:
                    print(f"Cache Not Found for Guild {member.guild.id}, Writing it Now")
                    cache.append({"guildID": member.guild.id, "messages": 0, "userdiff": 0, "vcsecdiff": int(vcmins) + vcsecs, "engagedusers": []})
                    json_cache = open('cache/stats.json', 'w')
                    json_str = '{"guilds":'+ json.dumps(cache)
                    json_cache.write(json_str + '}')
    
    @commands.Cog.listener()
    async def on_ready(self):
        if (datetime.datetime.now().time().hour % 2 == 0):
            print(f'Uploading DB Data at: {datetime.datetime.now().time().hour + 2}:00')
            await asyncio.sleep(seconds_until(int(math.ceil(datetime.datetime.now().time().hour + 2 / 2.)), 0))
            self.update_database_stats.start()
        else:
            print(f'Uploading DB Data at: {math.ceil(datetime.datetime.now().time().hour + 0.01 / 2.)}:00')
            await asyncio.sleep(seconds_until(int(math.ceil(datetime.datetime.now().time().hour + 0.01 / 2.)), 0))
            self.update_database_stats.start()

    @commands.command()
    @commands.check(is_dev)
    async def serverStats(self, ctx):
        async with ctx.typing():

            db = cluster[f"GUILD{ctx.guild.id}"] 
    
            col = db["serverstats"] 
            msgcol = db["messages"]

            cacheData = {
                "subID": [],
                "Messages": [],
                "Time": [],
            }

            cacheActiveUsers = []

            userMSGSDict = {}

            msgdocs = msgcol.find_one({"_id": ctx.guild.id})
            msgcount = msgdocs["count"]
      
            for x in col.find({}): 
                if (x["_id"] != ctx.guild.id):
                    if datetime.datetime.fromtimestamp(x["timestamp"]).date() == datetime.datetime.today().date():
                        cacheData["subID"].append(len(cacheData["subID"]))
                        cacheData["Messages"].append(x["messages"])
                        try:
                            cacheData["Time"].append((time.strftime('%I %p', time.localtime(x["timestamp"]))))
                        except Exception as e:
                            print(e)
                        for member in x["engagedusers"]:
                            if member["uid"] in userMSGSDict:
                                userMSGSDict[member["uid"]]["msgs"] += member["messagesSent"]
                            else:
                                userMSGSDict[member["uid"]] = {"msgs": member["messagesSent"], "id": member["uid"]}
            for u in userMSGSDict:
                cacheActiveUsers.append(userMSGSDict[u])
            cacheActiveUsers.sort(key=lambda x: x["msgs"], reverse=True)
            filePath = f'cache/guild{ctx.guild.id}-{datetime.datetime.now().date()}-stats.json'
            json_cache = open(filePath, 'w')
            json_cache.write(json.dumps(cacheData))
            json_cache.close()
            
            dataFile = open(filePath)
            df = pd.read_json(dataFile, 'r')
            df.set_index('subID', inplace=True)
            sns.reset_defaults()
            sns.set(
                rc={'figure.figsize':(7,5)}, 
            )
            plt.style.use("dark_background")
            sns.lineplot(data=df, x="Time", y="Messages")
            plt.gca().axes.xaxis.grid(False)
            plt.fill_between(df.Time.values, df.Messages.values, alpha=0.5)
            sns.despine(fig=None, ax=None, top=True, right=True, left=True, bottom=True, offset=None, trim=False)
            plt.xlabel(None)
            plt.ylabel(None)
            plt.savefig(f"sentAssets/guild{ctx.guild.id}-{datetime.datetime.now().date()}.png", transparent=True)
            embed=discord.Embed(title=f"{ctx.guild.name} Stats", url=f"http://localhost:3000/dashboard/server/{ctx.guild.id}/stats#", description=f"Go [here](http://infinibot.xyz/dashboard/server/{ctx.guild.id}/stats#) for further stats", color=0xff0000)
            embed.add_field(name="Total Messages", value=f"In All: `{msgcount} messages`", inline=False)
            counter = 0
            arr = []
            for i in range((len(cacheActiveUsers)) if (len(cacheActiveUsers) <= 5) else 5):
                arr.append(f"`{counter + 1}.` <@!" + str(cacheActiveUsers[counter]["id"]) + ">: `" + str(
                    cacheActiveUsers[counter]["msgs"]) + " messages`")
                counter += 1
            embed.add_field(name="Top 5 Users", value="\n".join(arr), inline=False)
            file=discord.File(f"sentAssets/guild{ctx.guild.id}-{datetime.datetime.now().date()}.png", filename=f"guild{ctx.guild.id}-{datetime.datetime.now().date()}.png")
            embed.set_image(url=f"attachment://guild{ctx.guild.id}-{datetime.datetime.now().date()}.png")
            await ctx.send(embed=embed, file=file)


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
        return []

cache = cache_init()

def setup(client):
    client.add_cog(Stats(client, cache))