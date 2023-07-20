

######### Librairies #########
# Pour gérer le système
import os

# Pour la connexion avec Spotify
import spotipy
import spotipy.util as util
from spotifyclient import SpotifyClient
from features import Features

# Pour le script
import numpy as np
import heapq



def main():


    ######### Declare the credentials #########
    # Propre à notre application
    cid = '86696316a6b446188061b1dbe24eab70'
    secret = '1cca02c822f84043b9875cf8568d2f89'
    # Pour tester sur en local
    redirect_uri='http://localhost:7777/callback'
    # Pour les autorisations concernant l'utilisateur
    username = '21a2j53ksave2oldrdd54l4fq'


    ######### Authorization flow #########
    # Les différentes autorisations concernant l'application Spotify
    scope = "playlist-modify-public playlist-modify-private user-read-recently-played playlist-read-private playlist-read-collaborative"
    # Comme l'application n'est pas déclarée auprès de Spotify le Token dure juste 1h, il faut le recharger à chaque fois
    token = util.prompt_for_user_token(username, scope, client_id=cid, client_secret=secret, redirect_uri=redirect_uri)
    # Il est possible qu'on atteigne le nombre maximal de requêtes à un moment, il faudrat récréer une application sur le Dashboard

    # Génération du Token
    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", username)
    spotify_client = SpotifyClient(token, username)
    spotify_client2 = Features(token, username)


    ######### Begining of the script #########
    # get all the playlists from an user
    playlists = spotify_client.get_user_playlists(username)
    print("\nHere are all the playlists you have in your Spotify account: ")
    for index, playlist in enumerate(playlists):
        print(f"{index+1}- Le nom de la playlist est '{playlist.name}' - l'Id à recopier par la suite est: {playlist.id.split(':')[-1]}")
    
    
    # choose which playlist to use as a seed to generate a new playlist
    index_playlist = input("\nEnter the id of the playlist you want: ")


    # get the seeds of the tracks you want to put in the recommendation
    tracks = spotify_client.get_info_playlist(index_playlist)
    for index, track in enumerate(tracks):
        print(f"{index+1}- {track}")

    
    # Create seed tracks which will be used for the recommendation
    # Ici on met en place les paramètres que nous allons utiliser par la suite
    seed_tracks = [track.id for track in tracks] # Les ids des morceaux que nous allons jouer
    length = len(seed_tracks) 
    num_tracks_to_visualise = int(input("How many tracks would you like to add in your playlist ? ")) # Le nombre de morceaux que l'on veut rajouter à la playlist
    vect = np.linspace(0, length + num_tracks_to_visualise, length).astype(int) # La position des morceaux demandés par l'utilisateur qui veut jouer ses morceaux 
    
    
    # get recommended tracks based off seed tracks
    recommended_tracks = []
    # On positionne le premier song qui va être joué
    recommended_tracks.append(tracks[0])


    # Pour chaque morceaux de notre vect nous allons trouver les recommandations et donner un score qui va nous permettre de savoir quelle musique nous voulons jouer
    for i in range(0, len(vect)-1):
        # Permet de savoir le nombre final de recommendations que nous devons trouver à partir de ce titre
        num_tracks_to_recommend = vect[i+1] - vect[i]
        # Prépare la liste des scores
        score = [] 
        recommandations = spotify_client.get_track_recommendations([seed_tracks[i]], limit=num_tracks_to_recommend*2)
        for reco in recommandations: # On génére deux fois plus de recommandation car nous allons établir un score et juste prendre les meilleures
            score.append(reco.id)
        score = spotify_client.get_features(score) # Trop la flemme de réfléchir a comment emboiter les classes, à reprendre proprement
        features_prec = spotify_client.get_features([seed_tracks[i]])
        get_score_values = spotify_client.get_score(features_prec, score, weight_danceability = 1, weight_energy= 0.5, weight_key= 1, weight_loudness= 0.5, weight_valence= 0.5, weight_tempo= 2)
        get_score_ind = heapq.nlargest(num_tracks_to_recommend, range(len(get_score_values)), key=get_score_values.__getitem__)
        
        for j in get_score_ind:
            recommended_tracks.append(recommandations[j])
        recommended_tracks.append(tracks[i+1])
    for trak in spotify_client.get_track_recommendations([seed_tracks[len(vect)-1]], limit=num_tracks_to_recommend):
            recommended_tracks.append(trak)
    print("\nHere are the recommended tracks which will be included in your new playlist:")
    for index, track in enumerate(recommended_tracks):
        print(f"{index+1}- {track}")

    # get playlist name from user and create playlist
    playlist_name = input("\nWhat's the playlist name? ")
    playlist = spotify_client.create_playlist(spotify_client, playlist_name)
    print(f"\nPlaylist '{playlist.name}' was created successfully.")

    # populate playlist with recommended tracks
    spotify_client.populate_playlist(playlist, recommended_tracks)
    print(f"\nRecommended tracks successfully uploaded to playlist '{playlist.name}'.")


if __name__ == "__main__":
    main()