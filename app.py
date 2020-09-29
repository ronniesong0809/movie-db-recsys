from flask import Flask, request, jsonify
import pickle
import os

app = Flask(__name__)

def load_pkl(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

def recommender(model, id, num = 5):
    python_list = list()
    recs = model[id][:num]
    for rec in recs:
        row = {}
        row['_id'] = str(rec[1])
        row['score'] = str(rec[0])
        row['link'] = '{}/movie/{}'.format(os.environ.get('MOVIEDB_URL'), rec[1])
        row['recommendations'] = '{}/movie?id={}&num={}'.format(os.environ.get('MOVIE_RECSYS_URL'), rec[1], num)
        python_list.append(row)
    return python_list

@app.route("/")
def home():
    return "<a href='/movie?id=155&num=5'> example 1 </a> </br> \
            <a href='/movie?id=120&num=10'> example 2 </a> </br>"

@app.route("/movie", methods=['GET'])
def getMovie():
    id = request.args.get('id')
    num = request.args.get('num')

    model = load_pkl('models/model.pkl')
    data = recommender(model, int(id), int(num))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
