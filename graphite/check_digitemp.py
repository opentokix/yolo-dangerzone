#!/usr/bin/env python
from subprocess import Popen, PIPE, STDOUT
import sys
import time

global DEBUG
DEBUG = False


def dump_to_carbon(server, port, payload):
    import socket
    sock = socket.socket()
    try:
        sock.connect((server, port))
    except socket.error as e:
        try:
            if DEBUG is True:
                print "Socket error in dump to carbon: %s" % e
            time.sleep(1)
            sock.connect((server, port))
        except socket.error as e:
            if 'Connection refused' in e:
                print '*** Connection refused ***'
                sock.close()
                return
            elif 'Connection reset by peer' in e:
                print "Connection Reset by peer"
                sock.close()
                return
            else:
                print 'Unknown socket error'
                sock.close()
                return
    sock.sendall(payload)
    sock.close()


def main(argv):
    process = Popen("digitemp_DS9097 -q -c /root/.digitemprc -r2000 -a",
                    shell=True, stdout=PIPE, stderr=STDOUT)

    for line in process.stdout:
        line = line.split()
        carbon_dest = "carbon.hypercube.temp1"
        message = "%s %.1f %d\n" % (carbon_dest, float(line[6]),
                                    int(time.time()))
        dump_to_carbon("172.16.135.1", int(2003), message)


if __name__ == '__main__':
    main(sys.argv[1:])
