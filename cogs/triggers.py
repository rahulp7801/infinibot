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

    '''
    Slows the bot down a lot, will be looking for a quicker way of implementation before deployment
    '''
    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if message.author.bot:
    #         return
    #     name = f"GUILD{message.guild.id}"
    #     db = cluster[name]
    #     collection = db['commands']
    #     query = {'id': message.guild.id}
    #     if collection.count_documents(query) == 0:
    #         return
    #     results = collection.find({'id': message.guild.id})
    #     arr = []
    #     for i in results:
    #         arr.append((i['trigger'], i['response']))
    #     for k in arr:
    #         if k[0] in message.content.lower().strip():
    #             await message.channel.send(k[1])
    #             break
    #         else:
    #             continue

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def addtrigger(self, ctx, *, trigger):
        name = f"GUILD{ctx.guild.id}"
        db = cluster[name]
        collection = db['commands']
        query = {'trigger': trigger.strip().lower(), 'id':ctx.guild.id}
        if collection.count_documents(query) == 0:
            await ctx.send(f"Success! `{trigger.strip()}` has been added as a trigger for {ctx.guild.name}!\n\n"
                           f"What would you like the bot to respond with? **Must be content!**")
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                msg = await self.client.wait_for('message', check=check, timeout = 120)
                if len(msg.content.strip()) == 0:
                    return await ctx.send("Somehow you managed to send an empty message, props to you!")
                ping_cm = {
                    "id": ctx.guild.id,
                    "name": ctx.guild.name,
                    'trigger': trigger.strip().lower(),
                    'response': msg.content.strip()
                }
                collection.insert_one(ping_cm)
                return await ctx.send(f"Success! `{msg.content.strip()}` has been saved as the response for `{trigger.strip()}`!")
            except asyncio.TimeoutError:
                return await ctx.reply("Timed out", mention_author = False)
        elif collection.count_documents(query) > 10:
            return await ctx.send(f"{ctx.guild.name} already has 10 triggers, remove one if you wish to create another.") #create donation thing here
        else:
            return await ctx.send(f"`{trigger.strip()}` already exists as a trigger for {ctx.guild.name}!")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def removetrigger(self, ctx, *, trigger):
        name = f"GUILD{ctx.guild.id}"
        db = cluster[name]
        collection = db['commands']
        query = {'trigger': trigger.strip().lower(), 'id': ctx.guild.id}
        x = collection.count_documents(query)
        if x == 0:
            return await ctx.send(f"It seems that `{trigger.strip()}` has not been saved in the database, double check that you spelled it right.")
        collection.delete_one({'trigger': trigger.strip().lower(), 'id': ctx.guild.id})
        await ctx.send(f"Success! `{trigger.strip()}` has successfully been deleted from the database. You have {x - 1} triggers remaining!")



def setup(client):
    client.add_cog(Triggers(client))