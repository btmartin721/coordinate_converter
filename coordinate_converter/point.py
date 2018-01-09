from coords import Coords

class Point:

    def __init__(self, str1, str2, number):

        self.lat = Coords(str1, number)
        self.long = Coords(str2, number)

    def convert_dms_2_dd(self, obj):

        if obj.dms_decimal:
            secdeci = obj.dms_seconds + "." + obj.dms_decimal
        elif obj.dms_seconds:
            secdeci = obj.dms_seconds

        sec = (float(secdeci) / (float(60)))
        min = ((float(obj.dms_minutes) + sec) / float(60))

        dd = (min + float(obj.dms_degrees))

        if obj.dms_sign == "negative":
            dd = (dd * -1)

        return dd

    def getlat(self):
        return self.lat

    def getlong(self):
        return self.long

    def convert_ddm_2_dd(self, obj):

        mindec = obj.ddm_minutes + "." + obj.ddm_decimal
        min = ((float(mindec) / float(60)))
        dd = (float(obj.ddm_degrees) + min)

        if obj.ddm_sign == "negative":
            dd = (dd * -1)

        return dd

    def get_dd(self, obj):

        dd = obj.dd_degrees + "." + obj.dd_decimal

        if obj.dd_sign == "negative":
            dd = (float(dd) * -1)

        return dd