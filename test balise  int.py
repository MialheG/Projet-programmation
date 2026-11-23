import random
import Geometrie

import Balise
import Fenetre_Secteur
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPolygon
from shapely.geometry import Polygon
import matplotlib.pyplot as plt


class Polygone :
    def __init__(self, Lpoints : list[Geometrie.Point]): 
        self.points=Lpoints
        self.xmin=min([point.x for point in self.points])
        self.xmax=max([point.x for point in self.points])
        self.ymin=min([point.y for point in self.points])
        self.ymax=max([point.y for point in self.points])

    def tracé(self):
        x = [point.x for point in self.points]+[self.points[0].x]
        y = [point.y for point in self.points]+[self.points[0].y]
        plt.plot(x, y)
        plt.plot([self.xmin,self.xmin, self.xmax, self.xmax,self.xmin], [self.ymin, self.ymax, self.ymax, self.ymin, self.ymin])
        plt.show()

    def contient(self,Balise:Balise):
        if self.xmin<=Balise.point.x<=self.xmax and self.ymin<=Balise.point.y<=self.ymax:
            return True
        else:
            return False
        
pol=Polygone(Fenetre_Secteur.pt_secteur)
pol.tracé()
bali=Balise.Balise(Geometrie.Point(300, 200))
print(pol.contient(bali))
