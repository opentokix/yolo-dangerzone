#!/bin/bash
if [ ! -d /data/graphite ]
then
  mkdir -p /data/graphite/whisper
fi
if [ ! -d /data/grafana ]
then 
  mkdir /data/grafana 
fi

if [ ! -d /var/log/grafana ]
then 
  mkdir /var/log/grafana
  chown grafana /var/log/grafana
fi

/etc/init.d/go-carbon start
/etc/init.d/memcached start 
/usr/bin/carbonapi -config /etc/carbonapi/carbonapi.yaml &
grafana-server -config /etc/grafana/grafana.ini -homepath /usr/share/grafana/
