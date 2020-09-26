import pandas as pd
import pickle

def load_obj(file):
    with open(file, 'rb') as f:
        return pickle.load(f)

# def getName(id):
#     return movies.loc[movies['id'] == id]['name'].tolist()

# def getDesc(id):
#     return movies.loc[movies['id'] == id]['description'].tolist()

# def recommender(item_id, num):
#     print('{} movies similar to {}'.format(num, getName(item_id)))
#     print('---------------------------------------')
#     recs = results[item_id][:num]
#     for i, rec in enumerate(recs):
#         print('Movie Id:    {}'.format(rec[1]))
#         print('score:       {}'.format(rec[0]))
#         print('Name:        {}'.format(getName(rec[1])))
#         print('Description: {}\n'.format(getDesc(rec[1])))

def recommender(item_id, num):
    py_list = list()
    recs = results[item_id][:num]
    for rec in recs:
        row = {}
        row['id'] = rec[1]
        row['score'] = rec[0]
        py_list.append(row)
    return py_list

# movies = pd.read_csv('data/data.csv', usecols = ['id', 'name', 'description'])

results = load_obj('models/model.pkl')
# recommender(item_id = 155, num = 5)
print(recommender(item_id = 155, num = 5))