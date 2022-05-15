#!/bin/bash

systemctl stop ceph-mon.target
systemctl stop ceph-mgr.target
systemctl stop ceph-mds.target
systemctl stop ceph-osd.target
sleep 3
rm -rf /etc/systemd/system/ceph*
sleep 3
killall -9 ceph-mon ceph-mgr ceph-mds
sleep 3
rm -rf /var/lib/ceph/mon/  /var/lib/ceph/mgr/  /var/lib/ceph/mds/
sleep 3
pveceph purge
sleep 3
apt -y purge ceph-mon ceph-osd ceph-mgr ceph-mds
rm /etc/init.d/ceph

