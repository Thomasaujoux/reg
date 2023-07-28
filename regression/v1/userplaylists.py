
class Userplaylists:
    """Playlists of an user"""

    def __init__(self, name, id):
        """
        :param name (str): Playlist name
        :param id (int): Spotify playlist id
        """
        self.name = name
        self.id = id

    def __str__(self):
        id = self.id.split(":")[-1]
        return self.name + " is the playlist name, here is the id if you want to choose this playlist for the recommendation" + id