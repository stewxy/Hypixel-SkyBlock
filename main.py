import requests
import discord
from discord.ext import commands
from requests.auth import HTTPBasicAuth

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

api_key = ""
api_uuid = ""


@client.event
async def on_ready():
    print("Online")


@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.send("pong")


api_url = "https://api.hypixel.net/skyblock/profiles?key={key}&uuid={uuid}".format(key = api_key, uuid = api_uuid)
response = requests.get(api_url)

profiles = (response.json()).get("profiles")
#print(profiles)
# collection = sorted(profiles[0].get('members').get(api_uuid).get("unlocked_coll_tiers"))
# print(collection)
collection = sorted(profiles[0].get('members').get(api_uuid).get("unlocked_coll_tiers"))
#print(collection)

u2 = "https://api.hypixel.net/v2/skyblock/bazaar"
r = requests.get(u2)
x = r.json().get("products").get("ENDER_PEARL").get("quick_status")
print(x)
# for item in x:
#     print(item)



client.run("")
