from flurs.data.entity import User, Item, Event
from sklearn.utils import Bunch
from datetime import datetime, timedelta
import numpy as np
import csv
from os import path
import pandas as pd
import time
from tqdm import tqdm
from calendar import monthrange

all_genres = ['Action', 'Adventure', 'Animation', "Children", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
              'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western', 'IMAX', '(no genres listed)']


def delta(d1, d2, opt='d'):
    delta = 0
    if opt == 'm':
        while True:
            mdays = monthrange(d1.year, d1.month)[1]
            d1 += timedelta(days=mdays)
            if d1 <= d2:
                delta += 1
            else:
                break
    else:
        delta = (d2 - d1).days

    return delta


class RecommenderHelper():
    def __init__(self, data_home='data/ml-latest', size='latest-small'):
        self.data_home = data_home
        self.size = size
        self.movies = {}

    def load_ratings(self):
        df = pd.read_csv(path.join(
            self.data_home, 'ratings.csv'), encoding='ISO-8859-1')
        df['rating'] = [int(x) for x in df['rating']]
        df = df[df['rating'] == 5]
        users = sorted(list(set(df['userId'])))
        sorted_data = df.values[np.argsort(df.values[:, 3])]
        self.users = users
        return (users, sorted_data)

    def load_movies(self):
        n_genre = len(all_genres)
        self.movies = {}
        self.movie_ids = set()
        self.mid2name = {}

        if self.size == 'latest-small':
            with open(path.join(self.data_home, 'movies.csv'), encoding='ISO-8859-1') as f:
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                    item_id_str = row['movieId']
                    title = row['title']
                    genres = row['genres']

                    movie_vec = np.zeros(n_genre)
                    genre_pieces = genres.split('|')
                    for genre in genre_pieces:
                        i = all_genres.index(genre)
                        movie_vec[i] = 1.
                    item_id = int(item_id_str)
                    self.movies[item_id] = movie_vec
                    self.mid2name[item_id] = title
                    self.movie_ids.add(item_id)
        else:
            print('ERROR')

        return self.movies

    def fetch_movielens(self):
        self.seen_movies = set()
        print('Getting ratings...')
        users, ratings = self.load_ratings()
        print('Getting movies...')
        movies = self.load_movies()

        samples = []

        user_ids = {}
        item_ids = {}

        head_date = datetime(*time.localtime(ratings[0, 3])[:6])
        dts = []

        last = {}

        cnt = 0
        print('Processing ratings...')
        for user_id, item_id, rating, timestamp in tqdm(ratings):
            # Remap user indices
            if user_id in user_ids:
                u_index = user_ids[user_id]
            else:
                u_index = len(user_ids)
                user_ids[user_id] = u_index

            # Remap item indices
            if item_id in item_ids:
                i_index = item_ids[item_id]
            else:
                i_index = len(item_ids)
                item_ids[item_id] = i_index
            self.seen_movies.add(item_id)

            date = datetime(*time.localtime(timestamp)[:6])
            dt = delta(head_date, date)
            dts.append(dt)

            weekday_vec = np.zeros(7)
            weekday_vec[date.weekday()] = 1

            if user_id in last:
                last_item_vec = last[user_id]
            else:
                last_item_vec = np.zeros(20)

            others = np.concatenate((weekday_vec, last_item_vec))

            # Dummy feature to prevent errors
            user = User(u_index, np.zeros(1))
            item = Item(i_index, movies[item_id])

            sample = Event(user, item, 1., others)
            samples.append(sample)

            last[user_id] = movies[item_id]
        self.user_ids = user_ids
        self.item_ids = item_ids
        self.rev_item_ids = {y: x for (x, y) in item_ids.items()}
        print('Done loading!')

        return Bunch(samples=samples,
                     can_repeat=False,
                     # 7 days of the week + 20 genres
                     # Dummy feature for user
                     contexts={'others': 7 + 20, 'item': 20, 'user': 1},
                     n_user=len(user_ids),
                     n_item=len(item_ids),
                     n_sample=len(samples))
    
    def create_user(self):
        new_idx = self.users[-1] + 1
        self.users.append(new_idx)
        i_idx = len(self.user_ids)
        self.user_ids[new_idx] = i_idx
        return User(new_idx, np.zeros(1))

    def movie_tid2name(self, tmovie_id):
        return self.movie_id2name(self.user_ids[int(tmovie_id)])

    def movie_id2name(self, movie_id):
        return self.mid2name[int(movie_id)]

    def get_movie(self, movie_id):
        return Item(self.item_ids[movie_id], self.movies[movie_id])

    def load_links(self):
        self.imdb2mid = {}
        self.mid2imdb = {}
        self.tmbd2mid = {}
        with open(path.join(self.data_home, 'links.csv'), 'r') as f:
            is_first = True
            for line in f:
                if is_first:
                    is_first = False
                    continue
                if not line.strip():
                    continue
                pieces = line.strip().split(',')
                # if any([len(x) == 0 for x in pieces]):
                #     print(pieces)
                movieId, imdbId, tmdbId = pieces
                i_movieId = int(movieId)
                if movieId and imdbId:
                    self.imdb2mid[int(imdbId)] = i_movieId
                    self.mid2imdb[i_movieId] = int(imdbId)
                if movieId and tmdbId:
                    self.tmbd2mid[int(tmdbId)] = i_movieId

