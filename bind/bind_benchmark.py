#!/usr/bin/env python3

import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query
import threading 
import time 
from random import choice 
times = []


def query(base, server):
  aa = "foo" + str(choice(base)) + ".example.aa"
  qname = dns.name.from_text(aa)
  q = dns.message.make_query(qname, dns.rdatatype.A)
  t1 = time.time()
  dns.query.udp(q, server)
  t2 = time.time()
  times.append(t2 - t1)



def main():
  maxconnections = 5 
  tpool = threading.BoundedSemaphore(value=maxconnections)
  l = []
  for i in range(1, 10001):
    l.append(i)
  threads = list()
  for i in range(0, 10000):
    x = threading.Thread(target=query, args=(l, '172.17.0.2'))
    threads.append(x)
    x.start()

  print(sum(times))


if __name__ == "__main__":
    main()