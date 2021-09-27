import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pickle

# load csv
movies = pd.read_csv('data/data.csv', usecols = ['id', 'name', 'genre', 'description'])

# combine name and description
movies['content'] = movies[['name', 'genre', 'description']].astype(str).apply(lambda x: ' // '.join(x), axis = 1)
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

# save to pkl
with open('models/model.pkl', 'wb') as f:
    pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)
