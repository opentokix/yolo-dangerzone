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
  command_line = ['docker', 'run', '--rm', 
                 '-v', '$(pwd):/mnt',
                 '-e', 'OS=rhel',
                 '-e', 'VERSION=1.10.2',
                 '-e', 'CONTAINER_RUNTIME=docker',
                 '-e', 'CNI_PROVIDER=flannel',
                 '-e', controller_string,
                 '-e', 'ETCD_IP=\"%{::ipaddress_eth0}\"',
                 '-e', 'KUBE_API_ADVERTISE_ADDRESS=\"%{::ipaddress_eth0}\"',
                 '-e', 'INSTALL_DASHBOARD=true puppet/kubetool:3.0.1']
  output = call(command_line)

"""
docker run --rm -v $(pwd):/mnt -e OS=rhel -e VERSION=1.10.2 \
-e CONTAINER_RUNTIME=docker -e CNI_PROVIDER=flannel \
-e ETCD_INITIAL_CLUSTER="kubetest01:10.156.2.143,kubetest02:10.156.2.142,kubetest03:10.156.2.141" \
-e ETCD_IP="%{::ipaddress_eth0}" \
-e KUBE_API_ADVERTISE_ADDRESS="%{::ipaddress_eth0}" \
-e INSTALL_DASHBOARD=true puppet/kubetool:3.0.1
"""



if __name__ == '__main__':
  main()