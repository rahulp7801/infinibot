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
from discord_components import Select, SelectOption, InteractionType

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
                if os.path.exists(f'./temp/token{channel.guild.id}.json'):
                    creds = Credentials.from_authorized_user_file(f'./temp/token{channel.guild.id}.json', SCOPES)
                if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                        print('[GOOGLE CLASSROOM] Requesting Refresh of User-Authorization')
                        creds.refresh(Request())
                    else:
                        continue
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
                            try:
                                embed.description += f'\n\n{len(k["materials"])} attachment{"" if len(k["materials"]) == 1 else "s"}'
                            except KeyError:
                                pass
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
                channel = i["channel"]
                channel = self.client.get_channel(channel)
                if os.path.exists(f'./temp/token{channel.guild.id}.json'):
                    creds = Credentials.from_authorized_user_file(f'./temp/token{channel.guild.id}.json', SCOPES)
                if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                    else:
                        continue
                service = build('classroom', 'v1', credentials=creds)
                results = service.courses().announcements().list(pageSize = 10, courseId = classid).execute() #replace that ID with "classid"
                courses = results.get('announcements', [])
                if not courses:
                    print('this')
                    continue
                for k in courses:
                    print(k)
                    if k["state"] == 'PUBLISHED':
                        x = (abs((pd.to_datetime(k["creationTime"]).timestamp()) - past) <= 25600)
                        print(x)
                        if not x:
                            break
                        else:
                            embed = discord.Embed(color = discord.Color.green())
                            embed.description = str(k["text"])[0:2000] + f"\n[View Announcement]({k['alternateLink']})"
                            try:
                                embed.description += f'\n\n{len(k["materials"])} attachment{"" if len(k["materials"]) == 1 else "s"}'
                            except KeyError:
                                pass
                            embed.timestamp = pd.to_datetime(k["creationTime"])
                            embed.title = 'New Announcement!'
                            channel = i["channel"]
                            channel = self.client.get_channel(channel)
                            print('her34342342e')
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
            if not x:
                return await ctx.send(f"{service}")

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
    @commands.guild_only()
    @commands.has_permissions(manage_guild = True)
    async def setclass(self, ctx):
        if not os.path.exists(f'./temp/token{ctx.guild.id}-{ctx.author.id}.json'):
            for i in os.listdir('./temp'): #checking to see who set it for the guild... unnecessary but helpful
                if i.startswith(f'token{ctx.guild.id}'):
                    new = i.removeprefix(f'token{ctx.guild.id}-').removesuffix('.json')
                    member = self.client.get_user(int(new))
                    return await ctx.send(f"`{member.name}#{member.discriminator}` has already authenticated themselves for this server.")
            else:
                res = await self.authenticateclassroom(ctx)
                if not res:
                    return
        res = await utils.set_classroom_class(ctx)
        if not res[0]:
            return await ctx.send(res[1])
        print('here3')
        arr = []
        res = res[1]
        print(res, "godem")
        for i, k in enumerate(res):
            print(i, res[i])
            arr.append(SelectOption(label=k['name'], value=k["id"], description=k["descriptionHeading"]))
        await ctx.send(content = "Click on the class you would like to set.",
                       components = [
                           Select(placeholder="Select a class",
                                  options=arr,
                                  max_values=1,
                                  min_values=1)
                       ])
        try:
            interaction = await self.client.wait_for("select_option", check=lambda i: i.author == ctx.author, timeout = 120)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long.")
        print('out')
        await interaction.respond(content = f"The selected class is `{interaction.component[0].label}`.")
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

        await ctx.send(f"Ok, all updates for `{interaction.component[0].label}` will be posted to {channel.mention}!")
        db = cluster[f'GUILD{ctx.guild.id}']
        collection = db['config']
        query = {'_id':interaction.component[0].value}
        if collection.count_documents(query) == 0:
            try:
                ping_cm = {
                    '_id' : interaction.component[0].value,
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
                collection.update_one({'_id':interaction.component[0].value}, {"$set":{'channel':channel.id, 'seton':datetime.datetime.utcnow()}})
                print('success')
            except Exception as e:
                print(e)
        db = cluster['GOOGLECLASSROOM']
        collection = db['guilds']
        query = {'gid': ctx.guild.id}
        if collection.count_documents(query) == 0:
            try:
                ping_cm = {
                    'classid' : interaction.component[0].value,
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
                collection.update_one({'gid':ctx.guild.id}, {"$set":{'channel':channel.id, 'seton':datetime.datetime.utcnow(), 'setby':ctx.author.id, "classid":interaction.component[0].value}})
                print('success')
            except Exception as e:
                print(e)

    @commands.command(aliases = ['authclass'])
    @commands.guild_only()
    async def authenticateclassroom(self, ctx):
        print('ere3')
        embed = utils.auth_classroom(ctx)
        await ctx.author.send(embed=embed)
        try:
            message = await self.client.wait_for('message', check=lambda m: m.author == ctx.author and isinstance(m.channel, discord.DMChannel), timeout = 120)
        except asyncio.TimeoutError:
            await ctx.author.send("You took too long.")
            return False
        try:
            print(message.content.strip())
            utils.save_class_creds(ctx, message.content.strip())
            print('done')
        except ClassroomError as e:
            await ctx.author.send(f"{e}")
            return False
        await ctx.author.send(f"You have been successfully authorized to use Google Classroom with InfiniBot.\n\nYou may now return to {ctx.channel.mention} to choose a class.")
        return True

    @commands.command(aliases = ['googleclassroomlogout'])
    @commands.guild_only()
    @commands.has_permissions(manage_guild = True)
    async def gclogout(self, ctx):
        res = utils.classroomlogout(ctx)
        if not res[0]:
            return await ctx.send(res[1])
        await ctx.send("You have successfully logged out of Google Classroom for this server.")

def setup(client):
    client.add_cog(GoogleC(client))
