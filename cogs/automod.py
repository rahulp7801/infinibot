
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

DISCORD_INVITE = r'discord(?:\.com|app\.com|\.gg)[\/invite\/]?(?:[a-zA-Z0-9\-]{2,32})'

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
        self.mass_mentions = []
        self.all_caps = []
        self.addressed = {}
        self.profguilds = []
        self.invitesblock = []
        self.spoilers = []
        self.blacklisted = []
        self.notready = True

    @commands.Cog.listener()
    async def on_ready(self):
        db = cluster["BLACKLIST"]
        col = db['channels']
        res = col.find({"type":'link'})
        for i in res:
            self.links_allowed.append(i["id"])
        res = col.find({"type":'image'})
        for i in res:
            self.images_allowed.append(i["id"])
        res = col.find({"type":'mention'})
        for i in res:
            self.mass_mentions.append(i["id"])
        res = col.find({"type": 'caps'})
        for i in res:
            self.all_caps.append(i["id"])
        res = col.find({"type": 'invite'})
        for i in res:
            self.invitesblock.append(i["id"])
        res = col.find({"type": 'spoiler'})
        for i in res:
            self.spoilers.append(i["id"])
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

        if not message.author.bot:
            try:
                if len(message.mentions) > 7 and message.channel.id in self.mass_mentions: #only checks for humans i guess
                    print('here sir')
                    #warn/mute/whateveraction
                    await message.reply("Warned for mass-mention.", delete_after = 20)
            except Exception as e:
                print(e)
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
            uppers = [l for l in message.clean_content if l.isupper() and l.isalpha()]
            if (len(message.clean_content) == len(uppers) and message.channel.id in self.all_caps): #all caps
                #custom action taken huh
                await message.channel.send("bruh stop the caps")
            if search(DISCORD_INVITE, message.content.lower()) and message.channel.id in self.invitesblock:
                await message.channel.send("No invites", delete_after = 20)
            if message.content.count('||') >= 6 and message.channel.id in self.spoilers:
                await message.channel.send("Too many spoilers.", delete_after = 20)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages = True)
    async def linktoggle(self, ctx, channel:Optional[discord.TextChannel], guild:Optional[bool]):
        if type(guild) == bool and not None:
            if guild:
                db = cluster["BLACKLIST"]
                col = db['channels']
                for i in ctx.guild.text_channels:
                    if col.count_documents({"id": i.id, "type":'link'}) == 0:
                        col.insert_one({"id": i.id, "type":'link'})
                        self.links_allowed.append(i.id)
                return await ctx.send("Success, added link blacklist to the server.")
            else:
                db = cluster["BLACKLIST"]
                col = db['channels']
                for i in ctx.guild.text_channels:
                    if col.count_documents({"id": i.id, "type":'link'}) != 0:
                        col.delete_one({'id':i.id, "type":'link'})
                        self.links_allowed.remove(i.id)
                return await ctx.send("Success, removed link blacklist for the server.")
        if channel is None:
            channel = ctx.channel
        db = cluster["BLACKLIST"]
        col = db['channels']
        if col.count_documents({"id":channel.id, "type":'link'}) == 0:
            col.insert_one({"id":channel.id, "type":'link'})
            await ctx.send(f"Success, added {channel.mention} to Link-detection")
            self.links_allowed.append(channel.id)
        else:
            col.delete_one({"id": channel.id, "type":'link'})
            await ctx.send(f"Success, removed {channel.mention} from Link-detection")
            self.links_allowed.remove(channel.id)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    async def imagetoggle(self, ctx, channel: Optional[discord.TextChannel], guild: Optional[bool]):
        if type(guild) == bool and not None:
            if guild:
                db = cluster["BLACKLIST"]
                col = db['channels']
                for i in ctx.guild.text_channels:
                    if col.count_documents({"id": i.id, "type":'image'}) == 0:
                        col.insert_one({"id": i.id, "type":'image'})
                        self.images_allowed.append(i.id)
                return await ctx.send("Success, added image blacklist to the server.")
            else:
                db = cluster["BLACKLIST"]
                col = db['channels']
                for i in ctx.guild.text_channels:
                    if col.count_documents({"id": i.id, "type":'image'}) != 0:
                        col.delete_one({'id': i.id, "type":'image'})
                        self.images_allowed.remove(i.id)
                return await ctx.send("Success, removed image blacklist for the server.")
        if channel is None:
            channel = ctx.channel
        db = cluster["BLACKLIST"]
        col = db['channels']
        if col.count_documents({"id": channel.id, "type":'image'}) == 0:
            col.insert_one({"id": channel.id, "type":'image'})
            await ctx.send(f"Success, added {channel.mention} to Image-detection")
            self.images_allowed.remove(channel.id)
        else:
            col.delete_one({"id": channel.id, "type":'image'})
            await ctx.send(f"Success, removed {channel.mention} from Image-detection")
            self.images_allowed.remove(channel.id)

    @commands.command(aliases=['bl', 'blackl'], help='Toggle the blacklisted word detection!')
    @commands.guild_only()
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

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    async def mentiontoggle(self, ctx, channel: Optional[discord.TextChannel], guild: Optional[bool]):
        if type(guild) == bool and not None:
            if guild:
                db = cluster["BLACKLIST"]
                col = db['channels']
                for i in ctx.guild.text_channels:
                    if col.count_documents({"id": i.id, "type": 'mention'}) == 0:
                        col.insert_one({"id": i.id, "type": 'mention'})
                        self.mass_mentions.append(i.id)
                return await ctx.send("Success, added mass-mention blacklist to the server.")
            else:
                db = cluster["BLACKLIST"]
                col = db['channels']
                for i in ctx.guild.text_channels:
                    if col.count_documents({"id": i.id, "type": 'mention'}) != 0:
                        col.delete_one({'id': i.id, "type": 'mention'})
                        self.mass_mentions.remove(i.id)
                return await ctx.send("Success, removed mass-mention blacklist for the server.")
        if channel is None:
            channel = ctx.channel
        db = cluster["BLACKLIST"]
        col = db['channels']
        if col.count_documents({"id": channel.id, "type": 'mention'}) == 0:
            col.insert_one({"id": channel.id, "type": 'mention'})
            await ctx.send(f"Success, added {channel.mention} to mass-mention blacklist.")
            self.mass_mentions.append(channel.id)
        else:
            col.delete_one({"id": channel.id, "type": 'mention'})
            await ctx.send(f"Success, removed {channel.mention} from mass-mention blacklist.")
            self.mass_mentions.remove(channel.id)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    async def capslock(self, ctx, channel: Optional[discord.TextChannel], guild: Optional[bool]):
        if type(guild) == bool and not None:
            if guild:
                db = cluster["BLACKLIST"]
                col = db['channels']
                for i in ctx.guild.text_channels:
                    if col.count_documents({"id": i.id, "type": 'caps'}) == 0:
                        col.insert_one({"id": i.id, "type": 'caps'})
                        self.all_caps.append(i.id)
                return await ctx.send("Success, added all-caps blacklist to the server.")
            else:
                db = cluster["BLACKLIST"]
                col = db['channels']
                for i in ctx.guild.text_channels:
                    if col.count_documents({"id": i.id, "type": 'caps'}) != 0:
                        col.delete_one({'id': i.id, "type": 'caps'})
                        self.all_caps.remove(i.id)
                return await ctx.send("Success, removed all-caps blacklist for the server.")
        if channel is None:
            channel = ctx.channel
        db = cluster["BLACKLIST"]
        col = db['channels']
        if col.count_documents({"id": channel.id, "type": 'caps'}) == 0:
            col.insert_one({"id": channel.id, "type": 'caps'})
            await ctx.send(f"Success, added {channel.mention} to all-caps detection")
            self.all_caps.append(channel.id)
        else:
            col.delete_one({"id": channel.id, "type": 'caps'})
            await ctx.send(f"Success, removed {channel.mention} from all-caps detection")
            self.all_caps.remove(channel.id)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    async def inviteblock(self, ctx, channel: Optional[discord.TextChannel], guild: Optional[bool]):
        if type(guild) == bool and not None:
            if guild:
                db = cluster["BLACKLIST"]
                col = db['channels']
                for i in ctx.guild.text_channels:
                    if col.count_documents({"id": i.id, "type": 'invite'}) == 0:
                        col.insert_one({"id": i.id, "type": 'invite'})
                        self.invitesblock.append(i.id)
                return await ctx.send("Success, added invite blacklist to the server.")
            else:
                db = cluster["BLACKLIST"]
                col = db['channels']
                for i in ctx.guild.text_channels:
                    if col.count_documents({"id": i.id, "type": 'invite'}) != 0:
                        col.delete_one({'id': i.id, "type": 'invite'})
                        self.invitesblock.remove(i.id)
                return await ctx.send("Success, removed invite blacklist for the server.")
        if channel is None:
            channel = ctx.channel
        db = cluster["BLACKLIST"]
        col = db['channels']
        if col.count_documents({"id": channel.id, "type": 'invite'}) == 0:
            col.insert_one({"id": channel.id, "type": 'invite'})
            await ctx.send(f"Success, added {channel.mention} to invite detection")
            self.invitesblock.append(channel.id)
        else:
            col.delete_one({"id": channel.id, "type": 'invite'})
            await ctx.send(f"Success, removed {channel.mention} from invite detection")
            self.invitesblock.remove(channel.id)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    async def spoilertoggle(self, ctx, channel: Optional[discord.TextChannel], guild: Optional[bool]):
        if type(guild) == bool and not None:
            if guild:
                db = cluster["BLACKLIST"]
                col = db['channels']
                for i in ctx.guild.text_channels:
                    if col.count_documents({"id": i.id, "type": 'spoiler'}) == 0:
                        col.insert_one({"id": i.id, "type": 'spoiler'})
                        self.spoilers.append(i.id)
                return await ctx.send("Success, added spoiler blacklist to the server.")
            else:
                db = cluster["BLACKLIST"]
                col = db['channels']
                for i in ctx.guild.text_channels:
                    if col.count_documents({"id": i.id, "type": 'spoiler'}) != 0:
                        col.delete_one({'id': i.id, "type": 'spoiler'})
                        self.spoilers.remove(i.id)
                return await ctx.send("Success, removed spoiler blacklist for the server.")
        if channel is None:
            channel = ctx.channel
        db = cluster["BLACKLIST"]
        col = db['channels']
        if col.count_documents({"id": channel.id, "type": 'spoiler'}) == 0:
            col.insert_one({"id": channel.id, "type": 'spoiler'})
            await ctx.send(f"Success, added {channel.mention} to spoiler-detection")
            self.spoilers.append(channel.id)
        else:
            col.delete_one({"id": channel.id, "type": 'spoiler'})
            await ctx.send(f"Success, removed {channel.mention} from spoiler-detection")
            self.spoilers.remove(channel.id)

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def statuscol(self, ctx):
        if str(ctx.author.status).strip() == 'idle':
            embed = discord.Embed(title='You are idle!', color=discord.Color.gold())
            await ctx.send(embed=embed)
        elif str(ctx.author.status).strip() == 'online':
            embed = discord.Embed(title='You are online!', color=discord.Color.green())
            await ctx.send(embed=embed)
        elif str(ctx.author.status).strip() == 'dnd':
            embed = discord.Embed(title='You are on do not disturb!', color=discord.Color.red())
            await ctx.send(embed=embed)
        elif str(ctx.author.status).strip() == 'invisible':
            embed = discord.Embed(title='You are on invis!', color=discord.Color.greyple())
            await ctx.send(embed=embed)
        elif str(ctx.author.status) == 'offline':
            embed = discord.Embed(title='You are offline!', color=discord.Color.greyple())
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Mod(client))