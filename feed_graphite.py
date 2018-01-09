#!/usr/bin/env python
#

import socket
import time
import getopt
import sys


def usage():
    print """
    This program reads a value from stdin and sends to carbon server

    It has no built in looping function etc. So one example usage is:

    while true; do ps ax |grep "php-fpm"|grep -v grep|wc -l| \
    ./feed_graphite.py -H 127.0.0.1 -p 2003 -d localhost.fpmnum; sleep 5; done

    options:
        -h help
        -H graphite hosts
        -p graphite server port (default: 2003)
        -d graphite destination (foo.bar.baz) mandatory
            (default: i.forgot.something)
    """


def dump_to_carbon(server, port, payload):
    sock = socket.socket()
    sock.connect((server, port))
    sock.sendall(payload)
    sock.close()


def main(argv):
    carbon_port = 2003
    carbon_dest = "undefined"

    try:
        opts, args = getopt.getopt(argv, 'd:h:p:H:')
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-h'):
            usage()
            sys.exit(1)
        elif opt in ('-H'):
            carbon_host = arg
        elif opt in ('-p'):
            carbon_port = int(arg)
        elif opt in ('-d'):
            carbon_dest = arg
        else:
            usage()
            sys.exit(1)

    if carbon_dest == 'undefined':
        print "ERROR: No carbon destination defined\n\n"
        usage()
        sys.exit(1)

    for line in sys.stdin:
        line = float(line)
        if isinstance(line, (int, long, float)):
            message = "%s %s %d\n" % (carbon_dest, line, int(time.time()))
            dump_to_carbon(carbon_host, carbon_port, message)
        else:
            sys.exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])

