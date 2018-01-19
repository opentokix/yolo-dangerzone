#!/usr/bin/env python
"""Create VM in ovirt."""


import ovirtsdk4 as sdk
import ovirtsdk4.types as types
import time
import ConfigParser
from optparse import OptionParser


def add_vm(api, options):
    """Adding a VM."""
    vms_service = api.system_service().vms_service()
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


def add_disk_to_vm(api, options):
    """Add disk to vm."""
    search_name = "name=" + options['vm_name']
    vms_service = api.system_service().vms_service()
    vm = vms_service.list(search=search_name)[0]
    disk_attachments_service = vms_service.vm_service(vm.id).disk_attachments_service()
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
    nics_service.add(
        types.Nic(
            name='nic1',
            description='My network interface card',
            vnic_profile=types.VnicProfile(
                id=profile_id,
            ),
        ),
    )


def main(opts):
    """Magic main."""
    options = {}
    options['credentials'] = opts.credentials
    options['num_cpus'] = int(opts.num_cpus)
    options['ram_amount'] = int(opts.ram_amount)
    options['vm_name'] = opts.vm_name
    options['vm_dc'] = opts.vm_dc
    options['os_type'] = opts.vm_dist
    config = ConfigParser.ConfigParser()
    config.read(options['credentials'])
    options['username'] = config.get('main', 'user')
    options['password'] = config.get('main', 'pass')
    options['url'] = config.get('main', 'url')
    url = options['url']
    user = options['username']
    password = options['password']
    options['vcpus'] = types.CpuTopology(cores=options['num_cpus'], sockets=1)
    options['vmem'] = int(options['ram_amount']) * 2**30
    api = sdk.Connection(url, user, password, insecure=True)
    add_vm(api, options)
    add_nic_to_vm(api, options)
    add_disk_to_vm(api, options)
    api.close()


if __name__ == '__main__':
    p = OptionParser()
    p.add_option("-n", "--name", dest="vm_name", help="Name of VM", metavar="myvm")
    p.add_option("-c", "--cpus", dest="num_cpus", help="number of cpus", metavar=1)
    p.add_option("-r", "--ram", dest="ram_amount", help="Amount of ram in GB", metavar=2)
    p.add_option("-o", "--osdisk", dest="osdisk", help="Amount of disk in GB", metavar=30)
    p.add_option("-d", "--datacenter", dest="vm_dc", help="Target datacenter", metavar="hypercube1")
    p.add_option("-z", "--credentials", dest="credentials", help="Credentials location")
    p.add_option("-l", "--linux_dist", dest="vm_dist", help="Linux Dist (rhel_7x64, rhel_6x64, debian7)", metavar='rhel_7x64')
    (opts, args) = p.parse_args()
    main(opts)
