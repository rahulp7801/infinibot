from discord.ext import tasks, commands
from modules import utils
import discord
from pymongo import MongoClient
import logging
import asyncio
import pandas as pd
import datetime
from googleapiclient.discovery import build


with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

with open('./youtubeapi.txt', 'r') as f:
    ytapi = f.read()

class YouTube(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.check_for_yt_posts.start()

    @tasks.loop(minutes = 5)
    async def check_for_yt_posts(self):
        print("[YOUTUBE] Checking for upload loop started...")
        past = datetime.datetime.utcnow().timestamp()
        db = cluster['YOUTUBE']
        col = db['guilds']
        result = col.find()
        for i in result:
            channel = i["textchannel"]
            ytchannel = i["channelid"]
            sendmsg = i["sendmsg"]
            channel = self.client.get_channel(channel)
            service = build('youtube', 'v3', developerKey = ytapi)
            k = service.search().list(part = "snippet", channelId = ytchannel, maxResults = 5, order = 'date').execute()  # replace that ID with "classid"
            counter = 0
            k = k['items']
            while True:
                try:
                    x = (abs((pd.to_datetime(k[counter]["snippet"]["publishedAt"]).timestamp()) - past) <= 25600)
                    if x:
                        print("[YOUTUBE] Uploads Found, Getting Data...")
                        embed = discord.Embed(color = discord.Color.green())
                        embed.description = k[counter]['snippet']['description']
                        embed.title = k[counter]['snippet']['title']
                        embed.set_image(url = k[counter]['snippet']['thumbnails']['default']['url'])
                        await channel.send(content = sendmsg, embed=embed)
                        counter += 1
                    else:
                        break
                except KeyError:
                    break

    @check_for_yt_posts.before_loop
    async def before_yt(self):
        await self.client.wait_until_ready()

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild = True)
    async def youtubetest(self, ctx, *, query):
        youtube = build('youtube', 'v3', developerKey=ytapi)
        result = youtube.search().list(part="snippet", type="channel", q=query.strip()).execute()
        counter = 0
        arr = []
        for i in result.items():
            if i[0] == 'items':
                if len(i[1]) == 0:
                    return await ctx.send("It looks like there are no channels with that name :(")
                for z in range(len(i[1])):
                    print(i[1][counter])
                    arr.append(f"{counter + 1}. {i[1][counter]['snippet']['title']}\n\"{str(i[1][counter]['snippet']['description'])[0:200]}\"")
                    counter += 1
                await ctx.send("```" + "\n\n".join(arr) + "\n\nRESPOND WITH THE NUMBER OF THE CHANNEL YOU WOULD LIKE TO SAVE!```")
                failcount = 0
                chanarr = []
                try:
                    while True:
                        if failcount >= 5:
                            return await ctx.send("Due to too many invalid choices, this session has ended.")
                        msg = await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 120)
                        try:
                            chanarr.append((i[1][(int(msg.content.strip()) - 1)]["snippet"]["channelId"], i[1][(int(msg.content.strip()) - 1)]["snippet"]["title"], i[1][(int(msg.content.strip()) - 1)]["snippet"]["description"]))
                            break
                        except ValueError:
                            await ctx.send("Did you mention a number and a number only? Try typing the `number` next to the channel.")
                            failcount += 1
                            continue
                        except IndexError:
                            await ctx.send(f"It looks like the number `{msg.content.strip()}` was not found, try again?")
                            failcount += 1
                            continue
                except asyncio.TimeoutError:
                    return await ctx.send("You took too long.")
        await ctx.send(f"Success! `{chanarr[0][1]}` \n({str(chanarr[0][2])[0:200]}) \nhas been saved as the channel for **{ctx.guild.name}**!\n\nNow, "
                       f"what channel would you like updates to be sent to? Mention it below.")
        try:
            failcount = 0
            while True:
                if failcount >= 5:
                    return await ctx.send("Due to too many invalid options, this session has ended.")
                msg = await self.client.wait_for('message', check = lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 120)
                try:
                    channel = msg.channel_mentions[0].id
                    channel = self.client.get_channel(channel)
                    res = utils.channelperms(channel)
                    if not res:
                        await ctx.send("Please give me permission to `Embed Links`, `Attach Files`, `Send Messages`, and `View Channel` in {0.mention} and try again.".format(channel))
                        continue
                    break
                except KeyError:
                    await ctx.send("Looks like you didn\'t mention a channel! Try again?")
                    failcount += 1
                    continue
        except asyncio.TimeoutError:
            return await ctx.send("You took too long, no preferences have been saved.")

        await ctx.send(f"Success, {channel.mention} has been saved as the YouTube Notifier Channel.\n\n"
                       f"Finally, what message would you like to be sent when this happens? Type `continue` to skip.\n**KEEP IT UNDER 1900 CHARACTERS!**")

        try:
            msg = await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 120)
            if msg.content.lower().strip() == 'continue':
                sendmsg = f'{chanarr[0][1]} has just uploaded a video!'
            else:
                sendmsg = msg.content.strip()[0:1900]
        except asyncio.TimeoutError:
            return await ctx.send("You took too long, no preferences have been saved.")

        await ctx.send("Your preferences are being saved...")
        try:
            db = cluster['YOUTUBE']
            col = db['guilds']
            ping_cm = {
                "channelid":chanarr[0][0],
                'textchannel':channel.id,
                'gid':ctx.guild.id,
                'sendmsg':sendmsg,
                'seton':datetime.datetime.utcnow(),
                'setby':ctx.author.id
            }
            col.insert_one(ping_cm)
            db = cluster[f'GUILD{ctx.guild.id}']
            col = db['config']
            ping_cm = {
                "_id": chanarr[0][0],
                'channel': channel.id,
                'gid': ctx.guild.id,
                'sendmsg':sendmsg,
                'seton': datetime.datetime.utcnow(),
                'setby': ctx.author.id
            }
            col.insert_one(ping_cm)
        except Exception as e:
            print(e)
        return

def setup(client):
    client.add_cog(YouTube(client))