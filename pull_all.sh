#!/bin/bash 

root_dir=$PWD
list=`ls -1`

for i in $list
do
    if [ -d ${root_dir}/${i}/.git ]
    then
        cd ${root_dir}/${i}
        git pull
        cd ${root_dir}
    fi
done

