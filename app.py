from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

def load_pkl(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

def recommender(model, id, num = 5):
    json = list()
    recs = model[id][:num]
    for rec in recs:
        row = {
            'id' : str(rec[1]),
            'score' : str(rec[0])
        }
        json.append(row)
    return json

@app.route("/")
def hello_world():
    return "hello world"

@app.route("/movie", methods=['GET'])
def getMovie():
    id = request.args.get('id')
    num = request.args.get('num')

    model = load_pkl('models/model.pkl')
    data = recommender(model, int(id), int(num))
    return jsonify(data)
