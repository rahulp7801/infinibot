import discord
from discord.ext import commands
import asyncio
from pymongo import MongoClient
import datetime
from PIL import Image, ImageDraw, ImageFont
import random
from discord_components import DiscordComponents
from modules import utils

with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

class Configuration(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.icon = '⚙'
        self.description = f'Setup InfiniBot for your server!'

    @commands.Cog.listener()
    async def on_ready(self):
        DiscordComponents(self.client, change_discord_methods=True)


    @commands.group(invoke_without_command = True, help = "Set up the bot for your server!")
    @commands.guild_only()
    async def setup(self, ctx):
        return await utils.send_command_help(ctx)

    @setup.command(help='Shows a list of all setup commands.')
    async def list(self, ctx):
        prefix = utils.serverprefix(ctx)
        embed = discord.Embed(title="Available Setup Commands for InfiniBot", color=discord.Color.greyple())
        embed.add_field(name=f"{prefix}setup welcomechannel <#channel>",
                        value="Set the server\'s welcome channel! All welcome messages will be sent to this channel.",
                        inline=False)
        embed.add_field(name=f"{prefix}setup welcometext <message>",
                        value="Set a custom welcome message to be sent in the specified welcome channel.\nAvailable parameters: {membercount}, {guild}, {user}, {mention}",
                        inline=False)
        embed.add_field(name=f"{prefix}setup privset <message>",
                        value="Set a custom welcome message to be sent in DMs to the new user. \nAvailable parameters: {members}, {guild}, {user}, {mention}",
                        inline=False)
        embed.add_field(name=f"{prefix}setup welcomerole <Role>",
                        value="Set a custom welcome role to be added to the new user. \n**NOTE: Role name is case-sensitive**",
                        inline=False)
        embed.add_field(name=f"{prefix}setup captcha <True or False>",
                        value=f"Set a captcha that the user has to solve before being verified. \n**NOTE: Role name MUST be set first using {prefix}setup welcomerole <Role>**",
                        inline=False)
        embed.add_field(name=f"{prefix}setup muterole <optional name>",
                        value="Create and set a muterole for the server.",
                        inline=False)
        embed.add_field(name=f"{prefix}setup leavemsg <message>",
                        value="Set a custom leave message that will be sent into the same channel as the welcome message.",
                        # add an option for changing the channel in the future.
                        inline=False)
        embed.add_field(name=f"{prefix}setup spamdetection <True or False>",
                        value="Set spam detection on, when if the user does not have the Manage Messages permission, they will be muted. \n**NOTE: Muterole must be set prior to usage of this command!**",
                        inline=False)
        embed.add_field(name=f"{prefix}setup logs <#channel> <True or False>",
                        value="Set up logs to a specific channel. **MAKE SURE I HAVE PERMISSION TO READ MESSAGES, SEND MESSAGES, AND EMBED LINKS. ",
                        inline=False)
        embed.add_field(name=f"{prefix}setup ghostping <True or False>",
                        value="Set up anti-ghost pinging. Works when the message is deleted or edited. Sends a message in the chat the ping was sent in.",
                        inline=False)
        embed.set_footer(text=f"InfiniBot Server Greetings Help | Requested by: {ctx.author.name}",
                         icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @setup.command(help='Setup a channel for welcome messages!')
    @commands.has_permissions(manage_messages=True)
    async def welcomechannel(self, ctx, channel: discord.TextChannel = None):
        db = cluster['CONFIGURATON']
        if channel is None:
            collection = db['guilds']
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                return await ctx.send("An error occurred, contact the developers immediately.")
            res = collection.find(query)
            for i in res:
                welcomechannel = i['welcomechannel']
            if welcomechannel == '':
                return await ctx.send("This server has not set a welcome channel yet!")
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'welcomechannel': ''}})
            return await ctx.send("The welcome channel for this server has successfully been removed.")
        if ctx.message.author.guild_permissions.manage_messages:
            res = utils.channelperms(channel)
            if not res:
                return await ctx.send(
                    f"Please give me permission to `View Channel`, `Send Messages`, and `Embed Links` in {channel.mention} before proceeding.\n")

            if channel.is_nsfw():
                return await ctx.send(
                    f"{channel.mention} is marked as NSFW, so I cannot send welcome messages in this channel.")
            collection = db['guilds']
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                utils.add_guild_to_db(ctx.guild)
            collection.update_one({'_id':ctx.guild.id}, {'$set': {'welcomechannel':channel.id}})
            return await ctx.send(f"{channel.mention} has been set as the welcome channel for {ctx.guild.name}!")
        else:
            await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
            return

    @setup.command(aliases=['welcomemsg', 'welcomemessage'], help='Setup text for welcome messages!')
    @commands.has_permissions(manage_messages=True)
    async def welcometext(self, ctx, *, text: str = None):
        db = cluster['CONFIGURATON']
        if text is None:
            collection = db['guilds']
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                return await ctx.send("An error occurred, contact the developers immediately.")
            res = collection.find(query)
            for i in res:
                welcometext = i['welcomemsg']
            if welcometext == '':
                return await ctx.send("This server has not set a welcome message yet!")
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'welcomemsg': ''}})
            return await ctx.send("The welcome message for this server has successfully been removed.")
        membercount = ctx.guild.member_count
        member = ctx.author.mention
        user = ctx.author.name
        guild = ctx.guild.name
        if len(text) > 2000:
            return await ctx.send(f"I cannot send this message due to discord limitations.")
        if ctx.message.author.guild_permissions.manage_messages:
            collection = db['guilds']
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                ping_cm = {
                    "_id": ctx.guild.id,
                    "name": ctx.guild.name,
                    "welcomemsg": text.strip()
                }
                collection.insert_one(ping_cm)
            else:
                collection.update_one({'_id': ctx.guild.id}, {'$set': {'welcomemsg': text.strip()}})
            embed = discord.Embed(
                description=str(text).format(members=membercount, member=member, user=user, guild=guild),
                color=discord.Color.blurple(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f'{ctx.author.name} just joined the server!', icon_url=f'{ctx.author.avatar_url}')
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(content=f"Message has been set to {text}. EXAMPLE:", embed=embed)

    @setup.command(aliases=['welcomenick', 'welconickname'], help = 'Setup a nickname for users to get on join!')
    @commands.has_permissions(manage_nicknames=True)
    async def onjoinnick(self, ctx, *, nick=None):
        db = cluster['CONFIGURATON']
        if nick is None:
            collection = db['guilds']
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                return await ctx.send("An error occurred, contact the developers immediately.")
            res = collection.find(query)
            for i in res:
                welcomenick = i['welcomenick']
            if welcomenick == '':
                return await ctx.send("This server has not set a welcome nickname yet!")
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'welcomenick': ''}})
            return await ctx.send("The welcome nickname for this server has successfully been removed.")
        if len(nick.strip()) > 20:
            return await ctx.send(f"I cannot set this nickname due to Discord limitations.")
        collection = db['guilds']
        query = {'_id': ctx.guild.id}
        if collection.count_documents(query) == 0:
            utils.add_guild_to_db(ctx.guild)
        collection.update_one({'_id': ctx.guild.id}, {'$set': {'welcomenick': nick.strip()}})
        return await ctx.send(f"The welcomenick for {ctx.guild.name} has been updated to {nick.strip()}")

    @setup.command(aliases=['minecraftip'], help = 'Set a Minecraft IP!')
    @commands.has_permissions(manage_guild = True)
    async def mcip(self, ctx, *, text: str = None):
        db = cluster['CONFIGURATON']
        if text is None:
            collection = db['guilds']
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                return await ctx.send("An error occurred, contact the developers immediately.")
            res = collection.find(query)
            for i in res:
                mcip = i['mcip']
            if mcip == '':
                return await ctx.send("This server has not set a Minecraft IP yet!")
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'mcip': ''}})
            return await ctx.send("The Minecraft IP for this server has successfully been removed.")
        if ctx.message.author.guild_permissions.manage_messages:
            collection = db['config']
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                utils.add_guild_to_db(ctx.guild)
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'mcip': text.strip()}})
            return await ctx.send(f"The Minecraft IP for {ctx.guild.name} has been updated to {text.strip()}")
        else:
            await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
            return

    @setup.command(aliases=['XP', 'levelups'], help = 'Enable leveling!')
    @commands.has_permissions(manage_guild = True)
    async def levels(self, ctx, enab=True):
        db = cluster['CONFIGURATON']
        collection = db['guilds']
        if str(enab).lower() not in ['true', 'false']:
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                return await ctx.send("An error occurred, contact the developers immediately.")
            res = collection.find(query)
            for i in res:
                levels = i['levelups']
            if levels == '':
                return await ctx.send("This server has not set up leveling yet!")
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'levelups': ''}})
            return await ctx.send("Leveling for this server has successfully been removed.")
        if ctx.message.author.guild_permissions.manage_messages:
            collection = db['config']
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                utils.add_guild_to_db(ctx.guild)
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'levelups': f"{'on' if enab else ''}"}})
            return await ctx.send(
                f"Levelups have been toggled to `{'on' if enab else 'off'}` for {ctx.guild.name}!")
        else:
            await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
            return

    @setup.command(aliases=['antighostping', 'antighost', 'ghostpingdetection'], help='Setup ghostping detection!')
    @commands.has_permissions(manage_guild = True)
    async def ghostping(self, ctx, enab=True):
        db = cluster['CONFIGURATON']
        collection = db['guilds']
        if str(enab).lower() not in ['true', 'false']:
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                return await ctx.send("An error occurred, contact the developers immediately.")
            res = collection.find(query)
            for i in res:
                ghost = i['ghostpingon']
            if ghost == '':
                return await ctx.send("This server has not set up ghost ping detection yet!")
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'ghostpingon': ''}})
            return await ctx.send("Ghost ping detection for this server has successfully been removed.")
        if ctx.message.author.guild_permissions.manage_messages:
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                utils.add_guild_to_db(ctx.guild)
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'ghostpingon': f"{'on' if enab else ''}"}})
            return await ctx.send(
                f"Ghostpings have been toggled to `{'on' if enab else 'off'}` for {ctx.guild.name}!")
        else:
            await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
            return

    @setup.command(aliases=['dmset', 'privmsg', 'privset', 'privatemsg', 'privatemessage', 'dmmsg', 'dmsg'], help = 'Set up a private DM message for when a member joins!')
    @commands.has_permissions(manage_guild = True)
    async def privatewelcomemessage(self, ctx, *, text: str = None):
        db = cluster['CONFIGURATON']
        collection = db['guilds']
        if text is None:
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                return await ctx.send("An error occurred, contact the developers immediately.")
            res = collection.find(query)
            for i in res:
                privmsg = i['priv_welcomemsg']
            if privmsg == '':
                return await ctx.send("This server has not set a private welcome message yet!")
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'priv_welcomemsg': ''}})
            return await ctx.send("The private welcome message for this server has successfully been removed.")
        membercount = ctx.guild.member_count
        mention = ctx.author.mention
        user = ctx.author.name
        guild = ctx.guild.name
        if ctx.message.author.guild_permissions.manage_messages:
            collection = db['config']
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                utils.add_guild_to_db(ctx.guild)
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'priv_welcomemsg': text.strip()}})
            embed = discord.Embed(
                description=str(text).format(members=membercount, mention=mention, user=user, guild=guild),
                color=discord.Color.blurple(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f'Welcome to {ctx.guild.name}!', icon_url=f'{ctx.guild.icon_url}')
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(content=f"Welcome DM has been updated to ```{text}```", embed=embed)
        else:
            await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
            return

    @setup.command(help = 'Set a role to be given when a user joins your server!')
    @commands.has_permissions(manage_guild = True)
    async def welcomerole(self, ctx, *, role: discord.Role = None):
        db = cluster['CONFIGURATON']
        collection = db['guilds']
        if role is None:
            query = {'_id':ctx.guild.id}
            if collection.count_documents(query) == 0:
                return await ctx.send("An error occurred, contact the developers immediately.")
            res = collection.find(query)
            for i in res:
                welcomerole = i['welcomerole']
            if welcomerole == '':
                return await ctx.send("This server has not set a welcome role yet!")
            collection.update_one({'_id':ctx.guild.id}, {'$set' : {'welcomerole' : ''}})
            return await ctx.send("The welcomerole for this server has successfully been removed.")

        if ctx.message.author.guild_permissions.manage_messages:
            rolez = discord.utils.get(ctx.guild.roles, name=role.name)
            res = utils.rolecheck(rolez, ctx)
            if not res:
                return await ctx.send(res[1])
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                utils.add_guild_to_db(ctx.guild)
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'welcomerole': role.id}})
            desc = f'Welcome role: **{role.mention}**\n\n' \
                   f'Make sure that **{role.mention}** is the exact name of the role, as it is case-sensitive. \nUse the command again if you wish to update.\n\n' \
                   f'Also, please make my highest role higher than **{role.mention}** so I can assign it.'
            embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f'{self.client.user.name} Welcomer', icon_url=self.client.user.avatar_url)
            embed.set_footer(text="InfiniBot Welcomer")
            await ctx.reply(embed=embed)
            return
        else:
            await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
            return

    @setup.command(aliases=['bl', 'blackl'], help = 'Toggle the blacklisted word detection!')
    @commands.has_permissions(manage_guild = True)
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
            return await ctx.send("The blacklist for this server has successfully been removed.")
        if ctx.message.author.guild_permissions.manage_messages:
            collection = db['config']
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                utils.add_guild_to_db(ctx.guild)
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'blacklistenab': f"{'on' if enab else ''}"}})
            return await ctx.send(f"Blacklist for {ctx.guild.name} has been toggled to {'on' if enab else 'off'}!")
        else:
            await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
            return

    @setup.command(aliases=['byemsg', 'leavemessage', 'leavemsg'], help = 'Setup a leave message.')
    @commands.has_permissions(manage_guild = True)
    async def goodbyemsg(self, ctx, *, text: str = None):
        db = cluster['CONFIGURATON']
        collection = db['guilds']
        if text is None:
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                return await ctx.send("An error occurred, contact the developers immediately.")
            res = collection.find(query)
            for i in res:
                leavemsg = i['leavemsg']
            if leavemsg == '':
                return await ctx.send("This server has not set a leave message yet!")
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'leavemsg': ''}})
            return await ctx.send("The leave message for this server has successfully been removed.")
        if ctx.message.author.guild_permissions.manage_messages:
            collection = db['config']
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                utils.add_guild_to_db(ctx.guild)
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'leavemsg': text.strip()}})
            await ctx.send(
                f"The goodbye message for {ctx.guild.name} has been updated to {text.strip()}! \nExample Usage:")
            membercount = ctx.guild.member_count
            mention = ctx.author.mention
            user = ctx.author.name
            guild = ctx.guild.name
            embed = discord.Embed(
                description=str(text).format(members=membercount, mention=mention, user=user, guild=guild),
                color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=f'{ctx.author.avatar_url}')
            embed.set_author(name=f'{ctx.author.name} just left the server.', icon_url=f'{ctx.author.avatar_url}')
            embed.set_footer(text=f"User ID: {ctx.author.id}")
            await ctx.send(embed=embed)

        else:
            await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
            return

    @setup.command(aliases=['starchannel', 'starchan'], help = 'Setup a starboard channel.')
    @commands.has_permissions(manage_guild = True)
    async def starboardchannel(self, ctx, channel: discord.TextChannel = None):
        db = cluster['CONFIGURATON']
        collection = db['guilds']
        if channel is None:
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                return await ctx.send("An error occurred, contact the developers immediately.")
            res = collection.find(query)
            for i in res:
                star = i['starchannel']
            if star == '':
                return await ctx.send("This server has not set a starboard channel yet!")
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'starchannel': ''}})
            return await ctx.send("The starboard channel for this server has successfully been removed.")
        if ctx.message.author.guild_permissions.manage_messages:
            res = utils.channelperms(channel)
            if not res:
                return await ctx.send(
                    f"Please give me permission to `View Channel`, `Send Messages`, and `Embed Links` in {channel.mention} before proceeding.")
            collection = db['config']
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                utils.add_guild_to_db(ctx.guild)
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'starchannel': channel.id}})
            await ctx.send(
                f"The starboard channel for {ctx.guild.name} has been updated to {channel.mention}!")
        else:
            await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
            return

    @setup.command(aliases=['servercaptcha'], help = 'Set a captcha that users need to solve before verifying!')
    @commands.has_permissions(manage_guild = True)
    async def captcha(self, ctx, text: bool = True):
        db = cluster['CONFIGURATON']
        collection = db['guilds']
        if str(text).lower() not in ['true', 'false']:
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                return await ctx.send("An error occurred, contact the developers immediately.")
            res = collection.find(query)
            for i in res:
                capt = i['captchaon']
            if capt == '':
                return await ctx.send("This server has not set up captcha yet!")
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'captchaon': ''}})
            return await ctx.send("Server captcha for this server has successfully been removed.")
        if text is None:
            return
        if ctx.message.author.guild_permissions.manage_messages:
            collection = db['config']
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                utils.add_guild_to_db(ctx.guild)
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'captchaon': f"{'on' if text else ''}"}})
            await ctx.send(
                f"Server captcha for {ctx.guild.name} has been toggled to {'on' if text else 'off'}!")
        else:
            await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
            return

    @setup.command(aliases=['spamdetect'], help = 'Setup spam detection!')
    @commands.has_permissions(manage_guild = True)
    async def spamdetection(self, ctx, text: bool = False):
        db = cluster['CONFIGURATON']
        collection = db['guilds']
        if str(text).lower() not in ['true', 'false']:
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                return await ctx.send("An error occurred, contact the developers immediately.")
            res = collection.find(query)
            for i in res:
                spamd = i['spamdetect']
            if spamd == '':
                return await ctx.send("This server has not set up spam detection yet!")
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'spamdetect': ''}})
            return await ctx.send("Spam detection for this server has successfully been removed.")
        if text is None:
            return
        if ctx.message.author.guild_permissions.manage_messages:
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                utils.add_guild_to_db(ctx.guild)
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'spamdetect': f"{'on' if text else ''}"}})
            await ctx.send(
                f"Spam detection for {ctx.guild.name} has been toggled to {'on' if text else 'off'}!")
        else:
            await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
            return

    @setup.command(aliases=['logs', 'log'], help = 'Setup logging!')
    @commands.has_permissions(manage_guild = True)
    async def logging(self, ctx, setup: bool = True, channel: discord.TextChannel = None):
        db = cluster['CONFIGURATON']
        collection = db['guilds']
        if str(setup).lower() not in ['true', 'false']:
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                return await ctx.send("An error occurred, contact the developers immediately.")
            res = collection.find(query)
            for i in res:
                logchannel = i['logchannel']
                logging = i['logging']
            if logchannel == '' or logging == '':
                return await ctx.send("This server has not set up logging yet!")
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'logging': ''}})
            return await ctx.send("Logging for this server has successfully been removed.")
        if channel is None:
            if not setup:
                query = {'_id': ctx.guild.id}
                if collection.count_documents(query) == 0:
                    utils.add_guild_to_db(ctx.guild)
                collection.update_one({'_id': ctx.guild.id}, {'$set': {'logging': f"{'on' if setup else ''}"}})
                return await ctx.send(
                    f"Logging for {ctx.guild.name} has been toggled to {'on' if setup else 'off'}!")

            embed = utils.errmsg(ctx)
            return await ctx.send(embed=embed)

        if ctx.message.author.guild_permissions.manage_messages:
            res = utils.channelperms(channel)
            if not res:
                return await ctx.send(
                    f"Please give me permission to `View Channel`, `Send Messages`, and `Embed Links` in {channel.mention} before proceeding.")
            if channel.is_nsfw():
                return await ctx.send(f"{channel.mention} is an NSFW channel, so I cannot send log messages here.")
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                utils.add_guild_to_db(ctx.guild)
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'logging': f"{'on' if setup else ''}"}})
            await ctx.send(
                f"Logging for {ctx.guild.name} has been toggled to {'on' if setup else 'off'}!")
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                utils.add_guild_to_db(ctx.guild)
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'logchannel': channel.id}})
            return await ctx.send(
                f"Logging channel for {ctx.guild.name} has been updated to {channel.mention}!")
        else:
            await ctx.reply(f'**{ctx.author.name}**, you don\'t have permission.', mention_author=False)
            return

    @setup.command(help  = 'Define a muterole!')
    @commands.has_permissions(manage_roles = True)
    async def muterole(self, ctx, *, name="Muted"):
        if len(name) > 20:
            return await ctx.send(f"Make sure that `{name}` is kept under 20 characters.")
        db = cluster['CONFIGURATON']
        collection = db['guilds']
        if ctx.author.guild_permissions.manage_roles:
            message = await ctx.send("Updating channel overrides...")
            skipcount = 0
            mutedRole = await ctx.guild.create_role(name=name)
            for channel in ctx.guild.channels:
                if str(channel.type).lower() == 'category':
                    continue
                if str(channel.type).lower() == 'text':
                    try:
                        await channel.set_permissions(mutedRole, send_messages=False)
                    except discord.Forbidden:
                        skipcount += 1
                        continue
                if str(channel.type).lower() == 'voice':
                    continue
            query = {'_id': ctx.guild.id}
            if collection.count_documents(query) == 0:
                utils.add_guild_to_db(ctx.guild)
            collection.update_one({'_id': ctx.guild.id}, {'$set': {'muterole': mutedRole.id}})
            await ctx.send(
                f"The muterole for {ctx.guild.name} has been updated to {mutedRole.mention}! With {skipcount} channel{'' if skipcount == 1 else 's'} skipped.")

    @commands.command(help = 'Change the prefix!')
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def changeprefix(self, ctx, prefix):
        try:
            if len(prefix) > 10:
                return await ctx.reply(f"The prefix `{prefix}` is larger than 10 characters.", mention_author=False)
            if prefix == "":
                return await ctx.reply("You must specify a prefix!", mention_author=False)
            if prefix.startswith(" "):
                return await ctx.reply(
                    f"The prefix `{prefix}` starts with a space. Rerun the command, and don't put a space next time.",
                    mention_author=False)
            if ('@everyone' or '@here') in prefix:
                await ctx.send("Bruh seriously")
                return
            try:
                prefix = prefix.strip()
            except Exception as e:
                print(e)
                pass

            db = cluster['CONFIGURATION']
            collection = db['guilds']
            collection.update_one({"_id": ctx.guild.id}, {"$set": {'prefix': str(prefix)}})
            x = utils.imgdraw(photo='./Images/prefiximg.png', font = 'arial.ttf', fontsize=15, xy=(75, 45), text=f"{prefix}tinyurl https://www.youtube.com/watch?v=dQw4w9WgXcQ", rgb=(255, 255, 255))
            desc = f"Prefix for **{ctx.guild.name}** has been updated to `{prefix}`. \n\n**NOTE:** If you want a word prefix with a space after it, you must surround it in quotes due to a Discord limitation.\n\nEXAMPLE: {prefix}changeprefix \"yo \""
            embed = discord.Embed(description=desc, color=discord.Color.green())
            embed.set_thumbnail(url=ctx.guild.icon_url)
            file = discord.File("./profile.png", filename='image.png')
            embed.set_image(url='attachment://image.png')
            await ctx.send(file=file, embed=embed)
        except Exception as e:
            print(e)

    @setup.command(help='Setup all of the setup commands in one, interactive session!')
    @commands.cooldown(1, 90000, commands.BucketType.guild)
    @commands.guild_only()
    @commands.has_permissions(manage_guild = True)
    async def all(self, ctx):
        db = cluster['CONFIGURATON']
        collection = db['guilds']
        try:
            desc = f"Hi {ctx.author.mention}, welcome to the all-in-one setup for {self.client.user.name}! Just take 5 minutes to complete this setup, and leave your server in the hands of {self.client.user.name}." \
                   f"To begin, react with the ✅. At any point in time if you would like to cancel, react with the ❌. \nReady to get started? Hit the checkmark below!"
            embed = discord.Embed(description = desc, color = discord.Color.green())
            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')
            await message.add_reaction('❌')

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌']
            reaction, user = await self.client.wait_for('reaction_add', check=check, timeout = 100)
            if reaction.emoji == '❌':
                desc = f"Thanks for using {self.client.user.name}!"
                embed = discord.Embed(description = desc, color = discord.Color.green())
                await message.edit(embed=embed)
                return await message.clear_reactions()
            await message.clear_reactions()
            while True:
                desc = f"We will begin by setting up a welcome message. \nReact with the ✅ if you would like to set this part up. If you don't want to set this up, react with the ⏩. If you want to cancel, react with " \
                       f"the ❌. React with ⏩ to skip."
                embed = discord.Embed(title = "Welcomer", description = desc, color = discord.Color.green())
                await message.edit(embed=embed)
                await message.add_reaction('✅')
                await message.add_reaction('⏩')
                await message.add_reaction('❌')

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌', '⏩']
                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout = 30)
                if reaction.emoji == '❌':
                    desc = f"Thanks for using {self.client.user.name}!"
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    return await message.clear_reactions()
                elif reaction.emoji == '⏩':
                    desc = "Skipping welcome message setup..."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    await asyncio.sleep(3)
                    break
                elif reaction.emoji == '✅':
                    while True:
                        desc = f"Great, we will be setting a welcome message! Please type the message in the chat below. \n\n**NOTE: Message must be under 2000 characters!**\n" \
                               f"PARAMETERS:\n" \
                               "{guild} -> a variable that is replaced with your server's name.\n" \
                               "{members} -> a variable that is replaced with the number of members in a server.\n" \
                               "{member} -> a variable that is replaced with an @mention of the user.\n" \
                               "{user} -> a variable that is replaced with the user's username.\n\n" \
                               "EXAMPLE: Hey {user}, welcome to {guild}!"
                        embed = discord.Embed(description=desc, color=discord.Color.green())
                        await message.edit(embed=embed)
                        await message.clear_reactions()

                        def check(m):
                            return m.author == ctx.author and m.channel == ctx.channel

                        msg = await self.client.wait_for('message', check=check, timeout=300)
                        try:
                            await msg.delete()
                        except discord.Forbidden:
                            pass
                        if len(msg.content) > 2000:
                            # nitro users :(
                            desc = f"Your message was longer than 2000 characters! `{len(msg.content)}` > 2000. \nPlease start over from the beginning."
                            embed = discord.Embed(description=desc, color=discord.Color.red())
                            return await message.edit(embed=embed)
                        membercount = ctx.guild.member_count
                        member = ctx.author.mention
                        user = ctx.author.name
                        guild = ctx.guild.name
                        embed = discord.Embed(
                            description=str(msg.content.strip()).format(members=membercount, member=member, user=user,
                                                                        guild=guild) + "\n\nIf you like "
                                                                                       "this format, react with the ✅. React with the ❌ to cancel. Or react with the ◀ to go back.",
                            color=discord.Color.blurple(), timestamp=datetime.datetime.utcnow())
                        embed.set_author(name=f'{ctx.author.name} just joined the server!',
                                         icon_url=f'{ctx.author.avatar_url}')
                        embed.set_thumbnail(url=ctx.author.avatar_url)
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        await message.add_reaction('✅')
                        await message.add_reaction('❌')
                        await message.add_reaction('◀️')

                        def check(reaction, user):
                            return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌', '◀️']

                        reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=180)
                        if reaction.emoji == '✅':

                            if ctx.message.author.guild_permissions.manage_messages:
                                query = {'_id': ctx.guild.id}
                                if collection.count_documents(query) == 0:
                                    utils.add_guild_to_db(ctx.guild)
                                collection.update_one({'_id': ctx.guild.id},
                                                      {'$set': {'welcomemsg': msg.content.strip()}})
                                desc = f"Success! Your welcome message has been saved and will apply as soon as setup is complete. Moving on ..."
                                embed = discord.Embed(description=desc, color=discord.Color.green())
                                await message.edit(embed=embed)
                                await message.clear_reactions()
                                await asyncio.sleep(3)
                                break
                                # continue from here!
                        elif reaction.emoji == '❌':
                            # create a go back thing here
                            desc = f"The welcome message has not been saved and setup has been cancelled."
                            embed = discord.Embed(description=desc, color=discord.Color.green())
                            await message.edit(embed=embed)
                            await message.clear_reactions()
                            return
                        elif reaction.emoji == '◀️':
                            continue
                break
            while True:
                desc = f"Excellent! Now that we've gotten that out of the way, let\'s specify the channel in which this message should be sent. \n" \
                       f"React with the ✅ if you want to proceed or ❌ if you wish to cancel, or ⏩ to skip this segment."
                embed = discord.Embed(description = desc, color = discord.Color.green())
                await message.edit(embed=embed)
                await message.add_reaction('✅')
                await message.add_reaction('❌')
                await message.add_reaction('⏩')

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌', '⏩']
                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout = 120)
                if reaction.emoji == '⏩':
                    desc = "Skipping welcome message channel setup..."
                    embed = discord.Embed(description = desc, color = discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    await asyncio.sleep(3)
                    break
                elif reaction.emoji == '✅':
                    desc = f"Excellent! Please mention the channel you would like these messages sent in below.\n\nExample: {ctx.channel.mention}"
                    embed = discord.Embed(title = "Welcomer", description = desc, color = discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel
                    msg = await self.client.wait_for('message', check=check, timeout = 120)
                    try:
                        await msg.delete()
                    except discord.Forbidden:
                        pass
                    try:
                        channel = msg.channel_mentions[0]
                        res = utils.channelperms(channel)
                        if not res:
                            desc = f"It looks like I am missing permissions to `Send Messages`, `View Channel`, and `Embed Links` in {channel.mention}. Please fix that " \
                                   f"and return to setup.\n" \
                                   f"If I have these permissions, it means the channel is marked as NSFW. If that is not the case, contact the developers with error code: 501"
                            embed = discord.Embed(description = desc, color = discord.Color.red())
                            await message.edit(embed=embed)
                            await asyncio.sleep(6)
                            continue
                        else:
                            query = {'_id': ctx.guild.id}
                            if collection.count_documents(query) == 0:
                                utils.add_guild_to_db(ctx.guild)
                            collection.update_one({'_id': ctx.guild.id},
                                                  {'$set': {'welcomechannel': channel.id}})
                            desc = f"We have saved {channel.mention} as the channel that welcome messages will be sent in!"
                            embed = discord.Embed(description = desc, color = discord.Color.green())
                            await message.edit(embed=embed)
                            await asyncio.sleep(3)
                            break
                    except IndexError:
                        desc = "There seems to be an error with the input you gave me. Please double-check that there is a channel mentioned? \n" \
                               "Going back now..."
                        embed = discord.Embed(description = desc, color = discord.Color.red())
                        await message.edit(embed=embed)
                        await message.clear_reactions()
                        await asyncio.sleep(3)
                        continue
                elif reaction.emoji == '❌':
                    desc = f"The welcome channel has not been saved and setup has been cancelled."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    return

            while True:

                desc = f"Next up is a private DM. Would you like {self.client.user.name} to send a DM when a user joins your server? React with ✅ for yes, ⏩ to skip, or ❌ to cancel. "
                embed = discord.Embed(title = "Welcomer", description = desc, color = discord.Color.green())
                await message.edit(embed=embed)
                await message.add_reaction('✅')
                await message.add_reaction('⏩')
                await message.add_reaction('❌')

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌','⏩']
                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout = 120)
                if reaction.emoji == '❌':
                    desc = f"The private message has not been saved and setup has been cancelled."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    return
                elif reaction.emoji == '⏩':
                    desc = "Skipping private welcome message setup..."
                    embed = discord.Embed(description = desc, color = discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    await asyncio.sleep(3)
                    break
                elif reaction.emoji == '✅':
                    await message.clear_reactions()
                    desc = "Excellent! Type out the message you would like to send now. \n\n" \
                           "PARAMETERS:\n" \
                           "{guild} -> a variable that is replaced with your server's name.\n" \
                           "{members} -> a variable that is replaced with the number of members in a server.\n" \
                           "{member} -> a variable that is replaced with an @mention of the user.\n" \
                           "{user} -> a variable that is replaced with the user's username.\n\n" \
                           "EXAMPLE: Thanks for joining {guild}, {member}!"
                    embed = discord.Embed(description = desc, color = discord.Color.green())
                    await message.edit(embed=embed)
                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel
                    msg = await self.client.wait_for('message', check=check, timeout = 300)
                    try:
                        await msg.delete()
                    except discord.Forbidden:
                        pass
                    if len(msg.content) > 2000:
                        # nitro
                        desc = f"Your message was longer than 2000 characters! `{len(msg.content)}` > 2000. \nAll your preferences have been saved. If you want to continue setup, run the command again."
                        embed = discord.Embed(description=desc, color=discord.Color.red())
                        return await message.edit(embed=embed)
                    membercount = ctx.guild.member_count
                    member = ctx.author.mention
                    user = ctx.author.name
                    guild = ctx.guild.name
                    mention = ctx.author.mention
                    uembed = discord.Embed(
                        description=str(msg.content.strip()).format(members=membercount, member=member, mention=mention, user=user,
                                                        guild=guild) + "\n\nIf you like "
                                                                                   "this format, react with the ✅. React with the ❌ to cancel. Or react with the ◀ to go back.",
                        color=discord.Color.green())
                    uembed.set_author(name=f'Welcome to {ctx.guild.name}!', icon_url=f'{ctx.guild.icon_url}')
                    await message.edit(embed=uembed)
                    await message.clear_reactions()
                    await message.add_reaction('✅')
                    await message.add_reaction('❌')
                    await message.add_reaction('◀️')

                    def check(reaction, user):
                        return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌', '◀️']

                    reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=180)

                    if reaction.emoji == '◀️':
                        await message.clear_reactions()
                        continue
                    elif reaction.emoji == '❌':
                        desc = f"The private message has not been saved and setup has been cancelled."
                        embed = discord.Embed(description=desc, color=discord.Color.green())
                        await message.edit(embed=embed)
                        await message.clear_reactions()
                        return
                    elif reaction.emoji == '✅':
                        query = {'_id': ctx.guild.id}
                        if collection.count_documents(query) == 0:
                            utils.add_guild_to_db(ctx.guild)
                        collection.update_one({'_id': ctx.guild.id}, {'$set': {'priv_welcomemsg': msg.content.strip()}})
                        await message.clear_reactions()
                        desc = "I have saved your private DM welcome message. Let's move on."
                        embed = discord.Embed(description=desc, color = discord.Color.red())
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        break

            while True:
                desc = "Next up is autoroles.\n\nWould you like to set up what role I should give to users when they join? React with ✅ for yes, ⏩ to skip, or ❌ to cancel."
                embed = discord.Embed(title="Welcomer", description=desc, color=discord.Color.green())
                await message.edit(embed=embed)
                await message.add_reaction('✅')
                await message.add_reaction('⏩')
                await message.add_reaction('❌')

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌', '⏩']

                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                if reaction.emoji == '❌':
                    desc = f"The welcomerole has not been saved and setup has been cancelled."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    return
                elif reaction.emoji == '⏩':
                    desc = "Skipping welcome role setup..."
                    embed = discord.Embed(description = desc, color = discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    await asyncio.sleep(3)
                    break
                elif reaction.emoji == '✅':
                    role = random.choice(ctx.guild.me.roles)
                    desc = "Yay! \nIn the chat, please mention the role you would like to set as the welcomerole.\n\n" \
                           f"EXAMPLE: {role.mention}"
                    embed = discord.Embed(description = desc, color = discord.Color.green())
                    await message.clear_reactions()
                    await message.edit(embed=embed)
                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel
                    msg = await self.client.wait_for('message', check=check, timeout = 120)
                    try:
                        await msg.delete()
                    except discord.Forbidden:
                        pass
                    try:
                        role = msg.role_mentions[0]
                        if role >= ctx.author.top_role:
                            if ctx.author.id == ctx.guild.owner_id:
                                pass
                            else:
                                desc = f"{role.mention} is above your highest role. Try again with a different role."
                                embed = discord.Embed(description=desc, color = discord.Color.red())
                                await message.edit(embed=embed)
                                await message.clear_reactions()
                                await asyncio.sleep(3)
                                continue
                        else:
                            res = utils.rolecheck(role, ctx)
                            if not res:
                                desc = res[1]
                                embed = discord.Embed(description=desc, color = discord.Color.red())
                                await message.edit(embed=embed)
                                await message.clear_reactions()
                                await asyncio.sleep(3)
                                continue
                            else:
                                query = {'_id': ctx.guild.id}
                                if collection.count_documents(query) == 0:
                                   utils.add_guild_to_db(ctx.guild)
                                collection.update_one({'_id': ctx.guild.id}, {'$set': {'welcomerole': role.id}})
                                desc = f"Success! {role.mention} has been set as the welcome role for {ctx.guild.name}. \nMoving on to next segment!"
                                embed = discord.Embed(description=desc, color = discord.Color.green())
                                await message.edit(embed=embed)
                                await message.clear_reactions()
                                await asyncio.sleep(3)
                                break
                    except IndexError:
                        desc = "There seems to be an error with the input you gave me. Please double-check that there is a role mentioned? \n" \
                               "Going back now..."
                        embed = discord.Embed(description=desc, color=discord.Color.red())
                        await message.edit(embed=embed)
                        await message.clear_reactions()
                        await asyncio.sleep(3)
                        continue

            while True:
                desc = f"Next up is captcha. Would you like {self.client.user.name} to send users a captcha they must solve before they can get the welcomerole?\n" \
                       f"React with ✅ for yes, ⏩ to skip, or ❌ to cancel."
                embed = discord.Embed(title="Welcomer", description=desc, color=discord.Color.green())
                await message.edit(embed=embed)
                await message.add_reaction('✅')
                await message.add_reaction('⏩')
                await message.add_reaction('❌')

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌', '⏩']
                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                if reaction.emoji == '❌':
                    desc = f"Captcha has not been toggled and setup has been cancelled."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    return
                elif reaction.emoji == '⏩':
                    desc = "Skipping captcha setup..."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    await asyncio.sleep(3)
                    break
                elif reaction.emoji == '✅':
                    desc = "Excellent! Would you like to turn it off or on? React with '✅' for on, and '❌' for off."
                    embed = discord.Embed(description = desc, color = discord.Color.green())
                    await message.clear_reactions()
                    await message.edit(embed=embed)
                    await message.add_reaction('✅')
                    await message.add_reaction('❌')
                    def check(reaction, user):
                        return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌']

                    reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                    if reaction.emoji == '✅':
                        query = {'_id': ctx.guild.id}
                        if collection.count_documents(query) == 0:
                            utils.add_guild_to_db(ctx.guild)
                        collection.update_one({'_id': ctx.guild.id},
                                              {'$set': {'captchaon': 'on'}})
                        desc = "Captcha has been toggled to on!\n\nMoving on to the next segment..."
                        embed = discord.Embed(description=desc, color = discord.Color.green())
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        break
                    elif reaction.emoji == '❌':
                        query = {'_id': ctx.guild.id}
                        if collection.count_documents(query) == 0:
                            utils.add_guild_to_db(ctx.guild)
                        collection.update_one({'_id': ctx.guild.id},
                                              {'$set': {'captchaon': ''}})
                        desc = "Captcha has been toggled to off!"
                        embed = discord.Embed(description=desc, color=discord.Color.green())
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        break
            while True:
                desc = f"Next segment is setting a muterole. The process is the same as before. Would you like to set this up? " \
                       "React with ✅ for yes, ⏩ to skip, or ❌ to cancel."
                embed = discord.Embed(description=desc, color = discord.Color.green())
                await message.edit(embed=embed)
                await message.add_reaction('✅')
                await message.add_reaction('⏩')
                await message.add_reaction('❌')

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌', '⏩']

                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                if reaction.emoji == '❌':
                    desc = f"A muterole has not been set and setup has been cancelled."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    return
                elif reaction.emoji == '⏩':
                    desc = "Skipping muterole setup..."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    await asyncio.sleep(3)
                    break
                elif reaction.emoji == '✅':
                    desc = "Great! Would you like me to create the muterole, or do you already have one? React with ✅ if you do and ❌ if you don't."
                    embed = discord.Embed(description = desc, color = discord.Color.green())
                    await message.clear_reactions()
                    await message.edit(embed=embed)
                    await message.add_reaction('✅')
                    await message.add_reaction('❌')

                    def check(reaction, user):
                        return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌']

                    reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                    if reaction.emoji == '❌':
                        desc = "Great, I am about to create the muterole.\n\nUpdating channel overrides..."
                        embed = discord.Embed(description = desc, color = discord.Color.green())
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        try:
                            mutedRole = await ctx.guild.create_role(name='Muted')
                            for channel in ctx.guild.channels:
                                if str(channel.type).lower() == 'category':
                                    continue
                                if str(channel.type).lower() == 'text':
                                    await channel.set_permissions(mutedRole, send_messages=False)
                                if str(channel.type).lower() == 'voice':
                                    continue
                            query = {'_id': ctx.guild.id}
                            if collection.count_documents(query) == 0:
                                utils.add_guild_to_db(ctx.guild)
                            collection.update_one({'_id': ctx.guild.id}, {'$set': {'muterole': mutedRole.id}})
                            desc = f"Success! The muterole for {ctx.guild.name} has been set to {mutedRole.mention}!\nMoving on to the next segment!"
                            embed = discord.Embed(description = desc, color = discord.Color.green())
                            await message.clear_reactions()
                            await message.edit(embed=embed)
                            await asyncio.sleep(3)
                            break
                        except discord.Forbidden:
                            desc = f"Hm, didn't work. Make sure that I have the `Manage Server` and `Manage Roles` permissions. Going back to the beginning of this segment..."
                            embed = discord.Embed(description=desc, color = discord.Color.red())
                            await message.clear_reactions()
                            await message.edit(embed=embed)
                            await asyncio.sleep(3)
                            continue
                    elif reaction.emoji == '✅':
                        role = random.choice(ctx.guild.me.roles)
                        desc = "Excellent! Please mention the muterole in the chat...\n" \
                               f"EXAMPLE: {role.mention}"
                        embed = discord.Embed(description=desc, color = discord.Color.green())
                        await message.clear_reactions()
                        await message.edit(embed=embed)

                        def check(m):
                            return m.author == ctx.author and m.channel == ctx.channel

                        msg = await self.client.wait_for('message', check=check, timeout=120)
                        try:
                            await msg.delete()
                        except discord.Forbidden:
                            pass
                        try:
                            role = msg.role_mentions[0]
                            if role >= ctx.author.top_role:
                                if ctx.author.id == ctx.guild.owner_id:
                                    pass
                                else:
                                    desc = f"{role.mention} is above your highest role. Try again with a different role."
                                    embed = discord.Embed(description=desc, color=discord.Color.red())
                                    await message.edit(embed=embed)
                                    await message.clear_reactions()
                                    await asyncio.sleep(3)
                                    continue
                            else:
                                res = utils.rolecheck(role, ctx)
                                if not res:
                                    desc = res[1]
                                    embed = discord.Embed(description=desc, color=discord.Color.red())
                                    await message.edit(embed=embed)
                                    await message.clear_reactions()
                                    await asyncio.sleep(3)
                                    continue
                                else:
                                    query = {'_id': ctx.guild.id}
                                    if collection.count_documents(query) == 0:
                                        utils.add_guild_to_db(ctx.guild)
                                    collection.update_one({'_id': ctx.guild.id}, {'$set': {'muterole': role.id}})
                                    desc = f"Success! {role.mention} has been set as the muterole for {ctx.guild.name}. \nMoving on to next segment!"
                                    embed = discord.Embed(description=desc, color=discord.Color.green())
                                    await message.edit(embed=embed)
                                    await message.clear_reactions()
                                    await asyncio.sleep(3)
                                    break
                        except IndexError:
                            desc = "There seems to be an error with the input you gave me. Please double-check that there is a role mentioned? \n" \
                                   "Going back now..."
                            embed = discord.Embed(description=desc, color=discord.Color.red())
                            await message.edit(embed=embed)
                            await message.clear_reactions()
                            await asyncio.sleep(3)
                            continue

            while True:
                desc = f"Next segment is setting a leave message. This message gets sent in the same channel as the welcome message, but is only triggered when a user leaves your server. \n" \
                       f"Would you like to set this up? " \
                       "React with ✅ for yes, ⏩ to skip, or ❌ to cancel."
                embed = discord.Embed(description=desc, color = discord.Color.green())
                await message.edit(embed=embed)
                await message.add_reaction('✅')
                await message.add_reaction('⏩')
                await message.add_reaction('❌')

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌', '⏩']

                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                if reaction.emoji == '❌':
                    desc = f"A leave message has not been set and setup has been cancelled."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    return
                elif reaction.emoji == '⏩':
                    desc = "Skipping leave message setup..."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    await asyncio.sleep(3)
                    break

                elif reaction.emoji == '✅':
                    desc = f"Great, we will be setting a leave message! Please type the message in the chat below. \n\n**NOTE: Message must be under 2000 characters!**\n" \
                           f"PARAMETERS:\n" \
                           "{guild} -> a variable that is replaced with your server's name.\n" \
                           "{members} -> a variable that is replaced with the number of members in a server.\n" \
                           "{member} -> a variable that is replaced with an @mention of the user.\n" \
                           "{user} -> a variable that is replaced with the user's username.\n\n" \
                           "EXAMPLE: Aw man, {member} has left us."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()

                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel

                    msg = await self.client.wait_for('message', check=check, timeout=300)
                    try:
                        await msg.delete()
                    except discord.Forbidden:
                        pass
                    if len(msg.content) > 2000:
                        # idk how this can happen
                        desc = f"Your message was longer than 2000 characters! `{len(msg.content)}` > 2000. \nPlease try again."
                        embed = discord.Embed(description=desc, color=discord.Color.red())
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        continue
                    else:
                        membercount = ctx.guild.member_count
                        member = ctx.author.mention
                        user = ctx.author.name
                        guild = ctx.guild.name
                        embed = discord.Embed(
                            description=str(msg.content.strip()).format(members=membercount, member=member, user=user,
                                                                        guild=guild) + "\n\nIf you like "
                                                                                       "this format, react with the ✅. React with the ❌ to cancel. Or react with the ◀ to go back.",
                            color=discord.Color.greyple(), timestamp=datetime.datetime.utcnow())
                        embed.set_author(name=f'{ctx.author.name} has left the server',
                                         icon_url=f'{ctx.author.avatar_url}')
                        embed.set_thumbnail(url=ctx.author.avatar_url)
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        await message.add_reaction('✅')
                        await message.add_reaction('❌')
                        await message.add_reaction('◀️')

                        def check(reaction, user):
                            return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌', '◀️']

                        reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=180)
                        if reaction.emoji == '✅':
                            if ctx.message.author.guild_permissions.manage_messages:
                                query = {'_id': ctx.guild.id}
                                if collection.count_documents(query) == 0:
                                    utils.add_guild_to_db(ctx.guild)
                                collection.update_one({'_id': ctx.guild.id},
                                                      {'$set': {'leavemsg': msg.content.strip()}})
                                desc = f"Success! Your leave message has been saved and will apply as soon as setup is complete. Moving on ..."
                                embed = discord.Embed(description=desc, color=discord.Color.green())
                                await message.edit(embed=embed)
                                await message.clear_reactions()
                                await asyncio.sleep(3)
                                break
                                # continue from here!
                        elif reaction.emoji == '❌':
                            # create a go back thing here
                            desc = f"The leave message has not been saved and restarting leave message segment..."
                            embed = discord.Embed(description=desc, color=discord.Color.green())
                            await message.edit(embed=embed)
                            await message.clear_reactions()
                            continue
                        elif reaction.emoji == '◀️':
                            continue

            while True:
                desc = f"Next segment is setting up spam detection. \n" \
                       f"Would you like to set this up? " \
                       "React with ✅ for yes, ⏩ to skip, or ❌ to cancel."
                embed = discord.Embed(description=desc, color=discord.Color.green())
                await message.edit(embed=embed)
                await message.add_reaction('✅')
                await message.add_reaction('⏩')
                await message.add_reaction('❌')

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌', '⏩']

                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                if reaction.emoji == '❌':
                    desc = f"Spam detection has not been toggled and setup has been cancelled."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    return
                elif reaction.emoji == '⏩':
                    desc = "Skipping spam detection setup..."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    await asyncio.sleep(3)
                    break
                elif reaction.emoji == '✅':
                    desc = "Excellent! Would you like to turn it off or on? React with '✅' for on, and '❌' for off."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.clear_reactions()
                    await message.edit(embed=embed)
                    await message.add_reaction('✅')
                    await message.add_reaction('❌')

                    def check(reaction, user):
                        return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌']

                    reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                    if reaction.emoji == '✅':
                        query = {'_id': ctx.guild.id}
                        if collection.count_documents(query) == 0:
                            utils.add_guild_to_db(ctx.guild)
                        collection.update_one({'_id': ctx.guild.id},
                                              {'$set': {'spamdetect': 'on'}})
                        desc = "Spam detection has been toggled to on!\n\nMoving on to the next segment..."
                        embed = discord.Embed(description=desc, color=discord.Color.green())
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        break
                    elif reaction.emoji == '❌':
                        query = {'_id': ctx.guild.id}
                        if collection.count_documents(query) == 0:
                            utils.add_guild_to_db(ctx.guild)
                        collection.update_one({'_id': ctx.guild.id},
                                              {'$set': {'spamdetect': ''}})
                        desc = "Spam detection has been toggled to off!"
                        embed = discord.Embed(description=desc, color=discord.Color.green())
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        break

            while True:
                desc = f"Next segment is setting up logging. \n" \
                       f"Would you like to set this up? " \
                       "React with ✅ for yes, ⏩ to skip, or ❌ to cancel."
                embed = discord.Embed(description=desc, color=discord.Color.green())
                await message.edit(embed=embed)
                await message.add_reaction('✅')
                await message.add_reaction('⏩')
                await message.add_reaction('❌')

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌', '⏩']

                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                if reaction.emoji == '❌':
                    desc = f"Logging has not been toggled and setup has been cancelled."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    return
                elif reaction.emoji == '⏩':
                    desc = "Skipping logging setup..."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    await asyncio.sleep(3)
                    break
                elif reaction.emoji == '✅':
                    desc = "Excellent! Would you like to turn it off or on? React with '✅' for on, and '❌' for off."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.clear_reactions()
                    await message.edit(embed=embed)
                    await message.add_reaction('✅')
                    await message.add_reaction('❌')

                    def check(reaction, user):
                        return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌']

                    reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                    if reaction.emoji == '✅':
                        query = {'_id': ctx.guild.id}
                        if collection.count_documents(query) == 0:
                            utils.add_guild_to_db(ctx.guild)
                        collection.update_one({'_id': ctx.guild.id},
                                              {'$set': {'logging': 'on'}})
                        desc = "Logging has been toggled to on!"
                        embed = discord.Embed(description=desc, color=discord.Color.green())
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        chan = random.choice(ctx.guild.text_channels)
                        desc = f"Excellent! Now mention the channel that these logs should be directed to.\n\nExample: {chan.mention}"
                        embed = discord.Embed(description=desc, color=discord.Color.green())
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        def check(m):
                            return m.author == ctx.author and m.channel == ctx.channel

                        msg = await self.client.wait_for('message', check=check, timeout = 120)
                        try:
                            await msg.delete()
                        except discord.Forbidden:
                            pass
                        try:
                            channel = msg.channel_mentions[0]
                            res = utils.channelperms(channel)
                            if not res:
                                desc = f"It looks like I am missing permissions to `Send Messages`, `View Channel`, and `Embed Links` in {channel.mention}. Please fix that " \
                                       f"and return to setup.\n" \
                                       f"If I have these permissions, it means the channel is marked as NSFW. If that is not the case, contact the developers with error code: 501"
                                embed = discord.Embed(description=desc, color=discord.Color.red())
                                await message.edit(embed=embed)
                                await asyncio.sleep(6)
                                continue
                            else:
                                query = {'_id': ctx.guild.id}
                                if collection.count_documents(query) == 0:
                                    utils.add_guild_to_db(ctx.guild)
                                collection.update_one({'_id': ctx.guild.id},
                                                      {'$set': {'logchannel': channel.id}})
                                desc = f"We have saved {channel.mention} as the channel that logs will be sent to!"
                                embed = discord.Embed(description=desc, color=discord.Color.green())
                                await message.edit(embed=embed)
                                await asyncio.sleep(3)
                                break
                        except IndexError:
                            desc = "There seems to be an error with the input you gave me. Please double-check that there is a channel mentioned? \n" \
                                   "Going back now..."
                            embed = discord.Embed(description=desc, color=discord.Color.red())
                            await message.edit(embed=embed)
                            await message.clear_reactions()
                            await asyncio.sleep(3)
                            continue
                    elif reaction.emoji == '❌':
                        query = {'_id': ctx.guild.id}
                        if collection.count_documents(query) == 0:
                            utils.add_guild_to_db(ctx.guild)
                        collection.update_one({'_id': ctx.guild.id},
                                              {'$set': {'logging': ''}})
                        desc = "Logging has been toggled to off!"
                        embed = discord.Embed(description=desc, color=discord.Color.green())
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        break

            while True:
                desc = f"Next segment is setting up ghostpings. \n" \
                       f"Would you like to set this up? " \
                       "React with ✅ for yes, ⏩ to skip, or ❌ to cancel."
                embed = discord.Embed(description=desc, color=discord.Color.green())
                await message.edit(embed=embed)
                await message.add_reaction('✅')
                await message.add_reaction('⏩')
                await message.add_reaction('❌')

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌', '⏩']

                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                if reaction.emoji == '❌':
                    desc = f"Ghost ping detection has not been toggled and setup has been cancelled."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    return
                elif reaction.emoji == '⏩':
                    desc = "Skipping ghost ping detection setup..."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    await asyncio.sleep(3)
                    break
                elif reaction.emoji == '✅':
                    desc = "Excellent! Would you like to turn it off or on? React with '✅' for on, and '❌' for off."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.clear_reactions()
                    await message.edit(embed=embed)
                    await message.add_reaction('✅')
                    await message.add_reaction('❌')

                    def check(reaction, user):
                        return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌']

                    reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                    if reaction.emoji == '✅':
                        query = {'_id': ctx.guild.id}
                        if collection.count_documents(query) == 0:
                            utils.add_guild_to_db(ctx.guild)
                        collection.update_one({'_id': ctx.guild.id},
                                              {'$set': {'ghostpingon': 'on'}})
                        desc = "Ghost ping detection has been toggled to on!\n\nMoving on to the next segment..."
                        embed = discord.Embed(description=desc, color=discord.Color.green())
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        break
                    elif reaction.emoji == '❌':
                        query = {'_id': ctx.guild.id}
                        if collection.count_documents(query) == 0:
                            utils.add_guild_to_db(ctx.guild)
                        collection.update_one({'_id': ctx.guild.id},
                                              {'$set': {'ghostpingon': ''}})
                        desc = "Ghost ping detection has been toggled to off!"
                        embed = discord.Embed(description=desc, color=discord.Color.green())
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        break

            while True:
                desc = f"Next up is blacklisted words. Would you like {self.client.user.name} to delete messages that contain words in a blacklist? \n" \
                       f"React with ✅ for yes, ⏩ to skip, or ❌ to cancel."
                embed = discord.Embed(description=desc, color=discord.Color.green())
                await message.edit(embed=embed)
                await message.add_reaction('✅')
                await message.add_reaction('⏩')
                await message.add_reaction('❌')

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌', '⏩']

                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                if reaction.emoji == '❌':
                    desc = f"Blacklist has not been toggled and setup has been cancelled."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    return
                elif reaction.emoji == '⏩':
                    desc = "Skipping blacklist setup..."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    await asyncio.sleep(3)
                    break
                elif reaction.emoji == '✅':
                    desc = "Excellent! Would you like to turn it off or on? React with '✅' for on, and '❌' for off."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.clear_reactions()
                    await message.edit(embed=embed)
                    await message.add_reaction('✅')
                    await message.add_reaction('❌')

                    def check(reaction, user):
                        return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌']

                    reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                    if reaction.emoji == '✅':
                        query = {'_id': ctx.guild.id}
                        if collection.count_documents(query) == 0:
                            utils.add_guild_to_db(ctx.guild)
                        collection.update_one({'_id': ctx.guild.id},
                                              {'$set': {'blacklistenab': 'on'}})
                        desc = "Blacklist has been toggled to on!\n\nMoving on to the next segment..."
                        embed = discord.Embed(description=desc, color=discord.Color.green())
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        break
                    elif reaction.emoji == '❌':
                        query = {'_id': ctx.guild.id}
                        if collection.count_documents(query) == 0:
                            utils.add_guild_to_db(ctx.guild)
                        collection.update_one({'_id': ctx.guild.id},
                                              {'$set': {'blacklistenab': ''}})
                        desc = "Blacklist has been toggled to off!"
                        embed = discord.Embed(description=desc, color=discord.Color.green())
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        break

            while True:
                desc = f"Next up is a custom prefix. Would you like to set this up? \n" \
                       f"React with ✅ for yes, ⏩ to skip, or ❌ to cancel."
                embed = discord.Embed(description=desc, color=discord.Color.green())
                await message.edit(embed=embed)
                await message.add_reaction('✅')
                await message.add_reaction('⏩')
                await message.add_reaction('❌')

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌', '⏩']

                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                if reaction.emoji == '❌':
                    desc = f"Prefix has not been changed and setup has been cancelled."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    return
                elif reaction.emoji == '⏩':
                    desc = "Skipping prefix setup..."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    await asyncio.sleep(3)
                    break
                elif reaction.emoji == '✅':
                    prefix = ctx.prefix
                    desc = "Excellent! What would you like to change it to?\n\nNOTE: If you want a word prefix, you **MUST** surround it in quotes.\n" \
                           f"Example: {prefix}changeprefix \"yo \""
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.clear_reactions()
                    await message.edit(embed=embed)

                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel
                    msg = await self.client.wait_for('message', check=check, timeout=120)
                    try:
                        await msg.delete()
                    except discord.Forbidden:
                        pass
                    pref = msg.content.lstrip()
                    if len(pref) > 10:
                        desc = f"The prefix `{pref}` is larger than 10 characters. Try again..."
                        embed = discord.Embed(description = desc, color = discord.Color.red())
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        continue
                    elif pref == "":
                        desc = "You must specify a prefix! Try again..."
                        embed = discord.Embed(description=desc, color=discord.Color.red())
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        continue
                    if msg.mentions:
                        await ctx.send("Bruh seriously")
                        continue
                    if '@everyone' in msg or '@here' in msg:
                        await ctx.send("Bruh seriously")
                        continue
                    else:
                        collection.update_one({"_id": ctx.guild.id}, {"$set": {'prefix': str(pref)}})
                        desc = f"Prefix for **{ctx.guild.name}** has been updated to `{pref}`. \n\nNext segment in 5 seconds..."
                        embed = discord.Embed(description=desc, color=discord.Color.green())
                        await message.edit(embed=embed)
                        await message.clear_reactions()
                        await asyncio.sleep(5)
                        break
            while True:
                desc = f"Next up is levelups. Would you like {self.client.user.name} to keep track of who is most active in {ctx.guild.name}?\n" \
                       f"React with ✅ for yes, ⏩ to skip, or ❌ to cancel."
                embed = discord.Embed(description=desc, color=discord.Color.green())
                await message.edit(embed=embed)
                await message.add_reaction('✅')
                await message.add_reaction('⏩')
                await message.add_reaction('❌')

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌', '⏩']

                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                if reaction.emoji == '❌':
                    desc = f"Level ups have not been toggled and setup has been cancelled."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    return
                elif reaction.emoji == '⏩':
                    desc = "Skipping leveling setup..."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    await asyncio.sleep(3)
                    break
                elif reaction.emoji == '✅':
                    desc = "Excellent! Would you like to turn it off or on? React with '✅' for on, and '❌' for off."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.clear_reactions()
                    await message.edit(embed=embed)
                    await message.add_reaction('✅')
                    await message.add_reaction('❌')

                    def check(reaction, user):
                        return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌']

                    reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                    if reaction.emoji == '✅':
                        query = {'_id': ctx.guild.id}
                        if collection.count_documents(query) == 0:
                            utils.add_guild_to_db(ctx.guild)
                        collection.update_one({'_id': ctx.guild.id},
                                              {'$set': {'levelups': 'on'}})
                        desc = "Leveling has been toggled to on!\n\nMoving on to the next segment..."
                        embed = discord.Embed(description=desc, color=discord.Color.green())
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        break
                    elif reaction.emoji == '❌':
                        query = {'_id': ctx.guild.id}
                        if collection.count_documents(query) == 0:
                            utils.add_guild_to_db(ctx.guild)
                        collection.update_one({'_id': ctx.guild.id},
                                              {'$set': {'levelups': ''}})
                        desc = "Leveling has been toggled to off!"
                        embed = discord.Embed(description=desc, color=discord.Color.green())
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        break

            while True:
                desc = f"Next up is a welcome nickname. Would you like {self.client.user.name} to change a user's nickname when they join the server?\n" \
                       f"React with ✅ for yes, ⏩ to skip, or ❌ to cancel."
                embed = discord.Embed(title="Welcomer", description=desc, color=discord.Color.green())
                await message.edit(embed=embed)
                await message.add_reaction('✅')
                await message.add_reaction('⏩')
                await message.add_reaction('❌')

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌', '⏩']

                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                if reaction.emoji == '❌':
                    desc = f"Welcome nickname has not been toggled and setup has been cancelled."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    return
                elif reaction.emoji == '⏩':
                    desc = "Skipping welcome nickname setup..."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    await asyncio.sleep(3)
                    break
                elif reaction.emoji == '✅':
                    desc = "Excellent! Would you like to turn it off or on? React with '✅' for on, and '❌' for off."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.clear_reactions()
                    await message.edit(embed=embed)
                    await message.add_reaction('✅')
                    await message.add_reaction('❌')

                    def check(reaction, user):
                        return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌']

                    reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                    if reaction.emoji == '✅':
                        desc = f"Type the nickname you would like to set..."
                        embed = discord.Embed(description = desc, color = discord.Color.green())
                        await message.edit(embed=embed)
                        await message.clear_reactions()
                        def check(m):
                            return m.author == ctx.author and m.channel == ctx.channel
                        msg = await self.client.wait_for('message', check=check, timeout = 120)
                        query = {'_id': ctx.guild.id}
                        if msg.content.strip() == "":
                            nick = "you tried"
                        else:
                            nick = msg.content.strip()
                        if collection.count_documents(query) == 0:
                            utils.add_guild_to_db(ctx.guild)
                        collection.update_one({'_id': ctx.guild.id}, {'$set': {'welcomenick': nick}})
                        desc = f"The welcome nickname has been set to {nick}!\n\nMoving on to the next segment..."
                        embed = discord.Embed(description=desc, color=discord.Color.green())
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        break
                    elif reaction.emoji == '❌':
                        query = {'_id': ctx.guild.id}
                        if collection.count_documents(query) == 0:
                            utils.add_guild_to_db(ctx.guild)
                        collection.update_one({'_id': ctx.guild.id},
                                              {'$set': {'welcomenick': ''}})
                        desc = "Welcome nickname has been toggled to off!"
                        embed = discord.Embed(description=desc, color=discord.Color.green())
                        await message.clear_reactions()
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        break

            while True:
                desc = f"Excellent! This is the last item to setup! Do you wish to set a starboard channel? \n" \
                       f"React with the ✅ if you want to proceed or ❌ if you wish to cancel."
                embed = discord.Embed(description=desc, color=discord.Color.green())
                await message.edit(embed=embed)
                await message.add_reaction('✅')
                await message.add_reaction('❌')

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌']

                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
                if reaction.emoji == '✅':
                    chan = random.choice(ctx.guild.text_channels)
                    desc = "Excellent! Please mention the channel you would like starred messages.\n\n" \
                           f"Example: {chan.mention}"
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()

                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel

                    msg = await self.client.wait_for('message', check=check, timeout=120)
                    try:
                        await msg.delete()
                    except discord.Forbidden:
                        pass
                    try:
                        channel = msg.channel_mentions[0]
                        res = utils.channelperms(channel)
                        if not res:
                            desc = f"It looks like I am missing permissions to `Send Messages`, `View Channel`, and `Embed Links` in {channel.mention}. Please fix that " \
                                   f"and return to setup.\n" \
                                   f"If I have these permissions, it means the channel is marked as NSFW. If that is not the case, contact the developers with error code: 501"
                            embed = discord.Embed(description=desc, color=discord.Color.red())
                            await message.edit(embed=embed)
                            await asyncio.sleep(6)
                            continue
                        else:
                            query = {'_id': ctx.guild.id}
                            if collection.count_documents(query) == 0:
                                utils.add_guild_to_db(ctx.guild)
                            collection.update_one({'_id': ctx.guild.id},
                                                  {'$set': {'starchannel': channel.id}})
                            desc = f"We have saved {channel.mention} as the starboard channel!"
                            embed = discord.Embed(description=desc, color=discord.Color.green())
                            await message.edit(embed=embed)
                            await asyncio.sleep(3)
                            break
                    except IndexError:
                        desc = "There seems to be an error with the input you gave me. Please double-check that there is a channel mentioned? \n" \
                               "Going back now..."
                        embed = discord.Embed(description=desc, color=discord.Color.red())
                        await message.edit(embed=embed)
                        await message.clear_reactions()
                        await asyncio.sleep(3)
                        continue
                elif reaction.emoji == '❌':
                    desc = f"The starboard channel has not been saved and setup has been cancelled."
                    embed = discord.Embed(description=desc, color=discord.Color.green())
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    return

            desc = f"Congratulations! {self.client.user.name} is all set up for {ctx.guild.name}! Thank you for using me, and now sit back and relax 😎."
            embed = discord.Embed(description = desc, color = discord.Color.green())
            await message.clear_reactions()
            await message.edit(embed=embed)
            return

        except asyncio.TimeoutError:
            desc = f"This setup session has timed out. All your preferences so far have been saved."
            embed = discord.Embed(description= desc, color = discord.Color.red())
            await message.edit(embed=embed)
            await message.clear_reactions()



def setup(client):
    client.add_cog(Configuration(client))