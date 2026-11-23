import sys
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QPolygon
from PyQt5.QtWidgets import QApplication, QWidget
import Geometrie

LARGEUR = 800           
HAUTEUR = 450         
AIRPORT_Z_VALUE = 0  

# Définition des points du secteur de controle
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

pt_secteur = [pt_a, pt_b, pt_c, pt_d, pt_e, pt_f, pt_g, pt_h, pt_i, pt_j]

class FenetreSecteur(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secteur de controle - ZONE 1")
        self.setStyleSheet("background-color: #A0E2CC;")
        self.resize(LARGEUR, HAUTEUR)
        """
        self.points = [
            QPoint(375, 45),   # Nord (Dunkerque)
            QPoint(535, 115),  # Alsace (Strasbourg)
            QPoint(505, 165),  # Franche-Comté / Jura
            QPoint(525, 225),  # Alpes du Nord (Savoie)
            QPoint(535, 325),  # Alpes du Sud / Nice
            QPoint(425, 380),  # Côte d'Azur (Toulon / Marseille)
            QPoint(255, 385),  # Pays Basque (Biarritz)
            QPoint(240, 250),  # Gironde / Charente
            QPoint(125, 195),  # Bretagne Sud (Finistère)
            QPoint(135, 165),  # Bretagne Nord
            QPoint(225, 125),  # Pointe du Cotentin (Cherbourg)
            QPoint(310, 105),  # Normandie / Picardie
        ]
        """
        self.points = [
            QPoint(pt_a.x, pt_a.y),
            QPoint(pt_b.x, pt_b.y),
            QPoint(pt_c.x, pt_c.y),
            QPoint(pt_d.x, pt_d.y),
            QPoint(pt_e.x, pt_e.y),
            QPoint(pt_f.x, pt_f.y),
            QPoint(pt_g.x, pt_g.y),
            QPoint(pt_h.x, pt_h.y),
            QPoint(pt_i.x, pt_i.y),
            QPoint(pt_j.x, pt_j.y)]
        
        self.z_min = 29000
        self.z_max = 41000

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        echelle_x = self.width() / LARGEUR
        echelle_y = self.height() / HAUTEUR
        echelle = min(echelle_x, echelle_y)

        painter.save()
        painter.scale(echelle, echelle)

        # 1. Configuration du contour (QPen) et du remplissage (QBrush) pour le polygone
        pen_polygone = QPen(QColor("#195577"), 3, Qt.SolidLine)
        brush_polygone = QBrush(QColor("#69C9A9"), Qt.SolidPattern)

        painter.setPen(pen_polygone)
        painter.setBrush(brush_polygone)

        # Création et tracé du polygone fermé
        polygone = QPolygon(self.points)
        painter.drawPolygon(polygone)

        # 2. Mise en évidence des points (sommets)
        painter.setPen(QPen(QColor("#860000FF"), 2))
        painter.setBrush(QBrush(QColor("#EE0000")))
        rayon = 4
        for pt in self.points:
            painter.drawEllipse(pt, rayon, rayon)

        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = FenetreSecteur()
    fenetre.show()
    sys.exit(app.exec_())