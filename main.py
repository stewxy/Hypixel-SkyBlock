import requests
import discord
from discord.ext import commands
import aiohttp
import asyncio
import re

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

api_key = ""
api_uuid = ""
api_url = "https://api.hypixel.net/skyblock/profiles?key={key}&uuid={uuid}".format(key=api_key, uuid=api_uuid)


@client.event
async def on_ready():
    print("Bot Online")


# @client.command(aliases=['p'])
# async def ping(ctx):
#     await ctx.send("pong")


@client.command(aliases=['b'])
async def get_bazaar(ctx, *item):
    join_text = ' '.join(item)
    processed_text = join_text.upper().replace(" ", "_").strip()

    bazaar_link = "https://api.hypixel.net/v2/skyblock/bazaar"
    bazaar_response = requests.get(bazaar_link)
    try:
        listing = bazaar_response.json().get("products").get(processed_text).get("quick_status")
        product_id = listing.get("productId")
        sell_price = round(listing.get("sellPrice"), 2)
        buy_price = round(listing.get("buyPrice"), 2)
        format_text = f"Item: {product_id} \nSell Price: {sell_price} \nBuy Price: {buy_price}"
        await ctx.send(format_text)
    except AttributeError as e:
        await ctx.send("COULDN'T FIND ITEM")

no_listings = 0
total_starting_bid = 0
async def getting_auctions(session, url, item_name, want_rarity = None, want_bin = None):
    global no_listings
    global total_starting_bid
    if want_rarity == "ANY":
        want_rarity = None
    if want_bin == "ANY":
        want_bin = None
    async with session.get(url) as resp:
        auctions = await resp.json()
        items = ""
        for auction in auctions.get("auctions"):
            re_item_name = re.sub("\[.*?\]", "", auction.get("item_name")).replace("✪", "").strip().upper()
            if item_name == re_item_name:
                name = auction.get("item_name")
                highest_bid = str(auction.get("highest_bid_amount"))
                starting_bid = str(auction.get("starting_bid"))
                rarity = auction.get("tier")

                check_bin = None
                if want_bin == "Y":
                    check_bin = True
                elif want_bin == "N":
                    check_bin = False;

                if auction.get("bin"):
                    auction_bin = "Available"
                else:
                    auction_bin = "Unavailable"

                if want_bin is not None and want_rarity is not None:
                    if item_name == re_item_name and want_rarity == rarity and check_bin == auction.get("bin"):
                        items += ("\nItem: " + name + "\nStarting bid: " + starting_bid + "\nHighest Bid: " + highest_bid + "\nRarity: " + rarity + "\nBIN: " + auction_bin + "\n")
                        no_listings += 1
                        total_starting_bid += auction.get("starting_bid")
                elif want_bin is not None and want_rarity is None:
                    if item_name == re_item_name and check_bin == auction.get("bin"):
                        items += ("\nItem: " + name + "\nStarting bid: " + starting_bid + "\nHighest Bid: " + highest_bid + "\nRarity: " + rarity + "\nBIN: " + auction_bin + "\n")
                        no_listings += 1
                        total_starting_bid += auction.get("starting_bid")
                elif want_bin is None and want_rarity is not None:
                    if item_name == re_item_name and want_rarity == rarity:
                        items += ("\nItem: " + name + "\nStarting bid: " + starting_bid + "\nHighest Bid: " + highest_bid + "\nRarity: " + rarity + "\nBIN: " + auction_bin + "\n")
                        no_listings += 1
                        total_starting_bid += auction.get("starting_bid")
                else:
                    items += ("\nItem: " + name + "\nStarting bid: " + starting_bid + "\nHighest Bid: " + highest_bid + "\nRarity: " + rarity + "\nBIN: " + auction_bin + "\n")
                    no_listings += 1
                    total_starting_bid += auction.get("starting_bid")


                # if items == "":
                #     items += ("Item: " + name + "\nStarting bid: " + starting_bid + "\nHighest Bid: " + highest_bid + "\nRarity: " + rarity + "\nBIN: " + auction_bin + "\n")
                # else:
                #     items += ("\nItem: " + name + "\nStarting bid: " + starting_bid + "\nHighest Bid: " + highest_bid + "\nRarity: " + rarity + "\nBIN: " + auction_bin + "\n")
        return items


