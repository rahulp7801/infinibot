from __future__ import print_function
import discord
from discord.ext import commands
import pandas as pd
from modules import utils
from modules.utils import ClassroomError


class GoogleC(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.icon = '🏫'
        self.description = 'Integration with Google Classroom!'

    @commands.command()
    #add an all param that does not filter out archived classes
    async def classes(self, ctx, limit:int = 10):
        await ctx.trigger_typing() #this takes super long for some reason
        try:
            try:
                x , service = utils.get_classes(ctx, limit)
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

def setup(client):
    client.add_cog(GoogleC(client))
