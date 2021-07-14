import pylast
import datetime
from hashlib import md5
import requests
import xmltodict
import lastpy
from pymongo import MongoClient
import asyncio
import aiohttp
import pandas as pd
import discord
from discord.ext import commands
from modules import utils

with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

class lastfm(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.icon = '🎼'
        self.description = 'Integration with Last.fm'


    @commands.command(help='Set your Last FM for InfiniBot!')
    async def fmset(self, ctx):
        url = 'https://ws.audioscrobbler.com/2.0/'
        apisig = md5(
            'api_key35722626b405419c84e916787e6bf949methodauth.getTokentoken3fc2809a9fc31fed3ea94864398cdd1b'.encode()).hexdigest()
        print(apisig)
        params = {
            'api_key': '35722626b405419c84e916787e6bf949',
            'method': 'auth.getToken',
            'api_sig': apisig,
            'format': 'json'
        }
        response = requests.get(url, params=params)
        data = (response.json())
        token = data['token']
        print(token)
        apisig = md5(
            f'api_key35722626b405419c84e916787e6bf949methodauth.getSessiontoken{token}3fc2809a9fc31fed3ea94864398cdd1b'.encode()).hexdigest()
        print(apisig)
        newurl = f"https://www.last.fm/api/auth/?api_key=35722626b405419c84e916787e6bf949&token={token}"
        try:
            embed = discord.Embed(color = discord.Color.red())
            embed.title = f"Logging into {self.client.user.name}..."
            embed.description = f"[{f'Click here to add your Last.fm account to {self.client.user.name}'}]({newurl})"
            embed.set_footer(text='Please allow up to a minute for changes to take effect.')
            message = await ctx.author.send(embed=embed)
        except:
            return await ctx.send("It looks like your DMs are off, please turn them on first.")
        await asyncio.sleep(60) #delay for the user to finish webbrowser auth conf
        z = lastpy.authorize(token)
        try:
            new = xmltodict.parse(z)
            print(new)
            print(new["lfm"]["session"]["key"])
            embed = discord.Embed(color = discord.Color.green())
            embed.description = f"You have successfully logged on as {new['lfm']['session']['name']}!"
            db = cluster['LASTFM']
            col = db['usernames']
            if col.count_documents({'_id':ctx.author.id}) != 0:
                pass
            else:
                col.delete_one({'_id':ctx.author.id})

            payload = {
                '_id': ctx.author.id,
                'username': new['lfm']['session']['name'],
                'sessionkey': new["lfm"]["session"]["key"],
                'timeset': datetime.datetime.utcnow()
            }
            col.insert_one(payload)

        except LookupError:  #did not authorize
            embed = discord.Embed(color = discord.Color.gold())
            embed.description = "Login failed, you took too long or something went wrong.\n\n" \
                                "Do feel free to join our support server for extra help if the problem persists."
        await message.edit(embed=embed)

    @commands.command(help='Get your currently playing track from Last.fm!')
    async def fm(self, ctx, *, member:discord.Member=None):
        if member is None:
            member = ctx.author
        with open('lfapi.txt', 'r') as f:
            key = f.read()
        async with ctx.typing():
            db = cluster["LASTFM"]
            col = db["usernames"]
            if col.count_documents({'_id':member.id}) == 0:
                return await ctx.send(f"**{(member.name if member != ctx.author else 'You')}** {('has' if member != ctx.author else 'have')} not set {('their' if member != ctx.author else 'your')} Last FM profile with InfiniBot!")
            res = col.find({'_id':member.id})
            for i in res:
                username = i["username"]
            params = {
                'user': f'{username}',
                'api_key': key,
                'method': 'user.getrecenttracks',
                'format': 'json',
                'limit': 1
            }
            async with aiohttp.ClientSession() as session:
                url = 'https://ws.audioscrobbler.com/2.0/'
                async with session.get(url, params=params) as response:
                    data = await response.json()
            x = (data['recenttracks']['track'])
            if not x:
                return await ctx.send(f"**{member.name}** has not listened to any tracks!")

            username = data['recenttracks']['@attr']['user']
            track = x[0]['name']
            trackurl = x[0]['url']
            album = x[0]['album']['#text']
            artist = x[0]['artist']['#text']
            thumbnail = x[0]['image'][-1]['#text']
            try:
                timestamp = x[0]['date']['#text']
                z = pd.to_datetime(timestamp)
                desc = f"{f'[{track}]({trackurl})'} \n**{artist}** | *{album}*"
                embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=z)
                embed.set_author(name=f"{username}'s last track:", icon_url=member.avatar_url)
                embed.set_thumbnail(url=str(thumbnail))
                embed.set_footer(
                    text=f"{member.name} has {data['recenttracks']['@attr']['total']} total scrobbles | Last scrobble: ")
            except KeyError:
                z = datetime.datetime.utcnow()
                desc = f"{f'[{track}]({trackurl})'} \n**{artist}** | *{album}*"
                embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=z)
                embed.set_author(name=f"{username}'s currently playing track:", icon_url=member.avatar_url)
                embed.set_thumbnail(url=str(thumbnail))
                embed.set_footer(text=f"{member.name} has {data['recenttracks']['@attr']['total']} total scrobbles")
            message = await ctx.send(embed=embed)
            await message.add_reaction("👍🏽")
            await message.add_reaction("👎🏽")

    @commands.command(help='Get your top artists over a time period!')
    async def fmta(self, ctx, param = '7day', *, member:discord.Member = None):
        await ctx.trigger_typing()
        param, phrase = utils.determine_timeframe(param)
        with open('lfapi.txt', 'r') as f:
            key = f.read()
        if member is None:
            member = ctx.author
        db = cluster["LASTFM"]
        col = db["usernames"]
        if col.count_documents({'_id':member.id}) == 0:
            return await ctx.send(
                f"**{(member.name if member != ctx.author else 'You')}** {('has' if member != ctx.author else 'have')} not set {('their' if member != ctx.author else 'your')} Last FM profile with InfiniBot!")
        res = col.find({'_id':member.id})
        for i in res:
            sessionkey = i["sessionkey"]
            username = i["username"]
        network = pylast.LastFMNetwork(
            api_key=key,
            api_secret='3fc2809a9fc31fed3ea94864398cdd1b',
            session_key=sessionkey
        )
        try:
            user = network.get_user(username=username)
            ta = user.get_top_artists(period=param, limit=10)
            print(ta)
            embed = discord.Embed(color = discord.Color.green())
            embed.set_author(icon_url=member.avatar_url, name=f"Top {phrase} artists for {member.display_name}")
            counter = 0
            descarr = []
            for i in ta:
                counter += 1
                descarr.append(f"{counter}. **{i[0]}** ({i[1]} play{'' if i[1] == 1 else 's'})")
            embed.description = "\n".join(descarr)
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @commands.command(help='Get your top tracks over a time period!')
    async def fmtt(self, ctx, param='7day', *, member: discord.Member = None):
        await ctx.trigger_typing()
        param, phrase = utils.determine_timeframe(param)
        with open('lfapi.txt', 'r') as f:
            key = f.read()
        if member is None:
            member = ctx.author
        db = cluster["LASTFM"]
        col = db["usernames"]
        if col.count_documents({'_id': member.id}) == 0:
            return await ctx.send(
                f"**{(member.name if member != ctx.author else 'You')}** {('has' if member != ctx.author else 'have')} not set {('their' if member != ctx.author else 'your')} Last FM profile with InfiniBot!")
        res = col.find({'_id': member.id})
        for i in res:
            sessionkey = i["sessionkey"]
            username = i["username"]
        network = pylast.LastFMNetwork(
            api_key=key,
            api_secret='3fc2809a9fc31fed3ea94864398cdd1b',
            session_key=sessionkey
        )
        try:
            user = network.get_user(username=username)
            ta = user.get_top_tracks(period=param, limit=10)
            embed = discord.Embed(color=discord.Color.green())
            embed.set_author(icon_url=member.avatar_url, name=f"Top {phrase} tracks for {member.display_name}")
            counter = 0
            descarr = []
            for i in ta:
                counter += 1
                descarr.append(f"{counter}. **{i[0]}** ({i[1]} play{'' if i[1] == 1 else 's'})")
            embed.description = "\n".join(descarr)
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @commands.command(help='Get your top albums over a time period!')
    async def fmtopalbums(self, ctx, param='7day', *, member: discord.Member = None):
        await ctx.trigger_typing()
        param, phrase = utils.determine_timeframe(param)
        with open('lfapi.txt', 'r') as f:
            key = f.read()
        if member is None:
            member = ctx.author
        db = cluster["LASTFM"]
        col = db["usernames"]
        if col.count_documents({'_id': member.id}) == 0:
            return await ctx.send(
                f"**{(member.name if member != ctx.author else 'You')}** {('has' if member != ctx.author else 'have')} not set {('their' if member != ctx.author else 'your')} Last FM profile with InfiniBot!")
        res = col.find({'_id': member.id})
        for i in res:
            sessionkey = i["sessionkey"]
            username = i["username"]
        network = pylast.LastFMNetwork(
            api_key=key,
            api_secret='3fc2809a9fc31fed3ea94864398cdd1b',
            session_key=sessionkey
        )
        try:
            user = network.get_user(username=username)
            ta = user.get_top_albums(period=param, limit=10)
            embed = discord.Embed(color=discord.Color.green())
            embed.set_author(icon_url=member.avatar_url, name=f"Top {phrase} albums for {member.display_name}")
            counter = 0
            descarr = []
            for i in ta:
                counter += 1
                descarr.append(f"{counter}. **{i[0]}** ({i[1]} play{'' if i[1] == 1 else 's'})")
            embed.description = "\n".join(descarr)
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @commands.command(aliases = ['fml'], help='Love a track on Last.fm')
    async def fmlove(self, ctx):
        await ctx.trigger_typing()
        with open('lfapi.txt', 'r') as f:
            key = f.read()
        db = cluster["LASTFM"]
        col = db["usernames"]
        if col.count_documents({'_id': ctx.author.id}) == 0:
            return await ctx.send(
                f"**You** have not set your Last FM profile with InfiniBot!")
        res = col.find({'_id': ctx.author.id})
        for i in res:
            sessionkey = i["sessionkey"]
            username = i["username"]
        network = pylast.LastFMNetwork(
            api_key=key,
            api_secret='3fc2809a9fc31fed3ea94864398cdd1b',
            session_key=sessionkey
        )
        async with aiohttp.ClientSession() as session:
            params = {
                'user': f'{username}',
                'api_key': key,
                'method': 'user.getrecenttracks',
                'format': 'json',
                'limit': 1
            }
            url = 'https://ws.audioscrobbler.com/2.0/'
            async with session.get(url, params=params) as response:
                data = await response.json()
        x = (data['recenttracks']['track'])
        if not x:
            return await ctx.send(f"**You** have not listened to any tracks!")
        track = x[0]['name']
        trackurl = x[0]['url']
        album = x[0]['album']['#text']
        artist = x[0]['artist']['#text']
        desc = f"{f'[{track}]({trackurl})'} \n**{artist}** | *{album}*"
        embed = discord.Embed(color=discord.Color.gold())
        embed.title = f"Loved track for {ctx.author.display_name}"
        embed.description = desc
        try:
            track = network.get_track(title=track, artist=artist)
            track.love()
            return await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @commands.command(aliases = ['fmul'], help='Unlove a track on Last.fm')
    async def fmunlove(self, ctx):
        await ctx.trigger_typing()
        with open('lfapi.txt', 'r') as f:
            key = f.read()
        db = cluster["LASTFM"]
        col = db["usernames"]
        if col.count_documents({'_id': ctx.author.id}) == 0:
            return await ctx.send(
                f"**You** have not set your Last FM profile with InfiniBot!")
        res = col.find({'_id': ctx.author.id})
        for i in res:
            sessionkey = i["sessionkey"]
            username = i["username"]
        network = pylast.LastFMNetwork(
            api_key=key,
            api_secret='3fc2809a9fc31fed3ea94864398cdd1b',
            session_key=sessionkey
        )
        async with aiohttp.ClientSession() as session:
            params = {
                'user': f'{username}',
                'api_key': key,
                'method': 'user.getrecenttracks',
                'format': 'json',
                'limit': 1
            }
            url = 'https://ws.audioscrobbler.com/2.0/'
            async with session.get(url, params=params) as response:
                data = await response.json()
        x = (data['recenttracks']['track'])
        if not x:
            return await ctx.send(f"**You** have not listened to any tracks!")
        track = x[0]['name']
        trackurl = x[0]['url']
        album = x[0]['album']['#text']
        artist = x[0]['artist']['#text']
        desc = f"{f'[{track}]({trackurl})'} \n**{artist}** | *{album}*"
        embed = discord.Embed(color=discord.Color.gold())
        embed.title = f"Unloved track for {ctx.author.display_name}"
        embed.description = desc
        try:
            track = network.get_track(title=track, artist=artist)
            track.unlove()
            return await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @commands.command(aliases = ['fmt'])
    #still in development
    #use PANDAS library
    async def fmtaste(self, ctx, *, member:discord.Member):
        return
        await ctx.trigger_typing()
        with open('lfapi.txt', 'r') as f:
            key = f.read()
        db = cluster["LASTFM"]
        col = db["usernames"]
        if col.count_documents({'_id': ctx.author.id}) == 0:
            return await ctx.send(
                f"**You** have not set your Last FM profile with InfiniBot!")
        res = col.find({'_id': ctx.author.id})
        for i in res:
            sessionkey = i["sessionkey"]
            username = i["username"]
        network = pylast.LastFMNetwork(
            api_key=key,
            api_secret='3fc2809a9fc31fed3ea94864398cdd1b',
            session_key=sessionkey
        )
        tar = network.get_top_artists(limit=10)
        user = network.get_user(username=username)
        pass

def setup(client):
    client.add_cog(lastfm(client))

