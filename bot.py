# -*- coding: utf-8 -*-
from discord.ext import commands
import discord
import os
import asyncio
import datetime
from discord_slash import SlashCommand
from modules import help, utils
from discord_components import DiscordComponents
import os
import threading
from pymongo import MongoClient
from typing import Optional

with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

client = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or('.'), intents = discord.Intents().all(), allowed_mentions=discord.AllowedMentions.none(), case_insenstive = True, strip_after_prefix = True)
slash = SlashCommand(client, sync_commands = True)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")
        print(f"{str(filename[:-3]).capitalize()} {'are' if filename[:-3].endswith('s') else 'is'} loaded.")

client.help_command = help.Help()

def voiceChatMain():
    os.system('cd DJFlame && node .')

t1 = threading.Thread(target=voiceChatMain)
_command_cache = {}
_cog_cache = {}

FORBIDDEN_COGS = [
    'Configuration',
    'Slash'
]

@client.event
async def on_ready():
    t1.start()
    print(f"{client.user.name} is ready, logged on at {datetime.datetime.utcnow()}.")
    await client.change_presence(activity=discord.Game(name=f'Watching {len(client.guilds)} servers'))

    try:
        for guild in client.guilds:
            try:
                utils.add_guild_to_db(guild)
            except:
                continue
        DiscordComponents(client, change_discord_methods=True)
    except Exception as e:
        print(e)
    db = cluster['DISABLED_COMMANDS']
    col = db['channels']
    res = col.find()
    resarr = []
    for i in res:
        resarr.append((i["name"], i["channels"]))
    for i in resarr:
        _command_cache[i[0]] = (i[1])
    col = db['modules']
    res = col.find()
    resarr = []
    for i in res:
        resarr.append((i["name"], i["channels"]))
    for i in resarr:
        _cog_cache[i[0]] = (i[1])

@client.check
async def is_blacklisted(ctx):
    if ctx.command.name == 'help':
        return True
    try:
        if ctx.channel.id in _command_cache[ctx.command.qualified_name]:
            embed = discord.Embed(color = discord.Color.red())
            embed.description = f"This command is disabled in {ctx.channel.mention}."
            await ctx.send(embed=embed)
            return False
    except LookupError:
        pass
    try:
        if ctx.channel.id in _cog_cache[ctx.command.cog.qualified_name]:
            embed = discord.Embed(color=discord.Color.red())
            embed.description = f"This module is disabled in {ctx.channel.mention}."
            await ctx.send(embed=embed)
            return False
        return True
    except LookupError:
        return True
    except AttributeError:
        return True

@client.command(help='Gives the ping of the bot!', aliases = ['clientping'])
async def botping(ctx):
    return await ctx.send(f"{round(client.latency * 1000)}ms")

@client.command()
async def feedback(ctx):
    try:
        await ctx.send(f'{ctx.author.mention}, thank you for using InfiniBot. Please state your feedback here:')

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        message = await client.wait_for('message', check=check, timeout=120)
        channel = client.get_channel(839951602168496149)
        fembed = discord.Embed(title=f"Feedback from {ctx.author} who is in the server **{ctx.guild.name}**",
                               description=f"{ctx.author.id} (User ID)\n{ctx.guild.id} (Guild ID)```" + message.content + "```",
                               color=discord.Color.blurple(), timestamp = datetime.datetime.utcnow())
        msg = await channel.send(embed=fembed)
        await msg.add_reaction(str('<:thumbsup:829860462966734898>'))
        await msg.add_reaction(str('<:thumbsdown:829860507125153795>'))
        await message.add_reaction(str('<:checked:829061772446531624>'))
        await ctx.send(str(f'{ctx.author.mention}, your feedback has been sent.'))
    except asyncio.TimeoutError:
        await ctx.reply("Timed out.", mention_author=False, delete_after=5)

@client.command(aliases = ['invite', 'botinvite'])
async def botinv(ctx):
    embed = discord.Embed(title="InfiniBot Invite Link",
                          description=r'https://discord.com/api/oauth2/authorize?client_id=829464107710677022&permissions=4294307063&scope=bot%20applications.commands',
                          color=discord.Color.blurple())
    embed.set_footer(text=f"InfiniBot Help | Requested by {ctx.author.name}")
    await ctx.reply(embed=embed)