@client.command(aliases=['ah'])
async def get_auctions(ctx, *item):
    global no_listings
    global total_starting_bid

    join_text = ''.join(item).upper()
    split_text = join_text.split("+")
    print(join_text)

    ah_link = "https://api.hypixel.net/v2/skyblock/auctions"
    ah_response = requests.get(ah_link)
    listing = ah_response.json()
    pages = listing.get("totalPages")

    async with aiohttp.ClientSession() as session:
        tasks = []
        list_rarity = ["COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY", "MYTHIC", "ANY"]
        list_bin = ["Y", "N", "ANY"]

        for i in range(pages):
            ah_link = f"https://api.hypixel.net/v2/skyblock/auctions?page={i}"
            if len(split_text) == 3:
                if split_text[1] in list_rarity and split_text[2] in list_bin:
                    tasks.append(asyncio.ensure_future(getting_auctions(session, ah_link, split_text[0], split_text[1], split_text[2])))
                else:
                    await ctx.send("INVALID FORMATTING\nTo search with tier and/or bin please use: !ah [item] + [tier/any] + [bin?(y/n)/any]")
                    return
            elif len(split_text) == 2:
                if split_text[1] in list_rarity:
                    tasks.append(asyncio.ensure_future(getting_auctions(session, ah_link, split_text[0], split_text[1])))
                else:
                    await ctx.send("INVALID FORMATTING\nTo search with tier and/or bin please use: !ah [item] + [tier/any] + [bin?(y/n)/any]")
                    return
            elif len(split_text) == 1:
                tasks.append(asyncio.ensure_future(getting_auctions(session, ah_link, split_text[0])))


        original = await asyncio.gather(*tasks)
        if (len(list(filter(None, original)))) == 0:
            await ctx.send("NO AUCTIONS FOUND FOR THIS ITEM")
            return

        format_string = ""
        for item in original:
            if item != "":
                format_string += item + "\n"
                #await ctx.send(format_string)
        print(no_listings, total_starting_bid, round(total_starting_bid/no_listings, 2))
        no_listings = 0
        total_starting_bid = 0


async def test_function(item_name, rarity = None, bin = None):
    print(item_name, rarity, bin)


@client.command(aliases=['x'])
async def test(ctx, *item):

    join_text = ''.join(item).upper()
    split_text = join_text.split("+")
    print(split_text)
    if len(split_text) == 3:
        await test_function(split_text[0], split_text[1], split_text[2])
    elif len(split_text) == 2:
        await test_function(split_text[0], split_text[1])
    elif len(split_text) == 1:
        await test_function(split_text[0])


# class BinDropdown(discord.ui.Select):
#     def __init__(self):
#         options = [
#             discord.SelectOption(label="ANY"),
#             discord.SelectOption(label="YES"),
#             discord.SelectOption(label="NO")
#         ]
#         super().__init__(placeholder="Please select an option", options=options, min_values=1, max_values=1)
#
#     async def callback(self, interaction: discord.Interaction):
#             await interaction.response.send_message(f"You chose '{self.values[0]}' as your options")
#
# class BinView(discord.ui.View):
#     def __init__(self):
#         super().__init__()
#         self.add_item(BinDropdown())
#
#
# class AuctionDropdown(discord.ui.Select):
#     def __init__(self, ctx):
#         self.ctx = ctx
#         options = [
#             discord.SelectOption(label="ANY"),
#             discord.SelectOption(label="COMMON"),
#             discord.SelectOption(label="UNCOMMON")
#         ]
#         super().__init__(placeholder="Please select an option", options=options, min_values=1, max_values=1)
#
#     async def callback(self, interaction: discord.Interaction):
#         await ctx.send("BIN?", view=BinView())
#
#
# class AuctionView(discord.ui.View):
#     def __init__(self):
#         super().__init__()
#         self.add_item(AuctionDropdown())





# @client.command(aliases=['c'])
# async def get_collection(ctx):
#     response = requests.get(api_url)
#     profiles = (response.json()).get("profiles")
#     collection = sorted(profiles[0].get('members').get(api_uuid).get("unlocked_coll_tiers"))
#     await ctx.send(collection)


# https://api.mojang.com/users/profiles/minecraft/{username}?
client.run("")
