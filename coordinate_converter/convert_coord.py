#!/usr/bin/env python

import argparse
import sys
import csv

from point import Point
import conversions as math


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

    idx1 = get_header_idx(first_line, latitude)
    idx2 = get_header_idx(first_line, longitude)

    return idx1, idx2


def write_output(line_lst, outfile, first_line):
    with open(outfile, "w") as out:
        csv_writer = csv.writer(out, delimiter=',', lineterminator="\n")
        csv_writer.writerow(first_line)
        for lne in line_lst:
            csv_writer.writerow(lne)


# Make sure header line has columns named 'regex' and gets the associated index
def get_header_idx(first_line, regex):
    if regex in first_line:
        idx = first_line.index(regex.lower().strip())

    else:
        print("Error: The header line must contain a column named '" + regex + "'")
        sys.exit(1)

    return idx


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
    dms_long, ddm_long, dd_long = point.long.parse_coordinates(longit, line_number)

    format = args.format.lower().strip()

    if format == "dd":

        if dms_lat and dms_long:
            dms2dd_lat = math.convert_dms_2_dd(point.getlat())
            dms2dd_long = math.convert_dms_2_dd(point.getlong())
            line[lat_idx] = dms2dd_lat
            line[long_idx] = dms2dd_long

        elif ddm_lat and ddm_long:
            ddm2dd_lat = math.convert_ddm_2_dd(point.getlat())
            ddm2dd_long = math.convert_ddm_2_dd(point.getlong())
            line[lat_idx] = ddm2dd_lat
            line[long_idx] = ddm2dd_long

        elif dd_lat and dd_long:
            dd2dd_lat = math.get_dd_from_dd(point.getlat())
            dd2dd_long = math.get_dd_from_dd(point.getlong())
            line[lat_idx] = dd2dd_lat
            line[long_idx] = dd2dd_long

    elif format == "dms":

        if dd_lat and dd_long:
            dd2dms_lat = math.convert_dd_2_dms(point.getlat())
            dd2dms_long = math.convert_dd_2_dms(point.getlong())
            line[lat_idx] = dd2dms_lat
            line[long_idx] = dd2dms_long

    elif format =="ddm":

            dd2ddm_lat = math.convert_dd_2_ddm(point.getlat())
            dd2ddm_long = math.convert_dd_2_ddm(point.getlong())
            line[lat_idx] = dd2ddm_lat
            line[long_idx] = dd2ddm_long

write_output(lines, args.outfile, header)

print(lines)
