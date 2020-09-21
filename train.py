import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# load csv
movies = pd.read_csv('data/data.csv', usecols = ['id', 'name', 'description'])

# combine name and description
movies['content'] = movies[['name', 'description']].astype(str).apply(lambda x: ' // '.join(x), axis = 1)
movies['content'].fillna('Null', inplace = True)

# tf–idf
tf = TfidfVectorizer(analyzer = 'word', ngram_range = (1, 2), min_df = 0, stop_words = 'english')
tfidf_matrix = tf.fit_transform(movies['content'])

# cosine similarity
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

# tf–idf matrix
results = {}
for idx, row in movies.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
    similar_items = [(cosine_similarities[idx][i], movies['id'][i]) for i in similar_indices]
    results[row['id']] = similar_items[1:]

def getName(id):
    return movies.loc[movies['id'] == id]['name'].tolist()

def getDesc(id):
    return movies.loc[movies['id'] == id]['description'].tolist()

def recommend_prettier(item_id, num):
    print('{} movies similar to {}'.format(num, getName(item_id)))
    print('---------------------------------------')
    recs = results[item_id][:num]
    for i, rec in enumerate(recs):
        print('Movie Id:    {}'.format(rec[1]))
        print('score:       {}'.format(rec[0]))
        print('Name:        {}'.format(getName(rec[1])))
        print('Description: {}\n'.format(getDesc(rec[1])))

movies = pd.read_csv('data/data.csv', usecols = ['id', 'name', 'description'])

recommend_prettier(item_id = 155, num = 5)