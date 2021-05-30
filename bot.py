from discord.ext import commands
import discord
import os
import asyncio
import datetime
from discord_slash import SlashCommand
from discord_components import DiscordComponents

client = commands.Bot(command_prefix='.', intents = discord.Intents.all(), allowed_mentions=discord.AllowedMentions.none(), case_insenstive = True)
slash = SlashCommand(client, sync_commands = False)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")
        print(f"{str(filename[:-3]).capitalize()} {'are' if filename[:-3].endswith('s') else 'is'} loaded.")

@client.event
async def on_ready():
    print(f"{client.user.name} is ready, logged on at {datetime.datetime.utcnow()}.")
    for i in client.guilds:
        print(i.name + "->" + str(i.owner_id))
    DiscordComponents(client, change_discord_methods=True)
    while True:
        await asyncio.sleep(10)
        with open('spamdetect.txt', 'r+') as f:
            f.truncate(0)

@client.command()
async def hi(ctx):
    return await ctx.send('hey')

with open('token.txt', 'r') as f:
    token = f.read()

client.run(token)