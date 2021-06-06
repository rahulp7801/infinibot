from discord.ext import commands
import discord
from pymongo import MongoClient
import datetime
import time
import math
import asyncio
from modules import utils

with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

class Afk(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.icon = '<a:afk:849686005149466654>'
        self.description = f'Moderate your server or take a step back and let InfiniBot moderate for you!'

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return
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
            except UnboundLocalError:
                pass
            finally:
                collection.delete_one({'_id': message.author.id})

    @commands.group(invoke_without_command=True, help="Set an AFK status!")
    async def afk(self, ctx, *, message="Away"):
        await asyncio.sleep(0.5) #the on message event is invoked after this command for a strange reason, so the trigger activates
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
        embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{ctx.author.name} is now afk", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text="The AFK setting has been saved.")
        await ctx.send(embed=embed)
        try:
            return await member.edit(nick=f"[AFK] {cnick}")
        except discord.Forbidden:
            return

    @afk.command(help = 'Clear AFK status for a person.')
    @commands.has_permissions(manage_guild=True)
    async def clear(self, ctx, member: discord.Member):
        if ctx.author.guild_permissions.manage_messages:
            db = cluster[f'GUILD{ctx.guild.id}']
            collection = db['afk']
            query = {'_id': member.id}
            if collection.count_documents(query) == 0:
                return await ctx.send(f"{member.mention} hasn't set an AFK status in {ctx.guild.name}.")
            else:
                results = collection.find({'_id': member.id})
                for i in results:
                    nick = i['display_name']
                collection.delete_one({'_id': member.id})
                try:
                    await member.edit(nick=nick)
                except discord.Forbidden:
                    pass
                finally:
                    await ctx.send(f"AFK status for {member.mention} has been removed.")
        else:
            await ctx.send(f"{ctx.author.mention}, you don't have permission.")

    @afk.command(help = 'Clears all AFK statuses in a server.')
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 300, commands.BucketType.guild)
    async def clearall(self, ctx):
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

def setup(client):
    client.add_cog(Afk(client))