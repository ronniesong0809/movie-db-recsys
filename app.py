from flask import Flask, request, jsonify
import pickle
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

app = Flask(__name__)

def load_pkl(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

def get_col(id, col):
    movies = pd.read_csv('data/data.csv', usecols = ['id', 'name', 'date', 'genre', 'description', 'backdrop', 'poster'])
    return movies.loc[movies['id'] == id][col].tolist()[0]

def recommender(model, id, num = 5):
    python_list = list()
    recs = model[id][:num]
    for rec in recs:
        row = {}
        row['_id'] = str(rec[1])
        row['name'] = get_col(rec[1], 'name')
        row['genre'] = get_col(rec[1], 'genre')
        row['date'] = get_col(rec[1], 'date')
        row['backdrop'] = '{}/{}'.format(os.environ.get('TMDB_BACKDROP_URL'), get_col(rec[1], 'backdrop'))
        row['poster'] = '{}/{}'.format(os.environ.get('TMDB_POST_URL'), get_col(rec[1], 'poster'))
        row['description'] = get_col(rec[1], 'description')
        row['score'] = str(rec[0])
        row['link'] = '{}/movie/{}'.format(os.environ.get('MOVIE_DB_URL'), rec[1])
        row['recommendations'] = '{}/movie?id={}&num={}'.format(os.environ.get('MOVIE_RECSYS_URL'), rec[1], num)
        python_list.append(row)
    return python_list

@app.route("/")
def home():
    return "<a href='/movie?id=155&num=5'> example 1 </a> </br> \
            <a href='/movie?id=120&num=10'> example 2 </a> </br>"

@app.route("/movie", methods=['GET'])
def get_movie():
    id = request.args.get('id')
    num = request.args.get('num')

    model = load_pkl('models/model.pkl')
    data = recommender(model, int(id), int(num))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
