import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

url = 'https://api.themoviedb.org/3/movie/top_rated?api_key={}&language=en-US&page=1'.format(os.environ.get('TMDB_API_KEY'))
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
r = requests.get(url=url, headers=headers)

response = r.json()

res = list()
for d in response['results']:
    x = {}
    x['id'] = d['id']
    x['name'] = d['title']
    x['description'] = d['overview']
    res.append(x)

with open('data/data.json', 'w') as f:
    json.dump(res, f, indent=4)