

######### Importation des librairies #########

#  Librairies pour les class
from spotifyuser import SpotifyUser
from spotifyclient import SpotifyClient
from features import Features 

# Pour le script
import numpy as np
import heapq

def main():




    ######### Identification de l'utilisateur #########
    # Arrivé de l'utilisateur sur l'application, il rentre ses identifiants, ect ...
    print("\nBonjour, bienvenu dans notre application. Nous sommes pour le moment en phase de développement")
    print("\nVeuillez rentrer dans l'application les informations suivantes: ")
 #   fname = input("\nVotre prénom:")
 #   name = input("\nVotre nom:")
 #   email = input("\nVotre email:")
 #   username = input("\nVotre nom d'utilisateur qui se trouve dans les réglages de votre compte Spotify:")
    fname = "Thomas"
    name = "Aujoux"
    email = "thomas.aujoux@gmail.com"
    username = "21a2j53ksave2oldrdd54l4fq"

    # Génération du token, utile pour la suite
    spotify_user = SpotifyUser(fname, name, email, username)
    spotify_user.token()





    ######### On prend les information de l'utilisateur concernant ses playlists #########
    client = SpotifyClient(fname, name, email, username)
    client.token()
    # get all the playlists from an user
    playlists = client.get_user_playlists()
    print("\nHere are all the playlists you have in your Spotify account: ")
    for index, playlist in enumerate(playlists):
        print(f"{index+1}- Le nom de la playlist est '{playlist.name}' - l'Id à recopier par la suite est: {playlist.id.split(':')[-1]}")




    ######### Mets en marche l'algorithme de regression #########
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sb

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

    #y_pred = model.predict(X_test)


    ######### On commence à demander à l'utilisateur sur quelle playlist il veut générer des nouveaux titres #########
    # choose which playlist to use as a seed to generate a new playlist
    index_playlist = input("\nEnter the id of the playlist you want: ")

    # get the seeds of the tracks you want to put in the recommendation
    tracks = client.get_info_playlist(index_playlist)
    for index, track in enumerate(tracks):
        print(f"{index+1}- {track}")






    ######### La partie pour la recommendation des musiques #########
    recom = Features(fname, name, email, username)
    recom.token()
    # Create seed tracks which will be used for the recommendation
    # Ici on met en place les paramètres que nous allons utiliser par la suite
    seed_tracks = [track.id for track in tracks] # Les ids des morceaux que nous allons jouer
    length = len(seed_tracks) 
    num_tracks_to_visualise = int(input("How many tracks would you like to approximatyvely add in your playlist ? ")) # Le nombre de morceaux que l'on veut rajouter à la playlist
    print("\nLe nombre de musiques affichés ne correspondra pas parfaitement, car l'algorithme choisira le nombre optimal: ")
    num_tracks_to_recommend = round(num_tracks_to_visualise/length) # Permet de savoir le nombre final de recommendations que nous devons trouver à partir de ce titre
    vect = []
    vect.append(0)
    for i in range(1, length):
        vect.append(i * num_tracks_to_recommend + 1)

    # get recommended tracks based off seed tracks
    recommended_tracks = []
    # On positionne le premier song qui va être joué
    recommended_tracks.append(tracks[0])

    # On commence la boucle pour les recommandations 
    # Pour chaque morceaux de notre vect nous allons trouver les recommandations et donner un score qui va nous permettre de savoir quelle musique nous voulons jouer
    for i in range(0, len(vect)-1):
        # Prépare la liste des scores
        score = [] 
        recommandations = recom.get_track_recommendations([seed_tracks[i]], limit = 50)
        for reco in recommandations: # On génére deux fois plus de recommandation car nous allons établir un score et juste prendre les meilleures
            score.append(reco.id)
        score = recom.get_features(score) # Trop la flemme de réfléchir a comment emboiter les classes, à reprendre proprement
        features_prec = recom.get_features([seed_tracks[i]])
        popu = recom.get_popularity(score)
        get_score_values = recom.get_score(features_prec, score, popu, model, weight_pos = 0, weight_model = 0.25, weight_popu=1)
        #print(get_score_values)
        get_score_ind = heapq.nlargest(num_tracks_to_recommend, range(len(get_score_values)), key=get_score_values.__getitem__)
        #print(get_score_ind)
        
        for j in get_score_ind:
            recommended_tracks.append(recommandations[j])
        recommended_tracks.append(tracks[i+1])
    
    # On termine par remplir les dernières recommandations
    score = [] 
    recommandations = recom.get_track_recommendations([seed_tracks[len(vect)-1]], limit = 50)
    for reco in recommandations: # On génére deux fois plus de recommandation car nous allons établir un score et juste prendre les meilleures
        score.append(reco.id)
    score = recom.get_features(score) # Trop la flemme de réfléchir a comment emboiter les classes, à reprendre proprement
    features_prec = recom.get_features([seed_tracks[len(vect)-1]])
    popu = recom.get_popularity(score)
    get_score_values = recom.get_score(features_prec, score, popu, model, weight_pos = 0, weight_model = 0.25, weight_popu=1)
    print(get_score_values)
    get_score_ind = heapq.nlargest(num_tracks_to_recommend, range(len(get_score_values)), key=get_score_values.__getitem__)
    print(get_score_ind)

    # 0 : 0.25 : 1 / 0 : 1 : 0.25 / 1 : 0 : 0 / 0 : 0  : 1
    # 0 : 0.5 : 1 / 0 : 1 : 0.25 / 0 : 0.25 : 1 / 0 : 0  : 1
    
    for j in get_score_ind:
            recommended_tracks.append(recommandations[j])

    




    ######### On affiche la playlist que l'on a générée #########
    print("\nHere are the recommended tracks which will be included in your new playlist:")
    for index, track in enumerate(recommended_tracks):
        print(f"{index+1}- {track}")






    ######### La partie pour créer la playlist et mettre les morceaux recommandés #########
    # get playlist name from user and create playlist
    playlist_name = input("\nWhat's the playlist name? ")
    playlist = client.create_playlist(playlist_name)
    print(f"\nPlaylist '{playlist.name}' was created successfully.")

    # populate playlist with recommended tracks
    client.populate_playlist(playlist, recommended_tracks)
    print(f"\nRecommended tracks successfully uploaded to playlist '{playlist.name}'.")




if __name__ == "__main__":
    main()