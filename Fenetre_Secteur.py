import sys
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QPolygon
from PyQt5.QtWidgets import QApplication, QWidget

import Geometrie
from Traffic import Flight
from Visualisation_traffic import Visualisation

# Constantes du Widget.
LARGEUR = 800           
HAUTEUR = 450         
AIRPORT_Z_VALUE = 0  

# Définition des points du secteur de controle.
pt_a = Geometrie.Point(210, 85, 0)
pt_b = Geometrie.Point(390, 60, 0)
pt_c = Geometrie.Point(565, 95, 0) 
pt_d = Geometrie.Point(630, 185, 0)
pt_e = Geometrie.Point(595, 295, 0)
pt_f = Geometrie.Point(475, 365, 0)
pt_g = Geometrie.Point(340, 380, 0)
pt_h = Geometrie.Point(235, 325, 0)
pt_i = Geometrie.Point(170, 230, 0)
pt_j = Geometrie.Point(180, 145, 0)

# Liste des points du secteur.
pt_secteur = [pt_a, pt_b, pt_c, pt_d, pt_e, pt_f, pt_g, pt_h, pt_i, pt_j]

class FenetreSecteur(QWidget):
    def __init__(self, pt_secteur :list[Geometrie.Point], list_balise :list[Balise.Balise], list_avion :list[Flight]):
        super().__init__()
        self.setWindowTitle("Secteur de controle - ZONE 1")
        self.setStyleSheet("background-color: #000000;")
        self.resize(LARGEUR, HAUTEUR)

        self.points = [QPoint(pt.x,pt.y) for pt in pt_secteur]
        
        self.z_min = 29000
        self.z_max = 41000
        self.balises = list_balise
        #self.avions = list_avion
        # Avions de tests (IMMOBILES).
        self.avions = [Visualisation(Flight("AFR123",Geometrie.Point(300, 150, 290),290,125)),
                        Visualisation(Flight("DLH456",Geometrie.Point(420, 200, 330),360,70)),
                        Visualisation(Flight("BAW789",Geometrie.Point(500, 300, 370),450,30)),
                        Visualisation(Flight("AFR321",Geometrie.Point(350, 300, 410),520,215))]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Echelle, adaptation à la taille de la fenêtre.
        echelle_x = self.width() / LARGEUR
        echelle_y = self.height() / HAUTEUR
        echelle = min(echelle_x, echelle_y)

        painter.save()
        painter.scale(echelle, echelle)

        # Configuration du contour (QPen) et du remplissage (QBrush) pour le polygone.
        pen_polygone = QPen(QColor("#195577"), 3, Qt.SolidLine)
        brush_polygone = QBrush(QColor("#111111"), Qt.SolidPattern)

        painter.setPen(pen_polygone)
        painter.setBrush(brush_polygone)

        # Création et tracé du polygone fermé.
        polygone = QPolygon(self.points)
        painter.drawPolygon(polygone)

        # Mise en évidence des points (sommets).
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#EE0000")))
        rayon = 4
        for pt in self.points:
            painter.drawEllipse(pt, rayon, rayon)

        # Dessin des avions.
        for avion in self.avions:
            avion.draw_plane(painter)

        painter.restore()
        painter.end()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = FenetreSecteur()
    fenetre.show()
    sys.exit(app.exec_())
