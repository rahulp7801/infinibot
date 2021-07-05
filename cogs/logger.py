import logging
from discord.ext import commands
import datetime

class Logging(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound): return
        if isinstance(error, commands.CommandOnCooldown): return
        if isinstance(error, commands.MissingRequiredArgument): return
        if isinstance(error, commands.MissingPermissions): return
        if isinstance(error, commands.MaxConcurrencyReached): return
        if isinstance(error, commands.MaxConcurrency): return
        errmsg = f"{ctx.command.name} raised {error} in {ctx.guild.name if ctx.guild is not None else 'DM'} ({ctx.guild.id if ctx.guild is not None else str(ctx.author.id) + ' DM'}) on {datetime.datetime.now()}"
        logging.basicConfig(filename='./errors.log')
        logging.error(errmsg)

def setup(client):
    client.add_cog(Logging(client))