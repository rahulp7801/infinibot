import xmltodict
from quart import Quart, request
import yaml
import discord
import threading
from concurrent.futures import ProcessPoolExecutor
import asyncio
from pymongo import MongoClient
from xml.parsers.expat import ExpatError

def startclient():
    with open('testbot.txt', 'r') as f:
        token = f.read()
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    client.run(token)

with open('config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

with open('./mongourl.txt', 'r') as file:
    url = file.read()

intents = discord.Intents().all()
client = discord.Client()
mongo_url = url.strip()
cluster = MongoClient(mongo_url)
db = cluster['YOUTUBE']
col = db['guilds']

app = Quart(__name__)


@client.event
async def on_ready():
    print('ready')

@client.event
async def on_message(message):
    print(message)

@app.route("/feed", methods = ["GET", "POST"])
async def feed():
    print('e')
    challenge = request.args.get("hub.challenge")
    if challenge:
        print('yes')
        return challenge
    try:
        print('ok1')
        xml_dict = xmltodict.parse(await request.data)
        print('ok2')
        channel_id = xml_dict["feed"]["entry"]["yt:channelId"]
        print('ok3')
        if (col.count_documents({'channelid': channel_id}) == 0):
            print('ok4')
            return "okokokok", 403
        video_url = xml_dict['feed']['entry']['link']['@href']
        video_author = xml_dict['feed']['entry']['author']['name']
        try:
            description = f"{xml_dict['feed']['entry']['description']}"
        except Exception:
            description = "No Description"

        title = xml_dict['feed']['entry']['title']
        print('ok5')
        print(f"New video url: {video_url}")
        embed = discord.Embed(color=discord.Color.green(), url=video_url)
        embed.title = title
        embed.description = description
        embed.set_author(name=video_author)
        result = col.find({'channelid': channel_id})
        for i in result:
            channel = i["textchannel"]
            print(channel)
            sendmsg = i["sendmsg"]
            print(sendmsg)
            channel = client.get_channel(channel)
            print(client.user.name)
            print(channel)
            client.loop.create_task(channel.send(content=sendmsg, embed=embed))

    except (ExpatError, LookupError) as e:
        print(e)
        return "yesthis", 403

    return "", 204

t1 = threading.Thread(target=startclient)

if __name__ == '__main__':
    t1.start()
    app.run()


