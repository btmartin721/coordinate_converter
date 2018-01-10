from coords import Coords

class Point:

    def __init__(self, str1, str2, number):

        self.lat = Coords(str1, number)
        self.long = Coords(str2, number)

    def getlat(self):
        return self.lat

    def getlong(self):
     return self.long