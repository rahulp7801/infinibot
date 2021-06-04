from discord.ext import commands

class Automod(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.icon = '<:ban:849687326736515092>'
        self.description = 'Auto Moderation using algorithms!'

def setup(client):
    client.add_cog(Automod(client))