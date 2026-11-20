import sys
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QBrush, QPainter, QPen, QPolygon
from PyQt5.QtWidgets import QApplication, QWidget


class FenetreSecteur(QWidget):
    def __init__self(self):
        super().__init__()
        self.setWidowtitle("Secteur de controle - ZONE 1")
        self.resize(250,250)

        self.points = [QPoint(100,120),
                       QPoint(120,220),
                       QPoint(240,180),
                       QPoint(260,70),
                       QPoint(180,100)]

    def paintEvent(self):
        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        # 1. Configuration du contour (QPen) et du remplissage (QBrush) pour le polygone
        pen_polygone = QPen(Qt.blue, 3, Qt.SolidLine)
        brush_polygone = QBrush(Qt.cyan, Qt.SolidPattern)

        painter.setPen(pen_polygone)
        painter.setBrush(brush_polygone)

        # Création et tracé du polygone fermé
        polygone = QPolygon(self.points)
        painter.drawPolygon(polygone)

        # 2. Mise en évidence des points (sommets)
        painter.setPen(QPen(Qt.darkRed, 2))
        painter.setBrush(QBrush(Qt.red))

if __name__ == "__main__":
  app = QApplication(sys.argv)
  fenetre = FenetreSecteur()
  fenetre.show()
  sys.exit(app.exec_())