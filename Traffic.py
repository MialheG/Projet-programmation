# Taux de montée : 2500ft/min
# Taux de descente : 1250ft/min



class Flight:
    """Informations du vol qui nous seront utiles/ Plans de vols :
    - call_sign : l'identifiant du vol
    - start_t : temps de départ (temps du premier point de la route dans la simulation)
    - end_t : temps d'arrivée (temps du dernier point de la route dans la simulation)
    - route : la route du vol (liste de balises/ niveaux de vol)
    - speed : la vitesse du vol (en nœuds)
    - position : la position de l'avion à un moment donné (en coordonnées x,y,z)
    - heading : la direction de l'avion à un moment donné (en radians)
    - history : l'historique des positions de l'avion (liste de positions)
    - active : si le vol est présent ou non dans notre simulation (booléen)
    """
    
    def __init__(self, call_sign, speed):
        """Initialisation de la classe.
        """
        self.call_sign = call_sign
        self.speed = speed
        self.start_t = None
        self.end_t = None
        self.route = ()

        self.current_leg = 0
        start_point = self.route[0][0]  
        self.x = start_point.x
        self.y = start_point.y
        self.z = self.route[0][1] 

        self.heading = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.history = []

        self.active = False
        self.manual_heading = None

    def __repr__(self):
        """Représentation du vol.

        Returns:
            Une chaîne de caractères de la forme \"<traffic.Flight call_sign>\".
        """
        return f"<traffic.Flight {self.call_sign}>"

    def get_position(self, t):
        """Accès à la position de l'avion à un moment donné.

        Args:
            t:  (int)  un horodatage (en pas de temps)

        Returns:
            La position (geometry.Point) de l'avion au pas de temps `t`.

        Raises:
            IndexError: si le vol n'est pas sur l'aéroport à @c t.
        """
        return self.route[t - self.start_t]

