import pandas as pd

from pydantic import BaseModel





def vector(song_ids, limit):

    length = len(song_ids)
    num_tracks_to_recommend = round(limit/length)

    vect = []
    vect.append(0)
    for i in range(1, length):
        vect.append(i * num_tracks_to_recommend + i)
    
    return vect, num_tracks_to_recommend


def spotify_reco(sp, song_id, limit):
    score = [] 
    recommandations = sp.recommendations(seed_tracks= song_id, limit=limit)
    for reco in recommandations["tracks"]:
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





def get_score(df, category, model, weight_pos = 1, weight_model = 1, weight_popu=1):
    prediction = pd.DataFrame(model.predict_proba(df))
    if category == "DJ":
       prediction = prediction.iloc[:,0]
    if category == "chill":
       prediction = prediction.iloc[:,1]
    if category == "date":
       prediction = prediction.iloc[:,2]
    if category == "melancholy":
       prediction = prediction.iloc[:,3]
    if category == "party":
       prediction = prediction.iloc[:,4]
    if category == "sport":
       prediction = prediction.iloc[:,5]
    if category == "study":
       prediction = prediction.iloc[:,6]
    predictions  = prediction.values.tolist() * weight_model  
    return prediction.values.tolist()
