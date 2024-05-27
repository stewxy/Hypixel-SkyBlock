import requests
from requests.auth import HTTPBasicAuth

url = "https://api.hypixel.net/v2/skyblock/profile"
api_url = "https://api.hypixel.net/skyblock/profiles?key=[]&uuid=[]"
r = requests.get(api_url)
print(r.json())

headers = {'Accept': 'application/json'}
auth = HTTPBasicAuth('apikey', "")
payload = {}

response = requests.get(url, headers=headers, auth=auth)
print(response.json())
print(response.status_code)


