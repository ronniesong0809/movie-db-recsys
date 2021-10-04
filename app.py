from flask import Flask, request, jsonify
import pickle
import os
import pandas as pd
import boto3
from botocore.client import Config

app = Flask(__name__)

s3 = boto3.resource('s3',
    endpoint_url=os.environ.get('AWS_S3_ENDPOINT_URL'),
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    config=Config(signature_version='s3v4'),
    region_name=os.environ.get('AWS_S3_REGION_NAME'))

def load_file(filname):
    return s3.Bucket(os.environ.get('AWS_S3_BUCKET')).Object(filname).get()['Body']

def get_col(id, col):
    movies = pd.read_csv(load_file('data.csv'), usecols = ['id', 'name', 'date', 'genre', 'description', 'backdrop', 'poster'])
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
        row['backdrop'] = '{}{}'.format(os.environ.get('TMDB_BACKDROP_URL'), get_col(rec[1], 'backdrop'))
        row['poster'] = '{}{}'.format(os.environ.get('TMDB_POST_URL'), get_col(rec[1], 'poster'))
        row['description'] = get_col(rec[1], 'description')
        row['score'] = str(rec[0])
        row['link'] = '{}/movie/{}'.format(os.environ.get('MOVIE_DB_URL'), rec[1])
        row['recommendations'] = '{}/movie?id={}&num={}'.format(os.environ.get('MOVIE_RECSYS_URL'), rec[1], num)
        python_list.append(row)
    return python_list

@app.route('/')
def home():
    return '<a href="/movie?id=155&num=5"> example 1 </a> </br> \
            <a href="/movie?id=120&num=10"> example 2 </a> </br>'

@app.route('/movie', methods=['GET'])
def get_movie():
    id = request.args.get('id')
    num = request.args.get('num')

    model = pickle.loads(load_file('model.pkl').read())
    data = recommender(model, int(id), int(num))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
