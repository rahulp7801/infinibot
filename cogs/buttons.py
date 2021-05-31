from discord.ext import commands
import discord
import datetime
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import asyncio

class Buttons(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        DiscordComponents(self.client, change_discord_methods=True)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return

        if '64gb ram' in msg.content.lower():
            await msg.channel.send(
                "That's insane my guy!",
                components=[
                    Button(style=ButtonStyle.blue, label="Blue"),
                    Button(style=ButtonStyle.red, label="Red"),
                    Button(style=ButtonStyle.URL, label="url", url="https://example.org"),
                ],
            )

            while True:
                res = await self.client.wait_for("button_click")
                if res.channel == msg.channel:
                    await res.respond(
                        type=InteractionType.ChannelMessageWithSource,
                        content=f'{res.component.label} clicked'
                    )
                    break
                else:
                    continue

    @commands.command(aliases=['terms', 'privacypolicy', 'termsofservice'])
    @commands.cooldown(5, 120, commands.BucketType.user)
    async def tos(self, ctx):
        await ctx.reply(
            f"Thank you for using {self.client.user.name}!",
            components=[
                Button(style=ButtonStyle.URL, label="Click Here!", url="https://docs.google.com/document/d/1XHOKPspuyqUIS9a0d0BMcO5oKXT5Xe5KdN_olG9sGFc/edit?usp=sharing"),
            ],
            mention_author = False
        )

    @commands.command()
    async def poll(self, ctx, title, *args):
        if len(args) >= 5:
            return await ctx.send(f"You cannot have more than 5 options! You have specified {len(args)} options.")
        descarr = []
        components = []
        for i in args:
            if args.count(i) > 1:
                return await ctx.send(f"It looks like you mentioned {args.count(i)} of the same arguments!")
            descarr.append(f'{i.strip()}: 0')
            components.append(Button(style=ButtonStyle.blue, label = i.strip()))
        r = '\n'.join(descarr)
        embed = discord.Embed(title = title.strip(), description = f"```{r}```", color = discord.Color.green())
        embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        msg = await ctx.send(
            embed = embed,
            components=[components]
        )
        arr = {}
        while True:
            res = await self.client.wait_for("button_click")
            if res.channel == ctx.channel:
                pollmsg = await ctx.fetch_message(msg.id)
                print(pollmsg)
                if pollmsg.author != ctx.guild.me:
                    return
                embed = pollmsg.embeds[0]
                ldesc = embed.description.strip('`')
                realdesc = ldesc.split('\n')
                reslen = len(res.component.label)
                for i in realdesc:
                    if i[0:reslen] == (str(res.component.label)):
                        try:
                            ogchoice = arr[res.author.id]
                            oglen = len(ogchoice)
                            for k in realdesc:
                                if k[0:oglen] == ogchoice:
                                    nums = int(k[-1])
                                    nums -= 1
                                    desc = f"{k[:-2]} {nums}"
                                    tst = realdesc.index(k)
                                    realdesc[tst] = desc
                                    break
                                else:
                                    continue
                            try:
                                arr.update({res.author.id: i[:-2]})
                                nums = int(i[-1])
                                nums += 1
                                desc = f"{i[:-2]} {nums}"
                                tst = realdesc.index(i)
                                realdesc[tst] = desc
                                desc = "\n".join(realdesc)
                                embed = discord.Embed(title=title.strip(), description=f"```{desc}```",
                                                      color=discord.Color.green())
                                embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}",
                                                 icon_url=ctx.author.avatar_url)
                                await msg.edit(embed=embed)
                                await res.respond(
                                    type=InteractionType.ChannelMessageWithSource,
                                    content=f'You changed your mind and chose `{res.component.label}`!'
                                )
                                break
                            except ValueError:
                                await res.respond(type=InteractionType.ChannelMessageWithSource,
                                    content=f'You already chose `{res.component.label}`!')
                                break
                        except KeyError:
                            arr.__setitem__(res.author.id, i[:-2])
                            nums = int(i[-1])
                            nums += 1
                            desc = f"{i[:-2]} {nums}"
                            tst = realdesc.index(i)
                            realdesc[tst] = desc
                            desc = "\n".join(realdesc)
                            embed = discord.Embed(title=title.strip(), description=f"```{desc}```",
                                                  color=discord.Color.green())
                            embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}",
                                             icon_url=ctx.author.avatar_url)
                            await msg.edit(embed=embed)
                            await res.respond(
                                type=InteractionType.ChannelMessageWithSource,
                                content=f'You chose `{res.component.label}`!'
                            )
                            break
                    else:
                        continue

            else:
                continue

    @commands.command()
    async def calculate(self, ctx):
        embed = discord.Embed(title=f"{ctx.author.name}'s calculator", description='```0```', timestamp = datetime.datetime.utcnow())
        components = [[
            Button(style=ButtonStyle.gray, label="1"),
            Button(style=ButtonStyle.gray, label="2"),
            Button(style=ButtonStyle.gray, label="3"),
            Button(style=ButtonStyle.gray, label="x"),
            Button(style=ButtonStyle.gray, label="Exit")
        ],
        [
            Button(style=ButtonStyle.gray, label="4"),
            Button(style=ButtonStyle.gray, label="5"),
            Button(style=ButtonStyle.gray, label="6"),
            Button(style=ButtonStyle.gray, label="÷"),
            Button(style=ButtonStyle.gray, label="←")
        ],
        [
            Button(style=ButtonStyle.gray, label="7"),
            Button(style=ButtonStyle.gray, label="8"),
            Button(style=ButtonStyle.gray, label="9"),
            Button(style=ButtonStyle.gray, label="+"),
            Button(style=ButtonStyle.gray, label="Clear")
        ],
        [
            Button(style=ButtonStyle.gray, label="00"),
            Button(style=ButtonStyle.gray, label="0"),
            Button(style=ButtonStyle.gray, label="."),
            Button(style=ButtonStyle.gray, label="-"),
            Button(style=ButtonStyle.gray, label="=")
        ]]

        msg = await ctx.send(embed=embed, components = components)
        arr = []
        while True:
            try:
                res = await self.client.wait_for("button_click", timeout = 120)
                if res.channel == ctx.channel and res.author == ctx.author:
                    if res.component.label == 'Exit':
                        await res.respond(
                            type=InteractionType.DeferredUpdateMessage,
                            content=f'You chose `{res.component.label}`!'
                        )
                        return
                    if res.component.label.isdigit():
                        try:
                            if str(arr[0]) == '0':
                                arr[0] = str(res.component.label)
                            else:
                                arr.append(str(res.component.label))
                        except IndexError:
                            arr.append(str(res.component.label))
                        finally:
                            desc = ''.join(arr)
                            embed = discord.Embed(title=f"{ctx.author.name}'s calculator", description=f"```{desc}```")
                            await msg.edit(embed=embed)
                            await res.respond(
                                type=InteractionType.DeferredUpdateMessage,
                                content=f'You chose `{res.component.label}`!'
                            )
                    else:
                        if res.component.label == '←':
                            try:
                                arr.pop(-1)
                            except IndexError:
                                pass
                            if len(arr) == 0:
                                arr.append('0')
                            desc = ''.join(arr)
                            embed = discord.Embed(title = f"{ctx.author.name}'s calculator", description=f"```{desc}```")
                            await msg.edit(embed=embed)
                            await res.respond(
                                type=InteractionType.DeferredUpdateMessage,
                                content=f'You chose `{res.component.label}`!'
                            )
                        elif res.component.label == 'x':
                            arr.append('*')
                            desc = ''.join(arr)
                            embed = discord.Embed(title=f"{ctx.author.name}'s calculator", description=f"```{desc}```")
                            await msg.edit(embed=embed)
                            await res.respond(
                                type=InteractionType.DeferredUpdateMessage,
                                content=f'You chose `{res.component.label}`!'
                            )
                        elif res.component.label == '+':
                            arr.append('+')
                            desc = ''.join(arr)
                            embed = discord.Embed(title=f"{ctx.author.name}'s calculator", description=f"```{desc}```")
                            await msg.edit(embed=embed)
                            await res.respond(
                                type=InteractionType.DeferredUpdateMessage,
                                content=f'You chose `{res.component.label}`!'
                            )
                        elif res.component.label == '÷':
                            arr.append('/')
                            desc = ''.join(arr)
                            embed = discord.Embed(title=f"{ctx.author.name}'s calculator", description=f"```{desc}```")
                            await msg.edit(embed=embed)
                            await res.respond(
                                type=InteractionType.DeferredUpdateMessage,
                                content=f'You chose `{res.component.label}`!'
                            )
                        elif res.component.label == '-':
                            arr.append('-')
                            desc = ''.join(arr)
                            embed = discord.Embed(title=f"{ctx.author.name}'s calculator", description=f"```{desc}```")
                            await msg.edit(embed=embed)
                            await res.respond(
                                type=InteractionType.DeferredUpdateMessage,
                                content=f'You chose `{res.component.label}`!'
                            )
                        elif res.component.label == '.':
                            arr.append('.')
                            desc = ''.join(arr)
                            embed = discord.Embed(title=f"{ctx.author.name}'s calculator", description=f"```{desc}```")
                            await msg.edit(embed=embed)
                            await res.respond(
                                type=InteractionType.DeferredUpdateMessage,
                                content=f'You chose `{res.component.label}`!'
                            )
                        elif res.component.label == 'Clear':
                            arr.clear()
                            arr.append('0')
                            embed = discord.Embed(title=f"{ctx.author.name}'s calculator", description=f"```0```")
                            await msg.edit(embed=embed)
                            await res.respond(
                                type=InteractionType.DeferredUpdateMessage,
                                content=f'You chose `{res.component.label}`!'
                            )
                        else:
                            try:
                                expression = ''.join(arr)
                                ans = (eval(expression))
                                arr.clear()
                                arr.append(str(ans))
                                desc = ''.join(arr)
                                embed = discord.Embed(title=f"{ctx.author.name}'s calculator", description=f"```{desc}```")
                                await msg.edit(embed=embed)
                                await res.respond(
                                    type=InteractionType.DeferredUpdateMessage,
                                    content=f'You chose `{res.component.label}`!'
                                )
                            except Exception as e:
                                if str(e) == 'invalid syntax (<string>, line 1)':
                                    arr.clear()
                                    desc = "Invalid Arguments - Try Again"
                                    embed = discord.Embed(title=f"{ctx.author.name}'s calculator", description=f"```{desc}```")
                                    await msg.edit(embed=embed)
                else:
                    continue

            except asyncio.TimeoutError:
                desc = "```Session timed out.```"
                embed = discord.Embed(title=f"{ctx.author.name}'s calculator", description=desc, timestamp = datetime.datetime.utcnow())
                await msg.edit(embed=embed)
                return
            except KeyError:
                pass







def setup(client):
    client.add_cog(Buttons(client))