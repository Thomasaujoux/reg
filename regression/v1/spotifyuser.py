
######### Explications #########
# Cette class est propre à chaque utilisateurs, elle va permettre de lui associer un token ce qui va nous être utile pour la suite


######### Importation des librairies pour la class #########
# On utilise la librairie 
# Pour la connexion avec Spotify
import spotipy
import spotipy.util as util








class SpotifyUser:

    ######### Declare the credentials #########
    # Class attribute, this a the redirection uri, for the developement mode it is the localhost
    # We have to change it in the future
    redirect_uri='http://localhost:7777/callback'
    # cid, propre à notre application en mode développement, peut être changé par la suite
    cid = '86696316a6b446188061b1dbe24eab70'
    secret = '1cca02c822f84043b9875cf8568d2f89'

    ######### Authorization flow #########
    # Les différentes autorisations concernant l'application Spotify
    scope = "playlist-modify-public playlist-modify-private user-read-recently-played playlist-read-private playlist-read-collaborative"
    # En mode de développement on a le droit à toutes les autorisations que l'on veut

    def __init__(self, fname, name, email, username):
        # On initialise les variables de l'utilisateur pour lui créer un token par la suite
        # Pour que cela marche il est d'abord nécessaire de rajouter l'utilisateur sur le DashBoard, en mode de développement on a uniquement le droit à 25 utilisateurs
        self.fname = fname
        self.name = name
        self.email = email
        self.username = username

    def token(self):
        # Comme l'application n'est pas déclarée auprès de Spotify le Token dure juste 1h, il faut le recharger à chaque fois
        self.token_user = util.prompt_for_user_token(self.username, self.scope, self.cid, self.secret, self.redirect_uri)
        # Il est possible qu'on atteigne le nombre maximal de requêtes à un moment, il faudrat récréer une application sur le Dashboard
        # Génération du Token
        if self.token_user:
            print(f"Vous êtes bien identifié {self.fname} {self.name} vous pouvez commencer à utiliser l'application")
            self.sp = spotipy.Spotify(auth=self.token_user) 
        else:
            print(f"Can't get token for you {self.fname} {self.name}")

        