from discord.ext import commands
import discord
import akinator
from akinator.async_aki import Akinator
import asyncio
import random
from modules import exceptions, utils
import time
import os

aki = Akinator()

class Games(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.icon = '🎮'
        self.description = f'Play games with InfiniBot!'

    @commands.command(name="Play an akinator game!")
    async def akinator(self, ctx, childmode:str = None):
        if childmode is None:
            childmode = True
        elif childmode.lower() != 'false':
            childmode = True
        else:
            if ctx.channel.is_nsfw():
                childmode = False
            else:
                return await ctx.send("You must be in an NSFW channel to access this feature!")

        while True:
            counter = 1
            await ctx.trigger_typing()
            q = await aki.start_game(child_mode=childmode)
            desc = f"**{q}**\n" \
                   f"[yes **(y)**/ no **(n)**/ probably **(p)**/ probably not **(pn)**/ back **(b)**]"
            embed = discord.Embed(description=desc, color=discord.Color.gold())
            embed.set_author(name=f"Question {counter}")
            await ctx.send(embed=embed)
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                while counter < 80:
                    while True:
                        a = await self.client.wait_for('message', check=check, timeout = 120)
                        if a.content.lower().strip() == 'cancel':
                            return await ctx.send("This game has been cancelled, see you another time!")
                        if a.content.lower().strip() == 'b':
                            try:
                                counter -= 1
                                q = await aki.back()
                                await ctx.send(f"Going back to question {counter}...")
                                break
                            except akinator.CantGoBackAnyFurther:
                                await ctx.send("I cannot go back any further!")
                        else:
                            try:
                                q = await aki.answer(a.content.lower().strip())
                                counter += 1
                                break
                            except akinator.InvalidAnswerError:
                                continue
                    await ctx.trigger_typing()
                    if aki.progression <= 80:
                        desc = f"**{q}**\n" \
                               f"[yes **(y)**/ no **(n)**/ probably **(p)**/ probably not **(pn)**/ back **(b)**]"
                        embed = discord.Embed(description=desc, color=discord.Color.gold())
                        embed.set_author(name=f"Question {counter}")
                        await a.reply(embed=embed, mention_author=False)
                    else:
                        await aki.win()
                        print(aki.first_guess)
                        desc = f"**{aki.first_guess['name']}**\n" \
                               f"{aki.first_guess['description']}\n" \
                               f"Ranking as **#{aki.first_guess['ranking']}**\n\n" \
                               f"[yes **(y)**/ no **(n)**/ back **(b)**]"
                        embed = discord.Embed(description=desc, color=discord.Color.green())
                        embed.set_author(name="Is this your character?")
                        embed.set_image(url=aki.first_guess['absolute_picture_path'])
                        await ctx.send(embed=embed)
                        while True:
                            msg = await self.client.wait_for('message', check=check, timeout = 120)
                            if msg.content.lower().strip() == 'y':
                                embed = discord.Embed(title='Thanks for playing!', description="Run the command to play again!", color = discord.Color.gold())
                                await ctx.send(embed=embed)
                                return
                            elif msg.content.lower().strip() == 'n':
                                    try:
                                        q = await aki.answer(a.content.lower().strip())
                                        counter += 1
                                        desc = f"**{q}**\n" \
                                               f"[yes **(y)**/ no **(n)**/ probably **(p)**/ probably not **(pn)**/ back **(b)**]"
                                        embed = discord.Embed(description=desc, color=discord.Color.gold())
                                        embed.set_author(name=f"Question {counter}")
                                        await a.reply(embed=embed, mention_author=False)
                                        break
                                    except akinator.InvalidAnswerError: continue
                            elif msg.content.lower().strip() == 'b':
                                f"Going back to question {counter - 1}..."
                                try:
                                    counter -= 1
                                    q = await aki.back()
                                    await ctx.send(f"Going back to question {counter}...")
                                    desc = f"**{q}**\n" \
                                           f"[yes **(y)**/ no **(n)**/ probably **(p)**/ probably not **(pn)**/ back **(b)**]"
                                    embed = discord.Embed(description=desc, color=discord.Color.gold())
                                    embed.set_author(name=f"Question {counter}")
                                    await a.reply(embed=embed, mention_author=False)
                                    break
                                except akinator.CantGoBackAnyFurther:
                                    await ctx.send("I cannot go back any further!")


            except asyncio.TimeoutError:
                return await ctx.reply("Game over due to inactivity.", mention_author = False)


    @commands.command(name="Unscramble the word as quickly as possible!")
    async def jumble(self, ctx):
        wordlist = [
            'insane',
            'domination',
            'greatest',
            'basketball',
            'football',
            'amazing',
            'phenomenal',
            'extravagant',
            'slam dunk',
            'pogchamp',
            'discord',
            'google',
            'apple',
            'cheetah',
            'lightning',
            'robot',
            'artificial intelligence',
            'New York City',
            'United States of America',
            'Coronavirus',
            'lockdown',
            'superior',
            'California',
            'Justin Bieber'
        ]
        x = random.choice(wordlist)
        newarr = []
        for i in x:
            newarr.append(i)
        random.shuffle(newarr)
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        await ctx.reply(f"Unscramble this word within **20 seconds**: `{''.join(newarr)}`", mention_author = False)
        try:
            msg = await self.client.wait_for('message', check=check, timeout=20.0)
            if msg.content.strip().lower() == x.lower():
                await msg.reply(f"Congratulations! The word was `{x}`!", mention_author = False)
            else:
                await msg.reply(f"Oof, your answer is incorrect! The correct answer was `{x}`!")
        except asyncio.TimeoutError:
            await ctx.send("You took too long!")

    @commands.group(aliases = ['cardsagainsthumanity'])
    async def cah(self, ctx):
        await ctx.send_help(ctx)

    @cah.command()
    async def start(self, ctx):
        await ctx.send(f'{ctx.author.mention}, by playing this game you acknowledge that **there may be NSFW content** (no images). Do you wish to proceed? Respond with `y` or `n`.')
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            message = await self.client.wait_for('message', check=check, timeout=30)
            if message.content.lower().strip() in ['y', 'yes', 'yessir']:
                answerdict = {}
                with open("./Discord Bot/CAH cards/White Cards/whitecards.txt", 'r') as myfile:
                    data = myfile.read()
                    embed = discord.Embed(title=f"{ctx.author.display_name} is starting a Cards Against Humanity game!",
                                               description=f"Type `join` to join in the next 120 seconds.\n\n {ctx.author.mention}, type `start` to begin once everyone has joined.",
                                               color=discord.Color.blue())
                    await ctx.send(embed=embed)
                    embed = utils.add_member_cah(ctx.author)
                    await ctx.send(embed=embed)
                    x = time.time() + 120
                    arr = [ctx.author.id]
                    while time.time() < x:
                        message = await self.client.wait_for('message', check = lambda m: m.channel == ctx.channel and not m.author.bot, timeout=120)
                        if message.content.lower().strip() == 'join':
                            if len(arr) > 10:
                                await ctx.send("Sorry pal, it looks like this game is full right now!")
                                break
                            if arr.count(message.author.id) != 0:
                                msg = await ctx.send(f'{message.author.mention}, you are already joined.')
                                await asyncio.sleep(2)
                                try:
                                    await msg.delete()
                                except discord.Forbidden:
                                    pass
                                finally:
                                    continue
                            try:
                                await message.delete()
                            except discord.Forbidden:
                                pass
                            finally:
                                embed = utils.add_member_cah(message.author)
                                await ctx.send(embed=embed)
                                arr.append(message.author.id)
                                answerdict.__setitem__(id, message.author.id)
                                try:
                                    embed = utils.priv_cah_msg(ctx.channel)
                                    await message.author.send(embed=embed)
                                except discord.Forbidden:
                                    arr.pop(arr.index(message.author.id))
                                    await message.reply(f"{message.author.mention}, your DMs are off. Please enable them and try joining the game again.")
                                continue
                        if message.content.lower().strip() == 'start' and message.author.id == ctx.author.id:
                            break #actually start the game
                        else:
                            continue

                    if len(arr) <= 1:
                        return await ctx.send(f"It looks like only {len(arr)} {'people' if len(arr) == 2 else 'person'} joined, so this game has automatically been ended.")

                    mentionstr = []
                    for i in arr:
                        user = self.client.get_user(i)
                        mentionstr.append(user.mention)

                    bgnembed = discord.Embed(title="**Time\'s up!**", description= f'{", ".join(mentionstr)} joined the game.',
                                             color=discord.Color.blue())
                    await ctx.send(embed=bgnembed)

                    await asyncio.sleep(1)
                    await ctx.send("The round will begin soon!")
                    currentind = 0
                    embed , tzar = utils.current_tzar(currentind, mentionstr)
                    await ctx.send(embed=embed)
                    bchoices = []
                    for file1 in os.listdir('./Discord Bot/CAH cards/Black Cards'):
                        if file1.endswith(".png"):
                            bchoices.append(file1)
                        if len(bchoices) == 0: #should NEVER happen
                            msg = 'I\'m not configured for Cards Against Humanity yet...'
                            await ctx.send(msg)
                            return
                    randnum1 = random.randint(0, (len(bchoices) - 1))
                    randLib1 = bchoices[randnum1]
                gameembed = discord.Embed(title=f"*This round\'s black card*", color=discord.Color.blue())
                gamefile = discord.File(
                    f"./Discord Bot/CAH Cards/Black Cards/{randLib1}",
                    filename="image.png")
                gameembed.set_image(url="attachment://image.png")
                gameembed.set_footer(text="InfiniBot | Game Mode")
                await ctx.send(file=gamefile, embed=gameembed)
                newL = []
                arr1 = []
                for k in mentionstr:
                    newL.append(k + " ❌ Not submitted.")
                    arr1.append((k, False))
                lDesc = " \n".join(newL)
                substat = discord.Embed(title="*Submission Status*", description=lDesc, color=discord.Color.red())
                await ctx.send(embed=substat)
                with open('./Discord Bot/CAH Cards/White Cards/whitecards.txt',
                          'r') as myfile2:
                    data = myfile2.read()
                    d2 = data.split(". ")
                allsubmit = False
                while not allsubmit:
                    for i in arr:
                        user = self.client.get_user(int(i))
                        await user.send("View your hand and select a card.")
                        listsk = []
                        count = 0
                        for k in range(0, 10):
                            count += 1
                            choice = str(random.choice(d2))
                            listsk.append("**" + str(count) + "**: " + str(choice) + ".")
                            answerdict.__setitem__(user.id, {"count": count, "option":str(choice)})
                            print(answerdict)

            else:
                return await ctx.send("I'll take that as a no, see you later!")
        except asyncio.TimeoutError:
            return await ctx.send("You took too long.")
        except Exception as e:
            print(e)

def setup(client):
    client.add_cog(Games(client))