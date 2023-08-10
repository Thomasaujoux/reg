# Load the libraries
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


from typing import Dict
import json

from joblib import load
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import pandas as pd
import numpy as np
import heapq

from operations import vector, spotify_reco, get_score
from model import Model_Input





# Initialize an instance of FastAPI
app = FastAPI(title="App test")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)




# Load the model
@app.on_event("startup")
def load_model():
    # load model from pickle file
    with open('model-0.1.0.pkl','rb') as file:
        global model
        model = load(file)
    # Connect to Spotify 
    global sp
    SPOTIPY_CLIENT_ID = 'c6ee3dcb91a246e69196806df90f1ea2'
    SPOTIPY_CLIENT_SECRET = 'ed497f19a2ef4cf7badbf7c15dd1f63d'
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)





@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/features/", response_model=Dict)
async def features(song_id: str) -> dict:
    print(song_id)
    song_id = song_id.split(",")
    features = sp.audio_features(song_id)
    return {"Song features: ": features}




# Define the route to the playlist predictor
@app.post("/predict/")
async def predict_playlist(input_parameters : Model_Input):
    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)
    category = input_dictionary['category']
    song_ids = input_dictionary['song_ids']
    genres = input_dictionary['genres']
    limit = input_dictionary['limit']


    # Create a list of songs ids
    song_ids = song_ids.split(",")
    # Create the list of songs to base on
    vect, num_tracks_to_recommend = vector(song_ids, limit)
    print(vect,num_tracks_to_recommend)
    # Create the list of recommended songs
    recommended_tracks = dict()
    recommended_tracks[vect[0]] = song_ids[vect[0]]


    for i in range(0, len(vect)-1):
        df = spotify_reco(sp, [song_ids[i]], 50)
        columns=["duration_ms", 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature', 'popularity']
        get_score_values = get_score(df[columns], category, model, weight_pos = 1, weight_model = 1, weight_popu=1)
        get_score_ind = heapq.nlargest(num_tracks_to_recommend, range(len(get_score_values)), key=get_score_values.__getitem__)
        z = 1
        for j in get_score_ind:
            recommended_tracks[vect[i] + z] = df["track_uri"][j]
            z = z + 1
        recommended_tracks[vect[i + 1]] = song_ids[i + 1]

    recommended_tracks[vect[-1]] = song_ids[-1]
    df = spotify_reco(sp, [song_ids[-1]], 50)
    columns=["duration_ms", 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature', 'popularity']
    get_score_values = get_score(df[columns], category, model, weight_pos = 1, weight_model = 1, weight_popu=1)
    get_score_ind = heapq.nlargest(num_tracks_to_recommend, range(len(get_score_values)), key=get_score_values.__getitem__)
    z = 1
    for j in get_score_ind:
        recommended_tracks[vect[-1] + z] = df["track_uri"][j]
        z = z + 1

    return {"message": recommended_tracks}