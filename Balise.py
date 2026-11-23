import random as rd
import Fenetre_Secteur
import Geometry

nbtoalpha = { 1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J", 11: "K", 12: "L", 13: "M", 14: "N", 15: "O", 16: "P", 17: "Q", 18: "R", 19: "S", 20: "T", 21: "U", 22: "V", 23: "W", 24: "X", 25: "Y", 26: "Z" }

class Balise:

    def __init__(self,Geometry.point):
        ## Nom balise :
        nomballist=[]
        for k in range(5):
            nomballist.append(nbtoalpha[rd.randint(1,26)])
        nombal=nomballist[0]+nomballist[1]+nomballist[2]+nomballist[3]+nomballist[4]
        
        self.nom=nombal
        self.point=point

    def __repr__(self):
        return "Balise "+self.nom+" en "+str(self.point)

    def surcontour(self,contour):
        if 1+1==2:
            return True
        pass
bal=Balise((0,0))
print(bal)














    
