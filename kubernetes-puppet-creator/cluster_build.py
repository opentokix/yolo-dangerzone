#!/usr/bin/env python
import os
import ConfigParser
from subprocess import call

def run_docker():
  config = ConfigParser.ConfigParser()
  config.readfp(open('cluster_setup.ini'))
  fdqn_base = config.get('main', 'domain')
  controller_string = ""
  for item in config.items('controllers'):
    controller_string += item[0] + ":" + item[1] + ","
  controller_string = "ETCD_INITIAL_CLUSTER=" + controller_string[:-1]
  volume_option = os.getcwd() + ":/mnt"
  os_option = "OS=" + config.get('main', 'os')
  version_option = "VERSION=" + config.get('main', 'version')
  container_runtime_option = "CONTAINER_RUNTIME=" + config.get('main', 'runtime')
  cni_provider_option = "CNI_PROVIDER=" + config.get('main', 'cniprovider')
  command_line = ['docker', 'run', '--rm',
                 '-v', volume_option,
                 '-e', os_option,
                 '-e', version_option,
                 '-e', container_runtime_option,
                 '-e', cni_provider_option,
                 '-e', controller_string,
                 '-e', 'ETCD_IP="%{::ipaddress_eth0}"',
                 '-e', 'KUBE_API_ADVERTISE_ADDRESS="%{::ipaddress_eth0}"',
                 '-e', 'INSTALL_DASHBOARD=true', 'puppet/kubetool:3.0.1']
  call(command_line)
  return config

def make_yaml_files(config):
  class_block = """
classes:
  - kubernetes
"""
  for controller in config.items('controllers'):
    f_name = controller[0] + "." + config.get('main', 'domain') + ".yaml"
    outfile = open(f_name, 'w')
    outfile.writelines(class_block)
    with open('Rhel.yaml') as infile:
      outfile.write(infile.read())
    with open(controller[0] + ".yaml") as infile:
      outfile.write(infile.read())

  for worker in config.items('workers'):
    f_name = worker[0] + "." + config.get('main', 'domain') + ".yaml"
    outfile = open(f_name, 'w')
    outfile.writelines(class_block)
    with open('Rhel.yaml') as infile:
      outfile.write(infile.read())

def main():
  config = run_docker()
  make_yaml_files(config)

if __name__ == '__main__':
  main()
