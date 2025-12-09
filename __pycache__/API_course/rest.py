# Сайт для конвертации curl to python: https://curlconverter.com/


import requests
from pprint import pprint

headers = {
    'accept': 'application/json',
}

params = {
    'page': '1',
}

response = requests.get(
    'https://api.geckoterminal.com/api/v2/networks/ton/trending_pools', params=params, headers=headers)

data = response.json()
# pprint(data)

i = 0
while i < 5:
    name = data['data'][i]['attributes']['name']
    print(name)
    i += 1
