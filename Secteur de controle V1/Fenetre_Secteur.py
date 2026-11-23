import sys
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QPolygon
from PyQt5.QtWidgets import QApplication, QWidget
import Geometrie

LARGEUR = 800           
HAUTEUR = 450         
AIRPORT_Z_VALUE = 0  

class FenetreSecteur(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secteur de controle - ZONE 1")
        self.resize(LARGEUR, HAUTEUR)

        self.points = [
            QPoint(100, 120),
            QPoint(120, 220),
            QPoint(240, 180),
            QPoint(260, 70),
            QPoint(180, 100)]

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
        painter.setPen(QPen(QColor("#F30000"), 2))
        painter.setBrush(QBrush(QColor("#920202")))
        rayon = 5
        for pt in self.points:
            painter.drawEllipse(pt, rayon, rayon)

        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = FenetreSecteur()
    fenetre.show()
    sys.exit(app.exec_())