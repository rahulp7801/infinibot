import discord
from discord.ext import commands, tasks
import datetime
import pandas as pd
import asyncio
from modules import utils
import random
import logging
from pymongo import MongoClient

with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

class Giveaways(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.icon = '🎉'
        self.description = "Create and participate in giveaways!"
        self.check_giveaways.start()

    async def get_msg(self, ctx):
        ctx.send('hi')


    @tasks.loop(seconds = 60)
    async def check_giveaways(self):
        print('checking giveaways...')
        db = cluster['GIVEAWAYS']
        collection = db['guilds']
        arr = []
        print('ok')
        results = collection.find()
        for i in results:
            arr.append((i['id'], i['chanid'], i['gid'], i['fintime'], i['winners'], i['title']))
        if not arr:
            return
        for k in arr:
            print(k)
            try:
                if pd.to_datetime(k[3]) < datetime.datetime.utcnow():
                    channel = self.client.get_channel(int(k[1]))
                    try:
                        message = await channel.fetch_message(int(k[0]))
                    except Exception as e:
                        print(e)
                        continue
                    print('ok')
                    users = await message.reactions[0].users().flatten()
                    users.pop(users.index(self.client.user))
                    if len(users) == 0:
                        return await message.channel.send("No one participated in the giveaway :((")
                    winarr = []
                    for i in range(0, int(k[4])):
                        winarr.append(random.choice(users))
                    uslist = []
                    for i in winarr:
                        uslist.append(i.mention)
                    winstr = ", ".join(uslist)
                    desc = f"Winner{'' if len(winarr) == 1 else 's'}: {winstr}"
                    embed = discord.Embed(title=k[5], description=desc, color=discord.Color.green(),
                                          timestamp=datetime.datetime.utcnow())
                    await message.edit(embed=embed)
                    await message.channel.send(
                        f"🎉 Congratulations {winstr}, you {'all ' if len(winstr) == 1 else ''}won the **{k[5]}**!\n"
                        f"{message.jump_url}")
                    collection.delete_one({'id':int(message.id), "gid":int(message.guild.id)})
            except Exception as e:
                print(e)
                errmsg = f"While parsing through giveaways, exception {e} was raised. {datetime.datetime.utcnow()}"
                logging.basicConfig(filename='./errors.log')
                logging.error(errmsg)
                continue

    @check_giveaways.before_loop
    async def beforecheckgiv(self):
        await self.client.wait_until_ready()

    @staticmethod
    async def channelperms(channel: discord.TextChannel):
        if channel.is_nsfw():
            return False
        if channel.guild.me.guild_permissions.administrator:
            return True
        y = channel.overwrites_for(channel.guild.default_role)
        if not y.send_messages or not y.read_messages or not y.embed_links:
            pass
        else:
            return True
        for role in channel.guild.me.roles:
            x = channel.overwrites_for(role)
            if not x.send_messages or not x.read_messages or not x.embed_links:
                continue
            else:
                return True

        z = channel.overwrites_for(channel.guild.me)
        if not z.send_messages or not z.read_messages or not z.embed_links:
            return False
    @commands.command(help = 'Start a giveaway!')
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def gcreate(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            while True:
                await ctx.reply(f"Hey {ctx.author.mention}, thanks for using {self.client.user.name}! Please mention the channel you would like the giveaway to be in.", mention_author = False)

                msg = await self.client.wait_for('message', check=check, timeout = 60)
                try:
                    channel = msg.channel_mentions[0]
                    res = await self.channelperms(channel)
                    if not res:
                        return await ctx.send(f"I don't have permission to `Read Messages`, `Send Messages`, `Embed Links`, `Use External Emoji`, and `Add Reactions` in {channel.mention}.")
                    break
                except IndexError:
                    await ctx.send("You didn't mention a channel! Going back now...", delete_after = 3)
                    await asyncio.sleep(1.5)
                    continue
            message = await ctx.send(f"Great, we have saved {channel.mention} as our giveaway channel.")
            await asyncio.sleep(2)
            await message.edit(content = 'How long should this giveaway last?')
            while True:
                msg = await self.client.wait_for('message', check=check, timeout = 60)
                res = utils.tmts(msg.content.lower().strip())
                if res is None or res == '':
                    await ctx.send("I didn't understand the time value you specified, try again?")
                    await asyncio.sleep(1)
                    continue
                break
            try:
                result = utils.stringfromtime(res)
                await ctx.send(f"Excellent! This giveaway will last {result}!")
            except Exception:
                return await ctx.send("Something went wrong. Contact the developers with error code 405 if this keeps happening. ")
            await ctx.send("How many winners would you like? Choose a number between 1 and 20.")
            msg = await self.client.wait_for('message', check=check, timeout = 60)
            try:
                numwin = int(msg.content.strip())
            except Exception:
                return await ctx.send("Something went wrong, did you mention a number? Please run the command again to create another giveaway.")
            if numwin > 20:
                numwin = 20
            await ctx.send(f"Excellent, we will have {numwin} winner{'' if numwin == 1 else 's'}!\n\nWhat do you want the prize to be? Keep it under 2000 characters, and this will start the giveaway.")
            msg = await self.client.wait_for('message', check=check, timeout = 300)
            title = msg.content.strip()[0:2000]
            await ctx.send(f"Great. The giveaway for `{msg.content.strip()}` is starting in {channel.mention}!")
            desc = f"{numwin} winner{'' if numwin == 1 else 's'}\n" \
                   f"Duration: {result}\n" \
                   f"Hosted by: {ctx.author.mention}"
            embed = discord.Embed(title = title, description = desc, color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
            messg = await channel.send(embed=embed)
            await messg.add_reaction('🎉')
            db = cluster['GIVEAWAYS']
            collection = db['guilds']
            query = {'id': messg.id, 'gid': ctx.guild.id}
            if collection.count_documents(query) == 0:  # only real choice here, no two messages have the same ID
                ping_cm = {
                    "id": messg.id,
                    "chanid": channel.id,
                    "gid": ctx.guild.id,
                    "fintime": datetime.datetime.utcnow() + datetime.timedelta(seconds=res),
                    'winners': numwin,
                    'title': title
                }
                collection.insert_one(ping_cm)
            return

        except asyncio.TimeoutError:
            return await ctx.send("Giveaway setup has timed out and setup has been cancelled.")

    @commands.command(help='Removes a giveaway from the database!')
    @commands.guild_only()
    async def gremove(self, ctx, message:discord.Message):
        try:
            x = await ctx.fetch_message(message.id)
        except Exception as e:
            return await ctx.send(str(e))
        db = cluster['GIVEAWAYS']
        collection = db['guilds']
        query = {'id': x.id, 'gid': ctx.guild.id}
        if collection.count_documents(query) == 0:
            return await ctx.send("It looks like that message has not been saved as a giveaway!")
        collection.delete_one({"id":x.id, 'gid':ctx.guild.id})
        await ctx.send("Success! The message has been cleared from the database and the giveaway will be deleted...")
        try:
            await x.delete()
        except discord.Forbidden:
            return
        except discord.errors.HTTPException:
            return

def setup(client):
    client.add_cog(Giveaways(client))
