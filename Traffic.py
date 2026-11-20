



class Flight:
    """Informations du vol qui nous seront utiles/ Plans de vols :
    - call_sign : l'identifiant du vol
    - start_t : temps de départ (temps du premier point de la route dans la simulation)
    - end_t : temps d'arrivée (temps du dernier point de la route dans la simulation)
    - route : la route du vol (liste de points, chaque point est un tuple (x, y, z) représentant les coordonnées du vol à un instant donné)
    """
    
    def __init__(self, call_sign):
        """Initialisation de la classe.
        """
        self.call_sign = call_sign
        self.start_t = None
        self.end_t = None
        self.route = ()

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

