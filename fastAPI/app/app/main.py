# Load the libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from typing import Dict

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import pandas as pd
import numpy as np
import json


import pickle
import heapq




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



df = pd.read_csv(r"C:\Users\thoma\Documents\GitHub\reg\v1\data_feature_final.cvs")
df = df.drop(["Unnamed: 0.1", "Unnamed: 0"], axis = 1)

columns = ['duration_ms', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']
x = df[columns]
y = df.Class.values
    
from sklearn.model_selection import train_test_split
#Split data into test and train
X_train, X_test, y_train, y_test=train_test_split(x,y, test_size=0.2, random_state=42)

from sklearn.ensemble import GradientBoostingRegressor
model = GradientBoostingRegressor(
    learning_rate = 0.06,
    n_estimators = 60,
    max_depth = 4,
    min_samples_split = 0.4,
    min_samples_leaf = 0.1,
    max_features = 12
    )
model.fit(x, y)

#model_pkl = pickle.load(open('trained_pipeline-0.1.0.pkl', 'rb'))

# Initialize an instance of FastAPI
app = FastAPI()

class Model_Input(BaseModel):

    duration_ms : float
    danceability : float
    energy : float
    key : float
    loudness : float
    mode : float
    speechiness : float
    acousticness : float
    instrumentalness : float
    liveness : float
    valence : float
    tempo : float
    time_signature : float


# Define the default route 
@app.get("/")
async def root():
    return {"message": "Welcome to your FastAPI"}


@app.get("/features/", response_model=Dict)
async def features(song_id: str) -> dict:
    song_id = song_id.split(",")
    features = sp.audio_features(song_id)
    return {"Song features: ": features}

@app.post('/predict/features')
def track_pred(input_parameters : Model_Input):
    
    df = pd.DataFrame([input_parameters.dict().values()], columns=input_parameters.dict().keys())
    
    prediction = model.predict(df)
    return {"prediction":prediction}

# Define the route to the playlist predictor
@app.get("/predict/", response_model=Dict)
async def predict_playlist(song_id: str, limit: int=50)-> dict:

    # Create a list of songs ids
    song_ids = song_id.split(",")

    # Create the list of songs to base on
    vect = vector(song_ids, limit)

    # Create the list of recommended songs
    recommended_tracks = dict()
    recommended_tracks[0] = song_ids[0]


    for i in range(0, len(vect)-1):
        df = spotify_reco(sp, [song_ids[i]], limit)
        columns=["duration_ms", 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']
        get_score_values = get_score(df[columns], model, weight_pos = 1, weight_model = 1, weight_popu=1)
        get_score_ind = heapq.nlargest(3, range(len(get_score_values)), key=get_score_values.__getitem__)
        z = 1
        for j in get_score_ind:
            recommended_tracks[i + z] = df["track_uri"][j]
            z = z + 1
    return {"message": recommended_tracks}
