import re

class Coords:

    pos = r"positive"
    neg = r"negative"

    def __init__(self, string):

        dms_lst, ddm_lst = self.parse_coordinates(string)

        if dms_lst:
            self.dms_degrees = dms_lst[2]
            self.dms_minutes = dms_lst[3]
            self.dms_seconds = dms_lst[4]
            self.dms_decimal = dms_lst[5]
            self.dms_sign = dms_lst[7]

        if ddm_lst:
            self.ddm_degrees = lst[2]
            self.ddm_minutes = lst[3]
            self.ddm_decimal = lst[4]
            self.ddm_sign = lst[6]

    def parse_coordinates(self, item):
        """
        :rtype: object
        """
        dms_regex = re.compile(
            ur"^\s*([A-Za-z]?)\s*(-?)(\d{1,3})\u00b0?\s+(\d{1,2})'?\s+(\d+)\"?\.?(\d*)\"?\s*([A-Za-z]?)$", re.UNICODE)
        ddm_regex = re.compile(ur"^\s*([A-Za-z]?)\s*(-?)(\d{1,3})\u00b0?\s+(\d{1,2})'?\.{1}(\d+)\"?\s*([A-Za-z]?)$",
                               re.UNICODE)
        line_number = 0

        dms_lst = []
        ddm_lst = []

        # for item in lst:
        item = item.lstrip(' ')
        dms_match = dms_regex.search(item)
        ddm_match = ddm_regex.search(item)
        line_number += 1

        if dms_match:
            dms_lst.append(dms_match.group(1))
            dms_lst.append(dms_match.group(2))
            dms_lst.append(dms_match.group(3))
            dms_lst.append(dms_match.group(4))
            dms_lst.append(dms_match.group(5))
            dms_lst.append(dms_match.group(6))
            dms_lst.append(dms_match.group(7))

            sign = self.check_direction(1, 7, dms_match, line_number)
            dms_lst.append(sign)

        if ddm_match:
            ddm_lst.append(ddm_match.group(1))
            ddm_lst.append(ddm_match.group(2))
            ddm_lst.append(ddm_match.group(3))
            ddm_lst.append(ddm_match.group(4))
            ddm_lst.append(ddm_match.group(5))
            ddm_lst.append(ddm_match.group(6))

            sign = self.check_direction(1, 6, ddm_match, line_number)
            ddm_lst.append(sign)

        return dms_lst, ddm_lst

    def check_direction(self, group_number1, group_number2, match, line):
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
        elif (match.group(group_number2) is "S" or match.group(group_number2) is "W") and match.group(2):
            sign = Coords.neg
        elif not match.group(group_number2) and match.group(2):
            sign = Coords.neg
        elif not match.group(group_number1) and not match.group(group_number2) and not match.group(2):
            print("Warning: No cardinal direction or negative sign defined on line(s) " + str(
                line) + "; default = + (N or E)")
            sign = Coords.pos
        else:
            print ("Error with cardinal direction")
            exit(1)

        return sign

