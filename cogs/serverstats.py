# import discord
# from discord.ext import commands
# import asyncio
# from pymongo import MongoClient
# import datetime

# with open('mongourl.txt', 'r') as file:
#     url = file.read()

# mongo_url = url.strip()
# cluster = MongoClient(mongo_url)

# class Serverstats(commands.Cog, name = "Server Statistics"):
#     def __init__(self, client):
#         self.client = client
#         self.icon = '📈'
#         self.description = 'See comprehensive server statistics for your server!'

#     @commands.command()
#     @commands.guild_only()
#     async def serverstats(self, ctx):
#         name = f"GUILD{ctx.guild.id}"
#         db = cluster[name]
#         collection = db['messages']
#         results = collection.find({'_id': ctx.guild.id})
#         for i in results:
#             msgcount = i['count']
#         if msgcount == '':
#             msgcount = 0
#         collection = db['serverstats']
#         results = collection.find({'_id': ctx.guild.id})
#         for i in results:
#             vcsecs = i['vcsecs']
#         if vcsecs == '':
#             vcsecs = 0

#         collection = db['config']
#         results = collection.find({'_id': ctx.guild.id})
#         for i in results:
#             ghostcount = i['ghostcount']
#         if ghostcount == '':
#             ghostcount = 0
#         x = ctx.guild.created_at
#         y = x.strftime("%b %d %Y %H:%S")
#         print(y)
#         z = datetime.datetime.utcnow() - x
#         lm = str(abs(z))
#         print(lm)
#         q = lm.split(", ")
#         a = q[0]
#         desc = f"This is only from when I joined **{ctx.guild.name}**. Anything before that has not been documented."
#         embed = discord.Embed(description=desc, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
#         embed.add_field(name="Channels:", value=f"```{str(len(ctx.guild.channels))}```", inline=True)
#         embed.add_field(name="Users:", value=f"```{ctx.guild.member_count}```", inline=True)
#         embed.add_field(name="Messages Sent:", value=f"```{msgcount}```", inline=True)
#         # embed.add_field(name=f"In #{ctx.channel.name}:", value = f"```{smsgcfount}```", inline = True)
#         # embed.add_field(name=f"By {ctx.author.name}:", value = f"```{smsgcount}```", inline = True)
#         # embed.add_field(name=f"In #{ctx.channel.name} by {ctx.author.name}:", value=f"```{result3[0]}```", inline = False)
#         embed.add_field(name="Seconds in Voice Channels", value=f"```{vcsecs}```", inline=True)
#         embed.add_field(name=f"Server Creation Date:",
#                         value=f"```{f'{y} ({a} ago)' if lm[0:6] != '1 day,' else 'Today'}```", inline=True)
#         # embed.add_field(name=f"Most active text channel in **{ctx.guild.name}**: ", value = f"```#{topchannel.name} with {smsgcffount} messages.```", inline = False)
#         # figure out most active VC
#         ownerser = self.client.get_user(ctx.guild.owner_id)
#         embed.add_field(name=f"Number of Ghost Pings", value=f"```{ghostcount}```", inline=False)
#         embed.add_field(name="Server Owner:", value=ownerser.mention, inline=False)
#         embed.set_thumbnail(url=ctx.guild.icon_url)
#         embed.set_author(name=f"{ctx.guild.name}'s Statistics", icon_url=ctx.guild.icon_url)
#         embed.set_footer(text=f"Server ID: {ctx.guild.id}")
#         await ctx.send(embed=embed)
#         # add graphs https://www.tutorialspoint.com/graph-plotting-in-python


def setup(client):
    pass
    # client.add_cog(Serverstats(client))

#     # user specific stats next