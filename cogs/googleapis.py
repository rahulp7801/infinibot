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
import math
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import logging
from google.oauth2.credentials import Credentials
from discord_components import Select, SelectOption, InteractionType, Button, ButtonStyle
import gspread

import aiohttp

REACTIONS = "abcdefghijklmnopqrstuvwxyz"

with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)
SCOPES = ['https://www.googleapis.com/auth/classroom.course-work.readonly', 'https://www.googleapis.com/auth/classroom.courses.readonly', 'https://www.googleapis.com/auth/classroom.announcements.readonly', 'https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly', 'https://www.googleapis.com/auth/classroom.coursework.me']

scope = [
'https://spreadsheets.google.com/feeds'
]
gc = gspread.service_account('config/dinesh-bot-c03b1a64f38f.json', scope)

class GoogleC(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.icon = '🏫'
        self.description = 'Integration with Google Classroom!'
        self.check_for_announcements.start()
        self.check_for_assignments.start()
        self.quizzes = {}

    async def send_result(self, mcq: bool,
                          ctx: commands.Context,
                          res,
                          options: list,
                          correct_index: int,
                          original_embed: discord.Embed,
                          count:int ) -> None:
        '''
        Sends the result of a quiz given the user's response
        '''
        if mcq:
            # Determine whether MCQ answer is correct or not

            ind = ord(res.component.label.lower()) - 97
            if ind == correct_index:
                self.quizzes[f"{ctx.guild.id}{ctx.author.id}"] += 1  # Add 1 to current score
                e = discord.Embed(
                    colour=discord.Color.green(), title="Correct",
                    description=utils.textToEmoji(REACTIONS[correct_index]) + " " + options[correct_index])
            else:
                e = discord.Embed(
                    colour=discord.Color.red(), title="Incorrect",
                    description=utils.textToEmoji(REACTIONS[correct_index]) + " " + options[correct_index])

            e.set_footer(
                text=f"You Answered: {res.component.label}\nCurrent Score: {self.quizzes[f'{ctx.guild.id}{ctx.author.id}']}/{count} = {round(self.quizzes[f'{ctx.guild.id}{ctx.author.id}'] / count * 100)}%")

        else:
            # Show flashcard answer
            e = discord.Embed(
                colour=discord.Color.green())

            answers = "\n".join(options)

            e.set_author(name="Answer",
                         icon_url="https://media.discordapp.net/attachments/724671574459940974/856634979001434142/unknown.png")

            if options and len(answers) < 256:
                e.title = answers
            elif options:
                e.description = answers
            else:
                e.title = "(No Answer Found)"

        await res.respond(type=InteractionType.UpdateMessage,
                          components=[], embeds=[original_embed, e])

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
                        continue #maybe send a message to the server owner saying that google classroom creds have expired... would become repetitive tho hmm
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
                    return await ctx.send(f"`{member.name}#{member.discriminator}` has already authenticated themselves for this server.") #maybe premium can offer 10 classes?
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
        await ctx.reply("Check your DMs!")
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

    @commands.command()
    async def quiz(self, ctx, url = None):
        await ctx.trigger_typing()
        if url is None:
            return await ctx.send(f"You need to specify a Google Sheets URL. Run the {ctx.prefix}template command to see how the sheets should be formatted. \n\n"
                                  f"Make sure that the sheet's visibility has been set to \"Anyone with the link\"!!!!")
        try:
            print(self.quizzes[f"{ctx.guild.id}{ctx.author.id}"]) #see if a quiz already exists, throws KeyError if this doesn't exist
            return await ctx.send("You already have a quiz going on in this server!")
        except LookupError:
            pass
        self.quizzes[f"{ctx.guild.id}{ctx.author.id}"] = 0
        try:
            sheet = gc.open_by_url(url).sheet1.get_all_values()
        except gspread.NoValidUrlKeyFound:
            await ctx.send(
                "Sheet not found. Please check that your sheet exists and is shared with **anyone with link**.")
            return
        except gspread.exceptions.APIError:
            await ctx.send(
                "The sheet you linked is not shared publicly. Please check that your sheet is shared with **anyone with link**.")
            return
        sheet.pop(0)
        count = 0
        while sheet:
            count += 1
            try:
                embed = discord.Embed(color = discord.Color.gold())
                cq = sheet.pop(0)
                prompt = cq[0]
                if not prompt:
                    continue
                image_url = cq[1]
                if len(prompt.strip()) < 252:
                    embed.title = prompt.strip()
                else:
                    embed.description = prompt.strip()
                if image_url:
                    embed.set_image(url=image_url)
                options = [
                    op.strip("\n") for op in cq[
                                             2:-1] if op]
                if cq[-1]:
                    mcq = True # multiple choice, otherwise free response
                    print(options)
                    correct_ind = ord(cq[-1][0].lower()) - 97
                    arr = [[] for i in range(math.ceil((len(options)) / 5))]
                    counter = 0
                    desc_text = ''
                    for i in range(math.ceil((len(options)) / 5)):
                        try:
                            for k in range(5):
                                print('here4')
                                print(options[counter])
                                arr[i].append(Button(style=ButtonStyle.blue, label=f'{REACTIONS[counter].upper()}'))
                                counter += 1
                            counter += 1
                        except IndexError:
                            break
                    if len(arr[-1]) < 5:
                        arr[-1].append(Button(style=ButtonStyle.red, label=f'🛑'))
                    else:
                        arr.append([Button(style=ButtonStyle.red, label=f'🛑')])
                    for i in range(len(options)):
                        desc_text += f"{utils.textToEmoji(REACTIONS[i])}: {options[i]}\n"
                    if embed.description:
                        embed.description += desc_text
                    else:
                        embed.description = desc_text
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    embed.set_footer(text='React with the 🛑 to stop the quiz.', icon_url=self.client.user.avatar_url)
                else:
                    correct_ind = 0
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    mcq = False
                    arr = [[Button(style=ButtonStyle.green, label=f'✅'), Button(style=ButtonStyle.red, label=f'🛑')]]
                msg = await ctx.send(embed=embed, components = arr)
                try:
                    res = await self.client.wait_for('button_click', check = lambda res: res.author.id == ctx.author.id and res.message.id == msg.id, timeout = 300)
                    if res.component.label == '🛑':
                        try:
                            final_score = f"Final Score: {self.quizzes[f'{ctx.guild.id}{ctx.author.id}']}/{count} = {round(self.quizzes[f'{ctx.guild.id}{ctx.author.id}']/count*100)}%"
                        except ZeroDivisionError:
                            final_score = f"Final Score: 0/0 = 0%"
                        await res.respond(content = final_score)
                        end_embed = discord.Embed(title="Quiz Terminated. Enter a new link to start again!",
                                                  description=("\n" + final_score) if final_score else "",
                                                  colour=discord.Colour.red())
                        end_embed.set_author(icon_url=ctx.author.avatar_url, name=f"Quiz for {ctx.author.display_name}")
                        await ctx.channel.send(embed=end_embed)
                        del self.quizzes[f"{ctx.guild.id}{ctx.author.id}"]
                        return
                    await self.send_result(mcq, ctx, res, options, correct_ind, embed, count)
                    await asyncio.sleep(0.5)
                except asyncio.TimeoutError:
                    return await ctx.send("Quiz has timed out.")
            except Exception as e:
                print(e)

        try:
            final_score = f"Final Score: {self.quizzes[f'{ctx.guild.id}{ctx.author.id}']}/{count} = {round(self.quizzes[f'{ctx.guild.id}{ctx.author.id}'] / count * 100)}%"
        except ZeroDivisionError:
            final_score = f"Final Score: 0/0 = 0%"
        end_embed = discord.Embed(title="Quiz Terminated. Enter a new link to start again!",
                                  description=("\n" + final_score) if final_score else "",
                                  colour=discord.Colour.red())
        end_embed.set_author(icon_url=ctx.author.avatar_url, name=f"Quiz for {ctx.author.display_name}")
        await ctx.channel.send(embed=end_embed)
        del self.quizzes[f"{ctx.guild.id}{ctx.author.id}"]
        return

    @commands.command()
    async def template(self, ctx):
        async with ctx.typing():
            return await ctx.send(f"Make a copy of this template. Make sure you set visibility to *Anyone with the link!*\n\n"
                              f"** DO NOT CHANGE THE ORDER OR LENGTH OF ANY OF THE COLUMNS!**\n\n"
                              f"https://docs.google.com/spreadsheets/d/1GnVmEqlIRM2mBdnE63g8fdb54b9jKSH7-Xj-gcBbHOI/edit#gid=0")


def setup(client):
    client.add_cog(GoogleC(client))
