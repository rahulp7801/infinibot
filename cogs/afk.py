from discord.ext import commands
import discord
from pymongo import MongoClient
import datetime
import time
from modules import utils

with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

class afk(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def afk(self, ctx, *, message="Away"):
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
            await member.edit(nick=f"[AFK] {cnick}")
        except discord.Forbidden:
            pass

    @afk.command()
    @commands.has_permissions(manage_guild=True)
    async def clear(self, ctx, member: discord.Member = None):
        if member is None:
            embed = utils.errmsg(ctx)
            return await ctx.send(embed=embed)
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

    @afk.command()
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
    client.add_cog(afk(client))