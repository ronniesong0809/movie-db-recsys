import requests
from dotenv import load_dotenv
import os
import json
import csv

load_dotenv()

res = list()
for i in range(1, 7, 1):
    url = 'https://api.themoviedb.org/3/movie/top_rated?api_key={}&language=en-US&page={}'.format(os.environ.get('TMDB_API_KEY'), i)
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    r = requests.get(url=url, headers=headers)

    response = r.json()

    for d in response['results']:
        x = {}
        x['id'] = d['id']
        
        if 'title' in d:
            x['name'] = d['title']
        elif 'original_title' in d:
            x['name'] = d['original_title']
        else:
            x['name'] = d['name']

        x['date'] = d['release_date']
        
        if d['overview'] != "":
            x['description'] = d['overview'].replace("\r", " ")
        else:
            x['description'] = "null"

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
