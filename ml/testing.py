from recommender import RecommenderHelper
from flurs.recommender import FMRecommender
from flurs.data.entity import User, Item, Event
from flurs.evaluator import Evaluator
import pickle
import numpy as np
import os


# with open('h.pickle', 'rb') as f:
#     print('Loading from pickle...')
#     h = pickle.load(f)
# with open('data.pickle', 'rb') as f:
#     data = pickle.load(f)

h = RecommenderHelper()
data = h.fetch_movielens()

with open('h.pickle', 'wb') as f:
    pickle.dump(h, f)
with open('data.pickle', 'wb') as f:
    pickle.dump(data, f)

if os.path.exists('model.pickle'):
    print('Using pickled model')
    with open('model.pickle', 'rb') as f:
        rec = pickle.load(f)
else:
    print('Training...')
    rec = FMRecommender(p=sum(data.contexts.values()),  # number of dimensions of input vector
                        k=60,
                        l2_reg_w0=2.,
                        l2_reg_w=8.,
                        l2_reg_V=16.,
                        learn_rate=.004)
    rec.initialize()

    n_batch_train = int(data.n_sample * 0.9)

    evaluator = Evaluator(rec, data.can_repeat)
    evaluator.debug = True
    evaluator.fit(
        data.samples[:n_batch_train],
        data.samples[n_batch_train:],
        n_epoch=4
    )
    print('Done training!')
    with open('model.pickle', 'wb') as f:
        pickle.dump(rec, f)

print('Model ready')

print(h.item_ids.keys())
match_lst = ['Snow White', 'Frozen', 'Lion King', 'Finding Nemo', 'Toy Story', 'How to Train Your Dragon']
new_u = h.create_user()

for i, mid in enumerate(h.seen_movies):
    name = h.movie_id2name(mid)
    match = False
    for item in match_lst:
        if item.lower() in name.lower():
            match = True
            break
    if not match:
        continue
    print(name)
    print(mid)
    
    print(h.item_ids[mid])
    ctx = np.zeros(27)
    ctx[4] = 1
    mov = h.get_movie(mid)
    evt = Event(new_u, mov, context=ctx)
    rec.update(evt)

print('===== Recommending =====')
cand = rec.recommend(new_u, np.array(sorted(list(h.item_ids.values()))), ctx)
for c in cand[0][:10]:
    c = int(c)
    print(c)
    # print(h.movie_id2name(c))
    print(h.movie_id2name(h.rev_item_ids[c]))
# print(dir(new_u))
