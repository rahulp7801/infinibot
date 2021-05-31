import logging
import discord
from discord.ext import commands
import datetime

class Logging(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        errmsg = f"{ctx.command.name} raised {error} in {ctx.guild.name} ({ctx.guild.id}) on {datetime.datetime.now()}"
        logging.basicConfig(filename='./errors.log')
        logging.error(errmsg)



def setup(client):
    client.add_cog(Logging(client))