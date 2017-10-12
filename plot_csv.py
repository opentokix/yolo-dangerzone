#!/usr/bin/env python
"""Program to take csv data from cbg project and plot."""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time
import sys
import getopt
from functools import wraps


global VERBOSE
VERBOSE = False


def verbose(func):
    """Decorator function for wallclock."""
    start_time = time.clock()
    wraps(func)

    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        if VERBOSE:
            end_time = time.clock()
            t = end_time - start_time
            print "%s wallclock: %f seconds" % (func.__name__, t)
        return res
    return wrapper


@verbose
def usage(message="", signal=0):
    """Program takes a CSV file on the format and plots graph."""
    info = """Format on expected csv file
    REQUEST_DATETIME,ID101,ID102,ID1,id1_diff,T2LIB_VER,STATUS,CONTENT_TYPE,XVALUE3
    2017-09-08 23:37:45,0,66,111,45,236,0,10,A01_ECSA1:1:1
    2017-09-08 23:39:49,0,510,563,53,236,40,30,B01_ECSA1:1028646091:208:239:1
    2017-09-08 23:39:51,0,500,542,42,236,0,11,B01_ECSA1
    2017-09-08 23:39:51,0,6,654,648,236,0,10,B01_ECSA1
    2017-09-08 23:39:58,0,5,124,119,236,42,30,A02_ECSA1:1005677816:208:239:1

    First line in file will be omitted
    Plots with matplotplib one column with dates on xaxis and values for y-axis

    Options:
        -f --file=      filename of csv file (required)
        -o --output=    image file name (png) (required)
        -w --width=     size in inches (default: 10)
        -h --height=    size in inches (default: 10)
        -d --dpi=       dpi (default: 300)
        -c --column=    column (required)
        -g --grid       grid toggle in plot
        -v --verbose    Verbose program info
    """
    if len(message) != 0:
        print "=================\nError:\n\n%s\n\n=======================" % message
    print info
    sys.exit(signal)


@verbose
def read_csv(file):
    """Reading csv file and returning numpy object."""
    data = np.genfromtxt(file,
                         skip_header=1,
                         delimiter=',',
                         dtype=None,
                         names=('time',
                                'id101',
                                'id102',
                                'id1',
                                'id1_diff',
                                't2lib_ver',
                                'status',
                                'type',
                                'xvalue3'))
    return data


@verbose
def plot_data(options, data):
    """Plotting data en returning figure."""
    color = 'cornflowerblue'
    wip_col = options['column']
    ax = plt.axes()
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
    ax.xaxis.grid(options['grid'])
    ax.yaxis.grid(options['grid'])
    ystart, yend = ax.get_ylim()
    try:
        plt.plot_date(mdates.datestr2num(data['time']),
                      data[wip_col],
                      xdate=True,
                      marker='8',
                      markersize='1',
                      color=color)
    except:
        usage("Unexpected error in plot function", 1)
    plt.xticks(rotation=90)
    plt.tick_params(axis='both', which='major', labelsize=4)
    try:
        plt.savefig(options['output'] + '.png',
                    figsize=(options['width'], options['height']),
                    dpi=options['dpi'])
    except:
        usage("Unexpected error in savefig function", 1)
    print "%s saved from %s datafile" % (options['output'], options['file'])
    return


@verbose
def parse_options(argv):
    """Generic options parser."""
    options = {}
    try:
        opts, args = getopt.getopt(argv, 'f:o:w:h:d:c:vhg',
                                   ['file=',
                                    'output=',
                                    'width=',
                                    'height=',
                                    'dpi=',
                                    'column=',
                                    'verbose',
                                    'help',
                                    'grid'])
    except getopt.GetoptError:
        usage("Options error", 1)
    # Setting defaults
    options['dpi'] = 300
    options['width'] = 10
    options['height'] = 10
    options['grid'] = False
    for opt, arg in opts:
        if opt in ['-h', '--help']:
            usage()
        elif opt in ['-f', '--file']:
            options['file'] = arg
        elif opt in ['-o', '--output']:
            options['output'] = arg
        elif opt in ['-w', '--width']:
            options['width'] = arg
        elif opt in ['-h', '--height']:
            options['height'] = arg
        elif opt in ['-d', '--dpi']:
            options['dpi'] = arg
        elif opt in ['-c', '--column']:
            options['column'] = arg
        elif opt in ['-v', '--verbose']:
            global VERBOSE
            VERBOSE = True
        elif opt in ['-g', '--grid']:
            options['grid'] = True
    if 'file' not in options:
        usage("Input file is a required options", 1)
    if 'output' not in options:
        usage("Output file is a required options", 1)
    if 'column' not in options:
        usage("Work column is a required options", 1)
    return options


@verbose
def main(argv):
    """Where the magic happens."""
    options = parse_options(argv)
    input_file = read_csv(options['file'])
    plot_data(options, input_file)


if __name__ == '__main__':
    main(sys.argv[1:])
