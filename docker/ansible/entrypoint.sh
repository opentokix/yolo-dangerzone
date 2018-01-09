#!/bin/bash

/usr/bin/ansible-playbook -i /etc/localhost.inv /playbook.yml
cd /opt
/usr/bin/rake spec
echo "============= Test Done =====================" 
