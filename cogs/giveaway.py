import discord
from discord.ext import commands
import datetime
import random
import asyncio

class Giveaways(commands.Cog):
    def __init__(self, client):
        self.client = client

    @staticmethod
    async def channelperms(channel: discord.TextChannel):
        if channel.is_nsfw():
            return False
        if channel.guild.me.guild_permissions.administrator:
            return True
        y = channel.overwrites_for(channel.guild.default_role)
        if not y.send_messages or not y.read_messages or not y.embed_links:
            pass
        else:
            return True
        for role in channel.guild.me.roles:
            x = channel.overwrites_for(role)
            if not x.send_messages or not x.read_messages or not x.embed_links:
                continue
            else:
                return True

        z = channel.overwrites_for(channel.guild.me)
        if not z.send_messages or not z.read_messages or not z.embed_links:
            return False


    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def gcreate(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            while True:
                await ctx.reply(f"Hey {ctx.author.mention}, thanks for using {self.client.user.name}! Please mention the channel you would like the giveaway to be in.", mention_author = False)

                msg = await self.client.wait_for('message', check=check, timeout = 60)
                try:
                    channel = msg.channel_mentions[0]
                    res = await self.channelperms(channel)
                    if not res:
                        return await ctx.send(f"I don't have permission to `Read Messages`, `Send Messages`, `Embed Links`, `Use External Emoji`, and `Add Reactions` in {channel.mention}.")
                    break
                except IndexError:
                    await ctx.send("You didn't mention a channel! Going back now...", delete_after = 3)
                    await asyncio.sleep(3)
                    continue
            message = await ctx.send(f"Great, we have saved {channel.mention} as our giveaway channel.")
            await asyncio.sleep(2)
            await message.edit(content = 'How long should this giveaway last?\n\nEnter the duration in seconds (`S`).\nIf you would like it in minutes, specify an `M` after the number, ' \
                               'and for days specify a `D` after.\n' \
                               'Example: `5D`')
            msg = await self.client.wait_for('message', check=check, timeout = 60)
            try:
                if msg.content.strip().lower().endswith('d'):
                    arr = (msg.content.strip().lower().partition('d'))
                    sleeps = arr[0]
                    sleeptime = 86400 * int(sleeps)
                    f"{sleeps} day{'' if int(sleeps) == 1 else 's'}"
                    await ctx.send(f"Excellent! This giveaway will last {sleeps} day{'' if int(sleeps) == 1 else 's'}!")
                elif msg.content.strip().lower().endswith('m'):
                    arr = (msg.content.strip().lower().partition('m'))
                    sleeps = arr[0]
                    sleeptime = 60 * int(sleeps)
                    givtime = f"{sleeps} minute{'' if int(sleeps) == 1 else 's'}"
                    await ctx.send(f"Excellent! This giveaway will last {sleeps} minute{'' if int(sleeps) == 1 else 's'}!")
                elif msg.content.strip().lower().endswith('s'):
                    arr = (msg.content.strip().lower().partition('s'))
                    sleeps = arr[0]
                    sleeptime = int(sleeps)
                    givtime = f"{sleeps} second{'' if int(sleeps) == 1 else 's'}"
                    await ctx.send(f"Excellent! This giveaway will last {sleeps} second{'' if int(sleeps) == 1 else 's'}!")
                else:
                    return await ctx.send("Your message did not end with either `S`, `M`, or `D`. Please run the command again and make sure this is fixed.")
            except Exception:
                return await ctx.send("Something went wrong. Contact the developers with error code 405 if this keeps happening. ")
            await ctx.send("How many winners would you like? Choose a number between 1 and 20.")
            msg = await self.client.wait_for('message', check=check, timeout = 60)
            try:
                numwin = int(msg.content.strip())
            except Exception as e:
                print(e)
                return await ctx.send("Something went wrong, did you mention a number? Please run the command again to create another giveaway.")

            await ctx.send(f"Excellent, we will have {numwin} winner{'' if numwin == 1 else 's'}!\n\nWhat do you want the prize to be? Keep it under 2000 characters, and this will start the giveaway.")
            msg = await self.client.wait_for('message', check=check, timeout = 300)
            await ctx.send(f"Great. The giveaway for `{msg.content.strip()}` is starting in {channel.mention}!")
            desc = f"{numwin} winner{'' if numwin == 1 else 's'}\n" \
                   f"Duration: {givtime}\n" \
                   f"Hosted by: {ctx.author.mention}"
            embed = discord.Embed(title = msg.content.strip(), description = desc, color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
            messg = await channel.send(embed=embed)
            await messg.add_reaction('🎉')
            await asyncio.sleep(sleeptime)
            masg = await channel.fetch_message(messg.id)
            users = await masg.reactions[0].users().flatten()
            users.pop(users.index(self.client.user))
            if len(users) == 0:
                return await messg.channel.send("No one participated in the giveaway :((")
            winarr = []
            for i in range(numwin):
                winarr.append(random.choice(users))
            uslist = []
            for i in winarr:
                uslist.append(i.mention)
            winstr = ", ".join(uslist)
            desc = f"Winner{'' if len(winarr) == 1 else 's'}: {winstr}"
            embed = discord.Embed(title = msg.content.strip(), description = desc, color = discord.Color.green(), timestamp = datetime.datetime.utcnow())
            await messg.edit(embed=embed)
            await messg.channel.send(f"🎉 Congratulations {winstr}, you {'all ' if len(winstr) == 1 else ''}won the **{msg.content.strip()}**!\n"
                           f"{messg.jump_url}")

        except asyncio.TimeoutError:
            return await ctx.send("Giveaway setup has timed out and setup has been cancelled.")

def setup(client):
    client.add_cog(Giveaways(client))
