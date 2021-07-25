import discord
from discord.ext import commands
import asyncio
from modules import utils, exceptions
import datetime
from pymongo import MongoClient
import math
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

with open('mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

class rr(commands.Cog, name = "Reaction Roles"):
    def __init__(self, client):
        self.client = client
        self.icon = '🔴'
        self.description = 'Reaction roles!'


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print(str(payload.emoji))
        name = f"RR"
        db = cluster[name]
        collection = db['guilds']
        query = {'_id': payload.message_id, 'type':'reaction'}
        if collection.count_documents(query) == 0:
            return
        user = collection.find({'_id': payload.message_id})
        guild1 = payload.guild_id
        guild = self.client.get_guild(guild1)
        member = guild.get_member(int(payload.user_id))
        if member.bot:
            return
        for i in user:
            roles = i['roles']
        for i in roles:
            if payload.emoji.name == i:
                role = discord.utils.get(guild.roles, id=int(roles[i]))
                if role in member.roles:
                    return
                await member.add_roles(role)
                return

    @commands.Cog.listener()
    async def on_button_click(self, button):
        if button.author.bot:
            return
        try:
            name = f"RR"
            db = cluster[name]
            collection = db['guilds']
            query = {'_id': button.message.id, 'type': 'button'}
            if collection.count_documents(query) == 0:
                return
            user = collection.find({'_id': button.message.id})
            guild1 = button.message.guild.id
            guild = self.client.get_guild(guild1)
            member = guild.get_member(int(button.author.id))
            for i in user:
                roles = i['roles']
            for i in roles:
                if button.component.label == i:
                    role = discord.utils.get(guild.roles, id=int(roles[i]))
                    if role in member.roles:
                        await button.respond(type=InteractionType.ChannelMessageWithSource,
                                             content=f"You already have the role **{button.component.label}**!")

                        return
                    await member.add_roles(role)
                    await button.respond(type=InteractionType.ChannelMessageWithSource, content=f"Gave you the role **{button.component.label}**!")
                    return
        except discord.NotFound:
            return

    @commands.group(invoke_without_command = True, help='Set up reaction roles! Use one of the subcommands.')
    async def rr(self, ctx):
        pass

    @rr.command(help='Creates reaction/button roles.')
    async def create(self, ctx):
        await ctx.trigger_typing()
        try:
            await ctx.send(f"Hey **{ctx.author.name}**, would you like to assign roles using buttons or reactions?\n\n**NOTE**: With buttons, sadly, there "
                           f"is a limitation of 25 max.\nReply with `button` for buttons or `reaction` for reactions.")
            def check(m):
                return (m.author == ctx.author and m.channel == ctx.channel and m.content.lower().strip() in ['button', 'reaction'])
            msg = await self.client.wait_for('message', check=check, timeout = 120)
            if msg.content.lower().strip() == 'button':
                settingup = "button"
            else:
                settingup = 'reaction'
            await ctx.send(f"Excellent! We will be setting up {settingup} roles!")
            await asyncio.sleep(1)
            await ctx.send(f"Now, which channel would you like this to be in?")
            counter = 0
            while True:
                if counter > 5:
                    return await ctx.send("Due to too many invalid choices, this session has ended.")
                msg = await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 120)
                try:
                    channel = msg.channel_mentions[0].id
                    break
                except IndexError:
                    await ctx.send("It looks like you did not mention a channel, try again?")
                    counter += 1
                    continue
            try:
                channel = self.client.get_channel(int(channel))
            except Exception as e:
                print(e)
            if str(channel.type) == 'voice':
                return await ctx.send(f"Unfortunately, you can't set a voice channel to be the reaction channel.")
            elif str(channel.type) == 'category':
                return await ctx.send(f"Unfortunately, you can't set a category channel to be the reaction channel.")
            res = utils.channelperms(channel)
            if not res:
                return await ctx.send(f"Please give me permission to `View Channel`, `Send Messages`, and `Embed Links` in {channel.mention} before proceeding.")
            desc = f"Role channel for **{ctx.guild.name}** has been set to {channel.mention}."
            embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp = datetime.datetime.utcnow())
            await msg.reply(embed=embed, mention_author=False)
            desc = f"What should the message content be? Use this format:\n" \
                       f"```Title | Message Content```\n\n" \
                   f"If you want me to automatically do this, type `continue`."
            embed = discord.Embed(description = desc, color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
            await ctx.send(embed=embed)
            while True:
                message = await self.client.wait_for('message', check=lambda m: (m.author == ctx.author and m.channel == ctx.channel), timeout = 300)
                takecare = True
                name = f"RR"
                db = cluster[name]
                collection = db['guilds']
                if message.content.lower().strip() == 'continue':
                    await ctx.send("Excellent, I will take care of that myself!")
                    title = "Reaction Role Menu"
                    description = "Click on a button for roles!"
                    break
                elif "|" not in message.content:
                    await ctx.send(f"It looks like {message.content} has been formatted incorrectly, try again?")
                    continue
                else:
                    takecare = False
                    z = message.content.strip().split("|")
                    await ctx.send(f"Ok, I will keep `{z[0]}` as the title and `{z[1]}` as the description! This is a **preview** of what the message will look like!")
                    embed = discord.Embed(title=str(z[0]).strip(), description=str(z[1]).strip(),
                                          color=discord.Color.green())
                    await ctx.send(embed=embed)
                    title = z[0]
                    description = z[1]
                    break
            ping_cm = {
                "id": ctx.message.id,
                "msgtitle": title,
                'roles': ''
            }
            x = collection.insert_one(ping_cm)
            await asyncio.sleep(1)
            resultarr = []
            mongodict ={}

            if settingup == 'reaction':
                await ctx.send(f"Great. Now it is time to assign roles. The format is the name of the emoji"
                               f" and then the role mention, and split the two by a `|`. Unfortunately, we are currently limited to default emojis, "
                               f"not any custom ones. **CASE SENSITIVE!** Example:```:sunglasses: | @cool kid```\n"
                               f"Type `done` when you are finished.")
                namearr = []
                while True: #limit needs to be defined as the number of reaction role messages a server has, but for testing purposes i wont keep it
                    message = await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 180)
                    if message.content.lower().strip() == 'done':
                        break
                    try:
                        args = message.content.split('|')
                        print(args)
                        emoji = (args[0].replace(':', '').strip())
                        xz = discord.utils.get(ctx.guild.roles, id=int(f"{args[1].strip().replace('<@&', '').replace('>', '')}"))
                        res = utils.rolecheck(xz, ctx)
                        if not res:
                            await ctx.send(res[1])
                            continue
                        elif namearr.count(emoji) == 1:
                            await ctx.send("You already set this emoji!")
                            continue
                        await message.add_reaction("👍🏽")
                        if resultarr.count(emoji) == 1 or resultarr.count(xz) == 1:
                            continue #add more check later, just getting basic functuonarlity
                        resultarr.append((args[0].strip(), args[1].strip()))
                        mongodict.__setitem__(args[0].strip(), args[1].strip().replace('>', "").replace('<@&', ''))
                        namearr.append(emoji)
                        continue
                    except IndexError:
                        await ctx.send(f"Did you format that correctly? Try again.")
                        continue
                    except Exception as e:
                        print(e)

                if len(resultarr) == 0:
                    return await ctx.send("It looks like you did not mention any roles, so I have ended this session.\nDon't try to break me <:AngryInfini:842156223037964299>")

                try:
                    if takecare:
                        arr = []
                        for i in resultarr:
                            roleid = str(i[1]).replace('>', "").replace('<@&', '')
                            role = discord.utils.get(ctx.guild.roles, id=int(roleid))
                            arr.append(f"{i[0]}: {role.mention}")
                        x = '\n'.join(arr)
                        embed = discord.Embed(title = f"{str(title).strip()}", description = f"{x}", color = discord.Color.green())
                        message = await channel.send(embed=embed)
                        for i in resultarr:
                            await message.add_reaction(str(i[0]))

                    else:
                        embed = discord.Embed(title=f"{str(z[0]).strip()}", description=f"{description.strip()}", color=discord.Color.green())
                        message = await channel.send(embed=embed)
                        for i in resultarr:
                            await message.add_reaction(str(i[0]))
                except ValueError as e:
                    await ctx.send("Unfortunately, we cannot take custom emojis at the moment.")
                finally:
                    print(mongodict)
                    x = collection.insert_one({'_id': message.id, 'roles': mongodict, 'type': settingup, 'gid':ctx.guild.id})
                    collection.delete_one({'id': ctx.message.id})
            else:
                await ctx.send(f"Great. Now it is time to assign roles. All you need to do is mention the roles, one by one after you see that I added a "
                               f"reaction to confirm I have saved it.\n\nYou can start now.\nType `done` when you are finished.")
                namearr = []
                while True:
                    message = await self.client.wait_for('message', check=lambda
                        m: m.author == ctx.author and m.channel == ctx.channel, timeout=180)
                    if message.content.lower().strip() == 'done':
                        break
                    try:
                        role = message.role_mentions[0].id
                        role = discord.utils.get(ctx.guild.roles, id=int(role))
                        res = utils.rolecheck(role, ctx)
                        if not res:
                            await ctx.send(res[1])
                            continue
                        if namearr.count(role.id) == 1:
                            await ctx.send("You already set this role!")
                            continue
                        resultarr.append((role.name, role.id))
                        namearr.append(role.id)
                        mongodict.__setitem__(role.name, role.id)
                        await message.add_reaction("👍🏽")
                    except IndexError:
                        await ctx.send("Are you sure you mentioned a role? Try again...")

                if len(resultarr) > 25:
                    return await ctx.send(f"Looks like you had too many roles. You had `{len(resultarr)}`, and the limit is 25. \n"
                                          f"Try again with creating a new message per 25.")
                if len(resultarr) == 0:
                    return await ctx.send("It looks like you did not mention any roles, so I have ended this session.\nDon't try to break me <:AngryInfini:842156223037964299>")

                try:
                    x = ((len(resultarr)) / 5)
                    arrlen = (math.ceil(x))
                    print(arrlen)
                    arr = [[] for i in range(arrlen)]
                    counter = 0
                    for i in range(arrlen):
                        try:
                            for k in range(5):
                                arr[i].append(Button(style=ButtonStyle.blue, label=f'{resultarr[counter][0]}'))
                                counter += 1
                            counter += 1
                        except IndexError:
                            break
                    embed = discord.Embed(title=f"Button Role Menu", description=f"{description.strip()}",
                                          color=discord.Color.green())
                    message = await channel.send(embed=embed, components = arr)
                    x = collection.insert_one({'_id': message.id, 'roles': mongodict, 'type': settingup, 'gid':ctx.guild.id})
                    collection.delete_one({'id': ctx.message.id})
                except Exception as e:
                    print(e)

        except asyncio.TimeoutError:
            return await ctx.send('You took too long.')

def setup(client):
    client.add_cog(rr(client))