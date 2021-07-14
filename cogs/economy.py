import discord
from discord.ext import commands
import asyncio
from modules.economy.classes import EconomyUser, Watch
from pymongo import MongoClient
import random
import datetime
from random import choice

_registered_users = []
initialbal = 100
storerate = 0.75

with open('mongourl.txt', 'r') as file:
    url = file.read()
mongo_url = url.strip()
cluster = MongoClient(mongo_url)
db = cluster['ECONOMY']
col = db['users']


class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        for member in list(set(self.client.users)):
            if (not member.bot) and (await self.exists(member) == False):
                newuser = EconomyUser(member, initialbal, member.id, 100, 100)
                guild = choice(member.mutual_guilds)
                bal, wallet, bank= await newuser.get_raw_balance(guild)
                print(bal, wallet, bank)
                newuser._set_cache_balance(wallet, bank)
                _registered_users.append(newuser)
        print(f"{len(_registered_users)} found, Wrote To cache...")


    @staticmethod
    async def exists(user):
        return True if _registered_users.count(user.id) != 0 else False

    @staticmethod
    async def get_user(id) -> EconomyUser:
        user = (list(filter(lambda i: i.id == id, _registered_users)))
        return user[0]

    @commands.command(aliases=['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        if member is None:
            user = ctx.author
        else:
            user = member
        econuser = await self.get_user(user.id)
        embed = discord.Embed(title=f"{user.name}'s balance",
                              description=f'**Wallet**: {econuser.wallet} coins \n**Bank**: {econuser.bank} coins',
                              color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f'😏')
        await ctx.send(embed=embed)

    @commands.command(aliases=['with'])
    async def withdraw(self, ctx, amount=None):
        if amount is None:
            await ctx.reply("Please specify the amoun\'t you\'d like to withdraw.", mention_author=False)
            return

        econuser = await self.get_user(ctx.author.id)
        bal = econuser.get_bank_wallet()
        if amount.lower() == 'all':
            amount = bal[1]

        amount = int(amount)
        if amount == 0:
            await ctx.reply("There is nothing in your bank to withdraw.", mention_author=False)
            return
        if amount > bal[1]:
            await ctx.reply(f"You don\'t have {amount} coins.", mention_author=False)
            return
        if amount < 0:
            await ctx.reply(f'{amount} is not a positive number.')
            return

        await econuser.updatebank(-1 * amount, ctx.guild)
        await econuser.updatewallet(amount, ctx.guild)
        await ctx.reply(f'You withdrew {amount} coins!')

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, amount=None):
        if amount is None:
            await ctx.reply("Please specify the amoun\'t you\'d like to deposit.", mention_author=False)
            return

        econuser = await self.get_user(ctx.author.id)
        bal = econuser.get_bank_wallet()
        if amount.lower() == 'all':
            amount = bal[0]

        amount = int(amount)
        if amount == 0:
            await ctx.reply("There is nothing in your wallet.", mention_author=False)
            return
        if amount > bal[0]:
            await ctx.reply(f"You don\'t have {amount} coins.", mention_author=False)
            return
        if amount < 0:
            await ctx.reply(f'{amount} is not a positive number.')
            return

        await econuser.updatebank(amount, ctx.guild)
        await econuser.updatewallet(-1 * amount, ctx.guild)
        await ctx.reply(f'You deposited **{amount}** coins!')

    @commands.guild_only()
    @commands.command(aliases=['give'])
    async def send(self, ctx, member: discord.Member = None, amount=None):
        if member is None:
            await ctx.reply("Please specify who you would like to send coins to!", mention_author=False)
            return

        if amount is None:
            await ctx.reply("Please specify the amoun\'t you\'d like to send.", mention_author=False)
            return

        authorbal = await self.get_user(ctx.author.id)
        givebal = await self.get_user(member.id)
        bal = authorbal.get_bank_wallet()
        if amount.lower() == 'all':
            amount = bal[0]

        amount = int(amount)
        if amount == 0:
            await ctx.reply("You don\'t have any coins in your wallet.", mention_author=False)
            return

        if amount > bal[0]:
            await ctx.reply(f"You don\'t have **{amount}** coins.", mention_author=False)
            return
        if amount < 0:
            await ctx.reply(f'**{amount}** is not a positive number.')
            return

        await authorbal.updatewallet(-1 * amount, ctx.guild)
        await givebal.updatewallet(amount, ctx.guild)
        await ctx.reply(f'Success! You gave `{amount}` coins to **{member.name}**!!', mention_author = False)

    @commands.command(aliases=['steal'])
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.guild_only()
    async def rob(self, ctx, member: discord.Member = None):
        if member == None:
            await ctx.reply("Please specify who you would like to rob from!", mention_author=False)
            return

        authorbal = await self.get_user(ctx.author.id)
        memberbal = await self.get_user(member.id)
        bal1 = authorbal.get_bank_wallet()
        bal = memberbal.get_bank_wallet()

        if bal[0] < 100:
            await ctx.reply(f"**{member.name}** doesn\'t have enough coins, it\'s not worth it.", mention_author=False)
            return

        if bal1[0] < 5000:
            await ctx.reply(
                f"{ctx.author.mention}, you don\'t have enough money in your wallet to rob people. You need 5000 coins.",
                mention_author=False)
            return

        earnings = random.randrange(0, bal[0])
        if earnings > 0:
            randd = random.randint(1, 4)
            if randd == 1:
                if earnings > 20000:
                    earnings = 15882
                else:
                    if earnings < 500:
                        earnings = 1000
                    else:
                        earnings = earnings
            else:
                earnings = 0

        if earnings == 0:
            await authorbal.updatebank(-5000, ctx.guild)
            await memberbal.updatebank(5000, ctx.guild)
            pfp = ctx.author.avatar_url
            author = ctx.author.name
            embd = f"Status: FAILED! You\'ve been caught in the act robbing from **{member.name}**!! You\'ve given them 5,000 coins from your wallet to their bank."
            embed = discord.Embed(description=embd, color=discord.Color.red())
            embed.set_author(name=f'{author}\'s robbery of {member.name}', icon_url=pfp)
            await ctx.send(embed=embed)
            return

        await authorbal.updatebank(earnings, ctx.guild)
        await memberbal.updatebank(earnings * -1, ctx.guild)
        pfp = ctx.author.avatar_url
        author = ctx.author.name
        embd = f"Status: Success! You\'ve robbed {earnings} coins from **{member.name}**."
        embed = discord.Embed(description=embd, color=discord.Color.green())
        embed.set_author(name=f'{author}\'s robbery of {member.name}', icon_url=pfp)
        await ctx.send(embed=embed)

    @commands.command(aliases=['slot', 'slotmachine'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slots(self, ctx, amount=None):
        if amount is None:
            await ctx.reply("Please specify the amount you\'d like to gamble.", mention_author=False)
            return

        econuser = await self.get_user(ctx.author.id)
        bal = econuser.get_bank_wallet()

        if amount.lower() == 'all':
            amount = bal[0]

        amount = int(amount)
        if amount < 0:
            await ctx.reply(
                f'**{ctx.author.name}**, {amount} is not a positive number. What are they teaching you at school smh.',
                mention_author=False)
            return
        if amount < 500:
            await ctx.reply(f"**{ctx.author.name}**, don\'t be a wimp. Please gamble 500 coins or more.",
                            mention_author=False)
            return
        if amount > bal[0]:
            await ctx.reply(f"You don\'t have {amount} coins.", mention_author=False)
            return

        final = []
        for i in range(3):
            a = random.choice(
                ["A", "B", "C", "D", "E", "F", "G", "H", "I"])
            final.append(a)

        x = " ".join(final)
        await ctx.send(f'{ctx.author.name}, your slot machine is spinning, be patient...')
        await asyncio.sleep(2)
        print(x)
        pfp = ctx.author.avatar_url
        if final[0] == final[1] == final[2]:
            await asyncio.sleep(1)
            await econuser.updatebank(int(1000 * amount), ctx.guild)
            embd = ">**" + x + f"**< \n\n You won **{int(amount * 1000)}** coins! \nYou now have **{bal[0] + int(amount * 1000)}** coins."
            embed = discord.Embed(description=embd, color=discord.Color.green())
            embed.set_author(name=f'{ctx.author.name}\'s slot machine', icon_url=pfp)
            await ctx.send(embed=embed)
            return
        if final[0] == final[1] or final[0] == final[2] or final[1] == final[2]:
            await asyncio.sleep(1)
            await econuser.updatebank(int(100 * amount), ctx.guild)
            embd = ">**" + x + f"**< \n\n You won **{int(amount * 100)}** coins! \nYou now have **{bal[0] + int(amount * 100)}** coins."
            embed = discord.Embed(description=embd, color=discord.Color.green())
            embed.set_author(name=f'{ctx.author.name}\'s slot machine', icon_url=pfp)
            await ctx.send(embed=embed)
            return
        else:
            await econuser.updatebank(int(-1 * amount), ctx.guild)
            await asyncio.sleep(1)
            embd = ">**" + x + f"**< \n\n You lost **{int(amount)}** coins. \nYou now have **{bal[0] - int(amount * 1)}** coins."
            embed = discord.Embed(description=embd, color=discord.Color.red())
            embed.set_author(name=f'{ctx.author.name}\'s slot machine', icon_url=pfp)
            await ctx.send(embed=embed)

    @commands.command()
    async def econtest(self, ctx):
        econ = Watch()
        embed = econ.about()
        await ctx.send(embed=embed, file=econ.file)

def setup(client):
    client.add_cog(Economy(client))