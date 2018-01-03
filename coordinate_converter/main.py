#!/usr/bin/env python

import argparse
import csv
import re
import sys

from coordlists import Coords

# Gets command-line arguments using argparse
def get_arguments():
    parser = argparse.ArgumentParser(description="Converts coordinates from one format to another")

    parser.add_argument("-i", "--infile", type=str, required=True, help="Input filename; must be Comma Separated (CSV)")
    parser.add_argument("-o", "--outfile", type=str, required=False, help="Output filename; Default = out.csv",
                        nargs="?", default="out.csv")
    parser.add_argument("-f", "--format", type=str, required=False, nargs="?", default="dd",
                        help="Specify the output coordinate format; default = dd (decimal degrees)")
    args = parser.parse_args()

    return args


# Reads comma-delimited file and gets index of 'latitude' and 'longitude' columns
def read_csv(infile):
    with open(infile, "rb") as fin:

        linenumber = 0

        lat_col = []
        long_col = []

        readCSV = csv.reader(fin, delimiter=",")

        for line in readCSV:
            if linenumber == 0:
                header = line

                latitude = r"latitude"
                longitude = r"longitude"

                latIDXlst = check_if_string(header, latitude)
                longIDXlst = check_if_string(header, longitude)

            if linenumber > 0:

                if len(latIDXlst) == 1:
                    latIDX = latIDXlst[0]
                    lat_col.append(line[latIDX])
                else:
                    print("Error: There can only be one 'latitude' column")
                    sys.exit(1)

                if len(longIDXlst) == 1:
                    longIDX = longIDXlst[0]
                    long_col.append(line[longIDX])
                else:
                    print("Error: There can only be one 'longitude' column")
                    sys.exit(1)

            linenumber += 1

        # print(lat_col)
        # print(long_col)

    return lat_col, long_col


# Make sure header line has columns named 'regex' and gets the associated index
def check_if_string(first_line, regex):
    if regex in first_line:
        IDX = [cnt for cnt, val in enumerate(first_line) \
               if re.search(regex, val.lower().strip())]

    else:
        print("Error: The header line must contain a column named '" + regex + "'")
        sys.exit(1)

    return IDX


def read_coordinates(lst):
    dms_regex = re.compile(
        ur"^\s*([A-Za-z]?)\s*(-?)(\d{1,3})\u00b0?\s+(\d{1,2})'?\s+(\d+)\"?\.?(\d*)\"?\s*([A-Za-z]?)$", re.UNICODE)
    ddm_regex = re.compile(ur"^\s*([A-Za-z]?)\s*(-?)(\d{1,3})\u00b0?\s+(\d{1,2})'?\.{1}(\d+)\"?\s*([A-Za-z]?)$",
                           re.UNICODE)
    line_number = 0
    direction_lst = []

    for item in lst:
        item = item.lstrip(' ')
        # print(item)
        dms_match = dms_regex.search(item)
        ddm_match = ddm_regex.search(item)
        line_number += 1
        if dms_match:
            print("Entire match: " + dms_match.group())
            dms = Coords(dms_match.group())
            dms.add_parts(dms_match.group(2))
            dms.add_parts(dms_match.group(3))
            dms.add_parts(dms_match.group(4))
            dms.add_parts(dms_match.group(5))
            dms.add_parts(dms_match.group(6))

            sign = check_direction(1, 7, dms_match, line_number)
            # print(dir_sign + " " + dms_match.group(1) + " " + dms_match.group(7))
            # print(dir_sign + dms_match.group())
            # if dms_match.group(7) is "N" or dms_match.group(7) is "E":
            # sign = r"positive"
            # elif dms_match.group(7) is "S" or dms_match.group(7) is "W":
            # sign = r"negative"

            dms_signlst = Coords(sign)

        if ddm_match:
            print("Entire match: " + ddm_match.group())
            sign = check_direction(1, 6, ddm_match, line_number)
            ddm_signlst = Coords(sign)

    return direction_lst

    # elif ddm_match:
    # print("Entire match: " + ddm_match.group().lstrip('0'))

    # print(dms_dash)


def check_direction(group_number1, group_number2, match, line):
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


################################################################################################################
##############################################    MAIN    ######################################################
################################################################################################################

# Gets command-line arguments using argparse; argparse must be imported
args = get_arguments()

lat_lst, long_lst = read_csv(args.infile)

lat_direction = []
long_direction = []

lat_direction = read_coordinates(lat_lst)
long_direction = read_coordinates(long_lst)

# print(long_direction)


