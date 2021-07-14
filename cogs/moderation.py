import discord
from discord.ext import commands, tasks
import asyncio
from pymongo import MongoClient
import datetime
import random
import pandas as pd
from discord_components import DiscordComponents
from modules import utils
import logging
#automoderation will be another cog
with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.icon = '🛠️'
        self.description = f'Moderate your server or take a step back and let InfiniBot moderate for you!'
        self.unmute_loop.start()

    def cog_unload(self):
        self.unmute_loop.close()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            name = f"CONFIGURATION"
            db = cluster[name]
            collection = db['guilds']
            query = {'id': payload.guild_id}
            if collection.count_documents(query) == 0:
                return
            user = collection.find({'msgid': payload.message_id, 'id': payload.guild_id})
            guild1 = payload.guild_id
            guild = self.client.get_guild(guild1)
            member = guild.get_member(int(payload.user_id))
            channel = payload.channel_id
            channel = self.client.get_channel(channel)
            message = await channel.fetch_message(payload.message_id)
            await message.remove_reaction('🎟️', member)
            if member.bot:
                return
            for i in user:
                role = i['supportrole']
            if role == '': role = None
            else: role = discord.utils.get(guild.roles, id=int(role))
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                member: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            num = random.randint(0000, 1002222384031)
            name = f"open-ticket-{num}"
            channel = await guild.create_text_channel(name, overwrites=overwrites)
            await channel.send(f"{member.mention}, you have opened a support ticket. {role.mention if role is not None else ''}")
            desc = f"Someone will be here to assist you shortly.\nWhile you are here, please state your issue/problem"
            embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"InfiniBot Ticketing Tool | Ticket Created by {member.name}")
            embed.title = "Support ticket opened"
            await channel.send(embed=embed)
        except UnboundLocalError:
            pass

    @tasks.loop(seconds=60)
    async def unmute_loop(self):
        db = cluster['TEMP']
        collection = db['muted']
        arr = []
        results = collection.find()
        for i in results:
            arr.append((i['id'], i['gid'], i['fintime']))
        if not arr:
            return
        for k in arr:
            try:
                if pd.to_datetime(k[2]) < datetime.datetime.utcnow():
                    guild = self.client.get_guild(int(k[1]))
                    user = guild.get_member(int(k[0]))
                    name = f"CONFIGURATION"
                    db = cluster[name]
                    collection = db['guilds']
                    results = collection.find({'_id': guild.id})
                    for i in results:
                        muterole = i['muterole']
                    if str(muterole) == '': #shouldnt happen
                        continue
                    else:
                        db = cluster['TEMP']
                        collection = db['muted']
                        role = discord.utils.get(guild.roles, id=int(muterole))
                        try:
                            await user.remove_roles(role)
                            collection.delete_one({'id':int(user.id), "gid":int(guild.id)})
                            continue
                        except discord.Forbidden:
                            collection.delete_one({'id': int(user.id), "gid": int(guild.id)})
                            continue
            except Exception as e:
                errmsg = f"While parsing through mutes, exception {e} was raised. {datetime.datetime.utcnow()}"
                logging.basicConfig(filename='./errors.log')
                logging.error(errmsg)
                continue
        collection = db['bans']
        arr = []
        results = collection.find()
        for i in results:
            arr.append((i['id'], i['gid'], i['fintime']))
        if not arr:
            return
        for k in arr:
            try:
                if pd.to_datetime(k[2]) < datetime.datetime.utcnow():
                    guild = self.client.get_guild(int(k[1]))
                    user = guild.get_member(int(k[0]))
                    try: #unban
                        await guild.unban(user=user)
                        collection.delete_one({'id':int(user.id), "gid":int(guild.id)})
                        continue
                    except discord.Forbidden:
                        collection.delete_one({'id': int(user.id), "gid": int(guild.id)})
                        continue
            except Exception as e:
                errmsg = f"While parsing through bans, exception {e} was raised. {datetime.datetime.utcnow()}"
                logging.basicConfig(filename='./errors.log')
                logging.error(errmsg)
                continue

    @unmute_loop.before_loop
    async def beforeunmute(self):
        await self.client.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        DiscordComponents(self.client, change_discord_methods=True)

    @commands.command(help='Clears the chat')
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount:int, user:discord.User = None):
        try:
            if user is None:
                await ctx.channel.purge(limit=amount + 1)
            else:
                check = lambda msg: msg.author == user and msg.channel == ctx.channel
                await ctx.channel.purge(limit=amount + 1, check=check)
            await asyncio.sleep(2)
            await ctx.send(f"Cleared {amount + 1} messages!", delete_after = 5)
        except discord.errors.HTTPException:
            await ctx.send("I cannot delete messages past two weeks old!", delete_after = 5)
            return

    @commands.command(help='Bans a member')
    @commands.guild_only()
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
            try:
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
            except discord.Forbidden:
                return await ctx.send("I cannot ban this person.")

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


    @commands.command(help='Temporarily bans a member, specify a duration.')
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    async def tempban(self, ctx, member:discord.Member, *, duration):
        duration = utils.tmts(duration.strip())
        durlen = utils.stringfromtime(duration)
        try:
            pfp = member.avatar_url
            author = member
            embed = discord.Embed(description="For reason: ```Naughty```", color=discord.Color.dark_red())
            embed.set_author(name=str(author) + f" has been banned for {durlen}.", icon_url=pfp)
            uembed = discord.Embed(title=f"You have been banned in {ctx.guild.name}",
                                   description=f"For reason: ```Naughty```", color=discord.Color.blurple())
            uembed.set_footer(text="If you believe this is in error, please contact an Admin.")
            if member.top_role >= ctx.author.top_role:
                await ctx.send(f"You can only use this moderation on a member below you.")
                return
            else:
                try:
                    if not member.bot:
                        await ctx.guild.ban(member, reason='Naughty')
                        await ctx.send(embed=embed)
                        try:
                            await member.send(embed=uembed)
                        except:
                            await ctx.send(f'A reason could not be sent to `{member}` as they had their dms off.')
                    else:
                        await ctx.guild.ban(member, reason='Naughty')
                        await ctx.send(embed=embed)
                except discord.Forbidden:
                    return await ctx.send("I cannot ban this person.")

                db = cluster['TEMP']
                collection = db['bans']
                query = {'id': member.id, 'gid': member.guild.id}
                if collection.count_documents(
                        query) == 0:  # only real choice here, a person cant get temp banned twice in the same server
                    ping_cm = {
                        "id": member.id,
                        "gid": ctx.guild.id,
                        "fintime": datetime.datetime.utcnow() + datetime.timedelta(seconds=duration)
                    }
                    collection.insert_one(ping_cm)
        except AttributeError as e:
            print(e)
            await ctx.reply("An error has occurred. The devs have been notified and will look into it.")
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
        if isinstance(error, commands.MemberNotFound):
            return await ctx.reply("Please mention someone to ban.")

    @commands.command(help='Kicks a member from your server.')
    @commands.guild_only()
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
                    try:
                        await ctx.guild.kick(member, reason=reason)
                        await ctx.channel.send(embed=kick)
                        try:
                            await member.send(embed=ukick)
                        except discord.Forbidden:
                            await ctx.send(f'A reason could not be sent to `{member}` as they had their dms off.')
                    except discord.Forbidden:
                        return await ctx.send("I cannot kick this person.")
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


    @commands.command(help='Unbans a member from your server!')
    @commands.guild_only()
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
        if isinstance(error, commands.UserNotFound):
            nban = discord.Embed(color=discord.Color.red())
            nban.set_author(name=f"User is not banned or doesn\'t exist!")
            await ctx.send(embed=nban)
    @commands.command(help='Mutes a member. If you haven\'t specified a muterole, this will not work.')
    @commands.guild_only()
    @commands.has_permissions(manage_roles = True)
    async def mute(self, ctx, member:discord.Member, *, dur = None):
        if member == self.client.user:
            return await ctx.send("I can't mute myself.")
        name = f"CONFIGURATION"
        db = cluster[name]
        collection = db['guilds']
        results = collection.find({'_id': ctx.guild.id})
        for i in results:
            muterole = i['muterole']
        if muterole is None or muterole == '':
            return await ctx.send(f"You haven't specified a muterole for me yet! Run `{ctx.prefix}setup muterole`!")
        prefix = ctx.prefix
        role = discord.utils.get(ctx.guild.roles, id=int(muterole))
        if role in member.roles:
            await ctx.send(f"`{member}` is already muted.")
            return
        if dur is not None:
            try:
                duration = utils.tmts(dur.strip())
                db = cluster['TEMP']
                collection = db['muted']
                query = {'id': member.id, 'gid':member.guild.id}
                if collection.count_documents(query) == 0: #only real choice here, a person cant get muted twice in the same server
                    ping_cm = {
                        "id": member.id,
                        "gid": ctx.guild.id,
                        "fintime": datetime.datetime.utcnow() + datetime.timedelta(seconds=duration)
                    }
                    collection.insert_one(ping_cm)
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
        if isinstance(error, commands.MemberNotFound):
            return await ctx.reply(error, mention_author=False)

    @commands.command(help='Unmutes a user in your server.')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        name = f"CONFIGURATION"
        db = cluster[name]
        collection = db['guilds']
        results = collection.find({'_id': ctx.guild.id})
        for i in results:
            muterole = i['muterole']
        if muterole is None or muterole == '':
            return await ctx.send(f"You haven't specified a muterole for me yet! Run `{ctx.prefix}setup muterole`!")
        pfp = member.avatar_url
        author = member
        role = discord.utils.find(lambda r: r.id == int(muterole), ctx.message.guild.roles)
        await member.remove_roles(role)
        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name=str(author) + " has been unmuted.", icon_url=pfp)
        await ctx.send(embed=embed)

    @commands.command(help='Removes Send message permissions for @everyone')
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        desc = str("🔒") + ctx.channel.mention + " **is now in lockdown.**"
        embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @lockdown.error
    async def lockdown_err(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            return await ctx.send("I don't have the Manage Channel permission for that channel.")

    @commands.command(help='Gives back Send Message permissions to @everyone')
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        res = await utils.channelperms(ctx.channel)
        if not res:
            raise ValueError(res[1])
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        desc = (str("🔓") + ctx.channel.mention + " ***has been unlocked.***")
        embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @unlock.error
    async def unlock_err(self, ctx, error):
        error = error.original
        if isinstance(error, ValueError):
            return await ctx.send(f"I don't have the `Manage Channel` permission for {ctx.channel.mention}.")

    @commands.command(aliases = ['rename', 'nickname'], help='Nick a member')
    @commands.guild_only()
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


    @commands.command(help='Bans and immediately unbans a user to delete messages.')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member = None, *, reason="To delete messages"):
        if member is None:
            embed = utils.errmsg(ctx)
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

    @commands.command(help='Warns a user')
    @commands.guild_only()
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
        db = cluster['WARNS']
        collection = db['guilds']
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

    @commands.command(help='Get a list of warns')
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def warns(self, ctx, member: discord.Member = None):
        await ctx.trigger_typing()
        db = cluster['WARNS']
        prefix = ctx.prefix
        if member is None:
            if ctx.author.guild_permissions.manage_roles:
                if member is None:
                    collection = db['guilds']
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
        collection = db['guilds']
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

    # @commands.command(aliases=['ot'])
    # @commands.guild_only()
    # async def openticket(self, ctx):
    #     await ctx.message.delete()
    #     overwrites = {
    #         ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
    #         ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
    #         ctx.message.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    #     }
    #     num = random.randint(0000, 1002222384031)
    #     name = f"open-ticket-{num}"
    #     channel = await ctx.message.guild.create_text_channel(name, overwrites=overwrites)
    #     await channel.send(f"{ctx.author.mention}, you have opened a support ticket.")
    #     desc = f"Someone will be here to assist you shortly.\nWhile you are here, please state your issue/problem."
    #     embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
    #     embed.set_footer(text=f"InfiniBot Ticketing Tool | Ticket Created by {ctx.author.name}")
    #     await channel.send(embed=embed)
    #     try:
    #         while True:
    #             message = await self.client.wait_for('message')
    #             if message.content.lower() == 'ct' or message.content.lower() == 'closeticket':
    #                 await ctx.trigger_typing()
    #                 msg = await message.reply(
    #                     f"{message.author.mention}, if you would like to save this channel, react with the ✅, otherwise react with the :no_entry: emoji to delete this channel.",
    #                     mention_author=False)
    #                 await msg.add_reaction("✅")
    #                 await msg.add_reaction('⛔')
    #
    #                 def check(reaction, user):
    #                     return user == message.author and str(reaction.emoji) in ["✅", '⛔']
    #
    #                 reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=30)
    #                 print('yes')
    #                 if reaction.emoji == '⛔':
    #                     print('hi')
    #                     await ctx.trigger_typing()
    #                     await message.channel.send('This channel will be deleted shortly...')
    #                     await asyncio.sleep(3)
    #                     await channel.delete()
    #                     return
    #                 if reaction.emoji == ("✅"):
    #                     print("yes")
    #                     await ctx.trigger_typing()
    #                     overwrites = {
    #                         ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
    #                         ctx.guild.me: discord.PermissionOverwrite(read_messages=False),
    #                         # ctx.message.author: discord.PermissionOverwrite(send_messages=True)
    #                         ctx.message.author: discord.PermissionOverwrite(read_messages=True, send_messages=False)
    #                     }
    #                     await message.channel.send('Great, this channel will be saved. Updating overwrites now...')
    #                     await asyncio.sleep(3)
    #                     newname = f"closed-ticket-{num}"
    #                     await channel.edit(overwrites=overwrites, name=newname)
    #                     return
    #             else:
    #                 continue
    #     except asyncio.TimeoutError:
    #         await channel.send(f"Since no one responded, I am going to delete the channel automatically in 5 seconds.")
    #         await asyncio.sleep(5)
    #         await channel.delete(name)

    @commands.command(aliases=['deleterole'], help='Deletes a role')
    @commands.guild_only()
    @commands.has_permissions(manage_guild = True)
    async def delrole(self, ctx, role: discord.Role = None):
        if role is None:
            embed = utils.errmsg(ctx)
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

    @commands.command(help='"Hackbans" a person (Ban before join)')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, user: discord.User, reason="No reason given"):
        ban = discord.Embed(description=f"Reason: ```{reason}```\nBy: {ctx.author.mention}",
                            color=discord.Color.dark_red())
        ban.set_author(name=f"{user.name} has been hack-banned.", icon_url=user.avatar_url)
        try:
            await ctx.guild.ban(user, reason=reason)
            await ctx.channel.send(embed=ban)
        except discord.Forbidden:
            return await ctx.send("I do not have proper permissions to ban this person!")

    @commands.command(help='Pins a message. Reference the message or pins the invocation message.')
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

    @commands.command(help='Unpins a message.')
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

    @commands.command(help='Sets up a ticketing system!')
    @commands.guild_only()
    @commands.has_permissions(manage_guild = True)
    async def setupticketing(self, ctx, title = None):
        name = f"CONFIGURATION"
        db = cluster[name]
        embed = discord.Embed(color = discord.Color.blue())
        if title is None:
            title = f"{ctx.guild.name} Ticketing"
        embed.title = title
        embed.description = "To create a ticket react with 🎟️!"
        embed.set_footer(text = "Advanced Ticketing", icon_url=self.client.user.avatar_url)
        try:
            await ctx.send("What channel would you like this message to be sent in?\nMention it below.")
            while True:
                msg = await self.client.wait_for('message', check=lambda m: m.channel == ctx.channel and m.author == ctx.author, timeout = 120)
                try:
                    channel = msg.channel_mentions[0].id
                    channel = self.client.get_channel(channel)
                    break
                except IndexError:
                    await ctx.send("Did you mention a channel? Try again...")
                    continue
            await ctx.send("Would you like a role to be pinged when a ticket gets opened? Reply with `yes` or `no`.")
            msg = await self.client.wait_for('message', check=lambda m: (m.channel == ctx.channel and m.author == ctx.author and m.content.lower().strip() in ['yes', 'no']), timeout = 120)
            if msg.content.lower().strip() == 'yes':
                await ctx.send("Please mention the role below...")
                while True:
                    msg = await self.client.wait_for('message', check=lambda m: m.channel == ctx.channel and m.author == ctx.author, timeout = 120)
                    try:
                        role = msg.role_mentions[0].id
                        role = discord.utils.get(ctx.guild.roles, id=role)
                        break
                    except IndexError:
                        await ctx.send("I didn\'t catch a role in that message. Try again?")
                        continue
                collection = db['guilds']
                try:
                    message = await channel.send(embed=embed)
                    await message.add_reaction('🎟️')
                    query = {'id': ctx.guild.id}
                    if collection.count_documents(query) == 0:
                        collection.insert_one({'id': ctx.guild.id, 'supportrole': role.id, 'msgid':message.id})
                    else:
                        collection.update_one({'id': ctx.guild.id}, {'$set': {'supportrole': role.id, 'msgid':message.id}})
                    await ctx.send("Success! I have saved your preferences and have sent the message...")
                    return
                except Exception as e:
                    print(e)
            else:
                return await ctx.send('Ok, cancelling.')
        except asyncio.TimeoutError:
            return await ctx.send("You took too long.")

    @commands.command(aliases = ['ct'], help='Closes an open ticket')
    @commands.guild_only()
    @commands.has_permissions(manage_guild = True)
    async def closeticket(self, ctx):
        name = f"CONFIGURATION"
        db = cluster[name]
        collection = db['guilds']
        query = {'id': ctx.guild.id}
        if collection.count_documents(query) == 0:
            return
        user = collection.find({'id': ctx.guild.id})
        for i in user:
            role = i['supportrole']
            break
        if ctx.channel.name.startswith('open-ticket-'):
            newname = ctx.channel.name.removeprefix('open-ticket-')
            await ctx.trigger_typing()
            msg = await ctx.reply(
                f"{ctx.author.mention}, if you would like to save this channel, react with the ✅, otherwise react with the :no_entry: emoji to delete this channel.",
                mention_author=False)
            await msg.add_reaction("✅")
            await msg.add_reaction('⛔')
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["✅", '⛔']

            reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=60)
            if reaction.emoji == '⛔':
                await ctx.trigger_typing()
                await ctx.channel.send('This channel will be deleted shortly...')
                await asyncio.sleep(3)
                await ctx.channel.delete()
                return
            elif reaction.emoji == ("✅"):
                await ctx.trigger_typing()
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    ctx.guild.me: discord.PermissionOverwrite(read_messages=False),
                    # ctx.message.author: discord.PermissionOverwrite(send_messages=True)
                    ctx.message.author: discord.PermissionOverwrite(read_messages=True, send_messages=False),
                    role: discord.PermissionOverwrite(read_messages=True, send_messages=False)
                }
                await ctx.channel.send('Great, this channel will be saved. Updating overwrites now...')
                await asyncio.sleep(3)
                newname = f"closed-ticket-{newname}"
                await ctx.channel.edit(overwrites=overwrites, name=newname)
                return

    @commands.command(name = 'clearstarboard', help='Clears all starboard messages')
    @commands.guild_only()
    @commands.has_permissions(manage_guild = True)
    async def clear_starboard(self, ctx):
        res = await utils.clear_guild_starboard_messages(ctx.guild)
        if not res:
            return await ctx.send(str(res[1]))
        await ctx.message.add_reaction('✅')

    @commands.command(help='Deletes all open tickets.')
    @commands.guild_only()
    @commands.has_permissions(manage_guild = True)
    async def closealltickets(self, ctx):
        for channel in ctx.guild.text_channels:
            if channel.name.startswith('open-ticket-'):
                try:
                    await channel.delete()
                except:
                    pass

    @commands.command(help='Nukes a channel, creates a new one with same permissions.')
    @commands.guild_only()
    @commands.has_permissions(manage_channels = True)
    async def nuke(self, ctx, channel:discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        try:
            embed = discord.Embed(color = discord.Color.green())
            embed.description = f"Are you sure you want to nuke {channel.mention}? React to confirm."
            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')
            await message.add_reaction('❌')

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌']
            reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=100)
            if reaction.emoji == '❌':
                return await ctx.send("Cancelling...")
            newchannel = await channel.clone()
            await channel.delete()
            await newchannel.send(f"#{channel.name} has been nuked successfully!")
            return
        except discord.Forbidden:
            return await ctx.send(f"I do not have the `Manage Channel` permission for {channel.mention}.")
        except asyncio.TimeoutError:
            return await ctx.reply("Timed out", mention_author = False)

    @commands.command(help='Kick a member from a voice channel.')
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def vckick(self, ctx, member: discord.Member):
        await member.edit(voice_channel=None)
        await ctx.send(f"**{member.name}** has been successfully kicked from VC!")

    @commands.command(help = 'Moves a member to a voice channel.')
    @commands.guild_only()
    @commands.has_permissions(manage_guild = True)
    async def move(self, ctx, member:discord.Member, channel:discord.VoiceChannel):
        try:
            await member.edit(voice_channel=channel)
            await ctx.send(f"**{member.name}** has been successfully moved to {channel.mention}!")
        except discord.Forbidden:
            return await ctx.send(f"I don\'t have permission to move `{member.name}#{member.discriminator}` to {channel.mention}!")

    @commands.command(aliases = ['permissions'], help='Get a list of your allowed and denied permissions.')
    @commands.guild_only()
    async def perms(self, ctx, member:discord.Member = None):
        if member is None:
            member = ctx.author
        giv = []
        den = []
        for i in ctx.channel.permissions_for(member):
            if i[1]:
                giv.append(str(i[0]).replace('_', ' ').title())
            else:
                den.append(str(i[0]).replace('_', ' ').title())
        embed = discord.Embed(color = discord.Color.green())
        embed.add_field(name = "Given", value="\n".join(giv))
        embed.add_field(name='Denied', value='\n'.join(den))
        await ctx.send(embed=embed)

    @commands.command(help='Clear only your messages.')
    @commands.bot_has_permissions(manage_messages = True)
    async def clearmine(self, ctx, limit:int = 50):
        user = ctx.author
        check = lambda msg: msg.author == ctx.author and not msg.pinned
        await ctx.message.delete()
        try:
            await ctx.channel.purge(limit=limit, check=check)
            await ctx.send(f"`{limit}` messages deleted for `{user.name}#{user.discriminator}` in {ctx.channel.mention}.", delete_after = 5)
        except discord.HTTPException:
            await ctx.send("I cannot delete messages older than 2 weeks!", delete_after = 5)
            return

    @commands.command(help='Mutes someone in voice chat.')
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def voicemute(self, ctx, member: discord.Member, on):
        if on.lower() not in ['true', 'false']:
            raise commands.MissingRequiredArgument
        try:
            mute = False if on.title() == 'False' else True
            await member.edit(mute=mute)
            await ctx.send(f"**{member.name}** has been successfully {'muted' if mute else 'unmuted'}!")
        except discord.Forbidden:
            return await ctx.send(
                f"I don\'t have permission to {'mute' if mute else 'unmute'} `{member.name}#{member.discriminator}`!")

    @commands.command(help='Deafen someone in voice chat.')
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def voicedeafen(self, ctx, member: discord.Member, on):
        if on.lower() not in ['true', 'false']:
            raise commands.MissingRequiredArgument
        try:
            mute = False if on.title() == 'False' else True
            await member.edit(deafen=mute)
            await ctx.send(f"**{member.name}** has been successfully {'deafened' if mute else 'undeafened'}!")
        except discord.Forbidden:
            return await ctx.send(
                f"I don\'t have permission to {'deafen' if mute else 'undeafen'} `{member.name}#{member.discriminator}`!")



def setup(client):
    client.add_cog(Moderation(client))


