import discord
from discord.ext import commands
import datetime
import random
import aiohttp
import asyncio
import wikipedia
import string
from googletrans import Translator
import pyfiglet
from googleapiclient import discovery
from pymongo import MongoClient
from modules import utils, help
import re
import urllib.request
import time
from chatbot import Chat

with open('mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()

with open('perspectiveapis.txt', 'r') as file:
    tokens = file.read()
    keys = tokens.split('\n')
PERSPECTIVE_KEYS = keys

chat = Chat()

cluster = MongoClient(mongo_url)


translator = Translator()
class Misc(commands.Cog, name="Miscellaneous"):
    def __init__(self, client):
        self.client = client
        self.icon = '❓'
        self.description = "These commands aren't sorted right now, but include everything."
        self.sma = {}
        self.smc = {}
        self.smt = {}
        self.ema = {}
        self.emc = {}
        self.emt = {}
        self.sessionids = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.sma[message.channel.id] = message.author.id
        self.smc[message.channel.id] = message.clean_content
        self.smt[message.channel.id] = message.created_at
        await asyncio.sleep(60)
        del self.smc[message.channel.id]
        del self.sma[message.channel.id]
        del self.smt[message.channel.id]

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        self.ema[before.channel.id] = before.author.id
        self.emc[before.channel.id] = before.clean_content
        self.emt[before.channel.id] = before.created_at
        await asyncio.sleep(60)
        del self.emc[before.channel.id]
        del self.ema[before.channel.id]
        del self.emt[before.channel.id]

    @commands.command()
    async def whois(self, ctx, member: discord.User = None):
        if member is None:
            member = ctx.author
        try:
            desc = f"Bot: {'⛔' if not member.bot else '✅'}\n" \
                   f"User ID: {member.id}\n" \
                   f"Created: {member.created_at.strftime('%D')}\n" \
                   f"Username: {member.name}#{member.discriminator}\n" \
                   f"Is Discord System: {'⛔' if not member.system else '✅'}"
            embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=f"About {member.name}", icon_url=member.avatar_url)
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    # @commands.command(aliases=['terms', 'termsofservice', 'privacypolicy'])
    # @commands.cooldown(1, 15, commands.BucketType.user)
    # async def tos(self, ctx):
    #     desc = '**View my User Agreement [here](https://docs.google.com/document/d/1XHOKPspuyqUIS9a0d0BMcO5oKXT5Xe5KdN_olG9sGFc/edit?usp=sharing).**\n' \
    #            '\nThank you for using InfiniBot!'
    #     embed = discord.Embed(title="InfiniBot User Agreement", description=desc, color=discord.Color.green(),
    #                           timestamp=datetime.datetime.utcnow())
    #     embed.set_thumbnail(url=self.client.user.avatar_url)
    #     await ctx.author.send(embed=embed)

    @commands.command()
    async def givecookie(self, ctx):
        await ctx.send(f"Fine, I will give you {random.randint(0, 10)} cookies.")

    @commands.command()
    async def news(self, ctx, *, query = "Elon Musk"):
        if query == 'Elon Musk':
            await ctx.send("You can specify a query next time!")
        async with aiohttp.ClientSession() as session:
            url = "https://free-news.p.rapidapi.com/v1/search"

            querystring = {"q": f"{query.strip()}", "lang": "en"}

            with open('freenews.txt', 'r') as f:
                token = f.read()
            headers = {
                'x-rapidapi-key': token,
                'x-rapidapi-host': "free-news.p.rapidapi.com"
            }

            async with session.get(url, headers=headers, params=querystring) as response:
                data = await response.json()
                print(data)



            try:
                x = random.randrange(len(data['articles']))
                print(len(data['articles']))
                likes = data['total_hits']
                title = data['articles'][x]['title']
                author = data['articles'][x]['author']
                if str(author) == 'None':
                    author = data['articles'][x]['clean_url']
                pubdate = str(data['articles'][x]['published_date'])[0:10]
                titleurl = data['articles'][x]['link']
                thumbnail = data['articles'][x]['media']
                desc = str(data['articles'][x]['summary'])[0:2000] + f"... \n[Click here to read the full story]({titleurl})"
                embed = discord.Embed(title = title, description=desc, color = discord.Color.green())
                embed.set_author(name = author, icon_url = 'https://th.bing.com/th/id/R3e0487abfc9c6b31806f4f6751fdc8ef?rik=hEriAUJIg5bKOA&riu=http%3a%2f%2fcdn.onlinewebfonts.com%2fsvg%2fimg_456930.png&ehk=bnskK1wWw7gco9UHxOQQxnCoBdDuCVGeyQsQTsaR2vk%3d&risl=&pid=ImgRaw')
                embed.set_footer(text = f"👍🏽 {likes} | Published on {pubdate}")
                embed.set_thumbnail(url=thumbnail)
                await ctx.send(embed=embed)
            except KeyError:
                return await ctx.send(f"Looks like `{query.strip()}` couldn't retrieve a valid article :( \n"
                                      f"If this keeps happening, contact the developers.")


    @commands.command()
    async def weather(self, ctx, *, place = 'New York'):
        url = "https://community-open-weather-map.p.rapidapi.com/find"

        querystring = {"q": place.strip(), "cnt": "1", "mode": "json", "lon": "0", "type": "link, accurate", "lat": "0",
                       "units": "imperial"}

        headers = {
            'x-rapidapi-key': "f7bdac7e35msh94c0ae5a3b2d0c7p15b828jsnc6ac6c2d5034",
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params = querystring) as response:
                data = await response.json()
                print(data)
        if int(data['count']) == 0:
            return await ctx.send(f"It looks like the place `{place.strip()}` doesn't exist!")
        author = data['list'][0]['name']
        authorurl = 'https://th.bing.com/th/id/Rd8c10ced4c324b34408dda90292e48c2?rik=hLutIkyyLdbkMw&riu=http%3a%2f%2ficons.iconarchive.com%2ficons%2fiynque%2fios7-style%2f1024%2fWeather-icon.png&ehk=gA92r%2fgxkM24%2f0TYtSFkMie4BkV1Samb0ZYBjpJMqpQ%3d&risl=&pid=ImgRaw'
        temp = data['list'][0]['main']['temp']
        feelstemp = data['list'][0]['main']['feels_like']
        tempmin = data['list'][0]['main']['temp_min']
        tempmax = data['list'][0]['main']['temp_max']
        pressure = data['list'][0]['main']['pressure']
        humidity = data['list'][0]['main']['humidity']
        print(humidity)
        embed = discord.Embed(color = discord.Color.green())
        descarr = []
        if str(data['list'][0]['rain']) != 'None':
            descarr.append('🌧️')
        if int(data['list'][0]['wind']['speed']) > 20:
            descarr.append('⛈')
        if str(data['list'][0]['snow']) != 'None':
            descarr.append('🌨️')
        if int(data['list'][0]['clouds']['all']) > 60:
            descarr.append('☁')
        if len(descarr) == 0:
            descarr.append(f'It\'s a nice day in {author} today!')
        embed.set_author(name=f"Weather in {author}", icon_url=authorurl)
        embed.set_footer(text = "All temperatures are in Fahrenheit.")
        embed.add_field(name='Temperature', value=f"{temp}°F")
        embed.add_field(name='Feels like', value = f"{feelstemp}°F")
        embed.add_field(name='Minumum Temperature', value =f"{tempmin}°F", inline = False)
        embed.add_field(name='Maximum Temperature', value = f"{tempmax}°F")
        embed.add_field(name='Pressure', value = pressure, inline = False)
        embed.add_field(name = 'Humidity', value = str(humidity))
        desc = ' '.join(descarr)
        print(desc)
        embed.add_field(name='Weather', value=desc, inline = False)
        await ctx.send(embed=embed)

    @commands.command(aliases = ['wiki'])
    async def wikipedia(self, ctx, *, q = "Elon Musk"):
        while True:
            try:
                res = wikipedia.page(q.strip(), auto_suggest=False)
                title = res.title
                readmore = res.url
                summ = str(wikipedia.summary(q.strip(), auto_suggest=False))[0:1800]
                desc = summ + f"... \n[Continue Reading]({readmore})"
                embed = discord.Embed(title=title, description=desc, color=discord.Color.green())
                try:
                    img = res.images[0]
                    embed.set_thumbnail(url=img)
                except IndexError:
                    pass
                await ctx.send(embed=embed)
                return
            except wikipedia.exceptions.PageError:
                return await ctx.send(f"The search term `{q.strip()}` did not return a Wikipedia page.")
            except wikipedia.exceptions.DisambiguationError as e:
                arr = str(e).split('\n')
                arr.pop(0)
                descarr = []
                for i, k in enumerate(arr):
                    if i > 19:
                        break
                    descarr.append(f"{i + 1}. {k}")
                desc = "\n".join(descarr)
                await ctx.send(f"Which `{q.strip()}` did you mean? \n```{desc}```\nRespond with the number of the correct `{q.strip()}`.")
                def check(m):
                    return m.author == ctx.author and m.channel==ctx.channel

                try:
                    counter = 0
                    while True:
                        if counter > 5:
                            return await ctx.send("Due to too many invalid choices, this session has ended.")
                        msg = await self.client.wait_for('message', check=check, timeout = 120)
                        try:
                            q = arr.pop((int(msg.content) - 1))
                            break
                        except IndexError:
                            await ctx.send(f"`{msg.content.lower()}` isn\'t a valid number in this list! Please try again!")
                            counter += 1
                            continue
                        except ValueError:
                            counter += 1
                            await ctx.send(f"You need to specify the number, not `{msg.content.lower()}`.")
                            continue
                except asyncio.TimeoutError:
                    return await ctx.reply("Timed out", mention_author = False)

    @commands.command(aliases = ['tr'])
    async def translate(self, ctx, language = 'en', *, text = "Como estas?"):
        try:
            newphrase = translator.translate(text.strip(), dest=language.strip().lower())
            await ctx.reply(f'Your phrase is: `{newphrase.text}`!', mention_author = False)
        except ValueError:
            await ctx.reply(f"You didn\'t mention the language you would like to translate to, or it was an invalid language!\n", mention_author = False)

    @commands.command()
    async def define(self, ctx, *, term = "hello"):
        async with aiohttp.ClientSession() as session:
            url = f'https://api.dictionaryapi.dev/api/v2/entries/en_US/{term.strip()}'
            async with session.get(url) as response:
                data = await response.json()
                print(data)
            try:
                word = data[0]['word']
                pronunctation = data[0]['phonetics'][0]['text']
                definitions = data[0]['meanings'][0]['definitions'][0]['definition']
                try:
                    synonyms = ", ".join(data[0]['meanings'][0]['definitions'][0]['synonyms'])
                except KeyError:
                    synonyms = None
                example = data[0]['meanings'][0]['definitions'][0]['example']
                pos = data[0]['meanings'][0]['partOfSpeech']
                embed = discord.Embed(color = discord.Color.green())
                embed.set_author(name=f"Definition of {word}")
                embed.add_field(name="Pronunciation", value = f"```{pronunctation}```")
                embed.add_field(name='Part Of Speech', value = f"```{pos}```")
                embed.add_field(name='Definition', value = f"```{definitions}```", inline = False)
                embed.add_field(name='Synonyms', value = f"```{synonyms if synonyms is not None else 'None'}```", inline = False)
                embed.add_field(name='Example Sentence', value = f"```{example}```", inline= False)
                await ctx.send(embed=embed)
            except KeyError:
                return await ctx.send(f"It looks like the term `{term.strip()}` could not be found.")

    @commands.command()
    async def inviteinfo(self, ctx, invite: discord.Invite):
        try:
            embed = discord.Embed(color=discord.Color.green())
            embed.add_field(name="Inviter", value=f"```{invite.inviter}```")
            embed.add_field(name="Code", value=f"```{invite.code}```")
            embed.add_field(name="Server", value=f"```{invite.guild}```")
            embed.add_field(name="URL", value=f"```{invite.url}```", inline=False)
            embed.add_field(name="Uses", value=f"```{invite.uses}```", inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            if str(e).strip() == 'Invite is invalid or expired.':
                return await ctx.reply(e, mention_author=False)

    @commands.command(aliases=['passwordgen', 'passgen', 'passwordgenerate'])
    # add to help menu
    @commands.cooldown(2, 15, commands.BucketType.user)
    async def passwordgenerator(self, ctx, lent=10):
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        num = string.digits
        symbols = string.punctuation
        if lent > 20:
            await ctx.send(f"Since your specified value was greater than 20 characters, we are shortening it to 20.")
        combined = lower + upper + num + symbols
        temp = random.sample(combined, lent)
        channel = ctx.channel
        desc = f'{"".join(temp)}'
        desc2 = f"\nYou requested this in {channel.mention} in the server **{ctx.guild.name}**"
        await ctx.message.add_reaction('✅')
        embed = discord.Embed(description=f"```{desc}```{desc2}", color=discord.Color.green())
        embed.set_author(name=f"{ctx.author.name}'s randomly generated password", icon_url=ctx.author.avatar_url)
        embed.set_footer(text="InfiniBot Password Generator")
        await ctx.author.send(embed=embed)

    @commands.command()
    async def asciitext(self, ctx, *, text="Next time put text you want converted lol"):
        if len(text) > 2000:
            await ctx.send("Your message was too long!")
            return
        result = pyfiglet.figlet_format(f"{text}")
        await ctx.send(f"```{result}```")

    @commands.command()
    # helpmenu addition !!!
    async def servericon(self, ctx):
        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_image(url=ctx.icon_url)
        embed.set_footer(text=f"{ctx.name} Server Icon | Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command()
    async def emojify(self, ctx, *, text):
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

            await ctx.send("".join(new))
        except:
            await ctx.send("Something went wrong, next time make sure to use only letters.")


    @commands.command(aliases = ['msg2embed', 'm2e'])
    async def msgtoembed(self, ctx, message:discord.Message=None):
        if ctx.message.reference:
            message = await ctx.fetch_message(ctx.message.reference.message_id)
        if message is None:
            message = ctx.message
        res = utils.messagetoembed(message)
        await ctx.send(embed=res)

    # # @commands.command()
    # # async def talk(self, ctx):
    # #     if ctx.author.bot:
    # #         return
    # #     try:
    # #         def check(m):
    # #             return m.author == ctx.author and m.channel == ctx.channel
    # #         await ctx.send(
    # #             f'{ctx.author.mention}, before I start I\'d like to go over a few things. When you wish to end the chat session, type `bye`. \n'
    # #             f'I only wait for 30 seconds between messages. If you don\'t respond, I will end the session on my own.\n'
    # #             f'Finally, press `y` to confirm you want to talk. Anything else, and the chat session ends.')
    # #         message = await self.client.wait_for('message', check=check, timeout=30)
    # #         if message.content.lower().strip() == 'y':
    # #             await ctx.send(f"Great {ctx.author.mention}, let's get to it. What's on your mind?")
    # #             while message.content.lower().strip() != "bye":
    # #                 message = await self.client.wait_for('message', check=check, timeout=30)
    # #                 response = await rs.get_ai_response(message.content.strip())
    # #                 await message.reply(response)
    # #                 if message.content.lower() == 'bye':
    # #                     await ctx.send(f'{ctx.author.mention}, we will meet again soon')
    # #                     return
    #
    #         else:
    #             await ctx.send(f'{ctx.author.mention}, we will meet again soon')
    #             return
    #     except asyncio.TimeoutError:
    #         await ctx.reply("Your chat session has timed out. Use the command again to chat.")
    #         return

    @commands.command()
    async def activities(self, ctx, member:discord.Member):
        pass

    @commands.group(invoke_without_command=True)
    async def youtube(self, ctx, *, query):
        html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={query}")
        vidid = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        await ctx.send(f"https://www.youtube.com/watch?v={vidid[0]}")

    @commands.command()
    async def echo(self, ctx, chanel: discord.TextChannel, *, message="Echo"):
        channel = chanel.id
        schannel = self.client.get_channel(channel)
        if not channel.permissions_for(ctx.message.author).send_messages: #oops ppl abused this
            return await ctx.reply(f'You don\'t have permission to send messages in {chanel.mention}!', mention_author = False)
        await schannel.send(content=message, allowed_mentions=discord.AllowedMentions.none())
        await ctx.message.add_reaction(str('✅'))
        await asyncio.sleep(2)
        await ctx.message.delete()

    @commands.command(aliases = ['tone', 'toxicity'])
    async def analyze(self, ctx, *, message):
        try:
            j = discovery.build(
                "commentanalyzer",
                "v1alpha1",
                developerKey=random.choice(PERSPECTIVE_KEYS),
                discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
                static_discovery=False,
            )

            analyze_request = {
                'comment': {'text': f'{message.strip()}'},
                'requestedAttributes': {'TOXICITY': {}}
            }
            embed = discord.Embed()
            embed.description = message.strip()
            embed.set_author(name=ctx.message.author.name + "#" + ctx.message.author.discriminator,
                             icon_url=ctx.message.author.avatar_url)
            embed.timestamp = ctx.message.created_at
            embed.colour = ctx.message.author.color
            response = j.comments().analyze(body=analyze_request).execute()
            tox = round((float(response['attributeScores']['TOXICITY']['summaryScore']['value']) * 100), 3)
            embed.set_footer(text=f"Toxicity: {tox}%")
            await ctx.send(embed=embed)


        except Exception as e:
            print(e)
            pass


    @commands.command(help='The ping of you to the bot (not the bot\'s ping)')
    async def ping(self, ctx):
        time_1 = time.perf_counter()
        await ctx.trigger_typing()
        time_2 = time.perf_counter()
        ping = round((time_2 - time_1) * 1000)
        await ctx.reply(f"Pong! 🏓 `{ping}ms`", mention_author=False)
        return

    @commands.command(aliases = ['discriminator'])
    async def discrim(self, ctx, discrim = None):
        try:
            if discrim is None:
                discrim = (ctx.author.discriminator)
            if len(discrim) != 4:
                return await ctx.send("That\'s not a valid disciminator!")
            if not discrim.isdigit() :
                return await ctx.send("That is not a number!!!")
            users = self.client.get_all_members()
            members = list(set(list(filter(lambda m: str(m.discriminator) == str(discrim), users))))
            embed = discord.Embed(color = discord.Color.red())
            desc = []
            if (len(members) == 1 and discrim == ctx.author.discriminator):
                return await ctx.send("It looks like you are the only person with this discriminator who uses InfiniBot!")
            if len(members) == 0:
                return await ctx.send("Looks like no one has that discriminator :(")
            for i in range((len(members) if len(members) <= 8 else 8)):
                desc.append(f"{members[i].name}#{members[i].discriminator}")
            embed.description = "\n".join(desc)
            embed.title = f"Members with the discriminator #{discrim}"
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @commands.command(aliases = ['flip'])
    async def coinflip(self, ctx):
        choices = [
            'heads', 'tails'
        ]
        return await ctx.reply(f"{random.choice(choices)}", mention_author = False)

    @commands.command()
    async def snipe(self, ctx):
        channel = ctx.channel
        try:
            member = self.client.get_user(self.sma[channel.id])
            embed = discord.Embed(color = discord.Color.green())
            embed.set_author(name = f"{member.name}#{member.discriminator}", icon_url = member.avatar_url)
            embed.description = self.smc[channel.id]
            embed.timestamp = self.smt[channel.id]
            await ctx.send(embed=embed)
        except LookupError:
            return await ctx.send("There is nothing to snipe!")

    @commands.command()
    async def editsnipe(self, ctx):
        channel = ctx.channel
        try:
            member = self.client.get_user(self.ema[channel.id])
            embed = discord.Embed(color=discord.Color.green())
            embed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url)
            embed.description = self.emc[channel.id]
            embed.timestamp = self.emt[channel.id]
            await ctx.send(embed=embed)
        except LookupError:
            return await ctx.send("There is nothing to snipe!")

    @commands.command(aliases = ['talk'])
    async def chat(self, ctx):
        try:
            print(self.sessionids[ctx.author.id])
            return await ctx.send("You already have another chat session in progress in another channel/server! Please end that one before starting a new one.")
        except LookupError:
            pass
        try:
            await ctx.send(
                f'{ctx.author.mention}, before I start I\'d like to go over a few things. When you wish to end the chat session, type `bye`. \n'
                f'I only wait for 30 seconds between messages. If you don\'t respond, I will end the session on my own.\n'
                f'Finally, press `y` to confirm you want to talk. Anything else, and the chat session ends.')
            message = await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
            if message.content.lower().rstrip() in ('y', 'yes'):
                await ctx.send(f"Great {ctx.author.mention}, let's get to it. What's on your mind?")
            else: return
            lower = string.ascii_lowercase
            upper = string.ascii_uppercase
            num = string.digits
            symbols = string.punctuation
            combined = lower + upper + num + symbols
            temp = random.sample(combined, 10)
            desc = f'{"".join(temp)}'
            self.sessionids[ctx.author.id] = desc
            message = await self.client.wait_for('message',
                                                 check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                                                 timeout=30)
            chat.start_new_session(session_id=desc, topic="none")
            response = chat.respond(message=message.clean_content, session_id=self.sessionids[ctx.author.id])
            await ctx.send(response)
            while True:
                message = await self.client.wait_for('message',
                                                     check=lambda
                                                         m: m.author == ctx.author and m.channel == ctx.channel,
                                                     timeout=30)
                if message.content.lower().strip() in ('quit', 'bye'):
                    await ctx.send("cya")
                    del self.sessionids[ctx.author.id]
                    break
                response = chat.respond(message=message.clean_content, session_id=self.sessionids[ctx.author.id])
                await message.reply(content = response, mention_author = False)
        except asyncio.TimeoutError:
            del self.sessionids[ctx.author.id]
            return

def setup(client):
    client.add_cog(Misc(client))
