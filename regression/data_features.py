import spotipy
from spotipy.oauth2 import SpotifyClientCredentials# Spotify credentials
from tqdm import tqdm
import os
import pandas as pd
import time

os.environ["SPOTIPY_CLIENT_ID"] = 'cae593fec3384b92892d0b6b26a910bd'
os.environ["SPOTIPY_CLIENT_SECRET"] = 'edbfb882cbf140bdabb5577bf0acb0b1'
os.environ['SPOTIPY_REDIRECT_URI'] = "http://localhost:8080"

sp = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials())

playlists =  pd.read_csv(r"C:\Users\Thomas Aujoux\Documents\GitHub\regression\raw_data.cvs")


def get_features(df):
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

   features = sp.audio_features(df['track_uri'])
   for track in features: 
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

   tracks = sp.tracks(pd.DataFrame(df[:50]['track_uri'].str.split(":", expand = True)).iloc[:,2])
   for track in tracks['tracks']: 
      popularity.append(track['popularity'])
    
   tracks = sp.tracks(pd.DataFrame(df[50:]['track_uri'].str.split(":", expand = True)).iloc[:,2])
   for track in tracks['tracks']:
      popularity.append(track['popularity'])
    
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
      



df = pd.DataFrame(columns=["playlist_id", "playlist_name", "track_number", "track_uri", "artist_name", "track_name", "album_name", "duration_ms", 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature', 'popularity'])
for i in range(983, 1000):
    df_new = get_features(playlists[0 + i*100 : 100 + i*100])
    df = pd.concat([df, df_new], axis=0, join='inner')
    time.sleep(1)


df['diff_duration_ms'] = df.groupby('playlist_id')['duration_ms'].diff()
df['diff_danceability'] = df.groupby('playlist_id')['danceability'].diff()
df['diff_energy'] = df.groupby('playlist_id')['energy'].diff()
df['diff_key'] = df.groupby('playlist_id')['key'].diff()
df['diff_loudness'] = df.groupby('playlist_id')['loudness'].diff()
df['diff_mode'] = df.groupby('playlist_id')['mode'].diff()
df['diff_speechiness'] = df.groupby('playlist_id')['speechiness'].diff()
df['diff_acousticness'] = df.groupby('playlist_id')['acousticness'].diff()
df['diff_instrumentalness'] = df.groupby('playlist_id')['instrumentalness'].diff()
df['diff_liveness'] = df.groupby('playlist_id')['liveness'].diff()
df['diff_valence'] = df.groupby('playlist_id')['valence'].diff()
df['diff_tempo'] = df.groupby('playlist_id')['tempo'].diff()
df['diff_time_signature'] = df.groupby('playlist_id')['time_signature'].diff()
df['diff_popularity'] = df.groupby('playlist_id')['popularity'].diff()

def conditions(s):
    if (s['playlist_id'] < 1000):
        return 1
    else:
        return 0
    
df['Class'] = df.apply(conditions, axis=1)


df.to_csv(r"C:\Users\Thomas Aujoux\Documents\GitHub\regression\raw_data_feature2.cvs")
data = pd.read_csv(r"C:\Users\Thomas Aujoux\Documents\GitHub\regression\raw_data_feature2.cvs")

new_data = data.groupby(['playlist_id'])[['popularity', 'duration_ms', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature', 'diff_popularity', 'diff_duration_ms', 'diff_danceability', 'diff_energy', 'diff_key', 'diff_loudness', 'diff_mode', 'diff_speechiness', 'diff_acousticness', 'diff_instrumentalness', 'diff_liveness', 'diff_valence', 'diff_tempo', 'diff_time_signature']].mean().reset_index()

new_data.to_csv(r"C:\Users\Thomas Aujoux\Documents\GitHub\regression\data_feature2.cvs")

# new_data = new_data.drop([ 'playlist_name', 'loudness', 'tempo'], axis = 1)

new_data.boxplot(vert = False, figsize = (13,7), showfliers = False, showmeans = True, 
                 patch_artist=True, boxprops=dict(linestyle='-', linewidth=1.5),
                 flierprops=dict(linestyle='-', linewidth=1.5),
                 medianprops=dict(linestyle='-', linewidth=1.5),
                 whiskerprops=dict(linestyle='-', linewidth=1.5),
                 capprops=dict(linestyle='-', linewidth=1.5))

plt.title("Original Playlist's Box Plot", fontsize=16, fontweight='heavy')
plt.show()

new_data.boxplot()
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.boxplot(data=new_data)

new_data.describe()