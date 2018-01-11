import re
import sys

class Coords:

    pos = r"positive"
    neg = r"negative"

    def __init__(self, string, linenum, pos, neg):
        dms_lst, ddm_lst, dd_lst = self.parse_coordinates(string, linenum)
        if dms_lst:     # If input format is dms
            self.dms_degrees = dms_lst[2]
            self.dms_minutes = dms_lst[3]
            self.dms_seconds = dms_lst[4]
            self.dms_decimal = dms_lst[5]
            self.dms_sign = dms_lst[7]

        elif ddm_lst:     # If input format is ddm
            self.ddm_degrees = ddm_lst[2]
            self.ddm_minutes = ddm_lst[3]
            self.ddm_decimal = ddm_lst[4]
            self.ddm_sign = ddm_lst[6]

        elif dd_lst:     # If input format is dd
            self.dd_degrees = dd_lst[2]
            self.dd_decimal = dd_lst[3]
            self.dd_sign = dd_lst[4]

        self.pos = pos
        self.neg = neg

    def parse_coordinates(self, item, line_number):
        """
        :rtype: object
        """
        dms_regex = re.compile(
            ur"^\s*([A-Za-z]?)\s*(-?)(\d{1,3})\u00b0?\s+(\d{1,2})'?\s+(\d+)\"?\.?(\d*)\"?\s*([A-Za-z]?)$", re.UNICODE)

        ddm_regex = re.compile(ur"^\s*([A-Za-z]?)\s*(-?)(\d{1,3})\u00b0?\s+(\d{1,2})'?\.{1}(\d+)\"?\s*([A-Za-z]?)$",
                               re.UNICODE)

        dd_regex = re.compile(ur"^\s*([A-Za-z]?)\s*(-?)(\d+)\.{1}(\d+)\u00b0?\s*([A-Za-z]?)$", re.UNICODE)

        dms_temp = []
        ddm_temp = []
        dd_temp = []

        item = item.lstrip(' ')
        dms_match = dms_regex.search(item)
        ddm_match = ddm_regex.search(item)
        dd_match = dd_regex.search(item)

        if dms_match:
            dms_temp.append(dms_match.group(1))
            dms_temp.append(dms_match.group(2))
            dms_temp.append(dms_match.group(3))
            dms_temp.append(dms_match.group(4))
            dms_temp.append(dms_match.group(5))
            dms_temp.append(dms_match.group(6))
            dms_temp.append(dms_match.group(7))

            sign = self.check_direction(1, 7, dms_match)
            dms_temp.append(sign)

        elif ddm_match:
            ddm_temp.append(ddm_match.group(1))
            ddm_temp.append(ddm_match.group(2))
            ddm_temp.append(ddm_match.group(3))
            ddm_temp.append(ddm_match.group(4))
            ddm_temp.append(ddm_match.group(5))
            ddm_temp.append(ddm_match.group(6))

            sign = self.check_direction(1, 6, ddm_match)
            ddm_temp.append(sign)

        elif dd_match:
            dd_temp.append(dd_match.group(1))
            dd_temp.append(dd_match.group(2))
            dd_temp.append(dd_match.group(3))
            dd_temp.append(dd_match.group(4))

            sign = self.check_direction(1, 5, dd_match)
            dd_temp.append(sign)

        else:
            print("Error: Coordinate format not recognized on line " + str(line_number) + ": " + str(item) + "\n")
            print("Aborting program\n")
            sys.exit(1)

        return dms_temp, ddm_temp, dd_temp     # returns three lists containing coordinate parts

    def check_direction(self, group_number1, group_number2, match):     # Checks cardinal sign
        if match.group(group_number1) is "N" or match.group(group_number1) is "E":
            sign = Coords.pos
        elif match.group(group_number1) is "S" or match.group(group_number1) is "W":
            sign = Coords.neg
        elif (match.group(group_number1) is "S" or match.group(group_number1) is "W") and match.group(2):
            sign = Coords.neg
        elif not match.group(group_number1) and match.group(2):
            sign = Coords.neg
        elif match.group(group_number2) is "N" or match.group(group_number2) is "E":
            sign = Coords.pos
        elif match.group(group_number2) is "S" or match.group(group_number2) is "W":
            sign = Coords.neg
        elif (match.group(group_number2) is "S" or match.group(group_number2) is "W") and dash:
            sign = Coords.neg
        elif not match.group(group_number2) and match.group(2):
            sign = Coords.neg
        elif (not match.group(group_number1) and not match.group(group_number2)) and match.group(2):
            sign = Coords.neg
        elif not match.group(group_number1) and not match.group(group_number2) and not match.group(2):
            sign = Coords.pos
        else:
            sign = Coords.pos

        return sign

