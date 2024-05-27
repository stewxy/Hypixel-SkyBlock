import requests
from requests.auth import HTTPBasicAuth

api_key = ""
api_uuid = ""

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
x = r.json().get("products").get("ESSENCE_DRAGON").get("quick_status")
print(x)
# for item in x:
#     print(item)



