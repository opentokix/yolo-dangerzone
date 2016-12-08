#!/usr/bin/python
"""Reading two metrics from the last hour and doing statistic correlation."""

from scipy.stats.stats import pearsonr
import requests
import urllib
import sys
import getopt


def usage(message, code=0):
    """Usage."""
    print usage.__doc__
    print message
    sys.exit(code)


def get_data(host, port, location):
    """Fetch data with functions from graphite and return."""
    if location is None:
        usage("Datalocation must be defined", 255)

    proto = "http"
    graphite_url = "%s://%s:%s/render?" % (proto, host, str(port))
    data = {"target": location,
            "format": "json",
            "from": "-65min",
            "to": "-5min"}
    querystring = urllib.urlencode(data)
    url = graphite_url + querystring
    try:
            r = requests.get(url)
    except requests.exceptions.RequestException as e:
            usage(e, 253)
    try:
            return r.json()[0][u'datapoints']
    except (IndexError, ValueError), e:
            usage(e, 254)


def main(argv):
    """Main function."""
    try:
        opts, args = getopt.getopt(argv, 'hc:w:G:A:B:')
    except getopt.GetoptError:
        usage("Unknown option", 255)

    # Setting defaults
    warn = 95
    crit = 50
    graphite_host = "127.0.0.1"
    source_a = None
    source_b = None

    for opt, arg in opts:
        if opt in ('-w'):
            warn = float(arg)
        elif opt in ('-c'):
            crit = float(arg)
        elif opt in ('-G'):
            graphite_host = arg
        elif opt in ('-A'):
            source_a = arg
        elif opt in ('-B'):
            source_b = arg
        elif opt in ('-h'):
            usage(None, 0)

    a = get_data(graphite_host, 80, source_a)
    b = get_data(graphite_host, 80, source_b)

    aa = []
    bb = []
    for item in a:
        aa.append(item[0])
    for item in b:
        bb.append(item[0])

    len_a = len(aa)
    len_b = len(bb)

    print pearsonr(aa[:60], bb[:60])

if __name__ == '__main__':
    main(sys.argv[1:])
