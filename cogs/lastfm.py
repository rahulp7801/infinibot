import pylast
import datetime
from hashlib import md5
import requests
import time
import xmltodict
import lastpy
from pymongo import MongoClient
import asyncio
import discord
from discord.ext import commands

with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

class lastfm(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
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

def setup(client):
    client.add_cog(lastfm(client))