@client.command()
@commands.guild_only()
@commands.has_guild_permissions(manage_guild = True)
async def togglecommand(ctx, commnd:Optional[str] = None, channel:Optional[discord.TextChannel] = None, guild:Optional[bool] = None):
    await ctx.trigger_typing()
    db = cluster['DISABLED_COMMANDS']
    try:
        if commnd is None:
            return await ctx.send("You need to specify which command you want to disable.")
        command = client.get_command(commnd.lower())
        if command.startswith('setup'):
            return await ctx.send("You cannot disable any of the setup commands.")
        if command is None:
            embed = discord.Embed(color = discord.Color.red())
            embed.description = f"Sorry, it looks like the command `{commnd.strip()}` could not be found.\n\n" \
                                f"Please make sure that if you were trying to reference a nested command, such as `{ctx.prefix}setup welcometext`, you type the **ENTIRE COMMAND, WRAPPED IN QUOTES!!!**.\n\n" \
                                f"EXAMPLE: `{ctx.prefix}togglecommand \"setup welcometext\"`."
            embed.set_footer(text=f"To disable a command in the server, type \"on\" or \"off\" right after the command name. To disable it in a channel, "
                                  f"mention the channel after the command name.")
            return await ctx.send(embed=embed)
        if channel is not None:
            print('here3332')
            channel = channel
            chan = True
        elif channel is None and guild is None:
            channel = ctx.channel
            chan = True

        elif channel is None and guild is not None:
            #guild toggle
            chan = False
        else:
            return

        col = db['channels']
        if chan:
            if col.count_documents({"name":command.qualified_name, "channels":channel.id}) == 0:
                if col.count_documents({"name": command.qualified_name}) == 0:
                    payload = {
                        'name':command.qualified_name,
                        'channels':[channel.id]
                    }
                    col.insert_one(payload)
                    try:
                        if _command_cache[command.qualified_name].count(channel.id) > 0:
                            pass
                        else:
                            _command_cache[command.qualified_name].append(channel.id)
                    except LookupError:
                        _command_cache[command.qualified_name] = [channel.id]
                else:
                    print('here')
                    col.update_one({"name":command.qualified_name}, {"$set":{"channels":[channel.id]}})
                    try:
                        if _command_cache[command.qualified_name].count(channel.id) > 0:
                            pass
                        else:
                            _command_cache[command.qualified_name].append(channel.id)
                    except LookupError:
                        _command_cache[command.qualified_name] = [channel.id]
                await ctx.send(f"The command `{command.qualified_name}` has been blacklisted in {channel.mention}!")
            else:
                print('sus')
                col.update_one({"name":command.qualified_name}, {"$pull":{"channels":channel.id}})
                if _command_cache[command.qualified_name].count(channel.id) < 1:
                    pass
                else:
                    _command_cache[command.qualified_name].pop(_command_cache[command.qualified_name].index(channel.id))
                await ctx.send(f"The command `{command.qualified_name}` has been whitelisted in {channel.mention}!")
        else: #guild blacklist the command
            for channel in ctx.guild.text_channels:
                if col.count_documents({"name":command.qualified_name, "channels":channel.id}) == 0:
                    if col.count_documents({"name": command.qualified_name}) == 0:
                        payload = {
                            'name':command.qualified_name,
                            'channels':channel.id
                        }
                        col.insert_one(payload)
                        try:
                            if _command_cache[command.qualified_name].count(channel.id) > 0:
                                pass
                            else:
                                _command_cache[command.qualified_name].append(channel.id)
                        except LookupError:
                            _command_cache[command.qualified_name] = [channel.id]
                    else:
                        print('here')
                        col.update_one({"name":command.qualified_name}, {"$push":{"channels":channel.id}})
                        try:
                            if _command_cache[command.qualified_name].count(channel.id) > 0:
                                pass
                            else:
                                _command_cache[command.qualified_name].append(channel.id)
                        except LookupError:
                            _command_cache[command.qualified_name] = [channel.id]

                else:
                    continue
            await ctx.send(f"Command {command.qualified_name} has been blacklisted from this server.")

    except Exception as e:
        print(e)

