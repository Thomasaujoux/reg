





class TrackPopularity:
    """Features representes the interesting parameters of the tracks"""

    def __init__(self, id, popularity):
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
        self.popularity = popularity
    
    def __str__(self):
        return([self.popularity])