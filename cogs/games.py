from discord.ext import commands
import discord
import akinator
from akinator.async_aki import Akinator
import asyncio
import random

aki = Akinator()

class Games(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.icon = '🎮'
        self.description = f'Play games with InfiniBot!'

    @commands.command()
    async def akinator(self, ctx, on:str = None):
        if on is None:
            on = True
        elif on.lower() != 'false':
            on = True
        else:
            if ctx.channel.is_nsfw():
                on = False
            else:
                return await ctx.send("You must be in an NSFW channel to access this feature!")

        while True:
            counter = 1
            await ctx.trigger_typing()
            q = await aki.start_game(child_mode=on)
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


    @commands.command()
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


def setup(client):
    client.add_cog(Games(client))