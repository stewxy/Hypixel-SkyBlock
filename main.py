import requests
import discord
from discord.ext import commands
from requests.auth import HTTPBasicAuth

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

api_key = ""
api_uuid = ""
api_url = "https://api.hypixel.net/skyblock/profiles?key={key}&uuid={uuid}".format(key = api_key, uuid = api_uuid)


@client.event
async def on_ready():
    print("Online")


@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.send("pong")


@client.command(aliases=['b'])
async def get_bazaar(ctx):
    bazaar_link = "https://api.hypixel.net/v2/skyblock/bazaar"
    bazaar_response = requests.get(bazaar_link)
    listing = bazaar_response.json().get("products").get("ENDER_PEARL").get("quick_status")
    await ctx.send(listing)


@client.command(aliases=['c'])
async def get_collection(ctx):
    response = requests.get(api_url)
    profiles = (response.json()).get("profiles")
    collection = sorted(profiles[0].get('members').get(api_uuid).get("unlocked_coll_tiers"))
    await ctx.send(collection)





client.run("")