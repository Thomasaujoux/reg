
import json
import requests
import pandas as pd


from track import Track
from playlist import Playlist
from userplaylists import Userplaylists
from trackfeatures import TrackFeatures
from spotifyuser import SpotifyUser
from trackpopularity import TrackPopularity


class Features(SpotifyUser):
    """Cette classe a pour objectif de récolter les features des musiques"""

    ######### Initialisation de la classe pour le token #########
    def __init__(self, fname, name, email, username):
        """
        :param authorization_token (str): Spotify API token
        :param user_id (str): Spotify user id
        """
        self.fname = fname
        self.name = name
        self.email = email
        self.username = username


    ######### Obtenir les recommandations #########
    def get_track_recommendations(self, seed_tracks, limit=50):
        """Get a list of recommended tracks starting from a number of seed tracks.

        :param seed_tracks (list of Track): Reference tracks to get recommendations. Should be 5 or less.
        :param limit (int): Number of recommended tracks to be returned
        :return tracks (list of Track): List of recommended tracks
        """
        seed_tracks_url = ""
        for seed_track in seed_tracks:
            seed_tracks_url += seed_track + ","
        seed_tracks_url = seed_tracks_url[:-1]
        url = f"https://api.spotify.com/v1/recommendations?seed_tracks={seed_tracks_url}&limit={limit}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        tracks = [Track(track["name"], track["id"], track["artists"][0]["name"]) for track in response_json["tracks"]]
        for t in tracks:
            print(t.name)
        return tracks 

    

    def get_features(self, seed_tracks):
        """Donnes toutes les features à partir d'un track
        :param list of seed_tracks (List with str): The seed (id) of the track in str put in a list
        :return features (Features): All the features needed
        """
        seed_tracks_url = ""
        for seed_track in seed_tracks:
            seed_tracks_url += seed_track + ","
        seed_tracks_url = seed_tracks_url[:-1]
        url = f"https://api.spotify.com/v1/audio-features?ids={seed_tracks_url}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        tracks = [TrackFeatures(track['id'], track["duration_ms"], track["danceability"], track["energy"], track["key"], track['loudness'], track["mode"], track["speechiness"], track["acousticness"], track["instrumentalness"], track["liveness"], track["valence"], track['tempo'], track["time_signature"]) for track in response_json["audio_features"]]
        return tracks
    
    def get_popularity(self, seed_tracks):
        """Donnes toutes les features à partir d'un track
        :param list of seed_tracks (List with str): The seed (id) of the track in str put in a list
        :return features (Features): All the features needed
        """
        seed_tracks_url = ""
        #print(seed_tracks)
        for seed_track in seed_tracks:
            seed_tracks_url += seed_track.id + ","
        seed_tracks_url = seed_tracks_url[:-1]
        url = f"https://api.spotify.com/v1/tracks?ids={seed_tracks_url}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        #print(response_json)
        tracks = [TrackPopularity(track["id"], track["popularity"]) for track in response_json["tracks"]]
        #print(tracks)
        return tracks
    
    
    def get_score(self, prec_features, new_features, popu, model, weight_pos = 1, weight_model = 1, weight_popu = 1):
        """Donnes un score à un ensemble de recommandations
        :param list of TrackFeatures (List of the class TrackFeatures): The features of the track in class put in a list
        :return list of score (list of float): List of score for each track
        """
        prec_features = prec_features[0]
        length = len(new_features)
        score_final = []
        i = 0
        scoring = 0
        for new_feature in new_features:
            data = [[new_feature.duration_ms, new_feature.danceability , new_feature.energy, new_feature.key, new_feature.loudness, new_feature.mode, new_feature.speechiness, new_feature.acousticness, new_feature.instrumentalness, new_feature.liveness, new_feature.valence, new_feature.tempo, new_feature.time_signature]]
            df = pd.DataFrame(data, columns=["duration_ms", 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature'])
            scoring_pos = (length - i) / length
            scoring_model = model.predict(df)
            popula = popu[i]
            scoring_popu = popula.popularity / 100
            print(scoring_popu)
            scoring = weight_pos * scoring_pos + weight_model * scoring_model[0] + weight_popu * scoring_popu

            i = i + 1
            score_final.append(scoring)

        return score_final
    

    def _place_get_api_request(self, url):
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token_user}"
            }
        )
        return response

    def _place_post_api_request(self, url, data):
        response = requests.post(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token_user}"
            }
        )
        return response

"""             if new_feature.danceability > 0.65:
                scoring = scoring + new_feature.danceability * weight_danceability
            if new_feature.danceability > prec_features.danceability :
                scoring = scoring + 1 * weight_danceability

            if new_feature.energy > prec_features.energy :
                scoring = scoring + new_feature.energy * weight_energy

            if (new_feature.key > prec_features.key - 3)  and (new_feature.key < prec_features.key + 3):
                scoring = scoring + 1 * weight_energy    

            if (new_feature.tempo > prec_features.tempo - 5)  and (new_feature.tempo < prec_features.tempo + 5):
                scoring = scoring + 1 * weight_tempo 
            if (new_feature.tempo > 125)  and (new_feature.tempo < 131):
                scoring = scoring + 1 * weight_tempo 
 """




