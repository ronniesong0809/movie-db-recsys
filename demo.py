import pandas as pd
import pickle

def load_obj(file):
    with open(file, 'rb') as f:
        return pickle.load(f)

def getName(id):
    return movies.loc[movies['id'] == id]['name'].tolist()

def getDesc(id):
    return movies.loc[movies['id'] == id]['description'].tolist()

def recommender(item_id, num):
    print('{} movies similar to {}'.format(num, getName(item_id)))
    print('---------------------------------------')
    recs = results[item_id][:num]
    for i, rec in enumerate(recs):
        print('Movie Id:    {}'.format(rec[1]))
        print('score:       {}'.format(rec[0]))
        print('Name:        {}'.format(getName(rec[1])))
        print('Description: {}\n'.format(getDesc(rec[1])))

movies = pd.read_csv('data/data.csv', usecols = ['id', 'name', 'description'])

results = load_obj('models/model.pkl')
recommender(item_id = 155, num = 5)