@client.command()
@commands.guild_only()
@commands.has_guild_permissions(manage_guild = True)
async def togglemodule(ctx, cogz = None, channel:Optional[discord.TextChannel] = None, guild:Optional[bool] = None):
    await ctx.trigger_typing()
    db = cluster['DISABLED_COMMANDS']
    try:
        if cogz is None:
            return await ctx.send("You need to specify which module you want to disable.")
        cog = client.get_cog(cogz.title())
        if cog is None:
            embed = discord.Embed(color = discord.Color.red())
            embed.description = f"Sorry, it looks like the module `{cogz.strip()}` could not be found.\n\n" \
                                f"Please make sure that if you were trying to reference a module that has two words, such as `Google Classroom`, you type the **ENTIRE MODULE NAME, WRAPPED IN QUOTES!!!**.\n\n" \
                                f"EXAMPLE: `{ctx.prefix}togglemodule \"Google Classroom\"`.\n\n" \
                                f"If you are sure that you are typing the correct name, run the {ctx.prefix}help command to make sure. **NOTE: CASE SENSITIVE!**"
            embed.set_footer(text=f"To disable a module in the server, type \"on\" or \"off\" right after the module name. To disable it in a channel, "
                                  f"mention the channel after the module\'s name.")
            return await ctx.send(embed=embed)
        if cog in FORBIDDEN_COGS:
            return await ctx.send("You are not allowed to disable this module.")
        if channel is not None:
            print('here3332')
            channel = channel
            chan = True
        elif channel is None and guild is None:
            channel = ctx.channel
            chan = True

        elif channel is None and guild is not None:
            #guild toggle
            chan = False
        else:
            return

        col = db['modules']
        if chan:
            if col.count_documents({"name":cog.qualified_name, "channels":channel.id}) == 0:
                if col.count_documents({"name": cog.qualified_name}) == 0:
                    payload = {
                        'name':cog.qualified_name,
                        'channels':channel.id
                    }
                    col.insert_one(payload)
                    try:
                        if _cog_cache[cog.qualified_name].count(channel.id) > 0:
                            pass
                        else:
                            _cog_cache[cog.qualified_name].append(channel.id)
                    except LookupError:
                        _cog_cache[cog.qualified_name] = [channel.id]
                else:
                    print('here')
                    col.update_one({"name":cog.qualified_name}, {"$push":{"channels":channel.id}})
                    try:
                        if _cog_cache[cog.qualified_name].count(channel.id) > 0:
                            pass
                        else:
                            _cog_cache[cog.qualified_name].append(channel.id)
                    except LookupError:
                        _cog_cache[cog.qualified_name] = [channel.id]
                await ctx.send(f"The module `{cog.qualified_name}` has been blacklisted in {channel.mention}!")
            else:
                print('sus')
                try:
                    col.update_one({"name":cog.qualified_name}, {"$pull":{"channels":channel.id}})
                    if _cog_cache[cog.qualified_name].count(channel.id) < 1:
                        pass
                    else:
                        _cog_cache[cog.qualified_name].pop(_cog_cache[cog.qualified_name].index(channel.id))
                except Exception:
                    pass
                await ctx.send(f"The module `{cog.qualified_name}` has been whitelisted in {channel.mention}!")
        else: #guild blacklist the cog
            for channel in ctx.guild.text_channels:
                if col.count_documents({"name":cog.qualified_name, "channels":channel.id}) == 0:
                    if col.count_documents({"name": cog.qualified_name}) == 0:
                        payload = {
                            'name':cog.qualified_name,
                            'channels':channel.id
                        }
                        col.insert_one(payload)
                        try:
                            if _cog_cache[cog.qualified_name].count(channel.id) > 0:
                                pass
                            else:
                                _cog_cache[cog.qualified_name].append(channel.id)
                        except LookupError:
                            _cog_cache[cog.qualified_name] = [channel.id]
                    else:
                        print('here')
                        col.update_one({"name":cog.qualified_name}, {"$push":{"channels":channel.id}})
                        try:
                            if _cog_cache[cog.qualified_name].count(channel.id) > 0:
                                pass
                            else:
                                _cog_cache[cog.qualified_name].append(channel.id)
                        except LookupError:
                            _cog_cache[cog.qualified_name] = [channel.id]

                else:
                    continue
            await ctx.send(f"The module `{cog.qualified_name}` has been blacklisted from this server.")

    except Exception as e:
        print(e)

with open('testbot.txt', 'r') as f:
    token = f.read()

client.run(token)