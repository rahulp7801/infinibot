import discord
import asyncio
from discord.ext import commands
import random
import datetime
from pymongo import MongoClient
import time
import traceback
import sys
import math
import pandas as pd
from modules import utils
import os

with open('mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def servercaptcha(self, member: discord.Member):
        name = f"GUILD{member.guild.id}"
        db = cluster[name]
        collection = db['config']
        results = collection.find({'_id': member.guild.id})
        for i in results:
            welcomerole = i['welcomerole']
        choices = []
        for file in os.listdir('./Discord Bot/Server Captcha'):
            if file.endswith(".png"):
                choices.append(file)
        randnum = random.randint(0, (len(choices) - 1))
        randLib = choices[randnum]
        icon_url = member.guild.icon_url
        desc = f"Please send the captcha code into this DM.\n\nHey there! Before joining **{member.guild.name}**, you are required by the admins" \
               f" to succesfully complete a captcha before you can get verified.\nThis is to protect the server against bot attacks and raids.\n" \
               f"\n**Note: Make sure your captcha response is exactly the same, as the captcha is case-sensitive. You will get 3 tries.\n\n **ANSWER WITHIN 5 MINUTES!"
        gameembed = discord.Embed(title=f"Welcome to {member.guild.name}!", description=desc,
                                  color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
        gamefile = discord.File(f"./Discord Bot/Server Captcha/{randLib}",
                                filename="image.png")
        gameembed.set_image(url="attachment://image.png")
        gameembed.set_author(name=f'{member.guild.name}', icon_url=icon_url)
        gameembed.set_footer(text="InfiniBot | Server Verification")
        await member.send(file=gamefile, embed=gameembed)
        d2 = randLib.split(".")

        def check(m):
            return m.author == member and isinstance(m.channel, discord.DMChannel)

        try:
            t_end = time.time() + 300
            tries = 0
            while time.time() < t_end and tries < 3:
                msg = await self.client.wait_for('message', check=check, timeout=300)
                if msg.content == d2[0]:
                    try:
                        role = discord.utils.get(member.guild.roles, id=int(welcomerole))
                        user = member
                        await user.add_roles(role)
                        confembed = discord.Embed(title=f"Thank you for verifying!",
                                                  description=f'You have been verified in the server **{member.guild.name}**!',
                                                  color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
                        confembed.set_footer(text="InfiniBot Server Verification")
                        await msg.channel.send(embed=confembed)
                        return True
                    except AttributeError:
                        confembed = discord.Embed(title=f"Thank you for verifying!",
                                                  description=f'You have been verified in the server **{member.guild.name}**!',
                                                  color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
                        confembed.set_footer(text="InfiniBot Server Verification")
                        await msg.channel.send(embed=confembed)
                        return True
                else:
                    tries += 1
                    await msg.reply(
                        f"**{msg.author.name}**, that\'s not correct. You have {3 - tries} attempt{'' if tries == 2 else 's'} left.",
                        mention_author=False)
                    continue

            await asyncio.sleep(1)
            dessc = f"{member.mention}, you failed to get the CAPTCHA within three guesses, so you must ask a server moderator to manually give you a role."
            embed = discord.Embed(title="STATUS: FAILED", description=dessc, color=discord.Color.red(),
                                  timestamp=datetime.datetime.utcnow())
            embed.set_author(name=member.guild.name + "'s CAPTCHA Verification", icon_url=icon_url)
            await member.send(embed=embed)
            return False
        except asyncio.TimeoutError:
            await member.send(
                f"{member.name}, you did not answer within 5 minutes, so you must ask a server moderator to manually give you a role.")
            return False

    @commands.Cog.listener()
    async def on_ready(self):
        aitalk = self.client.get_command('talk')
        aitalk.update(enabled=False)
        print(f"{self.client.user.name} is ready, logged on at {datetime.datetime.utcnow()}.")
        while True:
            await asyncio.sleep(10)
            with open('spamdetect.txt', 'r+') as f:
                f.truncate(0)


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                if channel.is_nsfw():
                    continue
                else:
                    await channel.send(
                        f'**Thanks for adding InfiniBot to {guild.name}!**\n'
                        f'I\'m InfiniBot and I hope our relationship can be infinite! To set me up please use `%setup` (limited to admins)\n'
                        f'By using InfiniBot in {guild.name} you agree to the [terms of service](https://docs.google.com/document/d/1XHOKPspuyqUIS9a0d0BMcO5oKXT5Xe5KdN_olG9sGFc/edit?usp=sharing). Use `%tos` to find it again.\n\n'
                        f'**---------------------**\n\n'
                        f'`-` Use `%changeprefix <prefix>` to change the prefix.\n'
                        f'`-` Use `%help` to see all commands.\n'
                        f'If you have a specific question, visit my support server (Coming soon!)')
                    break

        try:
            utils.add_guild_to_db(guild)
        except Exception:
            pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        if str(reaction) == "⭐":
            # make it work for images
            if reaction.count == 1:
                name = f"GUILD{reaction.message.guild.id}"
                db = cluster[name]
                collection = db['config']
                query = {"_id": reaction.message.guild.id}
                if collection.count_documents(query) == 0:
                    return
                else:
                    res = collection.find(query)
                    for result in res:
                        starchannel = result['starchannel']
                    if starchannel == '':
                        return
                    try:
                        chan = self.client.get_channel(int(starchannel))
                    except:
                        return
                    if reaction.message.attachments:
                        desc = f"{f'[Jump to the message!]({reaction.message.jump_url})'}\n\n"
                        embed = discord.Embed(description=desc, color=discord.Color.green(),
                                              timestamp=datetime.datetime.utcnow())
                        embed.set_image(url=reaction.message.attachments[0].url)
                        embed.set_author(name=reaction.message.author.name,
                                         icon_url=reaction.message.author.avatar_url)
                        await chan.send(
                            f"{reaction.message.author.name}'s message in {reaction.message.channel.mention}!")
                        return await chan.send(embed=embed)
                    desc = f"{f'[Jump to the message!]({reaction.message.jump_url})'}"
                    embed = discord.Embed(description=f"{desc}\n\n{reaction.message.content}",
                                          color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=reaction.message.author.name, icon_url=reaction.message.author.avatar_url)
                    embed.set_footer(text=f"Message ID: {reaction.message.id}")
                    await chan.send(
                        f"Sent by {reaction.message.author.name} in {reaction.message.channel.mention}!")
                    await chan.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        db = cluster['COMMANDCOUNT']
        collection = db['commandcount']
        query = {"_id": ctx.guild.id}
        if collection.count_documents(query) == 0:
            ping_cm = {"_id": ctx.guild.id, "count": 1}
            collection.insert_one(ping_cm)
        else:
            user = collection.find(query)
            for result in user:
                count = result['count']
            count += 1
            collection.update_one({"_id": ctx.guild.id}, {"$set": {'count': count}})
        query = {"_id": self.client.user.id}
        if collection.count_documents(query) == 0:
            ping_cm = {"_id": self.client.user.id, "count": 1}
            collection.insert_one(ping_cm)
        else:
            user = collection.find(query)
            for result in user:
                count = result['count']
            count += 1
            collection.update_one({"_id": self.client.user.id}, {"$set": {'count': count}})

    @commands.Cog.listener()
    #eventually, add the afk thing to its own .py file
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.author.system:
            return
        name = f"GUILD{message.guild.id}"
        db = cluster[name]
        collection = db['config']
        counter = 0
        with open('spamdetect.txt', 'r+') as f:
            for lines in f:
                if lines.strip("\n") == str(message.author.id):
                    counter += 1

            f.writelines(f"{str(message.author.id)}\n")
            if counter > 8:
                user = collection.find({'_id': message.guild.id})
                for i in user:
                    spamdetect = i['spamdetect']
                    muterole = i['muterole']
                try:
                    if message.author.guild_permissions.manage_messages or message.author.guild.owner_id == message.author.id:
                        pass
                    if spamdetect.lower().strip() != 'on':
                        pass
                    elif muterole == '':
                        pass
                    else:
                        mute_role = discord.utils.get(message.author.guild.roles, id=muterole)
                        await message.author.add_roles(mute_role)
                        await message.channel.send(f"{message.author.name} has been muted indefinitely for spamming.")
                except discord.Forbidden:
                    pass
        # add option to blacklist channels for spam detection
        x = datetime.datetime.utcnow().strftime('%b%e, %Y')
        name = f"GUILD{message.guild.id}"
        # add more messages params
        # maybe the author param can be the user_id
        collection = db['messages']
        query = {'_id': message.guild.id}
        if collection.count_documents(query) == 0:
            ping_cm = {
                "_id": message.guild.id,
                "name": message.guild.name,
                "count": 1
            }
            collection.insert_one(ping_cm)
        else:
            user = collection.find(query)
            for result in user:
                count = result['count']
            if count == '':
                count = 1
            else:
                count = int(count)
                count += 1
            collection.update_one({'_id': message.guild.id}, {'$set': {'count': str(count)}})



    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        name = f"GUILD{member.guild.id}"
        db = cluster[name]
        collection = db['config']
        res = collection.find({'_id': member.guild.id})
        for i in res:
            logenab = i['logging']
            logchannel = i['logchannel']
        if not before.channel and after.channel:
            collection = db['serverstats']
            ping_cm = {
                "_id": member.id,
                "name": member.name,
                "guild": member.guild.id,
                "gname": member.guild.name,
                "vcstart": datetime.datetime.utcnow()
            }
            x = collection.insert_one(ping_cm)
            if logenab == '' or logchannel == '':
                pass
            else:
                desc = f"{member.mention} joined `{after.channel.name}`"
                embed = discord.Embed(description=desc, color=discord.Color.green(),
                                      timestamp=datetime.datetime.utcnow())
                embed.set_author(name=f"{member.display_name} has joined a voice channel!", icon_url=member.avatar_url)
                embed.set_thumbnail(url=member.guild.icon_url)
                channel = self.client.get_channel(int(logchannel))
                return await channel.send(embed=embed)
        elif before.channel and after.channel:
            if before.channel == after.channel:
                return
            collection = db['serverstats']
            res = collection.find({'_id': member.id})
            for i in res:
                starttime = i['vcstart']
            collection.delete_one({'_id': member.id})
            x = pd.to_datetime(starttime)
            z = (abs(datetime.datetime.utcnow() - x))
            vcsecs = int(z.total_seconds())
            collection = db['serverstats']
            res = collection.find({'_id': member.guild.id})
            for i in res:
                vcmins = i['vcsecs']
            if vcmins == "":
                collection.update_one({'_id': member.guild.id}, {"$set": {'vcsecs': vcsecs}})
            else:
                collection.update_one({'_id': member.guild.id}, {"$set": {'vcsecs': (int(vcmins) + vcsecs)}})
            collection = db['serverstats']
            ping_cm = {
                "_id": member.id,
                "name": member.name,
                "guild": member.guild.id,
                "gname": member.guild.name,
                "vcstart": datetime.datetime.utcnow()
            }
            x = collection.insert_one(ping_cm)
            if logchannel == '' or logenab == '':
                pass
            else:
                desc = f"{member.mention} left `{before.channel.name}`"
                embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
                embed.set_author(name=f"{member.display_name} has left a voice channel!", icon_url=member.avatar_url)
                embed.set_thumbnail(url=member.guild.icon_url)
                channel = self.client.get_channel(int(logchannel))
                await channel.send(embed=embed)
                desc = f"{member.mention} joined `{after.channel.name}`"
                embed = discord.Embed(description=desc, color=discord.Color.green(),
                                      timestamp=datetime.datetime.utcnow())
                embed.set_author(name=f"{member.display_name} has joined a voice channel!", icon_url=member.avatar_url)
                embed.set_thumbnail(url=member.guild.icon_url)
                channel = self.client.get_channel(int(logchannel))
                await channel.send(embed=embed)
        elif before.channel and not after.channel:
            collection = db['serverstats']
            res = collection.find({'_id': member.id})
            for i in res:
                starttime = i['vcstart']
            collection.delete_one({'_id': member.id})
            x = pd.to_datetime(starttime)
            z = (abs(datetime.datetime.utcnow() - x))
            vcsecs = int(z.total_seconds())
            collection = db['serverstats']
            res = collection.find({'_id': member.guild.id})
            for i in res:
                vcmins = i['vcsecs']
            if vcmins == "":
                collection.update_one({'_id': member.guild.id}, {"$set": {'vcsecs': vcsecs}})
            else:
                collection.update_one({'_id': member.guild.id}, {"$set": {'vcsecs': (int(vcmins) + vcsecs)}})
            if logchannel == '' or logenab == '':
                pass
            else:
                desc = f"{member.mention} left `{before.channel.name}`"
                embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
                embed.set_author(name=f"{member.display_name} has left a voice channel!", icon_url=member.avatar_url)
                embed.set_thumbnail(url=member.guild.icon_url)
                channel = self.client.get_channel(int(logchannel))
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        if message.author.system:
            return
        name = f"GUILD{message.guild.id}"
        db = cluster[name]
        collection = db['config']
        res = collection.find({'_id': message.guild.id})
        for i in res:
            ghostcount = i['ghostcount']
            ghostpingon = i['ghostpingon']
            logchannel = i['logchannel']
            logging = i['logging']

        if message.mentions:
            if str(ghostpingon) == "on":
                if str(ghostcount) == '':
                    collection.update_one({'_id': message.guild.id}, {"$set": {'ghostcount': 1}})
                else:
                    collection.update_one({'_id': message.guild.id}, {"$set": {'ghostcount': ghostcount + 1}})
                desc = f"**Ghost ping detected!!**\n\nMessage Author: {message.author.mention}\nMessage: {message.content}"
                embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
                embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                embed.set_thumbnail(url=message.author.avatar_url)
                embed.set_footer(text=f"{message.guild.name} Anti-Ghost Ping")
                await message.channel.send(embed=embed)
            else:
                pass
        if '@everyone' in str(message.content.lower()) or "@here" in str(message.content.lower()):
            if str(ghostpingon) == "on":
                if str(ghostcount) == '':
                    collection.update_one({'_id': message.guild.id}, {"$set": {'ghostcount': 1}})
                else:
                    collection.update_one({'_id': message.guild.id}, {"$set": {'ghostcount': ghostcount + 1}})
                desc = f"**Ghost ping detected!!**\n\nMessage Author: {message.author.mention}\nMessage: {message.content}"
                embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
                embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                embed.set_thumbnail(url=message.author.avatar_url)
                embed.set_footer(text=f"{message.guild.name} Anti-Ghost Ping")
                await message.channel.send(embed=embed)
            else:
                pass

        if message.role_mentions:
            if str(ghostpingon) == "on":
                if str(ghostcount) == '':
                    collection.update_one({'_id': message.guild.id}, {"$set": {'ghostcount': 1}})
                else:
                    collection.update_one({'_id': message.guild.id}, {"$set": {'ghostcount': ghostcount + 1}})
                desc = f"**Ghost ping detected!!**\n\nMessage Author: {message.author.mention}\nMessage: {message.content}"
                embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
                embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                embed.set_thumbnail(url=message.author.avatar_url)
                embed.set_footer(text=f"{message.guild.name} Anti-Ghost Ping")
                await message.channel.send(embed=embed)
            else:
                pass

        if str(logging) == '':
            return
        if str(logchannel) == '':
            return
        pfp = message.author.avatar_url
        author = message.author
        channel = self.client.get_channel(id=int(logchannel))
        mid = message.id
        deletedem = discord.Embed(title=f"Message deleted in #{message.channel.name}",
                                  description=f"```{message.content}```", color=discord.Color.red(),
                                  timestamp=datetime.datetime.utcnow())
        deletedem.set_author(name=str(author), icon_url=pfp)
        deletedem.set_footer(text=f"Message ID: {mid}")
        await channel.send(embed=deletedem)
        return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        name = f"GUILD{member.guild.id}"
        db = cluster[name]
        collection = db['config']
        results = collection.find({'_id': member.guild.id})
        for i in results:
            welcomechannel = i['welcomechannel']
            welcomenick = i['welcomenick']
            logchannel = i['logchannel']
            logging = i['logging']
            welcomemsg = i['welcomemsg']
            privmsg = i['priv_welcomemsg']
            welcomerole = i['welcomerole']
            captchaon = i['captchaon']
        if str(welcomenick) == '':
            pass
        else:
            try:
                await member.edit(nick=str(welcomenick))
            except discord.Forbidden:
                pass
        membercount = member.guild.member_count
        mention = member.mention
        user = member.name
        guild = member.guild
        embed = discord.Embed(
            description=str(welcomemsg).format(members=membercount, member=mention, mention=mention, user=user,
                                               guild=guild),
            color=discord.Color.blurple(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f'{member.name} just joined the server!', icon_url=f'{member.avatar_url}')
        embed.set_thumbnail(url=member.avatar_url)
        try:
            channel = self.client.get_channel(id=int(welcomechannel))
            await channel.send(embed=embed)
        except Exception:
            pass

        try:
            if privmsg == '':
                pass
            else:
                uembed = discord.Embed(
                    description=str(privmsg).format(members=membercount, member=mention, mention=mention, user=user,
                                                    guild=guild),
                    color=discord.Color.green())
                uembed.set_author(name=f'Welcome to {member.guild.name}!', icon_url=f'{member.guild.icon_url}')
                await member.send(embed=uembed)
        except discord.Forbidden:
            pass
        except discord.errors.HTTPException:
            pass

        if str(logging) == 'on':
            try:
                embed1 = discord.Embed(title="Member joined server", description=member.mention,
                                       color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
                embed1.set_author(name=f"{member.guild.name}", icon_url=member.avatar_url)
                embed1.set_thumbnail(url=member.avatar_url)
                channel = self.client.get_channel(id=int(logchannel))
                await channel.send(embed=embed1)
            except discord.Forbidden:
                pass

        if str(captchaon) == "on":
            res = await self.servercaptcha(member)
            if res:
                await member.add_roles(discord.utils.get(member.guild.roles, id=int(welcomerole)))
            else:
                pass
        else:
            if str(welcomerole) == '':
                return
            await member.add_roles(discord.utils.get(member.guild.roles, id=int(welcomerole)))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        name = f"GUILD{member.guild.id}"
        db = cluster[name]
        collection = db['config']
        results = collection.find({'_id': member.guild.id})
        for i in results:
            welcomechannel = i['welcomechannel']
            logchannel = i['logchannel']
            logging = i['logging']
            leavemsg = i['leavemsg']
        if str(welcomechannel) == '':
            return
        else:
            if str(leavemsg) == '':
                leavemsg = "{user} has left the server."
            membercount = member.guild.member_count
            mention = member.mention
            user = member.name
            guild = member.guild
            embed = discord.Embed(
                description=str(leavemsg).format(members=membercount, mention=mention, user=user, guild=guild),
                color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=f'{member.avatar_url}')
            embed.set_author(name=f'{member.name} just left the server.', icon_url=f'{member.avatar_url}')
            embed.set_footer(text=f"User ID: {member.id}")
            channel = self.client.get_channel(id=int(welcomechannel))
            try:
                await channel.send(embed=embed)
            except discord.Forbidden:
                pass
            try:
                channel1 = self.client.get_channel(id=int(logchannel))
                embed1 = discord.Embed(title=f"{member} has left the server", color=discord.Color.greyple(),
                                       timestamp=datetime.datetime.utcnow())
                embed1.set_author(name=member.guild.name, icon_url=member.guild.icon_url)
                embed1.set_thumbnail(url=member.avatar_url)
                embed1.set_footer(text=f"User ID: {member.id}")
                await channel1.send(embed=embed1)
                return
            except discord.Forbidden:
                return

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.guild is None: return
        if before.author == self.client.user:
            return
        if before.author.id == self.client.user.id:
            return
        if before.clean_content == after.clean_content:
            return
        name = f"GUILD{before.guild.id}"
        db = cluster[name]
        collection = db['config']
        results = collection.find({'_id': before.guild.id})
        for i in results:
            ghostpingon = i['ghostpingon']
            ghostcount = i['ghostcount']
            logging = i['logging']
            logchannel = i['logchannel']
        if before.mentions and not after.mentions:
            if str(ghostpingon) == "on":
                if str(ghostcount) == '':
                    collection.update_one({"_id": before.guild.id}, {"$set": {'ghostcount': 1}})
                else:
                    collection.update_one({"_id": before.guild.id}, {"$set": {'ghostcount': int(ghostcount) + 1}})
                desc = f"**Ghost ping detected!!**\n\nMessage Author: {before.author.mention}\nMessage: {before.content}"
                embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
                embed.set_author(name=before.author.name, icon_url=before.author.avatar_url)
                embed.set_thumbnail(url=before.author.avatar_url)
                embed.set_footer(text=f"{before.guild.name} Anti-Ghost Ping")
                await before.channel.send(embed=embed)
            else:
                pass
        if ('@everyone' in str(before.content.lower()) or "@here" in str(before.content.lower())):
            if ('@everyone' not in str(after.content.lower()) and "@here" not in str(after.content.lower())):
                if str(ghostpingon) == "on":
                    if str(ghostcount) == '':
                        collection.update_one({"_id": before.guild.id}, {"$set": {'ghostcount': 1}})
                    else:
                        collection.update_one({"_id": before.guild.id}, {"$set": {'ghostcount': int(ghostcount) + 1}})
                    desc = f"**Ghost ping detected!!**\n\nMessage Author: {before.author.mention}\nMessage: {before.content}"
                    embed = discord.Embed(description=desc, color=discord.Color.red(),
                                          timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=before.author.name, icon_url=before.author.avatar_url)
                    embed.set_thumbnail(url=before.author.avatar_url)
                    embed.set_footer(text=f"{before.guild.name} Anti-Ghost Ping")
                    await before.channel.send(embed=embed)
                else:
                    pass

        if before.role_mentions and not after.role_mentions:
            if str(ghostpingon) == "on":
                if str(ghostcount) == '':
                    collection.update_one({"_id": before.guild.id}, {"$set": {'ghostcount': 1}})
                else:
                    collection.update_one({"_id": before.guild.id}, {"$set": {'ghostcount': int(ghostcount) + 1}})
                desc = f"**Ghost ping detected!!**\n\nMessage Author: {before.author.mention}\nMessage: {before.content}"
                embed = discord.Embed(description=desc, color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
                embed.set_author(name=before.author.name, icon_url=before.author.avatar_url)
                embed.set_thumbnail(url=before.author.avatar_url)
                embed.set_footer(text=f"{before.guild.name} Anti-Ghost Ping")
                await before.channel.send(embed=embed)
            else:
                pass

        if str(logchannel) == '' or str(logging) == '':
            return
        pfp = before.author.avatar_url
        channel = self.client.get_channel(id=int(logchannel))
        desc = f"{before.author.mention} edited a message in {before.channel.mention}! \n\nOriginal: ```{before.content.replace('`', '').replace('<', '').replace('>', '')}```\nUpdated: ```{after.content.replace('`', '').replace('<', '').replace('>', '')}```"
        embed = discord.Embed(description=f"{desc}\n[Jump to message!]({after.jump_url})", color=discord.Color.red(),
                              timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{before.author.name}", icon_url=pfp)
        embed.set_footer(text=f"Message ID: {before.id}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        name = f"GUILD{before.guild.id}"
        db = cluster[name]
        collection = db['config']
        results = collection.find({'_id': before.guild.id})
        for i in results:
            logging = i['logging']
            logchannel = i['logchannel']
        if str(logging) == '' or str(logchannel) == '':
            return
        if before.display_name != after.display_name:
            channel = self.client.get_channel(id=int(logchannel))
            desc = f"Before: ```{before.display_name}``` \nAfter: ```{after.display_name}```"
            embed = discord.Embed(description=desc, color=discord.Color.greyple(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"{before.name} has updated their nickname!", icon_url=before.avatar_url)
            embed.set_footer(text=f"User ID: {before.id}")
            await channel.send(embed=embed)

        if before.roles != after.roles:
            channel = self.client.get_channel(id=int(logchannel))
            if len(before.roles) < len(after.roles):
                newRole = next(role for role in after.roles if role not in before.roles)
                embed = discord.Embed(title="Role was added!", description=newRole.mention,
                                      color=discord.Color.greyple(), timestamp=datetime.datetime.utcnow())
                embed.set_author(name=f"{before}", icon_url=before.avatar_url)
                embed.set_footer(text=f"User ID: {before.id} | Server: {before.guild.name}")
                await channel.send(embed=embed)
            if len(before.roles) > len(after.roles):
                newRole = next(role for role in before.roles if role not in after.roles)
                embed = discord.Embed(title="Role was removed!", description=newRole.mention,
                                      color=discord.Color.greyple(), timestamp=datetime.datetime.utcnow())
                embed.set_author(name=f"{before}", icon_url=before.avatar_url)
                embed.set_footer(text=f"User ID: {before.id} | Server: {before.guild.name}")
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        name = f"GUILD{guild.id}"
        cluster.drop_database(name)


    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        name = f"GUILD{role.guild.id}"
        db = cluster[name]
        collection = db['config']
        results = collection.find({'_id': role.guild.id})
        for i in results:
            logging = i['logging']
            logchannel = i['logchannel']
        if str(logging) == '' or str(logchannel) == '':
            return
        channel = self.client.get_channel(id=int(logchannel))
        embed = discord.Embed(title="New role was created!", description=role.mention, color=discord.Color.greyple(),
                              timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{role.guild.name}", icon_url=role.guild.icon_url)
        embed.set_footer(text=f"Server: {role.guild.name}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        name = f"GUILD{role.guild.id}"
        db = cluster[name]
        collection = db['config']
        results = collection.find({'_id': role.guild.id})
        for i in results:
            logging = i['logging']
            logchannel = i['logchannel']
        if str(logging) == '' or str(logchannel) == '':
            return
        channel = self.client.get_channel(id=int(logchannel))
        embed = discord.Embed(title="Role was deleted", description=f"@{role.name}", color=discord.Color.greyple(),
                              timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{role.guild.name}", icon_url=role.guild.icon_url)
        embed.set_footer(text=f"Server: {role.guild.name}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        # check the documentation for specifics
        name = f"GUILD{before.guild.id}"
        db = cluster[name]
        collection = db['config']
        results = collection.find({'_id': before.guild.id})
        for i in results:
            logging = i['logging']
            logchannel = i['logchannel']
        if str(logging) == '' or str(logchannel) == '':
            return
        channel = self.client.get_channel(id=int(logchannel))
        embed = discord.Embed(title="Role was updated!", description=after.mention, color=discord.Color.greyple(),
                              timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{before.guild.name}", icon_url=before.guild.icon_url)
        embed.set_footer(text=f"Server: {before.guild.name}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        name = f"GUILD{guild.id}"
        db = cluster[name]
        collection = db['config']
        results = collection.find({'_id': guild.id})
        for i in results:
            logging = i['logging']
            logchannel = i['logchannel']
        if str(logging) == '' or str(logchannel) == '':
            return
        channel = self.client.get_channel(id=int(logchannel))
        embed = discord.Embed(title=f"Member was banned from {guild.name}:", description=member.mention,
                              color=discord.Color.greyple(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon_url)
        embed.set_footer(text=f"Server: {guild.name}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        name = f"GUILD{guild.id}"
        db = cluster[name]
        collection = db['config']
        results = collection.find({'_id': guild.id})
        for i in results:
            logging = i['logging']
            logchannel = i['logchannel']
        if str(logging) == '' or str(logchannel) == '':
            return
        channel = self.client.get_channel(id=int(logchannel))
        embed = discord.Embed(title=f"User was unbanned from {guild.name}:", description=member.mention,
                              color=discord.Color.greyple(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon_url)
        embed.set_footer(text=f"Server: {guild.name}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        name = f"GUILD{before.guild.id}"
        db = cluster[name]
        collection = db['config']
        results = collection.find({'_id': before.guild.id})
        for i in results:
            logging = i['logging']
            logchannel = i['logchannel']
        if str(logging) == '' or str(logchannel) == '':
            return
        if before.name != after.name:
            channel = self.client.get_channel(id=int(logchannel))
            desc = f"`{before.name}` --> `{after.name}`"
            embed = discord.Embed(title=f"Channel name was updated in {before.guild.name}:",
                                  description=f"{after.mention} \n\n{desc}",
                                  color=discord.Color.greyple(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"{before.guild.name}", icon_url=before.guild.icon_url)
            embed.set_footer(text=f"Server: {before.guild.name}")
            await channel.send(embed=embed)
        # channel topic i believe falls under here

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        name = f"GUILD{channel.guild.id}"
        db = cluster[name]
        collection = db['config']
        results = collection.find({'_id': channel.guild.id})
        for i in results:
            logging = i['logging']
            logchannel = i['logchannel']
        if str(logging) == '' or str(logchannel) == '':
            return
        channel1 = self.client.get_channel(id=int(logchannel))
        embed = discord.Embed(title=f"New channel created in {channel.guild.name}:",
                              description=channel.mention,
                              color=discord.Color.greyple(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{channel.guild.name}", icon_url=channel.guild.icon_url)
        embed.set_footer(text=f"Server: {channel.guild.name}")
        await channel1.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        name = f"GUILD{channel.guild.id}"
        db = cluster[name]
        collection = db['config']
        results = collection.find({'_id': channel.guild.id})
        for i in results:
            logging = i['logging']
            logchannel = i['logchannel']
        if str(logging) == '' or str(logchannel) == '':
            return
        channel1 = self.client.get_channel(id=int(logchannel))
        embed = discord.Embed(title=f"Channel deleted in {channel.guild.name}:",
                              description=f"**{channel.name}**",
                              color=discord.Color.greyple(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{channel.guild.name}", icon_url=channel.guild.icon_url)
        embed.set_footer(text=f"Server: {channel.guild.name}")
        await channel1.send(embed=embed)

    @commands.Cog.listener() #all errors come here
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound): return
        if isinstance(error, commands.MissingRequiredArgument):
            embed = utils.errmsg(ctx)
            return await ctx.send(embed=embed)
        if isinstance(error, commands.NoPrivateMessage):
            return await ctx.send("This command is not supported in DMs.")
        if isinstance(error, commands.DisabledCommand):
            return await ctx.send(f"**{ctx.command.name}** is temporarily disabled, try again later!")
        error = getattr(error, 'original', error)
        if isinstance(error, commands.BotMissingPermissions):
            regperm = ", ".join(f"**{k}**" for k in error.missing_perms)
            regperm = regperm.replace('_', '')
            await ctx.send(f"I am missing the {regperm} permission{'' if len(regperm) == 1 else 's'} to run this command!")
        if isinstance(error, commands.MissingPermissions):
            regperm = ", ".join(f"**{k}**" for k in error.missing_perms)
            regperm = regperm.replace('_', '')
            await ctx.send(
                f"You are missing the {regperm} permission{'' if len(regperm) == 1 else 's'} to run this command!")
        if isinstance(error, commands.CommandOnCooldown):
            #for patrons:
            #await ctx.reinvoke()
            time = round(error.retry_after)
            desc = f"{ctx.author.mention}, wait `{time}` seconds to use `{ctx.command.name}` again."
            embed = discord.Embed(title="Command on cooldown", description=desc, color=discord.Color.red(),
                                  timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"Message Author: {ctx.author}")
            await ctx.send(embed=embed)
            return
        if isinstance(error, discord.Forbidden): return
        if isinstance(error, commands.MemberNotFound): return await ctx.send(str(error))


def setup(client):
    client.add_cog(Events(client))