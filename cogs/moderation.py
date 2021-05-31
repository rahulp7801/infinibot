import discord
from discord.ext import commands
import asyncio
from pymongo import MongoClient
import datetime
import random
from discord_components import DiscordComponents
from modules import utils
#automoderation will be another cog

with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        DiscordComponents(self.client, change_discord_methods=True)

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount:int):
        try:
            await ctx.channel.purge(limit = amount + 1)
            await asyncio.sleep(2)
            await ctx.send(f"Cleared {amount + 1} messages!")
        except discord.errors.HTTPException:
            await ctx.send("I cannot delete messages past two weeks old!")

    @clear.error
    async def clear_err(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send("You can't use that!")
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"You need to specify the amount you would like to clear!")

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member:discord.Member, *, reason = "No reason given"):
        try:
            ban = discord.Embed(description=f"Reason: ```{reason.strip()}```\nBy: {ctx.author.mention}", color = discord.Color.red())
            ban.set_author(name=f"{member} has been banned", icon_url=member.avatar_url)
            uban = discord.Embed(title = f"You were banned from {ctx.guild.name}", description=f"Reason: ```{reason.strip()}```", color = discord.Color.red())
            uban.set_footer(text="If you believe this is an error, talk to the administrators.")
            try:
                if member.top_role >= ctx.author.top_role:
                    if member.id == ctx.guild.owner_id:
                        pass
                    else:
                        return await ctx.send(f"You can only use this moderation on a member below you.")
            except AttributeError:
                return
            if not member.bot:
                await ctx.guild.ban(member, reason=reason)
                await ctx.channel.send(embed=ban)
                try:
                    return await member.send(embed=uban)
                except discord.Forbidden:
                    return await ctx.send(f'A reason could not be sent to `{member}` as they had their dms off.')
            else:
                await ctx.guild.ban(member, reason=reason)
                ban = discord.Embed(
                    description=f"Reason: ```{reason}```\nBy: {ctx.author.mention}")
                ban.set_author(name=f"{member.name} was banned", icon_url=member.avatar_url)
                await ctx.channel.send(embed=ban)

        except discord.errors.Forbidden:
            if member.id == ctx.guild.owner_id:
                await ctx.send(f"You cannot take any action on the server owner.")
                return
            if member.id == self.client.user.id:
                return await ctx.send(f"Why would I ban myself, when I am in the brilliant server that is known as {ctx.guild.name}?")
            if ctx.guild.me.top_role <= member.top_role:
                return await ctx.send(f"My role needs to be higher than {member.name}'s in order for me to take action on them.")
            return await ctx.send(
                "I do not have the `Ban Members` permission. You can fix that by going into Server Settings and giving my role that permission.")


    @ban.error
    async def ban_err(self, ctx, error):
        prefix = utils.serverprefix(ctx)
        if isinstance(error, commands.MissingRequiredArgument):
            desc = f"```{prefix}ban [member] (reason)```"
            embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
            embed.set_footer(text="Parameters in [] are required and () are optional")
            return await ctx.send(embed=embed)
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send(f"{ctx.author.mention}, you can't use that!")

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def tempban(self, ctx, member:discord.Member, duration = 1, unit = "h", *, reason = "No reason given"):
        if unit == "s":
            dur = str(duration) + " seconds"
        elif unit == "m":
            dur = str(duration) + " minutes"
        elif unit == "h":
            dur = str(duration) + " hours"
        try:
            pfp = member.avatar_url
            author = member
            if unit not in ["s", "m", "h"]:
                await ctx.send("Please enter a correct unit. `(s)`, `(m)`, or `(h)`")
                return
            embed = discord.Embed(description=f"For reason: ```{reason}```", color=discord.Color.dark_red())
            embed.set_author(name=str(author) + f" has been banned for {dur}.", icon_url=pfp)
            uembed = discord.Embed(title=f"You have been banned in {ctx.guild.name}",
                                   description=f"For reason: ```{reason}```", color=discord.Color.blurple())
            uembed.set_footer(text="If you believe this is in error, please contact an Admin.")
            if member.top_role >= ctx.author.top_role:
                await ctx.send(f"You can only use this moderation on a member below you.")
                return
            else:
                if not member.bot:
                    await ctx.guild.ban(member, reason=reason)
                    await ctx.send(embed=embed)
                    try:
                        await member.send(embed=uembed)
                    except:
                        await ctx.send(f'A reason could not be sent to `{member}` as they had their dms off.')
                else:
                    await ctx.guild.ban(member, reason=reason)
                    await ctx.send(embed=embed)
                    try:
                        await member.send(embed=uembed)
                    except:
                        await ctx.send(f'A reason could not be sent to {member} as they had their dms off.')
                if unit == "s":
                    await asyncio.sleep(duration)
                    await ctx.guild.unban(user=member)
                elif unit == "m":
                    await asyncio.sleep(duration * 60)
                    await ctx.guild.unban(user=member)
                elif unit == "h":
                    await asyncio.sleep(duration * 60 * 60)
                    await ctx.guild.unban(user=member)
        except AttributeError as e:
            print(e)
            await ctx.reply("An error has occured. The devs have been notified and will look into it.")
            return
        except discord.errors.Forbidden:
            if member.id == ctx.guild.owner_id:
                await ctx.send(f"You cannot take any action on the server owner.")
                return
            if ctx.guild.me.top_role <= member.top_role:
                return await ctx.send(f"You must make my highest role above {member.display_name}'s highest role for me to take action. ")
            return await ctx.send("I do not have the `Ban Members` permission.")


    @tempban.error
    async def tempban_err(self, ctx, error):
        prefix = utils.serverprefix(ctx)
        if isinstance(error, commands.MissingRequiredArgument):
            desc = f"```{prefix}tempban [member] (duration) (unit) (reason)```"
            embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
            embed.set_footer(text="Parameters in [] are required and () are optional")
            return await ctx.send(embed=embed)
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send(f"{ctx.author.mention}, you can't use that!")
        if isinstance(error, commands.MemberNotFound):
            return await ctx.reply("Please mention someone to ban.")

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member:discord.Member, *, reason = "No reason given"):
        try:
            pfp = member.avatar_url
            author = member
            desc = f'Reason: ```{reason.strip()}```'
            kick = discord.Embed(description=str(desc), color=discord.Color.blurple())
            kick.set_author(name=str(author) + " has been kicked.", icon_url=pfp)
            ukick = discord.Embed(title=f"You were kicked from **{ctx.guild.name}**",
                                  description=f"Reason: ```{reason.strip()}```", color=discord.Color.blurple())
            ukick.set_footer(text="If you believe this is in error, please contact an Admin.")
            if member.top_role >= ctx.author.top_role:
                if ctx.author.id == ctx.guild.owner_id:
                    pass
                else:
                    await ctx.send(f"You can only use this moderation on a member below you.")
                    return

            else:
                if not member.bot:
                    await ctx.guild.kick(member, reason=reason)
                    await ctx.channel.send(embed=kick)
                    try:
                        await member.send(embed=ukick)
                    except discord.Forbidden:
                        await ctx.send(f'A reason could not be sent to `{member}` as they had their dms off.')
                else:
                    await ctx.guild.kick(member, reason=reason)
                    await ctx.channel.send(embed=kick)
        except discord.errors.Forbidden:
            if member.id == ctx.guild.owner_id:
                await ctx.send(f"You cannot take any action on the server owner.")
                return
            if member.id == self.client.user.id:
                return await ctx.send(f"Unfortunately, {ctx.author.mention}, I cannot kick myself.")
            if ctx.guild.me.top_role <= member.top_role:
                return await ctx.send(f"You must make my highest role above {member.display_name}'s top role in order for me to take action on them.")
            await ctx.send("I do not have the `Kick Members` permission.")

    @kick.error
    async def kick_err(self, ctx, error):
        prefix = utils.serverprefix(ctx)
        if isinstance(error, commands.MissingRequiredArgument):
            desc = f"```{prefix}kick [member] (reason)```"
            embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
            embed.set_footer(text="Parameters in [] are required and () are optional")
            return await ctx.send(embed=embed)
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send("You don't have permissions!")

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, user:discord.User):
        try:
            pfp = user.avatar_url
            author = user
            embed = discord.Embed(color=discord.Color.red())
            embed.set_author(name=str(author) + " is now unbanned", icon_url=pfp)
            guild = ctx.guild
            await guild.unban(user=user)
            await ctx.send(embed=embed)
        except discord.errors.Forbidden:
            await ctx.send("I do not have the `Ban Members` permission.")

    @unban.error
    async def unb_err(self, ctx, error):
        prefix = utils.serverprefix(ctx)
        if isinstance(error, commands.MissingRequiredArgument):
            desc = f"```{prefix}unban [user]```"
            embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
            embed.set_footer(text="Parameters in [] are required and () are optional")
            return await ctx.send(embed=embed)
        if isinstance(error, commands.UserNotFound):
            nban = discord.Embed(color=discord.Color.red())
            nban.set_author(name=f"User is not banned or doesn\'t exist!")
            await ctx.send(embed=nban)

    @commands.command()
    @commands.has_permissions(manage_roles = True)
    #use the durations_nlp module
    async def tempmute(self, ctx, member:discord.Member, duration = 1, unit = 'h', *, reason = "No reason given"):
        name = f"GUILD{ctx.guild.id}"
        db = cluster[name]
        collection = db['config']
        results = collection.find({'_id': ctx.guild.id})
        for i in results:
            prefix = i['prefix']
            muterole = i['muterole']
        if unit.lower() == "s":
            dur = str(duration) + " seconds"
        elif unit.lower() == "m":
            dur = str(duration) + " minutes"
        elif unit.lower() == "h":
            dur = str(duration) + " hours"
        try:
            pfp = member.avatar_url
            author = member
            if unit.lower() not in ["s", "m", "h"]:
                await ctx.send("Please enter a correct unit. `(s)`, `(m)`, or `(h)`")
                return
            embed = discord.Embed(description=f"For reason: ```{reason}```", color=discord.Color.dark_red())
            embed.set_author(name=str(author) + f" has been muted for {dur}.", icon_url=pfp)
            uembed = discord.Embed(title=f"You have been muted in {ctx.guild.name}",
                                   description=f"For reason: ```{reason}```", color=discord.Color.blurple())
            uembed.set_footer(text="If you believe this is in error, please contact an Admin.")
            if str(muterole) == '':
                await ctx.send(
                    f"This server doesn\'t have a muterole set up! Use `{prefix}setup muterole <Optionalname>` to set it up.")
                return
            role = discord.utils.get(ctx.guild.roles, id=int(muterole))
            if member.top_role >= ctx.author.top_role:
                await ctx.send(f"You can only use this moderation on a member below you.")
                return
            elif role in member.roles:
                await ctx.send(f"`{member}` is already muted.")
                return
            elif reason != None:
                await member.add_roles(role)
                await ctx.send(embed=embed)
                try:
                    await member.send(embed=uembed)
                except:
                    await ctx.send(f'A reason could not be sent to {member} as they had their dms off.')
                if unit.lower() == "s":
                    await asyncio.sleep(duration)
                    await member.remove_roles(role)
                elif unit.lower() == "m":
                    await asyncio.sleep(duration * 60)
                    await member.remove_roles(role)
                elif unit.lower() == "h":
                    await asyncio.sleep(duration * 60 * 60)
                    await member.remove_roles(role)
            elif reason is None:
                await ctx.reply("Please provide a reason for tempmute.")
        except AttributeError as e:
            return await ctx.reply(
                f"This server does not have a mute role. Use `{prefix}muterole` to create the muterole.")
        except discord.errors.Forbidden:
            if member.id == ctx.guild.owner_id:
                await ctx.send(f"You cannot take any action on the server owner.")
                return
            role = discord.utils.get(ctx.guild.roles, id=int(muterole))
            if role >= ctx.guild.me.top_role:
                return await ctx.send("I cannot assign this role as it is above my top role.")

    @tempmute.error
    async def tempmute_err(self, ctx, error):
        prefix = utils.serverprefix(ctx)
        if isinstance(error, commands.MissingRequiredArgument):
            desc = f"```{prefix}tempmute [member] (duration) (unit) (reason)```\nUnits: `s`, `m`, `h`"
            embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
            embed.set_footer(text="Parameters in [] are required and () are optional")
            return await ctx.send(embed=embed)
        if isinstance(error, commands.CommandInvokeError):
            return await ctx.send("I do not have the `Manage Roles` permission.")
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send(f"{ctx.author.name}, you can't use that!")

    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def mute(self, ctx, member:discord.Member, *, dur = None):
        if member == self.client.user:
            return await ctx.send("I can't mute myself.")
        name = f"GUILD{ctx.guild.id}"
        db = cluster[name]
        collection = db['config']
        results = collection.find({'_id': ctx.guild.id})
        for i in results:
            prefix = i['prefix']
            muterole = i['muterole']
        if dur is not None:
            try:
                duration = utils.tmts(dur.strip())
            except ValueError as e:
                return await ctx.reply(str(e), mention_author = False)
        try:
            pfp = member.avatar_url
            author = member
            embed = discord.Embed(description=f"For reason: ```Being Naughty```", color=discord.Color.red())
            embed.set_author(name=str(author) + f" has been muted {'indefinitely' if not dur else 'for ' + utils.stringfromtime(duration)}.", icon_url=pfp)
            uembed = discord.Embed(title=f"You have been muted in {ctx.guild.name}",
                                   description=f"For reason: ```Being Naughty```", color=discord.Color.blurple())
            uembed.set_footer(text="If you believe this is in error, please contact an Admin.")
            if str(muterole) == '':
                await ctx.send(
                    f"This server doesn\'t have a muterole set up! Use `{prefix}setup muterole <Optionalname>` to set it up.")
                return
            role = discord.utils.get(ctx.guild.roles, id=int(muterole))
            if role in member.roles:
                await ctx.send(f"`{member}` is already muted.")
                return
            if ctx.author.top_role >= member.top_role:
                await member.add_roles(role)
                await ctx.send(embed=embed)
                try:
                    await member.send(embed=uembed)
                except:
                    await ctx.send(f'A reason could not be sent to {member.mention} as they had their dms off.')
            else:
                await ctx.send(f"You can only use this moderation on a member below yourself.")
                return
        except AttributeError:
            return await ctx.send(
                f"This server does not have a mute role. Use `{prefix}muterole` to create the muterole.")
        except discord.errors.Forbidden:
            if member.id == ctx.guild.owner_id:
                return await ctx.send(f"You cannot take any action on the server owner.")
            role = discord.utils.get(ctx.guild.roles, id=int(muterole))
            if role >= ctx.guild.me.top_role:
                return await ctx.send("I cannot assign this role as it is above my top role.")
            await ctx.send(
                "I do not have the `Manage Roles` permission. You can fix that by going into Server Settings and giving my role that permission.\nOr my role is not high enough.")

    @mute.error
    async def mute_err(self, ctx, error):
        prefix = utils.serverprefix(ctx)
        if isinstance(error, commands.MissingRequiredArgument):
            desc = f"```{prefix}mute [member] (duration)```"
            embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
            embed.set_footer(text="Parameters in [] are required and () are optional")
            return await ctx.send(embed=embed)
        if isinstance(error, commands.MemberNotFound):
            return await ctx.reply(error, mention_author=False)
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send(f"{ctx.author.name}, you can't use that!")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        name = f"GUILD{ctx.guild.id}"
        db = cluster[name]
        collection = db['config']
        results = collection.find({'_id': ctx.guild.id})
        for i in results:
            muterole = i['muterole']
        pfp = member.avatar_url
        author = member
        role = discord.utils.find(lambda r: r.id == int(muterole), ctx.message.guild.roles)
        await member.remove_roles(role)
        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name=str(author) + " has been unmuted.", icon_url=pfp)
        await ctx.send(embed=embed)

    @unmute.error
    async def unmute_err(self, ctx, error):
        prefix = utils.serverprefix(ctx)
        if isinstance(error, commands.MissingRequiredArgument):
            desc = f"```{prefix}unmute [member]```"
            embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
            embed.set_footer(text="Parameters in [] are required and () are optional")
            return await ctx.send(embed=embed)
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send("You can't use that!")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        desc = str("🔒") + ctx.channel.mention + " **is now in lockdown.**"
        embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @lockdown.error
    async def lockdown_err(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send(f"{ctx.author.mention}, you do not have the `Manage Channels` permission.")
        if isinstance(error, commands.CommandInvokeError):
            return await ctx.send("I don't have the Manage Channel permission for that channel.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        desc = (str("🔓") + ctx.channel.mention + " ***has been unlocked.***")
        embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @unlock.error
    async def unlock_err(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send("You can't use that!")
        if isinstance(error, commands.CommandInvokeError):
            return await ctx.send("I don't have the Manage Channel permission for that channel.")

    @commands.command()
    @commands.has_permissions(manage_nicknames = True)
    async def nick(self, ctx, member:discord.Member, *, nick):
        try:
            if ctx.author.top_role <= member.top_role:
                return await ctx.send(f"You can't use this on a member above you.")
            if len(nick) > 32:
                return await ctx.send(f"You cannot set a nickname above 32 characters. Yours is `{len(nick)}`. ")
            await member.edit(nick=nick)
            await ctx.send('Nickname was changed for ' + member.mention)
        except discord.errors.Forbidden:
            if member.id == ctx.guild.owner_id:
                return await ctx.send("You cannot take action on the server owner.")
            if ctx.guild.me.top_role <= member.top_role:
                return await ctx.send(f"My top role must be higher than {member.display_name}'s top role.")
            return await ctx.send("I am missing the `Manage Nicknames` permission.")

    @nick.error
    async def nick_err(self, ctx, error):
        prefix = utils.serverprefix(ctx)
        if isinstance(error, commands.MissingRequiredArgument):
            desc = f"```{prefix}nick [member] [nickname]```"
            embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
            embed.set_footer(text="Parameters in [] are required and () are optional")
            return await ctx.send(embed=embed)

        if isinstance(error, commands.MissingPermissions):
            return await ctx.send(f"{ctx.author.name}, you can't use that!")
        if isinstance(error, commands.BotMissingPermissions):
            return await ctx.send("I don't have permission to `Manage Nicknames`. ")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member = None, *, reason="To delete messages"):
        prefix = utils.serverprefix(ctx)
        if member is None:
            desc = f"```{prefix}softban [member] (reason)```"
            embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
            embed.set_footer(text="Parameters in [] are required and () are optional")
            return await ctx.send(embed=embed)
        if ctx.author.guild_permissions.ban_members:
            try:
                pfp = member.avatar_url
                author = member
                embed = discord.Embed(description=f"For reason: ```{reason}```", color=discord.Color.dark_red())
                embed.set_author(name=f"{str(author.name)} has been softbanned.", icon_url=pfp)
                await ctx.send(embed=embed)
                await ctx.guild.ban(member, reason="To delete messages")
                await ctx.guild.unban(user=member)
                return
            except discord.Forbidden:
                await ctx.send(f'I don\'t have the required permissions to softban **{member.name}**')
                return

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason given."):
        if member.id == ctx.author.id:
            return await ctx.send("You cannot warn yourself.")
        if ctx.author.top_role <= member.top_role:
            if ctx.author.id == ctx.guild.owner_id:
                pass
            else:
                return await ctx.send("You can only use this moderation on a member below you.")
        if member.id == ctx.guild.owner_id:
            return await ctx.send("You cannot take any action on the server owner.")
        name = f"GUILD{ctx.guild.id}"
        db = cluster[name]
        collection = db['warns']
        ping_cm = {
            "name": member.name,
            'guild': ctx.guild.id,
            "reason": reason.strip(),
            "time": datetime.datetime.now().strftime('%D'),
            'mod': ctx.author.id,
            'offender': member.id
        }
        collection.insert_one(ping_cm)
        query = {'offender': member.id}
        x = collection.count_documents(query)
        desc = f"For reason: ```{reason}```"
        embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{member.name} has been warned", icon_url=member.avatar_url)
        embed.set_footer(text=f"Warning number {x} for {member.name}")
        uembed = discord.Embed(description=desc, color=discord.Color.red())
        uembed.set_author(name=f"You have been warned in the server **{ctx.guild.name}**", icon_url=ctx.guild.icon_url)
        uembed.set_footer(text="If you believe this is an error, please contact an Admin.")
        await ctx.send(embed=embed)
        await member.send(embed=uembed)

    @warn.error
    async def warn_err(self, ctx, error):
        prefix = utils.serverprefix(ctx)
        if isinstance(error, commands.MissingRequiredArgument):
            desc = f"```{prefix}warn [member] (reason)```"
            embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
            embed.set_footer(text="Parameters in [] are required and () are optional")
            return await ctx.send(embed=embed)

        if isinstance(error, commands.MissingPermissions):
            return await ctx.send(f"You cannot use this!")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def warns(self, ctx, member: discord.Member = None):
        await ctx.trigger_typing()
        name = f"GUILD{ctx.guild.id}"
        db = cluster[name]
        prefix = utils.serverprefix(ctx)
        if member is None:
            if ctx.author.guild_permissions.manage_roles:
                if member is None:
                    collection = db['warns']
                    query = {'guild': ctx.guild.id}
                    if collection.count_documents(query) == 0:
                        return await ctx.send(f"There have been no documented warns in **{ctx.guild.name}**.")
                    else:
                        results = collection.find(query)
                    embed = discord.Embed(color=discord.Color.green())
                    embed.set_author(name=f"{ctx.guild.name}'s warns", icon_url=ctx.guild.icon_url)
                    embed.set_thumbnail(url=ctx.guild.icon_url)
                    embed.set_footer(
                        text=f"I cannot send all of the warn cases due to Discord limitations. use `{prefix}warns <@user>` to see warns for a specific user.")
                    countr = 0
                    for i in results:
                        if countr >= 10:
                            break
                        mod = self.client.get_user(int(i['mod']))
                        mem = self.client.get_user(int(i['offender']))
                        embed.add_field(name=f"Warn case #{countr + 1}:",
                                        value=f"Responsible Moderator: **{mod.mention}**\n\nOffender: {mem.mention}\n\nTime: {i['time']} \n\n Reason:```{i['reason']}```")
                        countr += 1
                    return await ctx.send(embed=embed)
        collection = db['warns']
        query = {'offender': member.id}
        if collection.count_documents(query) == 0:
            return await ctx.send(f"**{member.mention}** does not have any warns in **{ctx.guild.name}**")
        else:
            results = collection.find(query)
        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name=f"{member.name}'s warns", icon_url=member.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        countr = 0
        for i in results:
            if countr >= 15:
                break
            mod = self.client.get_user(int(i['mod']))
            embed.add_field(name=f"Warn case #{countr + 1}:",
                            value=f"Responsible Moderator: **{mod.mention}**\n\nTime: {i['time']} \n\n Reason:```{i['reason']}```")
            countr += 1
        await ctx.send(embed=embed)

    @commands.command(aliases=['ot'])
    async def openticket(self, ctx):
        await ctx.message.delete()
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            ctx.message.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        num = random.randint(0000, 1002222384031)
        name = f"open-ticket-{num}"
        channel = await ctx.message.guild.create_text_channel(name, overwrites=overwrites)
        await channel.send(f"{ctx.author.mention}, you have opened a support ticket.")
        desc = f"Someone will be here to assist you shortly.\nWhile you are here, please state your issue/problem."
        embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"InfiniBot Ticketing Tool | Ticket Created by {ctx.author.name}")
        await channel.send(embed=embed)
        try:
            while True:
                message = await self.client.wait_for('message')
                if message.content.lower() == 'ct' or message.content.lower() == 'closeticket':
                    await ctx.trigger_typing()
                    msg = await message.reply(
                        f"{message.author.mention}, if you would like to save this channel, react with the ✅, otherwise react with the :no_entry: emoji to delete this channel.",
                        mention_author=False)
                    await msg.add_reaction("✅")
                    await msg.add_reaction('⛔')

                    def check(reaction, user):
                        return user == message.author and str(reaction.emoji) in ["✅", '⛔']

                    reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=30)
                    print('yes')
                    if reaction.emoji == '⛔':
                        print('hi')
                        await ctx.trigger_typing()
                        await message.channel.send('This channel will be deleted shortly...')
                        await asyncio.sleep(3)
                        await channel.delete()
                        return
                    if reaction.emoji == ("✅"):
                        print("yes")
                        await ctx.trigger_typing()
                        overwrites = {
                            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                            ctx.guild.me: discord.PermissionOverwrite(read_messages=False),
                            # ctx.message.author: discord.PermissionOverwrite(send_messages=True)
                            ctx.message.author: discord.PermissionOverwrite(read_messages=True, send_messages=False)
                        }
                        await message.channel.send('Great, this channel will be saved. Updating overwrites now...')
                        await asyncio.sleep(3)
                        newname = f"closed-ticket-{num}"
                        await channel.edit(overwrites=overwrites, name=newname)
                        return
                else:
                    continue
        except asyncio.TimeoutError:
            await channel.send(f"Since no one responded, I am going to delete the channel automatically in 5 seconds.")
            await asyncio.sleep(5)
            await channel.delete(name)

    @commands.command(aliases=['deleterole'])
    @commands.has_permissions(manage_guild = True)
    async def delrole(self, ctx, role: discord.Role = None):
        prefix = utils.serverprefix(ctx)
        if role is None:
            desc = f"```{prefix}delrole [role]```"
            embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
            embed.set_footer(text="Parameters in [] are required and () are optional")
            return await ctx.send(embed=embed)

        if ctx.author.top_role >= role:
            try:
                await role.delete()
                await ctx.send(f"**{role.name}** has been deleted.")
                return
            except discord.Forbidden:
                await ctx.reply(f"I am missing permissions to delete {role.mention}.")
                return
        await ctx.reply(f"{ctx.author.mention}, you can't use that.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, user: discord.User, reason="No reason given"):
        ban = discord.Embed(description=f"Reason: ```{reason}```\nBy: {ctx.author.mention}",
                            color=discord.Color.dark_red())
        ban.set_author(name=f"{user.name} has been banned.", icon_url=user.avatar_url)
        try:
            await ctx.guild.ban(user, reason=reason)
            await ctx.channel.send(embed=ban)
        except discord.Forbidden:
            return await ctx.send("I do not have proper permissions to ban this person!")

    @hackban.error
    async def hackban_err(self, ctx, error):
        prefix = utils.serverprefix(ctx)
        if isinstance(error, commands.MissingRequiredArgument):
            desc = f"```{prefix}slowmode [channel mention] [duration]```"
            embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
            embed.set_footer(text="Parameters in [] are required and () are optional")
            await ctx.send(embed=embed)
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send("You can't use this!")

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def pin(self, ctx, message:discord.Message = None):
        if message is None:
            if ctx.message.reference:
                msg = await ctx.fetch_message(ctx.message.reference.message_id)
            else:
                msg = ctx.message
        else:
            msg = message
        try:
            await msg.pin()
        except discord.Forbidden:
            return await ctx.send("I don't have permission to pin this message.")
        await ctx.message.add_reaction('👍🏽')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unpin(self, ctx, message: discord.Message = None):
        if message is None:
            if ctx.message.reference:
                msg = await ctx.fetch_message(ctx.message.reference.message_id)
            else:
                msg = ctx.message
        else:
            msg = message
        try:
            await msg.unpin()
        except discord.Forbidden:
            return await ctx.send("I don't have permission to unpin this message.")
        await ctx.message.add_reaction('👍🏽')
#

def setup(client):
    client.add_cog(Moderation(client))


