import discord
from discord.ext import commands
import datetime
import random

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


def setup(client):
    client.add_cog(Misc(client))
