# coordinate_converter
Used to convert GPS coordinates from one format to another.

    Usage: ./convert_coord.py [command-line arguments]

For a list of arguments, use the help flag: 

    ./convert_coord -h

Required argument:

    -i, --infile [ filename ]: input file with coordinates, must be comma separated (CSV)
    
Optional arguments:

    -f, --format [ dms | ddm | dd ]: output coordinate format; default = 'dd' (decimal degrees)
    -o, --outfile [ filename ]: Specify output filename; default = out.csv
    -h, --help: Displays help menu
    
Accepted input coordinate formats include degrees minutes seconds (dms), decimal degree minutes
(ddm), and decimal degrees (dd).

Input file can have mixed formats, as long as the format is dms, ddm, or dd.

Current output coordinate formats include dms, ddm, and dd. I plan to add the ability to
convert to and from UTM coordinates in the future.
