from discord.ext import commands
import discord
import asyncio
import datetime
from pymongo import MongoClient
from PIL import Image, ImageDraw

with open('./mongourl.txt', 'r') as file:
    url = file.read()

botversion = '2.0.0'
mongo_url = url.strip()
cluster = MongoClient(mongo_url)

class Leveling(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.icon = '🔼'
        self.description = f'Take part in InfiniBot\'s leveling system!'

    @commands.Cog.listener()
    async def on_ready(self):
        print("ready")

    # @commands.check
    # async def levels_enab(self, ctx):
    #     name = f"GUILD{ctx.guild.id}"
    #     db = cluster[name]
    #     collection = db['config']
    #     query = {"_id" : ctx.guild.id}
    #     if collection.count_documents(query) == 0:
    #         return False
    #     else:
    #         res = collection.find_one(query)
    #         for i in res:
    #             if i['levelups'] == 'on':
    #                 return True
    #         return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.guild is None: return
        name = f"LEVELLING"
        db = cluster[name]
        collection = db['guilds']
        stats = collection.find_one({'id':message.author.id, 'gid':message.guild.id})
        if stats is None:
            newuser = {"id": message.author.id, "xp":100, "gid":message.guild.id}
            collection.insert_one(newuser)
        else:
            xp = int(stats['xp']) + 5
            collection.update_one({'id':message.author.id, 'gid':message.guild.id}, {'$set':{'xp':xp}})
            lvl = 0
            while True:
                if xp < ((50*(lvl**2)) + (50*lvl)):
                    break
                lvl += 1
            xp -= ((50*((lvl-1)**2)) + (50*(lvl-1)))
            if xp == 0:
                await message.channel.send(f"GG on leveling up! You have achieved level {lvl}!")

    @commands.command(aliases = ['olrank'])
    async def oldrank(self, ctx, member:discord.Member = None):
        if member is None:
            member = ctx.author
        name = f"LEVELLING"
        db = cluster[name]
        collection = db['guilds']
        stats = collection.find_one({'id': member.id, 'gid':ctx.guild.id})
        if stats is None:
            return await ctx.send(f"{member.mention} hasn't sent any messages that the bot can see in {ctx.guild.name}!")
        xp = stats['xp']
        lvl = 0
        while True:
            if xp < ((50 * (lvl ** 2)) + (50 * lvl)):
                break
            lvl += 1
        xp -= ((50 * ((lvl - 1)**2)) + (50 * (lvl - 1)))
        boxes = int((xp/(200*((1/2) * lvl)))*20)
        print(boxes)
        rankings = collection.find().sort("xp", -1)
        rank = 0
        for i in rankings:
            rank += 1
            if i['id'] == stats['id']:
                break
        embed = discord.Embed(color = discord.Color.red())
        embed.set_author(name=f"{member.name}#{member.discriminator}'s rank", icon_url=member.avatar_url)
        embed.add_field(name='Level', value=str(lvl))
        embed.add_field(name="XP", value = f"{xp}/{int(200*((1/2) * lvl))}")
        embed.add_field(name='Rank', value = f"{rank}/{ctx.guild.member_count}")
        embed.add_field(name = "Progress", value = boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline = False)
        embed.set_thumbnail(url = member.avatar_url)
        #add role rewards
        await ctx.send(embed=embed)

    @commands.command(aliases = ['lb', 'levels'])
    async def leaderboard(self, ctx):
        name = f"LEVELLING"
        db = cluster[name]
        collection = db['guilds']
        rankings = collection.find({"gid":ctx.guild.id}).sort("xp", -1)
        c = 1
        embed = discord.Embed(title = "Ranks", color = discord.Color.green())
        for i in rankings:
            if c == 11:
                break
            try:
                print(i)
                print(i['id'])
                temp = self.client.get_user(i['id'])
                print(temp)
                tempxp = i['xp']
                embed.add_field(name=f"{c}. {temp.name}", value = f"XP: {tempxp}", inline = False)
                c += 1
            except Exception:
                pass

        embed.set_thumbnail(url = ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(aliases = ['position'])
    async def rank(self, ctx, member:discord.Member = None):
        if member is None:
            member = ctx.author
        name = f"LEVELLING"
        db = cluster[name]
        collection = db['guilds']
        stats = collection.find_one({'id': member.id, 'gid':ctx.guild.id})
        if stats is None:
            return await ctx.send(f"{member.mention} hasn't sent any messages that the bot can see in {ctx.guild.name}!")
        xp = stats['xp']
        lvl = 0
        while True:
            if xp < ((50 * (lvl ** 2)) + (50 * lvl)):
                break
            lvl += 1
        xp -= ((50 * ((lvl - 1)**2)) + (50 * (lvl - 1)))
        boxes = int((xp/(200*((1/2) * lvl)))*20)
        rankings = collection.find().sort("xp", -1)
        res = 625/20
        realres = int(boxes * res)
        rank = 0
        for i in rankings:
            rank += 1
            if i['id'] == stats['id']:
                break
        im = Image.open(r'progressbar.png').convert('RGB')
        draw = ImageDraw.Draw(im)
        color = (98, 211, 245)
        x, y, diam = realres + 14, 8, 34
        draw.ellipse([x, y, x + diam, y + diam], fill=color)
        ImageDraw.floodfill(im, xy=(14, 24), value=color, thresh=40)
        im.save(r'progressbar.png')
        file = discord.File('progressbar.png', filename='image.png')
        embed = discord.Embed(color=discord.Color.red())
        embed.set_author(name=f"{member.name}#{member.discriminator}'s rank", icon_url=member.avatar_url)
        embed.add_field(name='Level', value=str(lvl))
        embed.add_field(name="XP", value=f"{xp}/{int(200 * ((1 / 2) * lvl))}")
        embed.add_field(name='Rank', value=f"{rank}/{ctx.guild.member_count}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_image(url='attachment://image.png')
        await ctx.send(file = file, embed=embed)
        color = (72,75,78)
        x, y, diam = 591, 8, 34
        draw.ellipse([x, y, x + diam, y + diam], fill=color)
        ImageDraw.floodfill(im, xy=(14, 24), value=color, thresh=40)
        im.save(r'progressbar.png')
        im.close()

def setup(client):
    client.add_cog(Leveling(client))
