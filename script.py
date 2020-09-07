import requests
from dotenv import load_dotenv
import os
import json
import csv

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
    x['date'] = d['release_date']
    x['description'] = d['overview']
    res.append(x)

with open('data/data.json', 'w') as f:
    json.dump(res, f, indent=4)


data = []
with open('data/data.json') as f:
    data = json.loads(f.read())
    f = csv.writer(open('data/data.csv', 'w', newline='', encoding='utf-8'))

f.writerow(['id', 'name', 'date', 'description'])

for x in data:
    f.writerow([x['id'], x['name'], x['date'], x['description']])