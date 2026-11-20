import math

class Point:

    def __init__(self, x, y,FL):
        """
        x:  (int)  the x-coordinate en metres
        y:  (int)  the y-coordinate en metres
        z:  (int)  the z-coordinate en niveau de vol
        """
        self.x = x
        self.y = y
        self.z = FL

    def __repr__(self):
        return f"({self.x}, {self.y},{self.z})"

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __rmul__(self, k):
        """
        k:  (int)  the multiplication factor
        """
        return Point(k * self.x, k * self.y, k * self.z)

    def __abs__(self):
        """
        Norme Euclidienne.
        Distance entre le point et l'origine  (0, 0).
        """
        return math.sqrt(self.x * self.x + self.y * self.y)

    def sca(self, other):
        """
        Produit Scalaire.
        Renvoie le produit scalaire d'un vecteur avec un autre.
        """
        return self.x * other.x + self.y * other.y

    def det(self, other):
        """
        Determinant.
        Renvoie de determinant d'un vecteur avec un autre.
        """
        return self.x * other.y - self.y * other.x

    def distance(self, other):
        """
        Distance euclidienne.
        Renvoie la distance entre deux points en metres (m).
        """
        return abs(self - other)

    def distance_to_segment(self, a, b):
        """Distance to a segment.

        Args:
            a:  (geometry.Point)  first end of the segment
            b:  (geometry.Point)  second end of the segment

        Returns:
            A float corresponding to the distance in meters
            to the segment delimited by points `a` and `b`.
        """
        ab = b - a
        ap = self - a
        bp = self - b
        if ab.sca(ap) <= 0:
            return abs(ap)
        elif ab.sca(bp) >= 0:
            return abs(bp)
        else:
            return abs(ab.det(ap)) / abs(ap)