# Load the libraries
from fastapi import FastAPI, HTTPException

from typing import Dict

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Connect to Spotify 
SPOTIPY_CLIENT_ID = 'cae593fec3384b92892d0b6b26a910bd'
SPOTIPY_CLIENT_SECRET = 'edbfb882cbf140bdabb5577bf0acb0b1'

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



# Initialize an instance of FastAPI
app = FastAPI()


# Define the default route 
@app.get("/")
def root():
    return {"message": "Welcome to your FastAPI"}


@app.get("/features/", response_model=Dict)
async def features(song_id: str) -> dict:
    song_id = song_id.split(",")
    features = sp.audio_features(song_id)
    return {"Song features: ": features}



# Define the route to the playlist predictor
@app.get("/predict/", response_model=Dict)
async def predict_playlist(song_id: str, limit: int=100)-> dict:
    score = "aaa"

    song_id = song_id.split(",")


    length = len(song_id)
    num_tracks_to_recommend = round(limit/length)
    vect = []
    vect.append(0)
    for i in range(1, length):
        vect.append(i * num_tracks_to_recommend + 1)


    recommended_tracks = dict()
    recommended_tracks[0] = song_id[0]


    for i in range(0, len(vect)-1):
        score = [] 
        recommandations = sp.recommendations(seed_tracks=[song_id[i]], limit=limit)
        for reco in recommandations["tracks"]: # On génére deux fois plus de recommandation car nous allons établir un score et juste prendre les meilleures
            score.append(reco['id'])
        score =sp.audio_features(score) 
        get_score_values = get_score(score, model, weight_pos = 1, weight_model = 1.5)
    
    return {"message": score}
