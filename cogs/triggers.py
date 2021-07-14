import datetime

from discord.ext import commands
from pymongo import MongoClient
import asyncio
import random

with open('mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

class Triggers(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.icon = '🚩'
        self.description = 'Set message triggers!'
        self.triggers = {}
        self.notready = True
        self.ischanging = {}

    @commands.Cog.listener()
    async def on_ready(self):
        db = cluster['TRIGGERS']
        col = db['guilds']
        res = col.find()
        trigarr = []
        for i in res:
            print(i)
            trigarr.append((i["trigger"], i["response"], i["gid"], i["setby"], i["seton"]))
        print(trigarr)

        for i in range(len(trigarr)):
            print(trigarr)
            print(i)
            print(trigarr[i])
            self.triggers[trigarr[i][2]] = []
            for k in range(len(trigarr[i][0])):
                self.triggers[trigarr[i][2]].append((trigarr[i][0][k], trigarr[i][1][k], trigarr[i][3][k], trigarr[i][4][k]))
        print(self.triggers)
        self.notready = False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or self.notready:
            return
        try:
            print(self.ischanging)
            if self.ischanging[message.guild.id]:
                return
        except LookupError:
            pass
        try:
            for k in self.triggers[message.guild.id]:
                print(k)
                if k[0] in message.content.lower():
                    return await message.channel.send(k[1])
        except KeyError:
            return

    @commands.command(help='Adds a trigger for the bot to listen to.')
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def addtrigger(self, ctx, *, trigger):
        self.ischanging[ctx.guild.id] = True
        name = f"TRIGGERS"
        db = cluster[name]
        collection = db['guilds']
        query = {'trigger': trigger.strip().lower(), 'gid':ctx.guild.id}
        if collection.count_documents(query) == 0:
            await ctx.send(f"Success! `{trigger.strip()}` has been added as a trigger for {ctx.guild.name}!\n\n"
                           f"What would you like the bot to respond with? **Must be content!**")
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                msg = await self.client.wait_for('message', check=check, timeout = 120)
                if len(msg.content.strip()) == 0:
                    self.ischanging = False
                    return await ctx.send("Somehow you managed to send an empty message, props to you!")
                settime = datetime.datetime.utcnow()
                setby = ctx.author.id + random.randint(12, 523412312312312312)
                if collection.count_documents({"gid":ctx.guild.id}) == 0:

                    ping_cm = {
                        "gid": ctx.guild.id,
                        "name": ctx.guild.name,
                        'trigger': [trigger.strip().lower()],
                        'response': [msg.content.strip()],
                        'setby':[setby],
                        'seton':[settime]
                    }
                    collection.insert_one(ping_cm)
                    self.triggers[ctx.guild.id] = [(trigger.strip().lower(), msg.content.strip(), ctx.author.id, settime)]
                else:
                    collection.update_one({"gid":ctx.guild.id}, {"$push": {"trigger":trigger.strip().lower()}})
                    collection.update_one({"gid": ctx.guild.id}, {"$push": {"response": msg.content.strip()}})
                    collection.update_one({"gid": ctx.guild.id}, {"$push": {"setby": setby}})
                    collection.update_one({"gid": ctx.guild.id}, {"$push": {"seton": settime}})
                    self.triggers[ctx.guild.id].append((trigger.strip().lower(), msg.content.strip(), setby, settime))
                self.ischanging[ctx.guild.id] = False
                return await ctx.send(f"Success! `{msg.content.strip()}` has been saved as the response for `{trigger.strip()}`!")
            except asyncio.TimeoutError:
                self.ischanging[ctx.guild.id] = False
                return await ctx.reply("Timed out", mention_author = False)
        elif collection.count_documents({"gid":ctx.guild.id}) >= 10:
            self.ischanging[ctx.guild.id] = False
            return await ctx.send(f"{ctx.guild.name} already has 10 triggers, remove one if you wish to create another.") #create donation thing here
        else:
            self.ischanging[ctx.guild.id] = False
            return await ctx.send(f"`{trigger.strip()}` already exists as a trigger for {ctx.guild.name}!")

    @commands.command(help='Removes a trigger for the bot to respond to.')
    @commands.has_permissions(manage_messages=True)
    async def removetrigger(self, ctx, *, trigger):
        self.ischanging[ctx.guild.id] = True
        name = f"TRIGGERS"
        db = cluster[name]
        collection = db['guilds']
        query = {'trigger': trigger.strip().lower(), 'gid': ctx.guild.id}
        x = collection.count_documents(query)
        if x == 0:
            self.ischanging[ctx.guild.id] = False
            return await ctx.send(f"It seems that `{trigger.strip()}` has not been saved in the database, double check that you spelled it right.")
        for k in self.triggers[ctx.guild.id]:
            if k[0] == trigger.strip().lower():
                stuff = self.triggers[ctx.guild.id].pop(self.triggers[ctx.guild.id].index((k[0], k[1], k[2], k[3])))
                break
        else:
            return await ctx.send("I could not find that trigger in my cache.")
        collection.update_one({"gid":ctx.guild.id}, {"$pull": {"trigger":stuff[0]}})
        collection.update_one({"gid": ctx.guild.id}, {"$pull": {"response": stuff[1]}})
        collection.update_one({"gid": ctx.guild.id}, {"$pull": {"setby": stuff[2]}})
        collection.update_one({"gid": ctx.guild.id}, {"$pull": {"seton": stuff[3]}})
        res = collection.find({"gid":ctx.guild.id})
        for i in res:
            triggers = i["trigger"]
        try:
            x = len(triggers)
        except:
            x = 0
        await ctx.send(f"Success! `{trigger.strip()}` has successfully been deleted from the database. You have {10-x} triggers remaining!")
        self.ischanging[ctx.guild.id] = False



def setup(client):
    client.add_cog(Triggers(client))