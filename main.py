import requests
from requests.auth import HTTPBasicAuth

api_key = ""
api_uuid = ""

url = "https://api.hypixel.net/v2/skyblock/profile"
api_url = "https://api.hypixel.net/skyblock/profiles?key={key}&uuid={uuid}".format(key = api_key, uuid = api_uuid)
response = requests.get(api_url)

profiles = (response.json()).get("profiles")
collection = sorted(profiles[0].get('members').get(api_uuid).get("unlocked_coll_tiers"))
print(collection)


