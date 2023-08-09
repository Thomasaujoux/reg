

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import pandas as pd

import pickle
import numpy as np


# Connect to Spotify 
SPOTIPY_CLIENT_ID = 'cae593fec3384b92892d0b6b26a910bd'
SPOTIPY_CLIENT_SECRET = 'edbfb882cbf140bdabb5577bf0acb0b1'

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)




def vector(song_ids, limit):

    length = len(song_ids)
    num_tracks_to_recommend = round(limit/length)

    vect = []
    vect.append(0)
    for i in range(1, length):
        vect.append(i * num_tracks_to_recommend + 1)
    
    return vect


def spotify_reco(sp, song_id, limit):
    score = [] 

    recommandations = sp.recommendations(seed_tracks= song_id, limit=limit)

    for reco in recommandations["tracks"]: # On génére deux fois plus de recommandation car nous allons établir un score et juste prendre les meilleures
        score.append(reco['id'])

    df = pd.DataFrame(columns=["track_uri", "duration_ms", 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature', 'popularity'])
    track_uri = []
    danceability = []
    energy = []
    key = []
    loudness = []
    mode = []
    speechiness = []
    acousticness = []
    instrumentalness = []
    liveness = []
    valence = []
    tempo = []
    time_signature = []
    duration_ms = []
    popularity = []
    
    features =sp.audio_features(score)
    for track in features: 
      track_uri.append(track['id'])
      danceability.append(track['danceability'])
      energy.append(track['energy'])
      key.append(track['key'])
      loudness.append(track['loudness'])
      mode.append(track['mode'])
      speechiness.append(track['speechiness'])
      acousticness.append(track['acousticness'])
      instrumentalness.append(track['instrumentalness'])
      liveness.append(track['liveness'])
      valence.append(track['valence'])
      tempo.append(track['tempo'])
      time_signature.append(track['time_signature'])
      duration_ms.append(track['duration_ms'])

    popu = sp.tracks(score)
    for track in popu['tracks']: 
      popularity.append(track['popularity'])

    df['track_uri'] = track_uri
    df['danceability'] = danceability
    df['energy'] = energy
    df['key'] = key
    df['loudness'] = loudness
    df['mode'] = mode
    df['speechiness'] = speechiness
    df['acousticness'] = acousticness
    df['instrumentalness'] = instrumentalness
    df['liveness'] = liveness
    df['valence'] = valence
    df['tempo'] = tempo
    df['time_signature'] = time_signature
    df['duration_ms'] = duration_ms
    df['popularity'] = popularity

    return df
