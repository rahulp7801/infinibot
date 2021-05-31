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
from pymongo import MongoClient

with open('mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)


translator = Translator()
class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def statuscol(self, ctx):
        if str(ctx.author.status).strip() == 'idle':
            embed = discord.Embed(title='You are idle!', color = discord.Color.gold())
            await ctx.send(embed=embed)
        elif str(ctx.author.status).strip() == 'online':
            embed = discord.Embed(title = 'You are online!', color = discord.Color.green())
            await ctx.send(embed=embed)
        elif str(ctx.author.status).strip() == 'dnd':
            embed = discord.Embed(title='You are on do not disturb!', color=discord.Color.red())
            await ctx.send(embed=embed)
        elif str(ctx.author.status).strip() == 'invisible':
            embed = discord.Embed(title='You are on invis!', color=discord.Color.greyple())
            await ctx.send(embed=embed)
        elif str(ctx.author.status) == 'offline':
            embed = discord.Embed(title='You are offline!', color=discord.Color.greyple())
            await ctx.send(embed=embed)

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

    @emojify.error
    async def emojify_err(self, ctx, error):
        name = f"GUILD{ctx.guild.id}"
        db = cluster[name]
        collection = db['config']
        results = collection.find({'_id': ctx.guild.id})
        for i in results:
            prefix = i['prefix']
        if isinstance(error, commands.MissingRequiredArgument):
            desc = f"```{prefix}emojify [text]```"
            embed = discord.Embed(title="Incorrect Usage!", description=desc, color=discord.Color.red())
            embed.set_footer(text="Parameters in [] are required and () are optional")
            return await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Misc(client))
