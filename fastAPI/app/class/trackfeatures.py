
class TrackFeatures:
    """Features representes the interesting parameters of the tracks"""

    def __init__(self, id, duration_ms, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature):
        """
        :param id (int): Spotify track id
        :param danceability (reél): Spotify feature
        :param energy (réel): Spotify feature
        :param Key (int): Spotify feature
        :param loudness (float): Spotify feature
        :param valence (float): Spotify feature
        :param tempo (float): Spotify feature
        """

        self.id = id
        self.duration_ms = duration_ms
        self.danceability = danceability
        self.energy = energy 
        self.key = key
        self.loudness = loudness
        self.mode = mode
        self.speechiness = speechiness
        self.acousticness = acousticness
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.valence = valence
        self.tempo = tempo
        self.time_signature = time_signature

    def __str__(self):
        return([self.duration_ms, self.danceability, self.energy, self.key, self.loudness, self.mode, self.speechiness, self.acousticness, self.instrumentalness, self.liveness, self.valence, self.tempo, self.time_signature]) 