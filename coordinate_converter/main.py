#!/usr/bin/env python

import argparse
import re
import sys

from point import Point

# Gets command-line arguments using argparse
def get_arguments():
    parser = argparse.ArgumentParser(description="Converts coordinates from one format to another")

    parser.add_argument("-i", "--infile", type=str, required=True, help="Input filename; must be Comma Separated (CSV)")
    parser.add_argument("-o", "--outfile", type=str, required=False, help="Output filename; Default = out.csv",
                        nargs="?", default="out.csv")
    parser.add_argument("-f", "--format", type=str, required=False, nargs="?", default="dd",
                        help="Specify the output coordinate format; default = dd (decimal degrees)")
    parser.add_argument("-s", "--id", type=str, required=True, help="Sample ID column number (numbering starts on 1)")
    args = parser.parse_args()

    return args


# Reads comma-delimited file and gets index of 'latitude' and 'longitude' columns
def read_csv(infile):

    whole_line = []

    with open(infile, "rb") as fin:

        for line in fin:
            line = line.strip("\r\n")
            whole_line.append(line.strip().split(","))

    return whole_line

def convert_coords(lst):

    dms_lat = []
    dms_long = []
    linenumber = 0

    for line in lst:
        if linenumber == 0:
            first_line = line

            latitude = r"latitude"
            longitude = r"longitude"

            idx_lst1 = get_header_idx(first_line, latitude)
            idx_lst2 = get_header_idx(first_line, longitude)

            if len(idx_lst1) != 1:
                print("Error: There can only be one 'latitude' column")
                sys.exit(1)

            if len(idx_lst2) != 1:
                print("Error: There can only be one 'longitude' column")
                sys.exit(1)


        elif linenumber > 0:

            lat_idx = idx_lst1[0]
            lat = line[lat_idx]

            long_idx = idx_lst2[0]
            longit = line[long_idx]

            point = Point(lat, longit)
            dms_lat.append(point.convert_dms_2_dd(point.getlat()))
            dms_long.append(point.convert_dms_2_dd(point.getlong()))

        linenumber += 1

    return dms_lat, dms_long, first_line


# Make sure header line has columns named 'regex' and gets the associated index
def get_header_idx(first_line, regex):
    if regex in first_line:
        idx = [cnt for cnt, val in enumerate(first_line) \
               if re.search(regex, val.lower().strip())]

    else:
        print("Error: The header line must contain a column named '" + regex + "'")
        sys.exit(1)

    return idx

################################################################################################################
##############################################    MAIN    ######################################################
################################################################################################################

# Gets command-line arguments using argparse; argparse must be imported
args = get_arguments()

lines = read_csv(args.infile)

dms_lat, dms_long, header = convert_coords(lines)

#lat_direction = []
#long_direction = []

#lat_direction = read_coordinates(lat_lst)
#long_direction = read_coordinates(long_lst)