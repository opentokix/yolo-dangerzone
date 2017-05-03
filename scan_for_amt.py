#!/usr/bin/env python2
import requests

for i in range(1,255):
    url="https://10.0.111."+str(i)+":16992"
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