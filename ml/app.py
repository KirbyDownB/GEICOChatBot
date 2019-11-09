from flask import Flask, escape, request, jsonify
from recommender import RecommenderHelper
from itertools import chain
from lightfm import LightFM
from lightfm.data import Dataset
from os import path
import random
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time


NUM_DUMMY = 100 # Number of "dummy" users
GENRES = ['Action', 'Adventure', 'Animation', "Children", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western', 'IMAX', '(no genres listed)']
DATA_DIR = 'data/ml-latest'

ratings = pd.read_csv(path.join(DATA_DIR, 'ratings.csv'))
movies = pd.read_csv(path.join(DATA_DIR, 'movies.csv'))
years = []
for name in movies['title']:
    z = re.match(r'.+\(([0-9]{4})\)', name)
    if z:
        years.append(z.group(1))
    else:
        years.append('unknown')
movies['year'] = years
print(movies.head())

ratings.drop(ratings[ratings['rating'] != 5].index, inplace=True)
movies.drop(movies[movies['year'] == 'unknown'].index, inplace=True)
movies.drop(movies[movies['year'].astype('int') < 1950].index, inplace=True)

print(movies[movies['year'] == 'unknown'])
all_movies = set(movies['movieId'])
ratings.drop(ratings[~ratings['movieId'].isin(all_movies)].index, inplace=True)
drop_indices = np.random.choice(ratings.index, 1000000, replace=False)
ratings.drop(drop_indices, inplace=True)

print(f'# Ratings: {len(ratings)}')
print(f'# Users: {len(set(ratings["userId"]))}')
last_user = sorted(list(set(ratings['userId'])))[-1]
new_users = list(range(last_user + 1, last_user + NUM_DUMMY + 1))
# new_user = last_user + 1
# print('Added new user: %s' % new_user)

dataset = Dataset()
dataset.fit(chain(ratings['userId'], new_users), movies['movieId'], item_features=(GENRES + list(movies['year']) + list(set(movies['movieId']))))

user_mapping, _, item_mapping, _ = dataset.mapping()
rev_item_mapping = {y:x for (x,y) in item_mapping.items()}
rev_user_mapping = {y:x for (x,y) in user_mapping.items()}

print(ratings.head())
rating_iter = zip(ratings['userId'], ratings['movieId'])
dddd = list(rating_iter)
interactions, weights = dataset.build_interactions(dddd)

mov_features = ((row[0], row[2].split('|') + [row[3], row[0]]) for rid, row in movies.iterrows())
# print(mov_features[0])
item_features = dataset.build_item_features(mov_features)

model = LightFM(loss='warp', no_components=28, item_alpha=0.0001, learning_rate=0.05)
model.fit(interactions, item_features=item_features, num_threads=16)
n_users, n_items = dataset.interactions_shape()

movie2name = {}
for rid, row in movies.iterrows():
    movie2name[row[0]] = row[1]

def pred(mdl, user_id, k=10):
    # TODO(willshiao): change arange to unique items for the user
    base_mat = mdl.predict(0, np.arange(n_items), num_threads=16)
    base_mat = (base_mat + np.min(base_mat))
    scores = model.predict(user_id, np.arange(n_items), num_threads=16) - base_mat
    inner = [rev_item_mapping[x] for x in np.argsort(-scores)[:k]]
    top_items = []
    for x in inner:
        if x not in r.mid2imdb:
            print((x+1) in r.mid2imdb, (x-1) in r.mid2imdb)
            print(movie2name[x])
        else:
            top_items.append(r.mid2imdb[x])
    # top_items = [r.mid2imdb[x] for x in inner]
    return top_items

app = Flask(__name__)
r = RecommenderHelper(data_home='data/ml-latest')
r.load_links()

@app.route('/')
def index():
    return f'Hello!'

# Stores the next usable user
last_user = new_users[0]
username2id = {}
seen_dict = {}

@app.route('/recommend', methods=['POST'])
def recommend():
    global last_user
    global username2id
    global interactions
    global seen_dict

    start_time = time.time()
    data = request.get_json()
    if 'ids' not in data:
        return jsonify({ 'success': False, 'message': 'ids field required' })
    if 'user' not in data:
        return jsonify({ 'success': False, 'message': 'user field not found' })
    username = data['user']
    imdb_ids = [int(x[2:]) for x in data['ids']]
    if username not in username2id:
        print(f'Registering new user {username}')
        user_id = last_user
        username2id[username] = last_user
        seen_dict[username] = set()
        last_user += 1
    else:
        user_id = username2id[username]
    user_id = user_mapping[user_id]
    ret = []
    for imdb_id in imdb_ids:
        if imdb_id not in r.imdb2mid:
            continue
        ret.append(r.imdb2mid[imdb_id])
    print('Got movies: ', [movie2name[x] for x in ret if x in movie2name])

    #--- Timing block
    elapsed = time.time() - start_time
    print(f'Took {elapsed}s to register user')
    start_time = time.time()
    #--- End timing block

    # Adjust to dataset ID
    adj_ids = [item_mapping[x] for x in ret if x in item_mapping]
    # tmp = interactions.tolil()
    for adj_id in adj_ids:
        if adj_id in seen_dict[username]:
            print('Movie already added')
            continue
        # dddd.append((user_id, adj_id))
        # tmp[user_id, adj_id] = 1
    # interactions = tmp.tocoo()
        np.append(interactions.row, user_id)
        np.append(interactions.col, adj_id)
        np.append(interactions.data, 1)
        seen_dict[username].add(adj_id)
    # (interactions, _) = dataset.build_interactions(rating_list)'
        #--- Timing block
    elapsed = time.time() - start_time
    print(f'Took {elapsed}s to modify matrix')
    start_time = time.time()
    #--- End timing block
    
    model.fit(interactions, item_features=item_features, num_threads=16)

    #--- Timing block
    elapsed = time.time() - start_time
    print(f'Took {elapsed}s to perform partial_fit')
    start_time = time.time()
    #--- End timing block

    output = pred(model, user_id)
    #--- Timing block
    elapsed = time.time() - start_time
    print(f'Took {elapsed}s to perform prediction')
    start_time = time.time()
    #--- End timing block
    # print(output)
    return jsonify({ 'success': True, 'ids': list(output) })

@app.route('/expression', methods=['POST'])
def expression():
    data = request.get_json()
    if 'id' not in data:
        return jsonify({ 'success': False, 'message': 'Missing "id" field' })
    if 'expressions' not in data:
        return jsonify({ 'success': False, 'message': 'Missing "expressions field'})
    if 'username' not in data:
        return jsonify({ 'success': False, 'message': 'Missing "username field'})

    success_res = jsonify({ 'success': True })
    username = data['user']
    expr = data['expressions']

    if username not in username2id:
        return jsonify({ 'success': False, 'message': 'Unknown user'})
    user_id = username2id[username]
    imdb_id = int(data['id'][2:])
    mov_id = r.imdb2mid[imdb_id]

    print('Got expressions for movie: ', movie2name[mov_id] if mov_id in movie2name else '[NOT FOUND]')
    print(f'Expressions: {expr}')

    expr_sorted = sorted(expr.items(), key=lambda x: x[1], reverse=True)
    if mov_id not in item_mapping:
        print(f'Warning: {mov_id} not in item_mapping')
        return success_res
        
    adj_id = item_mapping[mov_id]
    adj_user_id = user_mapping[user_id]

    if adj_id in seen_dict[username]:
        print(f'Movie ({mov_id}) already added')
        return success_res

    if expr_sorted[0] == 'happy':
        print(f'Happy expression found for {mov_id}, updating rating...')
        np.append(interactions.row, adj_user_id)
        np.append(interactions.col, adj_id)
        np.append(interactions.data, 1)
        seen_dict[username].add(adj_id)

    return success_res

