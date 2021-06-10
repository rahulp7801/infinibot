from __future__ import print_function
import discord
from discord.ext import commands, tasks
import pandas as pd
from modules import utils
from modules.exceptions import ClassroomError
import asyncio
from pymongo import MongoClient
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import logging
from google.oauth2.credentials import Credentials

import aiohttp

with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)
SCOPES = ['https://www.googleapis.com/auth/classroom.course-work.readonly', 'https://www.googleapis.com/auth/classroom.courses.readonly', 'https://www.googleapis.com/auth/classroom.announcements.readonly', 'https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly', 'https://www.googleapis.com/auth/classroom.coursework.me']


class GoogleC(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.icon = '🏫'
        self.description = 'Integration with Google Classroom!'
        self.check_for_announcements.start()
        self.check_for_assignments.start()


    @tasks.loop(minutes = 5)
    async def check_for_assignments(self):
        print("[GOOGLE CLASSROOM] Assignment Check Loop Started...")

        past = datetime.datetime.utcnow().timestamp()
        db = cluster['GOOGLECLASSROOM']
        collection = db['guilds']
        creds = None
        res = collection.find()
        for i in res:
            channel = i["channel"]
            channel = self.client.get_channel(channel)
            try:
                classid = i["classid"]
                if os.path.exists('token.json'):
                    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
                if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                        print('[GOOGLE CLASSROOM] Requesting Refresh of User-Authorization')
                        creds.refresh(Request())
                    else:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            'credentials.json', SCOPES)
                        #should not happen!
                        print('[GOOGLE CLASSROOM] ERROR: Unauthorized User Set Up Google Classroom!')
                        creds = flow.run_local_server(port=0, open_browser=False)
                    # Save the credentials for the next run
                    try:
                        with open('token.json', 'w') as token:
                            token.write(creds.to_json())
                    except Exception as e:
                        print(f'[GOOGLE CLASSROOM] Exception Raised: {e}')
                        raise ClassroomError(e)

                service = build('classroom', 'v1', credentials=creds)
                results = service.courses().courseWork().list(pageSize=10, courseId=classid).execute()  # replace that ID with "classid"
                courses = results.get('courseWork', [])
                if not courses:
                    print(f'[GOOGLE CLASSROOM] No Courses Found For {channel.guild.name} [{channel.guild.id}], Breaking...')
                    continue
                for k in courses:
                    print(k)
                    if k["state"] == 'PUBLISHED':
                        x = (abs((pd.to_datetime(k["creationTime"]).timestamp()) - past) <= 25600)
                        print(x)
                        if not x:
                            break #because the API returns it ordered most recent, no need to waste time checking older ones.
                        if x and k["assigneeMode"] == 'ALL_STUDENTS':
                            print("[GOOGLE CLASSROOM] New Assignments Found, updating...")
                            embed = discord.Embed(color=discord.Color.green())
                            try:
                                embed.description = str(k["description"])[0:2000] + f"\n[View Assignment]({k['alternateLink']})" + f"\n\nDue {k['dueDate']['year']}-{k['dueDate']['month']}-{k['dueDate']['day']}"
                            except KeyError:
                                embed.description = "No description for this assignment."
                            embed.title = str(k["title"])[0:2000]
                            embed.timestamp = pd.to_datetime(k["creationTime"])
                            await channel.send(embed=embed)
                            continue
            except Exception as e:
                logging.basicConfig(filename='./errors.log')
                errmsg = f"[GOOGLE CLASSROOM] [ASSIGNMENTS] While scraping through assignments, exception {e} was raised."
                logging.error(errmsg)

    @check_for_assignments.before_loop
    async def before_check_assignments(self):
        await self.client.wait_until_ready()

    @tasks.loop(minutes = 5)
    async def check_for_announcements(self):
        print("Checking for announcements...")
        past = datetime.datetime.utcnow().timestamp()
        db = cluster['GOOGLECLASSROOM']
        collection = db['guilds']
        arr = []
        creds = None
        res = collection.find()
        for i in res:
            try:
                classid = i["classid"]
                arr.append((i['classid'], i['gid'], i['channel']))
                if os.path.exists('token.json'):
                    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
                if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                    else:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            'credentials.json', SCOPES)
                        creds = flow.run_local_server(port=0, open_browser=False)
                    # Save the credentials for the next run
                    try:
                        with open('token.json', 'w') as token:
                            token.write(creds.to_json())
                    except Exception as e:
                        raise ClassroomError(e)

                service = build('classroom', 'v1', credentials=creds)
                results = service.courses().announcements().list(pageSize = 10, courseId = classid).execute() #replace that ID with "classid"
                courses = results.get('announcements', [])
                if not courses:
                    print('this')
                    continue
                for k in courses:
                    print(k)
                    if k["state"] == 'PUBLISHED':
                        x = (abs((pd.to_datetime(k["creationTime"]).timestamp()) - past) <= 25700)
                        print(x)
                        if not x:
                            break
                        if x and k["assigneeMode"] == 'ALL_STUDENTS':
                            embed = discord.Embed(color = discord.Color.green())
                            embed.description = str(k["text"])[0:2000] + f"\n[View Assignment]({k['alternateLink']})"
                            embed.timestamp = pd.to_datetime(k["creationTime"])
                            embed.title = 'New Announcement!'
                            channel = i["channel"]
                            channel = self.client.get_channel(channel)
                            await channel.send(embed=embed)
                            continue
            except Exception as e:
                logging.basicConfig(filename='./errors.log')
                errmsg = f"[GOOGLE CLASSROOM] [ANNOUNCEMENTS] While scraping through announcements, exception {e} was raised."
                logging.error(errmsg)

    @check_for_announcements.before_loop
    async def before_check_announcements(self):
        await self.client.wait_until_ready()

    @commands.command()
    #add an all param that does not filter out archived classes
    async def classes(self, ctx, limit:int = 10):
        await ctx.trigger_typing() #this takes super long for some reason
        try:
            try:
                x , service = await utils.get_classes(ctx, limit)
            except ClassroomError as e:
                return await ctx.send(str(e))

            else:
                print('Courses:')
                for course in x:
                    courseWorkList = service.courses().courseWork().list(courseId=course["id"]).execute()
                    try:
                        for courseWork in courseWorkList["courseWork"]:
                            print(courseWork)
                            title = courseWork["title"]
                            embed = discord.Embed(color = discord.Color.green())
                            embed.set_author(name=title)
                            try:
                                embed.description = courseWork["description"]
                            except KeyError:
                                embed.description = "No description for this assignment."
                            try:
                                print(courseWork["materials"][0]['driveFile']['driveFile']['thumbnailUrl'])
                                embed.set_thumbnail(url=courseWork["materials"][0]['driveFile']['driveFile']['thumbnailUrl'])
                            except KeyError:
                                pass
                            embed.set_footer(text = f"Last updated:")
                            embed.timestamp = pd.to_datetime(courseWork['updateTime'])
                            await ctx.send(embed=embed)
                            break
                        break
                    except KeyError:
                        continue
        except Exception as e:
            print(e)

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def setclass(self, ctx):
        res = await utils.set_classroom_class(ctx, ctx.guild)
        arr = []
        for i, k in enumerate(res):
            arr.append(f"{i + 1}. {res[i]['name']}")
        await ctx.send('```' + '\n'.join(arr) + '\n\nRespond with the number of the class you would like to set.' + '```')
        counter = 0
        while True:
            if counter > 5:
                return await ctx.send("Due to too many invalid choices, this session has ended.")
            try:
                msg = await self.client.wait_for('message',
                                                 check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 120)
                index = int(msg.content.lower().strip())
                classreq = res[index - 1]
                break
            except asyncio.TimeoutError:
                return await ctx.send("You took too long.")
            except KeyError:
                await ctx.send(f"I couldn\'t find the index `{msg.content.lower()}`. Try again.")
                counter += 1
                continue
            except ValueError:
                await ctx.send("Try again, did you mention a number?")
                counter += 1
                continue
        await ctx.send(f"The selected class is `{classreq['name']}`.")
        await asyncio.sleep(1)
        await ctx.send("What channel would you like updates to be sent to? \nMention the channel below.")
        while True:
            msg = await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 120)
            try:
                channel = msg.channel_mentions[0].id
                channel = self.client.get_channel(channel)
                break
            except IndexError:
                await ctx.send("It doesn\'t look like you mentioned a channel, try again?")
                continue
            except asyncio.TimeoutError:
                await ctx.send("You took too long.")
                continue

        await ctx.send(f"Ok, all updates for `{classreq['name']}` will be posted to {channel.mention}!")
        db = cluster[f'GUILD{ctx.guild.id}']
        collection = db['config']
        query = {'_id':classreq['id']}
        if collection.count_documents(query) == 0:
            try:
                ping_cm = {
                    '_id' : classreq["id"],
                    'channel':channel.id,
                    'guild': ctx.guild.id,
                    'seton': datetime.datetime.utcnow(),
                    'setby':ctx.author.id
                }
                collection.insert_one(ping_cm)
                print('suces')
            except Exception as e:
                print(e)
        else:
            try:
                collection.update_one({'_id':classreq["id"]}, {"$set":{'channel':channel.id, 'seton':datetime.datetime.utcnow()}})
                print('success')
            except Exception as e:
                print(e)
        db = cluster['GOOGLECLASSROOM']
        collection = db['guilds']
        query = {'gid': ctx.guild.id}
        if collection.count_documents(query) == 0:
            try:
                ping_cm = {
                    'classid' : classreq["id"],
                    'channel':channel.id,
                    'gid': ctx.guild.id,
                    'seton': datetime.datetime.utcnow(),
                    'setby':ctx.author.id
                }
                collection.insert_one(ping_cm)
                print('suces')
            except Exception as e:
                print(e)
        else:
            try:
                collection.update_one({'gid':ctx.guild.id}, {"$set":{'channel':channel.id, 'seton':datetime.datetime.utcnow(), 'setby':ctx.author.id, "classid":classreq["id"]}})
                print('success')
            except Exception as e:
                print(e)

def setup(client):
    client.add_cog(GoogleC(client))
