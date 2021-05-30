import discord
from discord.ext import commands
from pymongo import MongoClient
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import datetime
import pandas as pd
import aiohttp

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_secret='1e52b491d90e4c858ad914b5b2741f23',
        client_id='61e47cc943bd4bd2b1c828a06f5fb2b0'
    ))

with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

class Spotifys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def artistsearch(self, ctx, *, query:str = None):
        if query is None:
            name = f"GUILD{ctx.guild.id}"
            db = cluster[name]
            collection = db['config']
            user = collection.find({'_id': ctx.guild.id})
            for i in user:
                prefix = i['prefix']
            desc = f"```{prefix}artistsearch [artist]```"
            embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
            embed.set_footer(text="Parameters in [] are required and () are optional")
            return await ctx.send(embed=embed)
        results = sp.search(q=query.strip(), limit=10)
        print(results)
        arr = []
        for i, k in enumerate(results['tracks']['items']):
            st = k['name']
            prvurl = k['preview_url']
            popl = k['popularity']
            arr.append(f"{i + 1}. [{st}]({prvurl}) -> Popularity {popl}%")
        desc = "\n".join(arr)
        title = f"Search results for {query.strip()}"
        song = results['tracks']['items'][0]
        albumcov = results['tracks']['items'][0]['album']['images'][-1]['url']
        embed = discord.Embed(title = title, description = desc, color = discord.Color.green())
        embed.set_thumbnail(url=albumcov)

        await ctx.send(embed=embed)

    @commands.group(invoke_without_command = True)
    async def fm(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        await ctx.trigger_typing()
        db = cluster['LASTFM']
        collection = db['usernames']
        query = {"_id": member.id}
        if collection.count_documents(query) == 0:
            return await ctx.send(f"**{member.name}** has not set their Last FM profile with InfiniBot!")
        else:
            user = collection.find(query)
            for result in user:
                username = result['username']
        with open('lfapi.txt', 'r') as f:
            key = f.read()
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

    @fm.command()
    async def set(self, ctx, username):
        db = cluster['LASTFM']
        collection = db['usernames']
        query = {"_id": ctx.author.id}
        with open('lfapi.txt', 'r') as f:
            key = f.read()
        if collection.count_documents(query) == 0:
            params = {
                'user': f'{username.strip()}',
                'api_key': key,
                'method': 'user.getinfo',
                'format': 'json',
                'limit': 1
            }
            async with aiohttp.ClientSession() as session:
                url = 'https://ws.audioscrobbler.com/2.0/'
                async with session.get(url, params=params) as response:
                    data = await response.json()
                    try:
                        if data['error'] == 6:
                            desc = f"❌ User `{username.strip()}` was not found in the Last FM database."
                            embed = discord.Embed(description=desc, color=discord.Color.red(),
                                                  timestamp=datetime.datetime.utcnow())
                            return await ctx.send(embed=embed)
                    except Exception as e:
                        print(e)
                        pass
            ping_cm = {
                "_id": ctx.author.id,
                "username": username.strip()
            }
            try:
                x = collection.insert_one(ping_cm)
            except Exception:
                return
            imgurl = (data['user']['image'][-1]['#text'])
            desc = f"Success! Your Last FM username has been set as `{username}`!"
            embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=imgurl)
            embed.set_author(name=f"Your profile has been saved!", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            params = {
                'user': f'{username.strip()}',
                'api_key': key,
                'method': 'user.getinfo',
                'format': 'json',
                'limit': 1
            }
            async with aiohttp.ClientSession() as session:
                url = 'https://ws.audioscrobbler.com/2.0/'
                async with session.get(url, params=params) as response:
                    data = await response.json()
                    print(data)
                    try:
                        if data['error'] == 6:
                            desc = f"❌ User `{username}` was not found in the Last FM database."
                            embed = discord.Embed(description=desc, color=discord.Color.red(),
                                                  timestamp=datetime.datetime.utcnow())
                            return await ctx.send(embed=embed)
                    except Exception as e:
                        print(e)
                        pass
            collection.update_one({"_id": ctx.author.id}, {"$set": {'username': username}})
            imgurl = (data['user']['image'][-1]['#text'])
            desc = f"Success! Your Last FM username has been updated to `{username}`!"
            embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=imgurl)
            embed.set_author(name=f"Your profile has been saved!", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @set.error
    async def set_error(self, ctx, error):
        name = f"GUILD{ctx.guild.id}"
        db = cluster[name]
        collection = db['config']
        user = collection.find({'_id': ctx.guild.id})
        for i in user:
            prefix = i['prefix']
        if isinstance(error, commands.MissingRequiredArgument):
            desc = f"```{prefix}fm set [username]```"
            embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
            embed.set_footer(text="Parameters in [] are required and () are optional")
            return await ctx.send(embed=embed)

    @fm.command(aliases=['remove'])
    async def unset(self, ctx):
        db = cluster['LASTFM']
        collection = db['usernames']
        query = {'_id': ctx.author.id}
        if collection.count_documents(query) == 0:
            return await ctx.send("You haven't set your LASTFM profile with InfiniBot!")
        collection.delete_one({'_id': ctx.author.id})
        desc = f"You have removed your Last FM username from InfiniBot."
        embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
        await ctx.send(embed=embed)

    @fm.command(aliases=['ta'])
    async def topartists(self, ctx, member: discord.Member = None):
        # add a time period param
        await ctx.trigger_typing()
        if member is None:
            member = ctx.author
        db = cluster['LASTFM']
        collection = db['usernames']
        query = {"_id": member.id}
        if collection.count_documents(query) == 0:
            return await ctx.send(f"**{member.name}** has not set their Last FM profile with InfiniBot!")
        user = collection.find(query)
        for result in user:
            username = result['username']
        with open('lfapi.txt', 'r') as f:
            key = f.read()
        params = {
            'user': f'{username}',
            'api_key': key,
            'method': 'user.gettopartists',
            'format': 'json',
            'limit': 10,
            'period': '12month'
        }
        async with aiohttp.ClientSession() as session:
            url = 'https://ws.audioscrobbler.com/2.0/'
            async with session.get(url, params=params) as response:
                data = await response.json()
        counter = 0

        descarr = []
        for i in range(0, 10):
            descarr.append(
                f"{counter + 1}. {data['topartists']['artist'][counter]['name']} - {data['topartists']['artist'][counter]['playcount']} plays")
            counter += 1

        x = "\n".join(descarr)
        # img = data['topartists']['artist'][0]['image'][-1]['#text']
        embed = discord.Embed(description=x, color=discord.Color.green())
        embed.set_author(name=f"{member.name}'s top 10 yearly artists", icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @fm.command(aliases=['tt'])
    async def toptracks(self, ctx, member: discord.Member = None):
        # add a time period param
        await ctx.trigger_typing()
        if member is None:
            member = ctx.author
        db = cluster['LASTFM']
        collection = db['usernames']
        query = {"_id": member.id}
        if collection.count_documents(query) == 0:
            return await ctx.send(f"**{member.name}** has not set their Last FM profile with InfiniBot!")
        user = collection.find(query)
        for result in user:
            username = result['username']
        with open('lfapi.txt', 'r') as f:
            key = f.read()
        params = {
            'user': f'{username}',
            'api_key': key,
            'method': 'user.gettoptracks',
            'format': 'json',
            'limit': 10,
            'period': '12month'
        }
        async with aiohttp.ClientSession() as session:
            url = 'https://ws.audioscrobbler.com/2.0/'
            async with session.get(url, params=params) as response:
                data = await response.json()
        counter = 0

        descarr = []
        for i in range(0, 10):
            descarr.append(
                f"{counter + 1}. {data['toptracks']['track'][counter]['name']} - {data['toptracks']['track'][counter]['artist']['name']} - **{data['toptracks']['track'][counter]['playcount']} plays**")
            counter += 1

        x = "\n".join(descarr)
        # img = data['topartists']['artist'][0]['image'][-1]['#text']
        embed = discord.Embed(description=x, color=discord.Color.green())
        embed.set_author(name=f"{member.name}'s top 10 yearly tracks", icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @fm.command(aliases=['talb', 'topalb'])
    async def topalbums(self, ctx, member: discord.Member = None):
        # add a time period paramom {name} WHERE user_id = {ctx.guild.id}")
        await ctx.trigger_typing()
        if member is None:
            member = ctx.author
        db = cluster['LASTFM']
        collection = db['usernames']
        query = {"_id": member.id}
        if collection.count_documents(query) == 0:
            return await ctx.send(f"**{member.name}** has not set their Last FM profile with InfiniBot!")
        user = collection.find(query)
        for result in user:
            username = result['username']
        with open('lfapi.txt', 'r') as f:
            key = f.read()
        params = {
            'user': f'{username}',
            'api_key': key,
            'method': 'user.gettopalbums',
            'format': 'json',
            'limit': 10,
            'period': '12month'
        }
        async with aiohttp.ClientSession() as session:
            url = 'https://ws.audioscrobbler.com/2.0/'
            async with session.get(url, params=params) as response:
                data = await response.json()
        counter = 0

        descarr = []
        for i in range(0, 10):
            descarr.append(
                f"{counter + 1}. {data['topalbums']['album'][counter]['name']} - **{data['topalbums']['album'][counter]['artist']['name']}** - {data['topalbums']['album'][counter]['playcount']} plays")
            counter += 1

        x = "\n".join(descarr)
        # img = data['topartists']['artist'][0]['image'][-1]['#text']
        embed = discord.Embed(description=x, color=discord.Color.green())
        embed.set_author(name=f"{member.name}'s top 10 yearly albums", icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @fm.command(aliases=['artinfo', 'artistinfo'])
    async def artist(self, ctx, *, name):
        with open('lfapi.txt', 'r') as f:
            key = f.read()
        params = {
            'api_key': key,
            'method': 'artist.getinfo',
            'format': 'json',
            'autocorrect': 1,
            'lang': 'eng',
            'artist': f'{name}'
        }
        async with aiohttp.ClientSession() as session:
            url = 'https://ws.audioscrobbler.com/2.0/'
            async with session.get(url, params=params) as response:
                data = await response.json()
                print(data)

        artt = data["artist"]["name"]
        artlink = data['artist']['url']
        learnmore = f"**{f'[{artt}]({artlink})'}**"
        listeners = data['artist']['stats']['listeners']
        playscount = data['artist']['stats']['playcount']
        img = data['artist']['image'][-1]['#text']
        similarart = f"[{data['artist']['similar']['artist'][0]['name']}]({data['artist']['similar']['artist'][0]['url']})"
        print(data['artist']['similar']['artist'][1]['name'])
        similarart1 = f"[{data['artist']['similar']['artist'][1]['name']}]({data['artist']['similar']['artist'][1]['url']})"
        print(similarart1)
        embed = discord.Embed(title=f"Information about {name}", color=discord.Color.green())
        embed.set_thumbnail(url=img)
        embed.add_field(name="Similar Artists:", value=f"{similarart}, \n{similarart1}")
        embed.set_footer(text=f"{listeners} listeners | {playscount} plays")
        await ctx.send(embed=embed)

    @artist.error
    async def art_error(self, ctx, error):
        name = f"GUILD{ctx.guild.id}"
        db = cluster[name]
        collection = db['config']
        user = collection.find({'_id': ctx.guild.id})
        for i in user:
            prefix = i['prefix']
        if isinstance(error, commands.MissingRequiredArgument):
            desc = f"```{prefix}fm artist [artist]```"
            embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
            embed.set_footer(text="Parameters in [] are required and () are optional")
            return await ctx.send(embed=embed)

    @fm.command(aliases=['cta'])
    async def charttopartista(self, ctx):
        with open('lfapi.txt', 'r') as f:
            key = f.read()
        params = {
            'api_key': key,
            'method': 'chart.gettopartists',
            'limit': 10,
            'format': 'json',
        }
        async with aiohttp.ClientSession() as session:
            url = 'https://ws.audioscrobbler.com/2.0/'
            async with session.get(url, params=params) as response:
                data = await response.json()
                print(data)
        counter = 0

        descarr = []
        for i in range(0, 10):
            descarr.append(
                f"{counter + 1}. {data['artists']['artist'][counter]['name']} - **{data['artists']['artist'][counter]['listeners']} listeners** - {data['artists']['artist'][counter]['playcount']} plays")
            counter += 1

        x = "\n".join(descarr)
        # img = data['topartists']['artist'][0]['image'][-1]['#text']
        embed = discord.Embed(description=x, color=discord.Color.green())
        embed.set_author(name="Last FM's top 10 artists", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Spotifys(client))