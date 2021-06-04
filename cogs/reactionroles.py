import discord
from discord.ext import commands
import asyncio
from modules import utils, exceptions
import datetime
from pymongo import MongoClient

with open('mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

class rr(commands.Cog, name = "Reaction Roles"):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        name = f"GUILD{payload.guild_id}"
        db = cluster[name]
        collection = db['reactionroles']
        query = {'_id': payload.message_id}
        if collection.count_documents(query) == 0:
            return
        user = collection.find({'_id': payload.message_id})
        guild1 = payload.guild_id
        guild = self.client.get_guild(guild1)
        member = guild.get_member(int(payload.user_id))
        for i in user:
            roles = i['roles']
        for i in roles:
            if payload.emoji.name == i:
                role = discord.utils.get(guild.roles, id=int(roles[i]))
                if role in member.roles:
                    return
                await member.add_roles(role)
                return

    @commands.group(invoke_without_command = True)
    async def rr(self, ctx):
        pass

    @rr.command()
    async def create(self, ctx):
        settingup = None
        await ctx.trigger_typing()
        try:
            await ctx.send(f"Hey **{ctx.author.name}**, would you like to assign roles using buttons or reactions?\n\n**NOTE**: With buttons, sadly, there "
                           f"is a limitation of 25 max.\nReply with `buttons` for buttons or `reaction` for reactions.")
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
                    print('okoko')
                    channel = msg.channel_mentions[0].id
                    break
                except IndexError:
                    await ctx.send("It looks like you did not mention a channel, try again?")
                    counter += 1
                    continue
            try:
                print('ok')
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
                name = f"GUILD{ctx.guild.id}"
                db = cluster[name]
                collection = db['reactionroles']
                if message.content.lower().strip() == 'continue':
                    await ctx.send("Excellent, I will take care of that myself!")
                    title = "Reaction Role Menu"
                    description = None
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
            await ctx.send(f"Great. Now it is time to assign roles. The format is the name of the emoji"
                           f" and then the role. Unfortunately, we are currently limited to default emojis, "
                           f"not any custom ones. **CASE SENSITIVE!** Example:```:sunglasses: @cool kid```")

            resultarr = []
            mongodict ={}
            while True: #limit needs to be defined as the number of reaction role messages a server has, but for testing purposes i wont keep it
                message = await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 180)
                if message.content.lower().strip() == 'done':
                    break
                try:
                    args = message.content.split(':')
                    emoji = (args[0].replace(':', '').strip())
                    xz = discord.utils.get(ctx.guild.roles, name=f"{args[1].strip()}")
                    await message.add_reaction("👍🏽")
                    if resultarr.count(emoji) == 1 or resultarr.count(xz) == 1:
                        continue #add more check later, just getting basic functuonarlity
                    resultarr.append((args[0].strip(), args[1].strip()))
                    mongodict.__setitem__(args[0].strip(), args[1].strip().replace('>', "").replace('<@&', ''))
                    continue
                except IndexError:
                    await ctx.send(f"Did you format that correctly? Try again.")
                    continue
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
            except Exception as e:
                print(e)
            finally:
                print(mongodict)
                x = collection.insert_one({'_id': message.id, 'roles': mongodict})
                collection.delete_one({'id': ctx.message.id})

        except asyncio.TimeoutError:
            return await ctx.send('You took too long.')

def setup(client):
    client.add_cog(rr(client))