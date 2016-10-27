#!/usr/bin/env python2


import socket
from time import time, sleep
import random


class Graphite(object):
    def __init__(self, host, port):
        self.s = socket.socket()
        self.s.connect((host, port))

    def send(self, prefix, data):
        message = "%s %s %s\n" % (prefix, str(data), str(time()))
        self.s.sendall(message)

    def __del__(self):
        self.s.close()


def main():
    graphite = Graphite('127.0.0.1', 2003)
    for i in range(10):
        graphite.send('first.data', random.random()*10)
        print "Sent data iteration %s" % str(i)
        sleep(10)


if __name__ == '__main__':
    main()
