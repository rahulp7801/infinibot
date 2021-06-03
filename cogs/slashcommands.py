import discord
from discord.ext import commands
import asyncio
import datetime
import random
from discord_slash import SlashCommand, SlashContext, cog_ext
import praw
import pyshorteners
from pymongo import MongoClient
import time
import pyfiglet
from aiohttp import ClientSession
import aiohttp
import psutil
import pandas as pd
import string
from googletrans import Translator
from PIL import Image, ImageDraw, ImageFont
from discord_components import DiscordComponents
from modules import utils
with open('./mongourl.txt', 'r') as file:
    url = file.read()

botversion = '2.0.0'
mongo_url = url.strip()
cluster = MongoClient(mongo_url)
translator = Translator()
with open('praw.txt', 'r') as f:
    ff = f.read()
    creds = ff.split('\n')
    client_id = creds[0]
    client_secret = creds[1]
    username = creds[2]
    password = creds[3]
    user_agent = creds[4]

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     username=username,
                     password=password,
                     user_agent=user_agent,
                     check_for_async=False)

url_shortener = pyshorteners.Shortener()
class Slash(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_ready(self):
        DiscordComponents(self.client, change_discord_methods=True)
        choices = [
            'with lines of code',
            'Testing new InfiniBot features!',
            'VALORANT',
            f'watching {len(self.client.guilds)} server{"" if len(self.client.guilds) == 1 else "s"}',
            'samosa gang gang IV out now',
            f'%help | {self.client.user.name} Universe',
            "New features coming soon!",
            "Improving speed and efficiency",
            'Google Chrome',
            "With the API"
        ]
        while True:
            status = random.choice(choices)
            await self.client.change_presence(activity=discord.Game(name=status))
            await asyncio.sleep(30)

    @cog_ext.cog_slash(name='emojify', description='Emojify a phrase')
    async def emojify(self, ctx:SlashContext, *, text):
        if len(text) > 2000:
            await ctx.send("Keep your message under 2000 characters.")
            return
        try:
            new = []
            for i in str(text):
                if i == " ":
                    new.append("         ")
                    continue
                if not i.isalpha():
                    continue
                else:
                    new.append(f":regional_indicator_{i.lower()}:")
                    continue

            await ctx.send(" ".join(new))
        except:
            await ctx.send("Something went wrong, next time make sure to use only letters.")

    @cog_ext.cog_slash(name='8ball', description='Let the magic 8ball decide your fate.')
    async def _eightball(self, ctx:SlashContext, *, question):
        choices = [
            'Outlook not so good.',
            'It is decidedly so.',
            'Without a doubt.',
            'It is certain.',
            'You may rely on it.',
            'As I see it, yes.',
            'Outlook good.',
            'Signs point to yes.',
            'Reply hazy try again.',
            'Ask again later.',
            'Better not tell you now!',
            'Cannot predict now.',
            'Concentrate and ask again.',
            'Don\'t count on it.',
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'Very doubtful.'
        ]
        response = random.choice(choices)
        await asyncio.sleep(1)
        embed = discord.Embed(title=f"{question.strip()}{'' if question.strip().endswith('?') else '?'}",
                              description=response, color=discord.Color.green())
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name='toascii', description='Convert a string into ASCII!')
    async def _asciitext(self, ctx:SlashContext, *, text):
        x = [ord(c) for c in text.strip()]
        await ctx.send(f"{text.strip()} -> {''.join(str(v) for v in x)}")

    @cog_ext.cog_slash(name='servericon', description='Get this server\'s icon!')
    async def _servericon(self, ctx:SlashContext):
        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_image(url=ctx.guild.icon_url)
        embed.set_footer(text=f"{ctx.guild.name} Server Icon | Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name='meme', description='Get a meme directly from r/memes!')
    async def _meme(self, ctx:SlashContext):
        all_subs = []
        subreddit = reddit.subreddit('jokes')
        top = subreddit.hot(limit=30)
        for sub in top:
            all_subs.append(sub)

        random_sub = random.choice(all_subs)
        name = random_sub.title
        tex = random_sub.selftext
        suburl = "https://www.reddit.com" + random_sub.permalink
        scr = random_sub.score
        com = random_sub.num_comments
        em = discord.Embed(title=name, description=tex, url=suburl, color=discord.Color.green())
        em.set_footer(text="👍 " + str(scr) + " | 💬 " + str(com))
        await ctx.send(embed=em)

    @cog_ext.cog_slash(name='flip', description='Flip a coin!')
    async def _flip(self, ctx: SlashContext):
        choices = ['heads', 'tails']
        res = random.choice(choices)
        return await ctx.send(res)

    @cog_ext.cog_slash(name='Reverse', description='Reverses text')
    async def _reverse(self, ctx: SlashContext, *, text):
        return await ctx.send(f"{text.strip()} -> {text[::-1].strip()}")

    @cog_ext.cog_slash(name='serverinvite', description='Generates an invite to the server!')
    async def _cinv(self, ctx: SlashContext):
        invite = await ctx.channel.create_invite(max_age=604800)
        await ctx.send(f"Here is an invite to **{ctx.guild.name}**: \n{invite}", hidden=True)

    @cog_ext.cog_slash(name='tinyurl', description='Generates a tinyurl')
    async def _tinyurl(self, ctx: SlashContext, url):
        try:
            x = url_shortener.tinyurl.short(url)
            await ctx.author.send(x)
            await ctx.send("Check your dms!", hidden=True)
        except Exception as e:
            print(e)
            return await ctx.send(
                "Something went wrong. Make sure after the command invocation you are only putting the URL link.", hidden=True)

    @cog_ext.cog_slash(name='truemembercount', description='Returns the amount of humans in a server.')
    async def _tmc(self, ctx: SlashContext):
        true_member_count = len([m for m in ctx.guild.members if not m.bot])
        return await ctx.send(f"There are {true_member_count} humans in the server **{ctx.guild.name}**")

    @cog_ext.cog_slash(name='afk', description='Sets an AFK status for you ')
    async def _afk(self, ctx:SlashContext, *, message = "Away"):
        name = f"GUILD{ctx.guild.id}"
        db = cluster[name]
        collection = db['afk']
        cnick = ctx.author.display_name
        member = ctx.author
        ping_cm = {
            "_id": ctx.author.id,
            "name": ctx.author.name,
            "display_name": cnick,
            "member": ctx.author.name,
            'start': time.time(),
            'status': message.strip()
        }
        try:
            x = collection.insert_one(ping_cm)
        except Exception:
            return await ctx.send("You are already afk!")
        desc = f"Your afk status has been successfully updated to: ```{message}```"
        embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{ctx.author.name} is now afk", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text="The AFK setting has been saved.")
        await ctx.send(embed=embed, hidden=True)

        try:
            await member.edit(nick=f"[AFK] {cnick}")
        except discord.Forbidden:
            pass

    @cog_ext.cog_slash(name='membercount', description='Get the total number of members!')
    async def _memcount(self, ctx:SlashContext):
        await ctx.send(f'There are `{ctx.guild.member_count}` members in **{ctx.guild.name}**.')

    @cog_ext.cog_slash(name='asciiart', description='Convert a string into ASCII art!')
    async def _asciiart(self, ctx:SlashContext, *, text):
        if len(text) > 2000:
            await ctx.send("Your message was too long!")
        result = pyfiglet.figlet_format(f"{text}")
        await ctx.send(f"```{result}```")

    @cog_ext.cog_slash(name='clap', description='Insert claps between letters!')
    async def _clap(self, ctx:SlashContext, *, text):
        arr = []
        for i in text:
            if i == " ":
                arr.append("    ")
            else:
                arr.append(i.strip())

        x = ":clap:".join(arr)
        await ctx.send(x)

    @cog_ext.cog_slash(name='urban', description='Search the Urban Dictionary!')
    async def _urban(self, ctx: SlashContext, *, text):
        with open('urbanapi.txt', 'r') as f:
            key = f.read()
        try:
            url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
            querystring = {"term": text}
            headers = {
                'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
                'x-rapidapi-key': key
            }
            async with ClientSession() as session:
                async with session.get(url, headers=headers, params=querystring) as response:
                    r = await response.json()
                    definition = r['list'][0]['definition']
                    desc = str(definition)
                    if r['list'][0]['example'] == "":
                        r['list'][0]['example'] = "..."
                    embed = discord.Embed(title=f"Urban Dictionary Definition of {text}", url=r['list'][0]['permalink'],
                                          description=desc, color=discord.Color.green())
                    embed.add_field(name="Example Sentence:", value=r['list'][0]['example'], inline=False)
                    embed.add_field(name="👍🏽", value=r['list'][0]['thumbs_up'])
                    embed.add_field(name="👎🏽", value=r['list'][0]['thumbs_down'])
                    embed.set_footer(text=f"Author: {r['list'][0]['author']} on {r['list'][0]['written_on'][0:10]}")
                    embed.set_thumbnail(url=ctx.guild.icon_url)
                    await ctx.send(embed=embed)
        except IndexError:
            return await ctx.send(f"Error! The search term **{text}** could not be found.")

    @cog_ext.cog_slash(name='avatar', description='Get the avatar of a user!')
    async def _avatar(self, ctx: SlashContext, member: discord.User = None):
        try:
            if member is None:
                author = ctx.author
                pfp = author.avatar_url
                embed = discord.Embed(title="**Avatar**")
                embed.set_author(name=author, icon_url=pfp)
                embed.set_image(url=pfp)
                await ctx.send(embed=embed)
                return
            else:
                author = member
                pfp = author.avatar_url
                embed = discord.Embed(title="**Avatar**")
                embed.set_author(name=str(author), icon_url=pfp)
                embed.set_image(url=pfp)
                await ctx.send(embed=embed)
                return
        except discord.ext.commands.errors.UserNotFound:
            await ctx.send(f'Couldn\'t find user -> {member}')
            return

    @cog_ext.cog_slash(name='feedback', description='Send feedback to the developers!')
    async def _feedback(self, ctx:SlashContext, *, text):
        channel = self.client.get_channel(839951602168496149)
        fembed = discord.Embed(title=f"Feedback from {ctx.author} who is in the server **{ctx.guild.name}**",
                               description=f"{ctx.author.id} (User ID)\n{ctx.guild.id} (Guild ID)```" + text + "```",
                               color=discord.Color.blurple(), timestamp=datetime.datetime.utcnow())
        msg = await channel.send(embed=fembed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        await ctx.send(str(f'Thank you for using InfiniBot!'), hidden=True)

    @cog_ext.cog_slash(name='quickpoll', description='A one or the other poll')
    async def _quickpoll(self, ctx: SlashContext, opt1, opt2):
        author = ctx.author
        pfp = author.avatar_url
        embed = discord.Embed(description=f"{opt1} or {opt2}", color=discord.Color.red(),
                              timestamp=datetime.datetime.utcnow())
        embed.set_author(name=author, icon_url=pfp)
        message = await ctx.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        return

    @cog_ext.cog_slash(name='choicepoll', description='A multiple choice poll!')
    async def _choicepoll(self, ctx: SlashContext, title, arg1, arg2, arg3, arg4=None, arg5=None, arg6=None, arg7=None, arg8=None, arg9=None):
        if len(title.strip()) > 50:
            return await ctx.send("Your title cannot be longer than 50 characters.")
        title = title.strip()
        descarr = []
        numarr = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        x = []
        x.append(arg1)
        x.append(arg2)
        x.append(arg3)
        if arg4 is not None:
            x.append(arg4)
        if arg5 is not None:
            x.append(arg5)
        if arg6 is not None:
            x.append(arg6)
        if arg7 is not None:
            x.append(arg7)
        if arg8 is not None:
            x.append(arg8)
        if arg9 is not None:
            x.append(arg9)

        for i, k in enumerate(x):
            descarr.append(f":{numarr[i]}: --> {k.strip()}")
        desc = "\n".join(descarr)
        embed = discord.Embed(title=title, description=desc, color=discord.Color.green(),
                              timestamp=datetime.datetime.utcnow())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        message = await ctx.send(embed=embed)
        emoji_numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        for i, k in enumerate(x):
            await message.add_reaction(f"{emoji_numbers[i]}")

    @cog_ext.cog_slash(name='botinfo', description=f'Get some statistics about InfiniBot!')
    async def _botinf(self, ctx:SlashContext):
        db = cluster['COMMANDCOUNT']
        collection = db['commandcount']
        results = collection.find({'_id': self.client.user.id})
        for i in results:
            countr = i['count']
        cpusage = psutil.cpu_percent()
        RAMuse = psutil.virtual_memory().percent
        embed = discord.Embed(color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Version:", value=f"```{botversion}```")
        embed.add_field(name="Python Version: ", value="```3.9.5```")
        embed.set_footer(text="Developed by glizzybeam7801#8196 and kidsonfilms#4635")
        embed.add_field(name="Commands run:", value=f"```{countr + 1}```", inline=False)
        embed.add_field(name="Servers:", value=f"```{len(self.client.guilds)}```")
        embed.add_field(name="CPU Usage:", value=f"```{cpusage}%```", inline=False)
        embed.add_field(name="RAM Usage:", value=f"```{RAMuse}%```")
        embed.add_field(name="Client Latency:", value=f"```{round(self.client.latency * 1000)}ms```", inline=False)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_author(name=f"InfiniBot Statistics", icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed, hidden=True)

    @cog_ext.cog_slash(name='botinvite', description='Get a link to invite InfiniBot!')
    async def _botinv(self, ctx:SlashContext):
        embed = discord.Embed(title="InfiniBot Invite Link",
                              description=r'https://discord.com/api/oauth2/authorize?client_id=829464107710677022&permissions=4294307063&scope=bot%20applications.commands',
                              color=discord.Color.blurple())
        embed.set_footer(text=f"InfiniBot Help | Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name='passwordgenerator', description='Generates a random password!')
    async def _passgen(self, ctx:SlashContext, length:int = 10):
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        num = string.digits
        symbols = string.punctuation
        if abs(length) > 20:
            await ctx.send(f"Since your specified value was greater than 20 characters, we are shortening it to 20.", hidden=True)
        combined = lower + upper + num + symbols
        temp = random.sample(combined, abs(length) if abs(length) <= 20 else 20)
        channel = ctx.channel
        desc = f'{"".join(temp)}'
        desc2 = f"\nYou requested this in {channel.mention} in the server **{ctx.guild.name}**"
        embed = discord.Embed(description=f"```{desc}```{desc2}", color=discord.Color.green())
        embed.set_author(name=f"{ctx.author.name}'s randomly generated password", icon_url=ctx.author.avatar_url)
        embed.set_footer(text="InfiniBot Password Generator")
        await ctx.send(embed=embed, hidden=True)

    @cog_ext.cog_slash(name='fm', description='Get your currently playing track from Last.fm!')
    async def _fm(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

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

    @cog_ext.cog_slash(name='serverstats', description='Get some basic server statistics!')
    async def _serverstats(self, ctx: SlashContext):
        name = f"GUILD{ctx.guild.id}"
        db = cluster[name]
        collection = db['messages']
        results = collection.find({'_id': ctx.guild.id})
        for i in results:
            msgcount = i['count']
        if msgcount == '':
            msgcount = 0
        collection = db['serverstats']
        results = collection.find({'_id': ctx.guild.id})
        for i in results:
            vcsecs = i['vcsecs']
        if vcsecs == '':
            vcsecs = 0

        collection = db['config']
        results = collection.find({'_id': ctx.guild.id})
        for i in results:
            ghostcount = i['ghostcount']
        if ghostcount == '':
            ghostcount = 0
        x = ctx.guild.created_at
        y = x.strftime("%b %d %Y %H:%S")
        print(y)
        z = datetime.datetime.utcnow() - x
        lm = str(abs(z))
        print(lm)
        q = lm.split(", ")
        a = q[0]
        desc = f"This is only from when I joined **{ctx.guild.name}**. Anything before that has not been documented."
        embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Channels:", value=f"```{str(len(ctx.guild.channels))}```", inline=True)
        embed.add_field(name="Users:", value=f"```{ctx.guild.member_count}```", inline=True)
        embed.add_field(name="Messages Sent:", value=f"```{msgcount}```", inline=True)
        # embed.add_field(name=f"In #{ctx.channel.name}:", value = f"```{smsgcfount}```", inline = True)
        # embed.add_field(name=f"By {ctx.author.name}:", value = f"```{smsgcount}```", inline = True)
        # embed.add_field(name=f"In #{ctx.channel.name} by {ctx.author.name}:", value=f"```{result3[0]}```", inline = False)
        embed.add_field(name="Seconds in Voice Channels", value=f"```{vcsecs}```", inline=True)
        embed.add_field(name=f"Server Creation Date:",
                        value=f"```{f'{y} ({a} ago)' if lm[0:6] != '1 day,' else 'Today'}```", inline=True)
        # embed.add_field(name=f"Most active text channel in **{ctx.guild.name}**: ", value = f"```#{topchannel.name} with {smsgcffount} messages.```", inline = False)
        # figure out most active VC
        ownerser = self.client.get_user(ctx.guild.owner_id)
        embed.add_field(name=f"Number of Ghost Pings", value=f"```{ghostcount}```", inline=False)
        embed.add_field(name="Server Owner:", value=ownerser.mention, inline=False)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name=f"{ctx.guild.name}'s Statistics", icon_url=ctx.guild.icon_url)
        embed.set_footer(text=f"Server ID: {ctx.guild.id}")
        await ctx.send(embed=embed, hidden=True)

    @cog_ext.cog_slash(name='prefix', description='Returns the prefix for your server!')
    async def _prefix(self, ctx: SlashContext):
        prefix = utils.serverprefix(ctx)
        # x = utils.imgdraw(photo = './Images/prefiximg.png', font = 'arial.ttf', fontsize=15, xy=(75,45), text=f"{prefix}tinyurl https://www.youtube.com/watch?v=dQw4w9WgXcQ", rgb=(255,255,255))
        desc = f"Prefix for **{ctx.guild.name}** is {prefix}. \n\n**NOTE:** If you want a word prefix with a space after it, you must surround it in quotes due to a Discord limitation.\n\nEXAMPLE: {prefix}changeprefix \"yo \""
        embed = discord.Embed(description=desc, color=discord.Color.green())
        embed.set_thumbnail(url=ctx.guild.icon_url)
        # file = discord.File("./profile.png", filename='image.png')
        # embed.set_image(url='attachment://image.png')
        await ctx.send(embed=embed, hidden=True)

    @cog_ext.cog_slash(name='inviteinfo', description='Get information about an invite!')
    async def _invinf(self, ctx:SlashContext, invite:discord.Invite):
        try:
            embed = discord.Embed(color = discord.Color.green())
            embed.add_field(name = "Inviter", value = f"```{invite.inviter}```")
            embed.add_field(name = "Code", value = f"```{invite.code}```")
            embed.add_field(name = "Server", value = f"```{invite.guild}```")
            embed.add_field(name = "URL", value = f"```{invite.url}```", inline = False)
            embed.add_field(name = "Uses", value = f"```{invite.uses}```", inline = False)
            await ctx.send(embed=embed, hidden=True)
        except Exception as e:
            return await ctx.send(str(e))

    @cog_ext.cog_slash(name='help', description='Get InfiniBot\'s help menu!')
    async def _help(self, ctx:SlashContext):
        prefix = utils.serverprefix(ctx)
        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name=f"{self.client.user.name}'s Help Menu", icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        # add individual help for each command
        embed.set_footer(text=f"Made by glizzybeam7801#8196 and kidsonfilms#4635")
        # add some example commands
        embed.add_field(name="🛠️ Setup", value=f"Setup {self.client.user.name} for {ctx.guild.name}!\n`{prefix}setup`")
        embed.add_field(name="🎮 Games", value=f"Play games with {self.client.user.name}!\n`{prefix}help games`")
        embed.add_field(name="📣 Moderation",
                        value=f"Moderate your server or take a step back and let {self.client.user.name} moderate for you!\n`{prefix}help moderation`")
        embed.add_field(name="❓ Miscellaneous",
                        value=f"These commands aren't sorted right now, but include everything.\n`{prefix}help misc`")
        embed.add_field(name="💰 Economy",
                        value=f"Participate in an economy system! (Currently in development). \n`{prefix}help economy`")
        embed.add_field(name="📈 Server Stats",
                        value=f"See server stats for {ctx.guild.name} \n`{prefix}help serverstats`")
        embed.add_field(name="About Us!",
                        value=f"[Invite Link](https://discord.com/api/oauth2/authorize?client_id=829464107710677022&permissions=4294307063&scope=bot%20applications.commands) - [Support Server](https://discord.gg/4VnUA8ZXyH)\nSend the devs feedback by using `{prefix}feedback`!",
                        inline=False)
        await ctx.send(embed=embed, hidden=True)

    @cog_ext.cog_slash(name='translate', description='Translate a phrase!')
    async def _translate(self, ctx:SlashContext, target_language, *, phrase):
        try:
            newphrase = translator.translate(phrase.strip(), dest=target_language.strip().lower())
            await ctx.send(f'Your phrase is: `{newphrase.text}`!')
        except ValueError:
            await ctx.send(
                f"You didn\'t mention the language you would like to translate to, or it was an invalid language!")

def setup(client):
    client.add_cog(Slash(client))
