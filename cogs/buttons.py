from discord.ext import commands
import discord
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

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


def setup(client):
    client.add_cog(Buttons(client))