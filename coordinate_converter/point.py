from coords import Coords

class Point:

    def __init__(self, str1, str2):

        self.lat = Coords(str1)
        self.long = Coords(str2)

    def convert_dms_2_dd(self, obj):

        if obj.dms_decimal:
            secdeci = obj.dms_seconds + "." + obj.dms_decimal
        else:
            secdeci = obj.dms_seconds

        sec = (float(secdeci) / (float(60)))
        min = ((float(obj.dms_minutes) + sec) / float(60))

        deg = (min + float(obj.dms_degrees))

        if obj.dms_sign == "negative":
            deg = (deg * -1)

        return deg

    def getlat(self):
        return self.lat

    def getlong(self):
        return self.long