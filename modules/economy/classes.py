from pymongo import MongoClient
import discord
import datetime

from ..exceptions import *

with open('mongourl.txt', 'r') as file:
    url = file.read()

mongo_url = url.strip()
cluster = MongoClient(mongo_url)
db = cluster['ECONOMY']
col = db['users']

mainshop = [
    {"name": "Watch", "price": 100, "description": "Time"},
    {"name": "Laptop", "price": 1000, "description": "Work"},
    {"name": "PC", "price": 10000, "description": "Gaming"}
]

class EconomyUser:
    def __init__(self, user, balance, id, bank, wallet):
        self.user = user
        self.balance = balance
        self.id = id
        self.bank = bank
        self.wallet = wallet
        self.boosts = []

    def __str__(self):
        return f"{self.user.name} has {self.balance} credits"

    def __repr__(self):
        return f"EconomyUser(user={self.user}, balance={self.balance}, id={self.id})"

    @staticmethod
    def guild_lb(guild):
        if col.count_documents({"gid":guild.id}) == 0:
            return None
        res = col.find({"gid":guild.id}).sort("balance", -1).limit(10)
        lb = []
        for i in res:
            lb.append(i["username"])

        return lb

    async def add_user(self, guild):
        payload = {
            '_id':self.user.id,
            'gid': guild.id,
            'seton': datetime.datetime.utcnow(),
            'username': f"{self.user.name}#{self.user.discriminator}",
            'wallet':100,
            'bank':100
        }
        col.insert_one(payload)

    async def updatewallet(self, balance, guild):
        if col.count_documents({"_id":self.user.id}) == 0:
            await self.add_user(guild)
        col.update_one({"_id":self.user.id}, {"$inc": {'wallet':balance}})
        self.wallet += balance

    async def updatebank(self, balance, guild):
        if col.count_documents({"_id":self.user.id}) == 0:
            await self.add_user(guild)
        col.update_one({"_id":self.user.id}, {"$inc": {'bank':balance}})
        self.bank += balance

    async def get_raw_balance(self, guild): #ONLY USED IN INITIALIZATION
        if col.count_documents({"_id":self.user.id}) == 0:
            await self.add_user(guild)
            return 100, 100, 100
        res = col.find({"_id":self.user.id})
        for i in res:
            wallet = i["wallet"]
            bank = i["bank"]
        return True, int(wallet), int(bank)

    @property
    def bal(self):
        return self.balance

    def _set_cache_balance(self, wallet, bank):
        self.balance = wallet + bank
        self.wallet = wallet
        self.bank = bank

    def get_bank_wallet(self):
        return self.wallet, self.bank

class Economy:
    def __init__(self, price, name, description, icon, power = None):
        self.price = price
        self.description = description
        self.name = name
        self.icon = icon
        self.power = power

    def help(self):
        embed = discord.Embed(color = discord.Color.red())
        embed.description = self.description
        embed.set_thumbnail(url=self.icon)
        embed.description += f"\n\n{self.price} coins"
        embed.title = self.name
        return embed

    def about(self): #an alias for help
        embed = discord.Embed(color=discord.Color.red())
        embed.description = self.description
        embed.set_thumbnail(url=self.icon)
        embed.description += f"\n\n{self.price} coins"
        embed.title = self.name
        return embed

class EconomyCollectible(Economy):
    #Add custom Economy Collectible functions
    def __init__(self, name, price, description, icon):
        super().__init__(
            name=name,
            price=price,
            description=description,
            icon=icon
        )

class EconomyPowerUp(Economy):
    #Add custom functions for each type of Economy Shop Item
    def __init__(self, name, price, description, icon, power):
        super().__init__(
            name=name,
            price=price,
            description=description,
            icon=icon,
            power=power
        )

class Watch(EconomyCollectible, object):
    '''
    Add custom functions to each shop item here, this is just a collectible
    '''
    def __init__(self):
        file = discord.File(f"modules/economy/assets/watch.png", filename='watch.png')
        super().__init__(
            price=100,
            description="Tells the time! A collectable, cannot be sold.",
            name='Watch',
            icon='attachment://watch.png'
        )
        self.file = file


