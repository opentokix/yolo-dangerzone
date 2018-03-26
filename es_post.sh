#!/bin/bash

hostname=`hostname -f|sed 's/\./_/g'`
tag=$hostname",change"
username=`whoami`

if [ -z ${@+x} ]
then
    echo "script_name message is required"
else
    message=$@
fi

if [ -z ${SUDO_USER+x} ]
then 
    username=`whoami`
else 
    username=$SUDO_USER
fi

data="{\"user\": \"${username}\", \"message\": \"${message}\", \"tags\": \"${tag}\"}"

curl -XPUT -i -H 'Content-Type: application/json' -d '\"$data\"' http://localhost:9200/info?pretty
