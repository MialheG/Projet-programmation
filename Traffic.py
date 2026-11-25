# Taux de montée : 2500ft/min
# Taux de descente : 1250ft/min
# z en FL 

import math

from Geometrie import Point

# Résultat : x et y en m, z en FL convverti directement en feet ; Cap normalement ok et vitesse qui en découle ; l'appel de 
# distance est ok (distance entre deux points en m), pas de prise en compte de z dans la méthode car on passe au dessus des balises

## Dans pyairport, la route est une liste de tuples qui se crée à l'aide du fichier texte où chaque ligne comporte les 
# caractéristiques de l'avion puis ses coordonnées sous la forme (x,y), le programme crée ensuite la liste route en 
# ajoutant des points que l'algo forme à partir des lignes de texte (via une méthode point_from_string).

class Flight:
    """Informations du vol qui nous seront utiles/ Plans de vols :
    - call_sign : l'identifiant du vol
    - start_t : temps de départ (temps du premier point de la route dans la simulation)
    - end_t : temps d'arrivée (temps du dernier point de la route dans la simulation)
    - route : la route du vol (liste de (balises, niveaux de vol))
    - speed : la vitesse du vol (en nœuds)
    - position : la position de l'avion à un moment donné (en coordonnées x,y,z)
    - heading : la direction de l'avion à un moment donné (en radians)
    - history : l'historique des positions de l'avion (liste de positions)
    - active : si le vol est présent ou non dans notre simulation (booléen)
    """
    
    def __init__(self, call_sign, speed):
        self.call_sign = call_sign
        self.speed = speed
        self.start_t = None
        self.end_t = None
        self.route = ()

        self.current_beacon = 0  # Vers quelle balise l'avion se dirige-t-il actuellement (0 = première balise, 1 = deuxième balise, etc.)
        start_point = self.route[0][0]  
        self.x = start_point.x
        self.y = start_point.y
        self.z = self.route[0][1] * 100  # Conversion en feet
        self.position = Point(self.x, self.y, self.z/100)

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
        return self.history[t - self.start_t]

    def update(self, current_time, dt):
        """Met à jour la position de l'avion en fonction du temps écoulé.

        Args:
            current_time:  (int)  le temps actuel
            dt:  (int)  le pas de temps écoulé depuis la dernière mise à jour
        """
        if current_time < self.start_t or current_time > self.end_t:
            return 

        self.active = True

        # Ajouter la position actuelle à l'historique et enlève les positions plus anciennes si nécessaire
        self.history.append((self.x, self.y, self.z))
        if len(self.history) > 10:
            self.history.pop(0) 

        speed_m_per_sec = self.speed*1852/3600  # Conversion de nœuds en m/s
        beacon_position = self.route[self.current_beacon][0]
        #current_position = Point(self.x, self.y, self.z)
        if beacon_position.distance(self.position) < speed_m_per_sec * dt:  # Si l'avion est proche de la balise actuelle
            self.current_beacon += 1  # Passer à la balise suivante
            if self.current_beacon < len(self.route):
                self.active = True  # L'avion est toujours actif tant qu'il n'a pas atteint la dernière balise
            
            else:
                self.active = False  # L'avion a atteint la dernière balise et n'est plus actif
                return
                
        # Calcul du cap (heading) et du vecteur vitesse vers la balise cible
        dx=beacon_position.x - self.x
        dy=beacon_position.y - self.y
        self.heading = math.degrees(math.atan2(dx, dy)%(2 * math.pi))  # Calcul du cap en radians

        self.vx = speed_m_per_sec * math.sin(math.radians(self.heading))  # Vitesse en x
        self.vy = speed_m_per_sec * math.cos(math.radians(self.heading))

        # Mettre à jour la position (x et y) de l'avion en fonction de sa vitesse et de sa direction
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Mettre à jour l'altitude de l'avion en fonction de la route et du temps écoulé
        if self.current_beacon < len(self.route):
            target_altitude = self.route[self.current_beacon][1] * 100
            altitude_difference = target_altitude - self.z

            if altitude_difference > 0:
                # Montée
                climb_rate = 2500 / 60  # ft/min converti en ft/sec
                self.z += min(climb_rate * dt, altitude_difference)
            elif altitude_difference < 0:
                # Descente
                descent_rate = 1250 / 60  # ft/min converti en ft/sec
                self.z += max(-descent_rate * dt, altitude_difference)
        
        self.position.x = self.x  # Mettre à jour la position de l'avion
        self.position.y = self.y  # Mettre à jour la position de l'avion
        self.position.z = self.z/100  # Mettre à jour la position de l'avion
