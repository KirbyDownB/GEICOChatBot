import pandas as pd
from os import path
from itertools import chain
from lightfm import LightFM
from lightfm.data import Dataset
import numpy as np
import re
import matplotlib.pyplot as plt

DATA_DIR = 'data/ml-latest'
GENRES = ['Action', 'Adventure', 'Animation', "Children", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western', 'IMAX', '(no genres listed)']
match_lst = ['Snow White', 'Frozen', 'Lion King', 'Finding Nemo', 'Toy Story', 'How to Train Your Dragon', 'Aladdin', 'Big Hero', 'Incredibles', 'Hunchback']
# match_lst = ['Chucky', 'Texas Chainsaw', 'Ring, The', 'Conjuring, The', 'Exorcist, The', 'Insidious']
# match_lst = ['Harold and Kumar', 'Dictator, The', 'Borat', 'Bill and Ted', 'Hangover, The', 'Anchorman, The', 'Zombieland', 'Deadpool']

ratings = pd.read_csv(path.join(DATA_DIR, 'ratings.csv'))
movies = pd.read_csv(path.join(DATA_DIR, 'movies.csv'))

good_ratings = ratings[ratings['rating'] == 5]
years = []
for name in movies['title']:
    z = re.match(r'.+\(([0-9]{4})\)', name)
    if z:
        years.append(z.group(1))
    else:
        years.append('unknown')
movies['year'] = years
print(movies.head())

print(f'# Ratings: {len(ratings)}')
print(f'# Users: {len(set(ratings["userId"]))}')
last_user = sorted(list(set(ratings['userId'])))[-1]
new_user = last_user + 1
print('Added new user: %s' % new_user)

dataset = Dataset()
dataset.fit(chain(ratings['userId'], [new_user]), movies['movieId'], item_features=(GENRES + list(movies['year']) + list(set(movies['movieId']))))

_, _, item_mapping, _ = dataset.mapping()
rev_item_mapping = {y:x for (x,y) in item_mapping.items()}

matches = []
for rid, row in movies.iterrows():
    for m in match_lst:
        if m.lower() in row[1].lower():
            matches.append(row[0])

print(good_ratings.head())
rating_iter = zip(good_ratings['userId'], good_ratings['movieId'])
new_iter = ((new_user, x) for x in matches)
interactions, weights = dataset.build_interactions(chain(rating_iter, new_iter))

print(repr(interactions))
mov_features = ((row[0], row[2].split('|') + [row[3], row[0]]) for rid, row in movies.iterrows())
# print(mov_features[0])
item_features = dataset.build_item_features(mov_features)


model = LightFM(loss='warp', no_components=28, item_alpha=0.0001, learning_rate=0.05)
model.fit(interactions, item_features=item_features, num_threads=16)

movie2name = {}
for rid, row in movies.iterrows():
    movie2name[row[0]] = row[1]


n_users, n_items = dataset.interactions_shape()
# Adjust using base ratings
base_mat = model.predict(0, np.arange(n_items), num_threads=16)
base_mat = (base_mat + np.min(base_mat))
# base_mat = np.log2(base_mat + np.min(base_mat))
def sample_recommendation(model, interations, user_ids):
    n_users, n_items = dataset.interactions_shape()

    for user_id in user_ids:
        user_id = int(user_id)
        known_positives = [movie2name[rev_item_mapping[x]] for x in interactions.tocsr()[user_id].indices]

        scores = model.predict(user_id, np.arange(n_items), num_threads=16) - base_mat #np.log2(np.clip(base_mat, 0.0001, None))
        print(scores.dtype)
        top_items = [(x, movie2name[rev_item_mapping[x]]) for x in np.argsort(-scores)]
        # fig = plt.figure()
        plt.plot(scores)
        # plt.savefig('img_%d.png' % user_id)
        # plt.close(fig)

        print("User %s" % user_id)
        print("     Known positives (%d):" % len(known_positives))
        
        for x in known_positives[:5]:
            print("        %s" % x)

        print("     Recommended:")
        
        for (idx, x) in top_items[:5]:
            print("        %s (%f)" % (x, scores[idx]))

n_users, n_items = dataset.interactions_shape()
sample_recommendation(model, interactions, list(np.linspace(0, n_users - 1, 30)) + [new_user - 1])
plt.savefig('img_all.png')
