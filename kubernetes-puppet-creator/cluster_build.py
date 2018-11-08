#!/usr/bin/env python
import os
import ConfigParser
from subprocess import call

def main():
  config = ConfigParser.ConfigParser()
  config.readfp(open('cluster_setup.ini'))
  fdqn_base = config.get('main', 'domain')
  controller_string = ""
  for item in config.items('controllers'):
    controller_string += item[0] + ":" + item[1] + ","
  controller_string = "ETCD_INITIAL_CLUSTER=" + controller_string[:-1]
  volume_option = os.getcwd() + ":/mnt"
  command_line = ['docker', 'run', '--rm',
                 '-v', volume_option,
                 '-e', 'OS=rhel',
                 '-e', 'VERSION=1.10.2',
                 '-e', 'CONTAINER_RUNTIME=docker',
                 '-e', 'CNI_PROVIDER=flannel',
                 '-e', controller_string,
                 '-e', 'ETCD_IP="%{::ipaddress_eth0}"',
                 '-e', 'KUBE_API_ADVERTISE_ADDRESS="%{::ipaddress_eth0}"',
                 '-e', 'INSTALL_DASHBOARD=true', 'puppet/kubetool:3.0.1']
  call(command_line)
if __name__ == '__main__':
  main()
