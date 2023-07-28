
################# Librairies  #################
import os
import json
import pandas as pd



################# Importation des playlists utiles  #################

def loop_slices(path, category, num_slices=20):
  cnt = 0 # We initiate the number of file to 0
  mpd_playlists = pd.DataFrame(columns=["playlist_id", "playlist_name", "track_number", "track_uri", "artist_name", "track_name", "album_name", "duration_ms"]) # Create the DataFrame for the playlists
  filenames = os.listdir(path) # get all the file paths
  id = 0 + 1000

  for fname in sorted(filenames):

    print(fname)
    if fname.startswith("mpd.slice.") and fname.endswith(".json"):
      cnt += 1
      fullpath = os.sep.join((path, fname))
      f = open(fullpath)
      js = f.read()
      f.close()
      current_slice = json.loads(js)      
      
      # Create a list of all playlists
      for playlist in current_slice['playlists']:
        if len([e for e in category if e in playlist["name"]]) > 0:
          for track in playlist["tracks"]:
            entry = pd.DataFrame.from_dict({"playlist_id": id, "playlist_name": playlist["name"],"track_number": track["pos"], "track_uri": track['track_uri'], "artist_name": track['artist_name'], "track_name": track['track_name'], "album_name": track['album_name'], "duration_ms": track['duration_ms']})
            mpd_playlists = pd.concat([mpd_playlists, entry], ignore_index=True)
          id = id + 1
    
      if cnt == num_slices:
        break

  return mpd_playlists# Path where the json files are extracted


################# For the party  #################
path = 'C:\\Users\\Thomas Aujoux\\Documents\\GitHub\\regression\\data\\'
num_slices = 100
#category = ["party", "soiree", "festivity", "fete", "event", "dance", "fête", "soirée", "DJ", "dj", "Dj" ]
#category = ["soiree", "festivity", "fete", "event", "fête", "soirée", "DJ", "dj", "Dj"]
category = ["party", "DJ"]

playlists_party  = loop_slices(path, category, num_slices)
names = pd.DataFrame(playlists_party.playlist_name.unique())
searchfor = ['Khaled', 'Snake'] # Playlist we want to delete
playlists_party = playlists_party[~playlists_party.playlist_name.str.contains('|'.join(searchfor))]
length = len(pd.DataFrame(playlists_party.playlist_id.unique()))


################# For the chill  #################
path = 'C:\\Users\\Thomas Aujoux\\Documents\\GitHub\\regression\\data\\'
num_slices = 50
category = ["chill"]

playlists_chill  = loop_slices(path, category, num_slices)
names = pd.DataFrame(playlists_chill.playlist_name.unique())
length = len(pd.DataFrame(playlists_chill.playlist_id.unique()))



################# Save the playlist  #################

df = pd.concat([playlists_party, playlists_chill], ignore_index=True)
df.to_csv(r"C:\Users\Thomas Aujoux\Documents\GitHub\regression\raw_data.cvs")