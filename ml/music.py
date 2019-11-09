import spotipy
import spotipy.util as sputil
import numpy as np
import pandas as pd
import os

from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.preprocessing import StandardScaler

AUDIO_FEATURES = ['danceability', 'duration_ms', 'energy', 'acousticness', 'instrumentalness', 'key', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature', 'valence']

def related_artists(artist_id):
    res = sp.artist_related_artists(artist_id)
    return [a['id'] for a in res['artists']]

def chunk(l, chunk_sz=50): 
    for i in range(0, len(l), chunk_sz):  
        yield l[i:i + chunk_sz]

client_credentials_manager = SpotifyClientCredentials(client_id=os.environ['CLIENT_ID'], client_secret=os.environ['CLIENT_SECRET'])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

QUERY = input('Enter a song name: ')

# Convert song name to artist ID
res = sp.search(q=QUERY)
t_id = res['tracks']['items'][0]['id']
artist_id = res['tracks']['items'][0]['artists'][0]['id']
print('Got artist name: ' + res['tracks']['items'][0]['artists'][0]['name'])

related = related_artists(artist_id)

# Collect songs from related
songs = []
for rid in related:
    songs += [x['id'] for x in sp.artist_top_tracks(rid)['tracks']]

# Get features from related
feat_list = []
for c in chunk(songs):
    feat = sp.audio_features(c)
    feat_list += [x for x in feat if x is not None]

# Convert to DF
df = pd.DataFrame.from_records(feat_list)
feat_df = df[AUDIO_FEATURES]

# Z-normalize input
scaler = StandardScaler()
scaled = scaler.fit_transform(feat_df.values)

# Get original track's audio features
base_feat_dict = sp.audio_features(t_id)[0]
x_in = np.array([base_feat_dict[feat] for feat in AUDIO_FEATURES]).reshape((1, -1))
x_scaled = scaler.transform(x_in)

# Find NN
best_idx = np.argmin(np.sum(np.square(scaled - x_scaled), axis=1))
best_id = df.loc[best_idx]['id']
print(f'Found best result at {best_idx} ({best_id})')
print(f'https://open.spotify.com/track/{best_id}')
