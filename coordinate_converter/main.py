#!/usr/bin/env python

import argparse
import re
import sys
import csv

from point import Point

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

    whole_line = []

    with open(infile, "rb") as fin:
        line1 = fin.readline().strip().split(",")
        for line in fin:
            line = line.strip("\r\n")
            if line.strip():
                whole_line.append(line.strip().split(","))

    return whole_line, line1

def get_index_from_regex(first_line):

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

    idx1 = idx_lst1[0]
    idx2 = idx_lst2[0]

    return idx1, idx2


# Make sure header line has columns named 'regex' and gets the associated index
def get_header_idx(first_line, regex):
    if regex in first_line:
        idx = [cnt for cnt, val in enumerate(first_line) \
               if re.search(regex, val.lower().strip())]

    else:
        print("Error: The header line must contain a column named '" + regex + "'")
        sys.exit(1)

    return idx

def write_output(line_lst, outfile, first_line):

    with open(outfile, "w") as out:
        csv_writer = csv.writer(out, delimiter=',', lineterminator="\n")
        csv_writer.writerow(first_line)
        for lne in line_lst:
            csv_writer.writerow(lne)



################################################################################################################
##############################################    MAIN    ######################################################
################################################################################################################

# Gets command-line arguments using argparse; argparse must be imported
args = get_arguments()

lines, header = read_csv(args.infile)

lat_idx, long_idx = get_index_from_regex(header)

line_number = 1

for line in lines:
    lat = line[lat_idx]
    longit = line[long_idx]

    point = Point(lat, longit, line_number)

    line_number += 1
    dms_lat, ddm_lat, dd_lat = point.lat.parse_coordinates(lat, line_number)
    dms_long, ddm_long, dd_long = point.lat.parse_coordinates(longit, line_number)

    if dms_lat and dms_long:
        dms_final_lat = point.convert_dms_2_dd(point.getlat())
        dms_final_long = point.convert_dms_2_dd(point.getlong())
        line[lat_idx] = dms_final_lat
        line[long_idx] = dms_final_long

    elif ddm_lat and ddm_long:
        ddm_final_lat = point.convert_ddm_2_dd(point.getlat())
        ddm_final_long = point.convert_ddm_2_dd(point.getlong())
        line[lat_idx] = ddm_final_lat
        line[long_idx] = ddm_final_long

    elif dd_lat and dd_long:
        dd_final_lat = point.get_dd(point.getlat())
        dd_final_long = point.get_dd(point.getlong())
        line[lat_idx] = dd_final_lat
        line[long_idx] = dd_final_long

write_output(lines, args.outfile, header)
