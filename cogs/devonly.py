import discord
from discord.ext import commands
import datetime
import os


async def is_dev(ctx):
    return ctx.author.id in [645388150524608523, 759245009693704213]

class Developers(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.icon = '👨🏽‍💻'

    @commands.group(invoke_without_command = True)
    @commands.check(is_dev)
    async def sudo(self, ctx):
        return await ctx.author.send("Available params are `--shutdown` and `--restart`.")

    @sudo.command(name = '--restart')
    @commands.check(is_dev)
    async def _restart(self, ctx, reason = "No reason given"):
        channel = self.client.get_channel(id=844611738133463121)
        desc = f"Attempting restart..."
        embed = discord.Embed(title="Bot restarting --force restart activated", description=desc,
                              color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Time", value=f"```{datetime.datetime.utcnow().strftime('%D')}```")
        embed.add_field(name='Server', value=f"```{ctx.guild.name}```")
        embed.add_field(name='Server ID', value=f"```{ctx.guild.id}```")
        embed.add_field(name='Reason', value=f"```{reason.strip()}```", inline=False)
        await ctx.message.add_reaction('✅')
        await channel.send(embed=embed)
        try:
            await self.client.close()
        except Exception as e:
            print(e)
            await ctx.author.send("Something went wrong while attempting a restart.")
            pass
        finally:
            os.system('python bot.py')


    @sudo.command(name = '--shutdown')
    @commands.check(is_dev)
    async def _shutdown(self, ctx, reason = "No reason given"):
        channel = self.client.get_channel(id=844611738133463121)
        desc = f"Attempting shutdown..."
        embed = discord.Embed(title = "Bot shutting down --force shutdown activated", description = desc, color = discord.Color.red(), timestamp = datetime.datetime.utcnow())
        embed.add_field(name="Time", value = f"```{datetime.datetime.utcnow().strftime('%D')}```")
        embed.add_field(name='Server', value = f"```{ctx.guild.name}```")
        embed.add_field(name='Server ID', value = f"```{ctx.guild.id}```")
        embed.add_field(name='Reason', value = f"```{reason.strip()}```", inline = False)
        await channel.send(embed=embed)
        await ctx.message.add_reaction('✅')
        try:
            await self.client.close()
            print('Client closed')
        except Exception as e:
            print(e)
            await ctx.author.send("Something went wrong while shutting down.")

    @commands.command()
    @commands.check(is_dev)
    async def servercount(self, ctx):
        await ctx.send(f"I'm in {len(self.client.guilds)} servers!")

    @commands.command()
    @commands.check(is_dev)
    async def uniquemembers(self, ctx):
        await ctx.send(len(set(self.client.users)))

    @commands.command()
    @commands.check(is_dev)
    async def broadcast(self, ctx):
        try:
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            await ctx.send(f"Type message now....")
            message = await self.client.wait_for('message', check=check)
            for k in self.client.guilds:
                for channel in k.text_channels:
                    if channel.permissions_for(k.me).send_messages:
                        await channel.send(message.content)
                        break
            await message.add_reaction('✅')
        except Exception as e:
            print(e)

def setup(client):
    client.add_cog(Developers(client))
