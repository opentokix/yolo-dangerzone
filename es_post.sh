#!/bin/bash

es_server=localhost
es_port=9200
es_type=_doc
es_index=info
hostname=`hostname -f|sed 's/\./_/g'`
tag=$hostname",change"


# check for curl and wget
curl_bin=`whereis -b curl|cut -d " " -f 2`
wget_bin=`whereis -b wget|cut -d " " -f 2`

# hereis -b returns only "name:" if not found, but if found that will be cut.
# ugly hack, but it works.
if [[ $curl_bin != *":"* ]]
then
    http_prog=curl
elif [[ $wget_bin != *":"* ]]
then
    http_prog=wget
else
    echo "Neither curl or wget found, exiting. This script requires one of them."
    exit 1
fi


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
if [ $http_prog == 'curl' ]
then
    $curl_bin -O /dev/null -s -H 'Content-Type: application/json' -d "$data" http://$es_server:$es_port/$es_index/$es_type?pretty
elif [ $http_prog == 'wget' ]
then
    $wget_bin -q -O /dev/null --post-data="$data" --header=Content-Type:application/json "http://$es_server:$es_port/$es_index/$es_type?pretty"
else
    echo "Not sure how you came this far, but something is wrong"
    exit 1
fi
