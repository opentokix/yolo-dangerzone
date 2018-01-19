# Simple ovirtsdk4 util to add a VM


    "-n", "--name", dest="vm_name", help="Name of VM", metavar="myvm")
    "-c", "--cpus", dest="num_cpus", help="number of cpus", metavar=1)
    "-r", "--ram", dest="ram_amount", help="Amount of ram in GB", metavar=2)
    "-o", "--osdisk", dest="osdisk", help="Amount of disk in GB", metavar=30)
    "-d", "--datacenter", dest="vm_dc", help="Target datacenter", metavar="hypercube1")
    "-z", "--credentials", dest="credentials", help="Credentials location")
    "-l", "--linux_dist", dest="vm_dist", help="Linux Dist (rhel_7x64, rhel_6x64, debian7)", metavar='rhel_7x64')


## Ini-file

Credentials is stored in a ini.file in a destination of your choice.

    [ovirt]
    url=https://ovirtmanager.example.com/ovirt-engine/api
    user=admin@internal
    pass=asc123

## Example usage

**Add a vm named myvm2 with 3 cpus and 3 GB or ram and 10 GB OS disk with rhel 6 x64 in DC Hypercube1**

    ./add_vm.py --name myvm2 --cpus 3 --ram 3 --osdisk 10 -z /home/peter/credentials/ovirt_api.conf -d Hypercube1 -l rhel_6x64

**Add a vm named bamboozle with 4 cpus and 32 GB or ram and 30 GB OS disk with rhel 7 x64 in DC Hypercube1**

    ./add_vm.py --name bamboozle --cpus 3 --ram 32 --osdisk 30 -z /home/peter/credentials/ovirt_api.conf -d Hypercube1 -l rhel_7x64

