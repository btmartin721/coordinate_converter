from coords import Coords

class Point:

    def __init__(self, str1, str2, number):

        self.lat = Coords(str1, number, "N", "S")     # Create lat object
        self.long = Coords(str2, number, "E", "W")    # Create long object

    def getlat(self):
        return self.lat

    def getlong(self):
     return self.long
