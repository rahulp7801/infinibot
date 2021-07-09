import datetime

from discord.ext import commands
from pymongo import MongoClient
import asyncio

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
        self.ischanging = False

    '''
    Slows the bot down a lot, will be looking for a quicker way of implementation before deployment
    '''

    @commands.Cog.listener()
    async def on_ready(self):
        db = cluster['TRIGGERS']
        col = db['guilds']
        res = col.find()
        for i in res:
            triggers = i["trigger"]
            response = i["response"]
            gid = i["gid"]
        self.triggers[gid] = []
        for i in range(len(triggers)):
            self.triggers[gid].append((triggers[i], response[i]))
        self.notready = False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or self.notready or self.ischanging:
            return
        for k in self.triggers[message.guild.id]:
            if k[0] in message.content.lower():
                return await message.channel.send(k[1])

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def addtrigger(self, ctx, *, trigger):
        self.ischanging = True
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
                if collection.count_documents({"gid":ctx.guild.id}) == 0:
                    ping_cm = {
                        "gid": ctx.guild.id,
                        "name": ctx.guild.name,
                        'trigger': [trigger.strip().lower()],
                        'response': [msg.content.strip()],
                        'setby':[ctx.author.id],
                        'seton':[datetime.datetime.utcnow()]
                    }
                    collection.insert_one(ping_cm)
                    self.triggers[ctx.guild.id] = [(trigger.strip().lower(), msg.content.strip())]
                else:
                    collection.update_one({"gid":ctx.guild.id}, {"$push": {"trigger":trigger.strip().lower()}})
                    collection.update_one({"gid": ctx.guild.id}, {"$push": {"response": msg.content.strip()}})
                    collection.update_one({"gid": ctx.guild.id}, {"$push": {"setby": ctx.author.id}})
                    collection.update_one({"gid": ctx.guild.id}, {"$push": {"seton": datetime.datetime.utcnow()}})
                    self.triggers[ctx.guild.id].append((trigger.strip().lower(), msg.content.strip()))
                self.ischanging = False
                return await ctx.send(f"Success! `{msg.content.strip()}` has been saved as the response for `{trigger.strip()}`!")
            except asyncio.TimeoutError:
                self.ischanging = False
                return await ctx.reply("Timed out", mention_author = False)
        elif collection.count_documents({"gid":ctx.guild.id}) >= 10:
            self.ischanging = False
            return await ctx.send(f"{ctx.guild.name} already has 10 triggers, remove one if you wish to create another.") #create donation thing here
        else:
            self.ischanging = False
            return await ctx.send(f"`{trigger.strip()}` already exists as a trigger for {ctx.guild.name}!")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def removetrigger(self, ctx, *, trigger):
        self.ischanging = True
        name = f"TRIGGERS"
        db = cluster[name]
        collection = db['guilds']
        query = {'trigger': trigger.strip().lower(), 'gid': ctx.guild.id}
        x = collection.count_documents(query)
        if x == 0:
            self.ischanging = False
            return await ctx.send(f"It seems that `{trigger.strip()}` has not been saved in the database, double check that you spelled it right.")
        collection.update_one({"gid":ctx.guild.id}, {"$pull": {"trigger":trigger.strip().lower()}})
        res = collection.find()
        for i in res:
            triggers = i["trigger"]
        try:
            x = len(triggers)
        except:
            x = 0
        await ctx.send(f"Success! `{trigger.strip()}` has successfully been deleted from the database. You have {10-x} triggers remaining!")
        for k in self.triggers[ctx.guild.id]:
            if k[0] == trigger.strip().lower():
                self.triggers[ctx.guild.id].pop(self.triggers[ctx.guild.id].index((k[0], k[1])))
                break
        self.ischanging = False



def setup(client):
    client.add_cog(Triggers(client))