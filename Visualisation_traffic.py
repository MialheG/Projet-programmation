import sys
from PyQt5.QtCore import QPointF, Qt, QLineF
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QPolygonF
from PyQt5.QtWidgets import QApplication, QWidget
import Geometrie
from Traffic import Flight

# Couleur de base test.
COULEUR_AVION = QColor("#000000")

# Dictionnaire des couleurs en fonction des niveaux de vol.
dict_clr = {
    290: QColor("#9DFF00"),
    300: QColor("#00FF15"),
    310: QColor("#00FF62"),
    320: QColor("#00FFAE"),
    330: QColor("#00FFD0"),
    340: QColor("#00E5FF"),
    350: QColor("#00BFFF"),
    360: QColor("#0084FF"),
    370: QColor("#002AFF"),
    380: QColor("#6200FF"),
    390: QColor("#9000FF"),
    400: QColor("#E100FF"),
    410: QColor("#FF00E1")}

# Couleurs situations critiques.
warning_clr = QColor("#FF6200")
danger_clr = QColor("#DF0000")

# Constantes de base.
LARGEUR_PEN = 1
NO_PEN = QPen(Qt.NoPen)
RAYON_LOSANGE = 5
FACTEUR_VITESSE = 0.08

class Visualisation:
    def __init__(self, vol):
        self.vol = vol

    # Couleur = f(FL).
    def get_color_FL(self):
        if self.vol.position.z <= 29499:
            return dict_clr[290]
        elif 29500 < self.vol.position.z <= 30499:
            return dict_clr[300]      
        elif 30500 < self.vol.position.z <= 31499:
            return dict_clr[310]     
        elif 31500 < self.vol.position.z <= 32499:
            return dict_clr[320]  
        elif 32500 < self.vol.position.z <= 33499:
            return dict_clr[330]
        elif 33500 < self.vol.position.z <= 34499:
            return dict_clr[340]
        elif 34500 < self.vol.position.z <= 35499:
            return dict_clr[350]
        elif 35500 < self.vol.position.z <= 36499:
            return dict_clr[360]
        elif 36500 < self.vol.position.z <= 37499:
            return dict_clr[370]
        elif 37500 < self.vol.position.z <= 38499:
            return dict_clr[380]
        elif 38500 < self.vol.position.z <= 39499:
            return dict_clr[390]
        elif 39500 < self.vol.position.z <= 40499:
            return dict_clr[400]
        elif 40500 < self.vol.position.z <= 41000:
            return dict_clr[410]

    # Attribue la couleur au stylo.
    def get_pen(self):
        return QPen(self.get_color_FL(), LARGEUR_PEN)

    # Dessine les avions (losange + Vecteur vitesse).
    def draw_plane(self, painter):
            painter.save()
            painter.translate(self.vol.position.x, self.vol.position.y)
            painter.rotate(self.vol.heading)

            couleur = self.get_color_FL()
            pen = self.get_pen()

            # Losange avec 4 coins.
            losange = QPolygonF([
                QPointF(0, -RAYON_LOSANGE),             
                QPointF(RAYON_LOSANGE * 0.75, 0),       
                QPointF(0, RAYON_LOSANGE),               
                QPointF(-RAYON_LOSANGE * 0.75, 0)])

            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawPolygon(losange)

            # Vecteur vitesse partant du coin avant.
            longueur_vecteur = max(0.0, self.vol.speed * FACTEUR_VITESSE)
            vecteur = QLineF(
                QPointF(0, -RAYON_LOSANGE),
                QPointF(0, -RAYON_LOSANGE - longueur_vecteur))
            painter.drawLine(vecteur)

            painter.restore()