#!/usr/bin/env python
"""Create VM in ovirt."""


import ovirtsdk4 as sdk
import ovirtsdk4.types as types
import time
import ConfigParser
from optparse import OptionParser
import os
import sys
import uuid
import getpass


def construct_credentials(opts):
    """Construct credentials. First read environment, then command line, lastly ini."""
    raw_credentials = {'username': '',
                       'password': '',
                       'url': ''}
    try:
        raw_credentials['username'] = os.environ['ovirt_user']
    except KeyError:
        pass
    try:
        raw_credentials['password'] = os.environ['ovirt_password']
    except KeyError:
        pass
    try:
        raw_credentials['url'] = os.environ['ovirt_url']
    except KeyError:
        pass

    if opts.password:
        raw_credentials['password'] = opts.password
    if opts.username:
        raw_credentials['username'] = opts.username
    if opts.url:
        raw_credentials['url'] = opts.url

    if opts.credentials:
        cred_ini = opts.credentials
        config = ConfigParser.ConfigParser()
        config.read(cred_ini)
        try:
            raw_credentials['username'] = config.get('ovirt', 'user')
        except:
            pass
        try:
            raw_credentials['password'] = config.get('ovirt', 'pass')
        except:
            pass
        try:
            raw_credentials['url'] = config.get('ovirt', 'url')
        except:
            pass
    for key in raw_credentials:
        if len(raw_credentials[key]) == 0:
            if key == "username":
                raw_credentials['username'] = raw_input("Username: ")
            if key == "password":
                raw_credentials['password'] = getpass.getpass()
            if key == "url":
                hostname = raw_input("Hostname of ovirt manager: ")
                raw_credentials['url'] = "https://%s/ovirt-engine/api" % hostname
    return raw_credentials


def add_vm(api, options):
    """Adding a VM."""
    vms_service = api.system_service().vms_service()
    try:
        vms_service.add(
            types.Vm(
                name=options['vm_name'],
                memory=options['vmem'],
                cpu=types.Cpu(topology=options['vcpus']),
                type=types.VmType('server'),
                os=types.OperatingSystem(type=options['os_type']),
                cluster=types.Cluster(
                    name=options['vm_dc'],
                ),
                template=types.Template(name='Blank',),
            ),
        )
    except Exception as e:
        print "Can't add VM: %s" % str(e)
        api.close()
        sys.exit(1)


def add_disk_to_vm(api, options):
    """Add disk to vm."""
    search_name = "name=" + options['vm_name']
    vms_service = api.system_service().vms_service()
    vm = vms_service.list(search=search_name)[0]
    disk_attachments_service = vms_service.vm_service(vm.id).disk_attachments_service()
    try:
        disk_attachment = disk_attachments_service.add(
            types.DiskAttachment(
                disk=types.Disk(
                    name='os_disk',
                    description='OS',
                    format=types.DiskFormat.COW,
                    provisioned_size=10 * 2**30,
                    storage_domains=[
                        types.StorageDomain(
                            name='hypercube1',
                        ),
                    ],
                ),
                interface=types.DiskInterface.VIRTIO,
                bootable=True,
                active=True,
            ),
        )
    except Exception as e:
        print "Can't add Disk: %s" % str(e)
        api.close()
        sys.exit(1)

    disks_service = api.system_service().disks_service()
    disk_service = disks_service.disk_service(disk_attachment.disk.id)
    while True:
        time.sleep(5)
        disk = disk_service.get()
        if disk.status == types.DiskStatus.OK:
            break


def add_nic_to_vm(api, options):
    """Add nic to vm."""
    search_name = "name=" + options['vm_name']
    vms_service = api.system_service().vms_service()
    vm = vms_service.list(search=search_name)[0]
    """Get id of network."""
    profiles_service = api.system_service().vnic_profiles_service()
    profile_id = None
    for profile in profiles_service.list():
        if profile.name == 'ovirtmgmt':
            profile_id = profile.id
            break
    nics_service = vms_service.vm_service(vm.id).nics_service()
    try:
        nics_service.add(
            types.Nic(
                name='nic1',
                description='My network interface card',
                vnic_profile=types.VnicProfile(
                    id=profile_id,
                ),
            ),
        )
    except Exception as e:
        print "Can't add NIC: %s" % str(e)
        api.close()
        sys.exit(1)


def main(opts):
    """Magic main."""
    options = construct_credentials(opts)
    options['num_cpus'] = int(opts.num_cpus)
    options['ram_amount'] = int(opts.ram_amount)
    if opts.vm_name:
        options['vm_name'] = opts.vm_name
    else:
        options['vm_name'] = str(uuid.uuid1())
    options['vm_dc'] = opts.vm_dc
    options['os_type'] = opts.vm_dist
    options['vcpus'] = types.CpuTopology(cores=options['num_cpus'], sockets=1)
    options['vmem'] = int(options['ram_amount']) * 2**30
    try:
        api = sdk.Connection(options['url'],
                             options['username'],
                             options['password'],
                             insecure=True)
    except Exception as e:
        print "Can't make API Connection: %s" % str(e)
        sys.exit(1)

    add_vm(api, options)
    add_nic_to_vm(api, options)
    add_disk_to_vm(api, options)
    api.close()


if __name__ == '__main__':
    p = OptionParser()
    p.add_option("-u", "--user", dest="username", help="Username for ovirtmanager", metavar="user@domain", default="admin@internal")
    p.add_option("-U", "--url", dest="url", help="Url of the ovirt api: https://ovirtmanager.example.com/ovirt-engine/api", metavar="STRING")
    p.add_option("-p", "--password", dest="password", help="Password for ovirtmanager")
    p.add_option("-n", "--name", dest="vm_name", help="Name of VM")
    p.add_option("-c", "--cpus", dest="num_cpus", help="number of cpus", metavar="INT", default=1)
    p.add_option("-r", "--ram", dest="ram_amount", help="Amount of ram in GB", metavar="INT", default=2)
    p.add_option("-o", "--osdisk", dest="osdisk", help="Amount of disk in GB", metavar="INT", default=30)
    p.add_option("-d", "--datacenter", dest="vm_dc", help="Target datacenter", metavar="STRING", default="Hypercube1")
    p.add_option("-z", "--credentials", dest="credentials", help="Credentials location")
    p.add_option("-l", "--linux_dist", dest="vm_dist", help="Linux Dist (rhel_7x64, rhel_6x64, debian7)", metavar="STRING", default='rhel_7x64')
    (opts, args) = p.parse_args()
    main(opts)
