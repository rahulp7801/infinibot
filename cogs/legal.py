import discord
from discord.ext import commands
import asyncio
import datetime
from pymongo import MongoClient
with open('./mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)

class Legal(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 90000, commands.BucketType.user)
    async def dntu(self, ctx):
        desc = f"{ctx.author.mention}, by requesting not to track your data, you understand that you will not be allowed to run commands with {self.client.user.name} from this point on. " \
               f"Do you still wish to proceed? React with the ✅ if yes, or with the ⛔ to cancel.\n\n**NOTE: TO UNDO THIS ACTION, YOU MUST CONTACT THE DEVELOPERS OR JOIN THE SUPPORT SERVER**"
        embed = discord.Embed(description=desc, color=discord.Color.red())
        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
        await message.add_reaction('⛔')

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in ['✅', '⛔']

        reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
        if reaction.emoji == '✅':
            db = cluster['DONOTTRACK']
            collection = db['users']
            query = {"_id": ctx.author.id}
            if collection.count_documents(query) == 0:
                ping_cm = {"_id": ctx.author.id, "name": ctx.author.name,
                           'time': datetime.datetime.utcnow().strftime('%D')}
                collection.insert_one(ping_cm)
            else:
                results = collection.find(query)
                for i in results:
                    date = i['time']
                desc = f"You have already requested not to track your data. \nLAST REQUESTED: {date}"
                embed = discord.Embed(description=desc, color=discord.Color.red())
                await message.edit(embed=embed)
                return await message.clear_reactions()
            desc = f"Success! From this point on, all data pertaining to {ctx.author.mention} will now be deleted.\n\nTo undo this action, please visit the support server."
            embed = discord.Embed(description=desc, color=discord.Color.green())
            await message.edit(embed=embed)
            return await message.clear_reactions()

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    async def dntg(self, ctx):
        db = cluster['DONOTTRACK']
        collection = db['guilds']
        query = {"_id": ctx.guild.id}
        if collection.count_documents(query) == 0:
            ping_cm = {"_id": ctx.guild.id, "name": ctx.guild.name, 'time': datetime.datetime.utcnow()}
            collection.insert_one(ping_cm)
        else:
            return await ctx.send(f"{ctx.guild.name} has already requested to not track its data.")
        # dblist = (cluster.list_database_names())
        # if name in dblist:
        #     print(name)
        await ctx.send("Success!")

    @commands.command(aliases=['clear_server_data', 'clearguilddata', 'clear_guild_data'])
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.cooldown(1, 900, commands.BucketType.guild)
    async def clearserverdata(self, ctx):
        await ctx.message.delete()
        name = f"GUILD{ctx.guild.id}"
        desc = f"Here at {self.client.user.name}, we take your privacy seriously. By clearing this data you acknowledge that ALL information pertaining to {ctx.guild.name}, such as message counts and server configuration settings, WILL BE LOST. THIS IS AN IRREVERSIBLE ACTION! \n\nTo confirm clearing **{ctx.guild.name}'s** information, react with the ✅. \n\nIf you would like to cancel, react with ⛔."
        embed = discord.Embed(description=desc, color=discord.Color.red())

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in ['✅', '⛔']

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
        await message.add_reaction('⛔')
        try:
            reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=120)
            if reaction.emoji == '✅':
                cluster.drop_database(name)
                name = f"GUILD{ctx.guild.id}"
                db = cluster[name]
                collection = db['config']
                ping_cm = {
                    "_id": ctx.guild.id,
                    "name": ctx.guild.name,
                    'prefix': '%',
                    'welcomemsg': "",
                    "welcomechannel": "",
                    'priv_welcomemsg': "",
                    'leavemsg': "",
                    'captchaon': "",
                    'muterole': "",
                    'spamdetect': "",
                    'logging': "",
                    'logchannel': "",
                    'levelups': "",
                    'ghostpingon': "",
                    'ghostcount': '',
                    'blacklistenab': "",
                    'mcip': "",
                    'starchannel': '',
                    'welcomenick': '',
                    'welcomerole': ''
                }
                x = collection.insert_one(ping_cm)
                collection = db['afk']
                ping_cm = {
                    "_id": ctx.guild.id,
                    "name": ctx.guild.name,
                    'afkstatus': "",
                    'startafk': '',
                    'preafknick': '',
                    'afkid': ''
                }
                x = collection.insert_one(ping_cm)
                collection = db['serverstats']
                ping_cm = {
                    "_id": ctx.guild.id,
                    "name": ctx.guild.name,
                    'vcsecs': "",
                    'msgcount': ''
                }
                x = collection.insert_one(ping_cm)
                collection = db['levels']
                ping_cm = {
                    "_id": ctx.guild.id,
                    "name": ctx.guild.name
                }
                x = collection.insert_one(ping_cm)
                collection = db['customcmnd']
                ping_cm = {
                    "_id": ctx.guild.id,
                    "name": ctx.guild.name,
                    'commandname': ""
                }
                x = collection.insert_one(ping_cm)
                collection = db['commands']
                ping_cm = {
                    "_id": ctx.guild.id,
                    "name": ctx.guild.name,
                    'commandname': "",
                    'commandcount': '',
                    'commandchannel': ''
                }
                x = collection.insert_one(ping_cm)
                collection = db['warns']
                ping_cm = {
                    "_id": ctx.guild.id,
                    "name": ctx.guild.name,
                    'reason': "",
                    'time': '',
                    'mod': '',
                    'offender': ''
                }
                x = collection.insert_one(ping_cm)
                collection = db['messages']
                ping_cm = {
                    "_id": ctx.guild.id,
                    "name": ctx.guild.name,
                    'author': "",
                    'date': '',
                    'channel': '',
                    'count': ''
                }
                x = collection.insert_one(ping_cm)
                collection = db['typing']
                ping_cm = {
                    "_id": ctx.guild.id,
                    "name": ctx.guild.name,
                    'uid': '',
                    'date': "",
                    'accuracy': '',
                    'wpm': ''
                }
                x = collection.insert_one(ping_cm)
                await message.clear_reactions()
                desc = f"All server data for {ctx.guild.name} has successfully been cleared from the database."
                embed = discord.Embed(description=desc, color=discord.Color.green())
                await message.edit(embed=embed)
            elif (reaction.emoji) == '⛔':
                await message.clear_reactions()
                desc = f"Session has been cancelled."
                embed = discord.Embed(description=desc, color=discord.Color.red())
                return await message.edit(embed=embed)
        except asyncio.TimeoutError:
            await message.clear_reactions()
            desc = "Session has ended due to inactivity, data has not been cleared."
            embed = discord.Embed(description=desc, color=discord.Color.red())
            return message.edit(embed=embed)

    @clearserverdata.error
    async def clr_err(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f"Data for **{ctx.guild.name}** has recently been cleared. Please try again later.")

    #privacy command
    @commands.command()
    async def privacy(self, ctx):
        desc = f"{self.client.user.name}'s Privacy Policy\n" \
               f"\n**What data we collect**\n" \
               f"We collect information such as your server's ID, your server's icon, your username, your profile picture, the name of your server, your configuration settings (such as welcomerole), " \
               f"number of ghost pings, how many messages have been sent, and how many minutes people have been in Voice Channels.\n" \
               f"\n**How your data is protected**\n" \
               f"All of {self.client.user.name}'s data is stored in an encrypted and password-protected MongoDB instance. Only two, yes TWO, " \
               f"people have access to it. Here at {self.client.user.name}, we take your privacy very seriously.\n" \
               f"\n**Why we need this data**\n" \
               f"This data is required so that commands will be able to work. An example use case might be for when a user joins your server, to get the welcome " \
               f"message and welcome channel. \nWE DO NOT STORE ANY PII (Personal Identifiable Information)!\n" \
               f"\n**Data Sharing**\n" \
               f"At {self.client.user.name}, we do not share your data with anyone except ourselves and Discord.\n" \
               f"\n**Contact and Removal of Data**\n" \
               f"If at any point in time you wish for your data to be removed, you can run the `dntu` command, or for your entire server run `clearserverdata`.\n" \
               f"If this does not work, please join our [support server](https://discord.gg/4VnUA8ZXyH) or use the `feedback` command to report the bug.\n\n" \
               f"[Read More](https://docs.google.com/document/d/1XHOKPspuyqUIS9a0d0BMcO5oKXT5Xe5KdN_olG9sGFc/edit?usp=sharing)"
        embed = discord.Embed(description = desc, color = discord.Color.red())
        embed.set_author(name=f'High-Level TOS for {self.client.user.name}', icon_url = self.client.user.avatar_url)
        await ctx.send(embed=embed)



def setup(client):
    client.add_cog(Legal(client))