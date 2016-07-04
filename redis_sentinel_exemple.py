#!/usr/bin/env python2

import redis
from redis.sentinel import Sentinel
from random import randint

def main():
    s = Sentinel([('sentinel-server1', 26379),
                  ('sentinel-server2', 26379),
                  ('sentinel-server3', 26379)], socket_timeout=0.1)

    r_master = s.discover_master('rediscluster01')
    r_slaves = s.discover_slaves('rediscluster01')
    print r_master
    print r_slaves

    r = redis.StrictRedis(host=r_master[0], port=r_master[1], db=3)
    number = randint(1,100)
    print "number: %d" % number
    r.set('foo', number)
    print len(r_slaves)
    select_slave = randint(0, len(r_slaves)-1)
    r_s = redis.StrictRedis(host=r_slaves[select_slave][0], port=r_slaves[select_slave][1], db=3)
    print r_s.get('foo')

if __name__ == '__main__':
    main()
