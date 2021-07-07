
from asyncio import sleep
from datetime import datetime, timedelta
from re import search
from typing import Optional

import discord
from better_profanity import profanity
from discord import Embed, Member, NotFound, Object
from discord.utils import find
from discord.ext.commands import Cog, Greedy, Converter
from discord.ext.commands import CheckFailure, BadArgument
from discord.ext.commands import command, has_permissions, bot_has_permissions
from discord.ext import commands, tasks
from pymongo import MongoClient

with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

profanity.load_censor_words()

class BannedUser(Converter):
    async def convert(self, ctx, arg):
        if ctx.guild.me.guild_permissions.ban_members:
            if arg.isdigit():
                try:
                    return (await ctx.guild.fetch_ban(Object(id=int(arg)))).user
                except NotFound:
                    raise BadArgument

        banned = [e.user for e in await ctx.guild.bans()]
        if banned:
            if (user := find(lambda u: str(u) == arg, banned)) is not None:
                return user
            else:
                raise BadArgument
class Mod(Cog):
    def __init__(self, client):
        self.client = client
        self.url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        self.links_allowed = []
        self.images_allowed = []
        self.addressed = {}
        self.profguilds = []
        self.notready = True

    @commands.Cog.listener()
    async def on_ready(self):
        db = cluster["BLACKLIST"]
        col = db['channels-links']
        res = col.find()
        for i in res:
            self.links_allowed.append(i["_id"])
        col = db['channels-images']
        res = col.find()
        for i in res:
            self.images_allowed.append(i["_id"])
        db = cluster['CONFIGURATION']
        col = db['guilds']
        res = col.find()
        for i in res:
            if i["blacklistenab"] == 'on':
                self.profguilds.append(i["_id"])
        self.notready = False

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.client.is_ready() and self.notready:
            return
        def _check(m):
            return (m.author == message.author
                    and len(m.mentions)
                    and (datetime.utcnow() - m.created_at).seconds < 20
                    and m.channel == message.channel)

        if not message.author.bot: #add action
            print(message.channel.id)
            # if message.author.guild_permissions.manage_guild: return
            if len(list(filter(lambda m: _check(m), self.client.cached_messages))) >= 3:
                try:
                    if self.addressed[f"{message.guild.id}-{message.author.id}"]:
                        print("already addressed")
                except KeyError:
                    await message.channel.send("Don't spam mentions!", delete_after=20)
                    print('nice')
                    self.addressed[f"{message.guild.id}-{message.author.id}"] = True
                    await sleep(20)
                    del self.addressed[f"{message.guild.id}-{message.author.id}"]
            if profanity.contains_profanity(message.content) and message.guild.id in self.profguilds:
                await message.delete()
                await message.channel.send("You can't use that word here.", delete_after=10)
            if message.channel.id in self.links_allowed and search(self.url_regex, message.content.lower()):
                await message.delete()
                await message.channel.send("You can't send links in this channel.", delete_after=10)
            if (message.channel.id in self.images_allowed and any([hasattr(a, "width") for a in message.attachments])):
                await message.delete()
                await message.channel.send("You can't send images here.", delete_after=10)

    @commands.command()
    async def linktoggle(self, ctx, channel:Optional[discord.TextChannel], guild:Optional[bool]):
        if type(guild) == bool and not None:
            if guild:
                db = cluster["BLACKLIST"]
                col = db['channels-links']
                for i in ctx.guild.text_channels:
                    if col.count_documents({"_id": i.id}) == 0:
                        col.insert_one({"_id": i.id})
                        self.links_allowed.append(i.id)
                return await ctx.send("Success, added link blacklist to the server.")
            else:
                db = cluster["BLACKLIST"]
                col = db['channels-links']
                for i in ctx.guild.text_channels:
                    if col.count_documents({"_id": i.id}) != 0:
                        col.delete_one({'_id':i.id})
                        self.links_allowed.remove(i.id)
                return await ctx.send("Success, removed link blacklist for the server.")
        if channel is None:
            channel = ctx.channel
        db = cluster["BLACKLIST"]
        col = db['channels-links']
        if col.count_documents({"_id":channel.id}) == 0:
            col.insert_one({"_id":channel.id})
            await ctx.send(f"Success, added {channel.mention} to Link-detection")
        else:
            col.delete_one({"_id": channel.id})
            await ctx.send(f"Success, removed {channel.mention} from Link-detection")

    @commands.command()
    async def imagetoggle(self, ctx, channel: Optional[discord.TextChannel], guild: Optional[bool]):
        if type(guild) == bool and not None:
            if guild:
                db = cluster["BLACKLIST"]
                col = db['channels-images']
                for i in ctx.guild.text_channels:
                    if col.count_documents({"_id": i.id}) == 0:
                        col.insert_one({"_id": i.id})
                        self.links_allowed.append(i.id)
                return await ctx.send("Success, added image blacklist to the server.")
            else:
                db = cluster["BLACKLIST"]
                col = db['channels-links']
                for i in ctx.guild.text_channels:
                    if col.count_documents({"_id": i.id}) != 0:
                        col.delete_one({'_id': i.id})
                        self.links_allowed.remove(i.id)
                return await ctx.send("Success, removed image blacklist for the server.")
        if channel is None:
            channel = ctx.channel
        db = cluster["BLACKLIST"]
        col = db['channels-images']
        if col.count_documents({"_id": channel.id}) == 0:
            col.insert_one({"_id": channel.id})
            await ctx.send(f"Success, added {channel.mention} to Image-detection")
        else:
            col.delete_one({"_id": channel.id})
            await ctx.send(f"Success, removed {channel.mention} from Image-detection")

    @commands.command(aliases=['bl', 'blackl'], help='Toggle the blacklisted word detection!')
    @commands.has_permissions(manage_guild=True)
    async def blacklist(self, ctx, enab: bool = False):
        db = cluster['CONFIGURATON']
        collection = db['guilds']
        if str(enab).lower() not in ['true', 'false']:
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                return await ctx.send("An error occurred, contact the developers immediately.")
            res = collection.find(query)
            for i in res:
                blak = i['blacklistenab']
            if blak == '':
                return await ctx.send("This server has not set up a blacklist yet!")
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'blacklistenab': ''}})
            try:
                self.profguilds.remove(ctx.guild.id)
            except:
                pass
            return await ctx.send("The blacklist for this server has successfully been removed.")
        if ctx.message.author.guild_permissions.manage_messages:
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'blacklistenab': f"{'on' if enab else ''}"}})
            try:
                self.profguilds.append(ctx.guild.id) if enab else self.profguilds.remove(ctx.guild.id)
            except:
                pass
            return await ctx.send(f"Blacklist for {ctx.guild.name} has been toggled to {'on' if enab else 'off'}!")
        else:
            await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
            return


def setup(client):
    client.add_cog(Mod(client))