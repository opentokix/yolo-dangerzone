#!/usr/bin/env python2
"""Tool to scan a subnet for AMT."""

import requests


def main():
    """Everything in main."""
    for i in range(1, 255):
        url = "https://10.0.111." + str(i) + ":16992"
        print "Testing: %s" % url
        try:
            r = requests.get(url, timeout=1)
        except:
            continue

        if r.status_code != 200:
            break

        server = str(r.headers['server'])

        result = server.find("anagemen")
        if result != 0:
            print "Vulnurable: %s %s" % (url, result)

        if server == "AMT":
            print "Vulnurable: %s %s" % (url, result)

if __name__ == '__main__':
    main()
