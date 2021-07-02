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
from modules import invitetrack



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

class Stats(commands.Cog, name = "Server Statistics"):

    def __init__(self, client, cache):
        self.client = client
        self.cache = cache
        self.icon = '📈'
        self.description = 'See comprehensive server statistics for your server!'
        self._tracker = invitetrack.InviteTracker(self.client)

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
            name = "STATS"
            db = cluster[name]
            collection = db['data']
            collection.insert_one({
                "messages": g["messages"],
                "userdiff": g["userdiff"],
                "vcsecdiff": g["vcsecdiff"],
                "engagedusers": g["engagedusers"],
                "timestamp": time.time(),
                "guildID": g["guildID"]
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

        inviter = await self._tracker.fetch_inviter(member)
        print(inviter.id)
        db = cluster['INVITES']
        col = db['guilds']
        if col.count_documents({'gid':member.guild.id, "userid":inviter.id}) == 0:
            payload = {
                'gid':member.guild.id,
                "userid": inviter.id,
                "invites": 1
            }
            col.insert_one(payload)
        else:
            res = col.find({'gid':member.guild.id, "userid":inviter.id})
            for i in res:
                _count = i["invites"]

            _newcount = _count + 1
            col.update_one({'gid':member.guild.id, "userid": inviter.id}, {'$set': {"invites":_newcount}})


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
        name = f"CONFIGURATION"
        db = cluster[name]
        collection = db['guilds']
        res = collection.find({'_id': member.guild.id})
        if before.channel and after.channel:
            if before.channel == after.channel:
                return
        elif before.channel and not after.channel:
            collection = cluster['STATS']['guilds']
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
            try:
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
            except UnboundLocalError:
                pass
    @commands.Cog.listener()
    async def on_ready(self):
        if (datetime.datetime.now().time().hour % 2 == 0):
            print(f'Uploading DB Data at: {datetime.datetime.now().time().hour + 2}:00, in {seconds_until(int(math.ceil(datetime.datetime.now().time().hour + 2 / 2.)), 0)}s')
            await asyncio.sleep(seconds_until(int(math.ceil(datetime.datetime.now().time().hour + 2 / 2.)), 0))
            self.update_database_stats.start()
        else:
            print(f'Uploading DB Data at: {math.ceil(datetime.datetime.now().time().hour + 0.01 / 2.)}:00, in {seconds_until(int(math.ceil(datetime.datetime.now().time().hour + 0.01 / 2.)), 0)}s')
            await asyncio.sleep(seconds_until(int(math.ceil(datetime.datetime.now().time().hour + 0.01 / 2.)), 0))
            self.update_database_stats.start()
        await self._tracker.cache_invites()

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        await self._tracker.update_invite_cache(invite)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        await self._tracker.remove_invite_cache(invite)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self._tracker.add_guild_cache(guild)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self._tracker.remove_guild_cache(guild)
    
    @commands.group(pass_context=True, invoke_without_command=True, help="")
    async def stats(self, ctx):
        embed = discord.Embed(title="Incorrect Usage",
            description=f'Please use one of the following subcommands:\n\n**general** *Aliases: g*\n**messages** *Aliases: m*',
            color=discord.Color.blurple())
        embed.set_footer(text=f"InfiniBot Help | Requested by {ctx.author.name}")
        await ctx.reply(embed=embed)
        pass

    @stats.command(aliases=['g'], help="View the General Stats of your Server")
    async def general(self, ctx):
        name = f"STATS"
        db = cluster[name]
        collection = db['guilds']
        results = collection.find({'_id': ctx.guild.id})
        for i in results:
            msgcount = i['msgcount']
        if msgcount == '':
            msgcount = 0
        collection = db['serverstats']
        results = collection.find({'_id': ctx.guild.id})
        for i in results:
            vcsecs = i['vcsecs']
        if vcsecs == '':
            vcsecs = 0

        collection = cluster['CONFIGURATION']["guilds"]
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
        ownerser = self.client.get_user(ctx.guild.owner_id)
        embed.add_field(name=f"Number of Ghost Pings", value=f"```{ghostcount}```", inline=False)
        embed.add_field(name="Server Owner:", value=ownerser.mention, inline=False)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name=f"{ctx.guild.name}'s Statistics", icon_url=ctx.guild.icon_url)
        embed.set_footer(text=f"Server ID: {ctx.guild.id}")
        await ctx.send(embed=embed)
        # add graphs https://www.tutorialspoint.com/graph-plotting-in-python
        pass
    
    @stats.command(aliases=['m'], help="View the Leadership Boards of Messages, and a Graph showing Messages Sent Over Time")
    @commands.check(is_dev)
    async def messages(self, ctx, timeframe=''):
        print('[STATS LOGGER]  Server Stats Requested')
        async with ctx.typing():

            db = cluster[f"STATS"] 
    
            col = db["data"] 
            msgcol = db["guilds"]

            cacheData = {
                "subID": [],
                "Messages": [],
                "Time": [],
            }

            cacheActiveUsers = []

            userMSGSDict = {}
            wTimeDict = {}

            msgdocs = msgcol.find_one({"_id": ctx.guild.id})
            msgcount = msgdocs["msgcount"]
      
            if timeframe == 'd' or timeframe == 'day' or timeframe == 'today':
                for x in col.find({"guildID": ctx.guild.id}): 
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
            elif timeframe == 'w' or timeframe == 'week' or timeframe == '':
                print('Getting Stats for Week')
                for x in col.find({"guildID": ctx.guild.id}): 
                    if (x["_id"] != ctx.guild.id):
                        if datetime.datetime.fromtimestamp(x["timestamp"]).isocalendar()[1] == datetime.datetime.today().isocalendar()[1]:
                            if datetime.datetime.fromtimestamp(x["timestamp"]).date().day in wTimeDict:
                                wTimeDict[datetime.datetime.fromtimestamp(x["timestamp"]).date().day]["Messages"] += x["messages"]
                                wTimeDict[datetime.datetime.fromtimestamp(x["timestamp"]).date().day]["Time"] = time.strftime('%m/%d', time.localtime(x["timestamp"]))
                            else:
                                wTimeDict[datetime.datetime.fromtimestamp(x["timestamp"]).date().day] = {"Messages": x["messages"], "Time": datetime.datetime.fromtimestamp(x["timestamp"]).date().day}
                            for member in x["engagedusers"]:
                                if member["uid"] in userMSGSDict:
                                    userMSGSDict[member["uid"]]["msgs"] += member["messagesSent"]
                                else:
                                    userMSGSDict[member["uid"]] = {"msgs": member["messagesSent"], "id": member["uid"]}
                for d in wTimeDict:
                    print('[STATS LOGGER] Adding Item to Cache... ')
                    cacheData["subID"].append(len(cacheData["subID"]))
                    cacheData["Messages"].append(wTimeDict[d]["Messages"])
                    cacheData["Time"].append(wTimeDict[d]["Time"])
            print('[STATS LOGGER] Done Gathering Data From Database')
            for u in userMSGSDict:
                cacheActiveUsers.append(userMSGSDict[u])

            cacheActiveUsers.sort(key=lambda x: x["msgs"], reverse=True)
            filePath = f'cache/guild{ctx.guild.id}-{datetime.datetime.now().date()}-stats.json'
            json_cache = open(filePath, 'w')
            json_cache.write(json.dumps(cacheData))
            json_cache.close()
            
            dataFile = open(filePath)
            df = pd.read_json(dataFile)
            df.set_index('subID', inplace=True)
            sns.reset_defaults()
            sns.set(
                rc={'figure.figsize':(7,5)}, 
            )
            plt.style.use("dark_background")
            sns.lineplot(data=df, x="Time", y="Messages")
            plt.gca().axes.xaxis.grid(False)
            plt.fill_between(df.Time.values, df.Messages.values, alpha=0.5)
            print('[STATS LOGGER] Standby...')
            plt.ylim(0,max(df.Messages) + 20)
            sns.despine(fig=None, ax=None, top=True, right=True, left=True, bottom=True, offset=None, trim=False)
            plt.xlabel(None)
            plt.ylabel(None)
            plt.savefig(f"cache/guild{ctx.guild.id}-{datetime.datetime.now().date()}.png", transparent=True)
            plt.close()
            print('[STATS LOGGER]  Server Graph Saved')
            embed=discord.Embed(url=f"http://localhost:3000/dashboard/server/{ctx.guild.id}/stats#", description=f"This is only from when I joined **{ctx.guild.name}**. Anything before that has not been documented. \n\nGo [here](http://infinibot.xyz/dashboard/server/{ctx.guild.id}/stats#) for further stats", color=0xff0000, timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Total Messages", value=f"In All: `{msgcount} messages`", inline=False)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_author(name=f"{ctx.guild.name}'s Message Statistics", icon_url=ctx.guild.icon_url)
            embed.set_footer(text=f"Server ID: {ctx.guild.id}")
            counter = 0
            arr = []
            for i in range((len(cacheActiveUsers)) if (len(cacheActiveUsers) <= 5) else 5):
                arr.append(f"`{counter + 1}.` <@!" + str(cacheActiveUsers[counter]["id"]) + ">: `" + str(
                    cacheActiveUsers[counter]["msgs"]) + " messages`")
                counter += 1
            embed.add_field(name="Top 5 Users", value="\n".join(arr), inline=False)
            file=discord.File(f"cache/guild{ctx.guild.id}-{datetime.datetime.now().date()}.png", filename=f"guild{ctx.guild.id}-{datetime.datetime.now().date()}.png")
            embed.set_image(url=f"attachment://guild{ctx.guild.id}-{datetime.datetime.now().date()}.png")
            await ctx.send(embed=embed, file=file)
            os.remove(filePath)
            os.remove(f"cache/guild{ctx.guild.id}-{datetime.datetime.now().date()}.png")

    @commands.command()
    async def invleaderboard(self, ctx):
        print('here')
        try:
            db = cluster['INVITES']
            col = db['guilds']
            if col.count_documents({'gid':ctx.guild.id}) == 0:
                return await ctx.send(f"I have not documented any invites in **{ctx.guild.name}**!")
            res = col.find({"gid":ctx.guild.id}).sort("invites", -1).limit(10)
            for i in res:
                print(i) #gtg
        except Exception as e:
            print(e)


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