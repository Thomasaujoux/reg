import json
import requests


from track import Track
from playlist import Playlist
from userplaylists import Userplaylists
from trackfeatures import TrackFeatures
from spotifyuser import SpotifyUser

class SpotifyClient(SpotifyUser):
    """SpotifyClient performs operations using the Spotify API.
    Cette classe va permettre de réaliser toutes les opérations concernant la prise en compte
    des données du compte"""


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

    
    ######### Connaître les informations concernant les playlists de l'utilisateur #########    
    def get_user_playlists(self):
        """Get all the playlists from an user.
        :return playlists (list of playlists): List of playlists
        """
        url = f"https://api.spotify.com/v1/users/{self.username}/playlists"
        response = self._place_get_api_request(url)
        response_json = response.json()
        playlists = [Userplaylists(playlist["name"], playlist["uri"]) for playlist in response_json["items"]]
        return playlists
    
    def get_info_playlist(self, seed_playlist):
        """Get the tracks of an user playlist
        :param seed_playlist (playlist id): The playlist the user choosen
        :return tracks (list of Track): List of tracks in the playlist
        """
        url = f"https://api.spotify.com/v1/playlists/{seed_playlist}/tracks"
        response = self._place_get_api_request(url)
        response_json = response.json()
        tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"]) for track in response_json["items"]]
        return tracks


    ######### Connaitre en direct ce que l'utilisateur joue #########
    def get_last_played_tracks(self, limit=10):
        """Get the last n tracks played by a user

        :param limit (int): Number of tracks to get. Should be <= 50
        :return tracks (list of Track): List of last played tracks
        """
        url = f"https://api.spotify.com/v1/me/player/recently-played?limit={limit}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"]) for track in response_json["items"]]
        return tracks
    


    ######### Modifier les playlists de l'utilisateur #########
    def create_playlist(self, name):
        """
        :param name (str): New playlist name
        :return playlist (Playlist): Newly created playlist
        """
        data = json.dumps({
            "name": name,
            "description": "Recommended songs",
            "public": True
        })
        url = f"https://api.spotify.com/v1/users/{self.username}/playlists"
        response = self._place_post_api_request(url, data)
        response_json = response.json()
        # create playlist
        playlist_id = response_json["id"]
        playlist = Playlist(name, playlist_id)
        return playlist

    def populate_playlist(self, playlist, tracks):
        """Add tracks to a playlist.

        :param playlist (Playlist): Playlist to which to add tracks
        :param tracks (list of Track): Tracks to be added to playlist
        :return response: API response
        """
        track_uris = [track.create_spotify_uri() for track in tracks]
        data = json.dumps(track_uris)
        url = f"https://api.spotify.com/v1/playlists/{playlist.id}/tracks"
        response = self._place_post_api_request(url, data)
        response_json = response.json()
        return response_json
    



    ######### Envoyer les requetes Get et Post #########
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
        tracks = [TrackFeatures(track['id'], track["danceability"], track["energy"], track["key"], track['loudness'], track["valence"], track['tempo']) for track in response_json["audio_features"]]
        return tracks
    

    
    def get_score(self, prec_features, new_features, weight_danceability = 1, weight_energy= 0.5, weight_key= 1, weight_loudness= 0.5, weight_valence= 0.5, weight_tempo= 2):
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
            scoring = (length - i) * 0.7

            if new_feature.danceability > 0.65:
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

            i = i + 1
            score_final.append(scoring)
        return score_final
    


