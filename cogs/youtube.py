from discord.ext import tasks, commands
from modules import utils
import discord
from pymongo import MongoClient
import logging
import asyncio
import pandas as pd
import datetime
from googleapiclient.discovery import build
from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists, InvalidArgument
from google.cloud.pubsub import PublisherClient, SchemaServiceClient
from google.pubsub_v1.types import Encoding


project_id = 'dinesh-bot'

subscription_id = 'GUILD830158413408239646'
timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

with open('./youtubeapi.txt', 'r') as f:
    ytapi = f.read()

class YouTube(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild = True)
    async def setyoutubechannel(self, ctx, *, query):
        print('ok')
        try:
            youtube = build('youtube', 'v3', developerKey=ytapi)
            result = youtube.channels().list(part="snippet", type="channel", q=query.strip()).execute()
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
                    except IndexError:
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
        except Exception as e:
            print(e)
def setup(client):
    client.add_cog(YouTube(client))