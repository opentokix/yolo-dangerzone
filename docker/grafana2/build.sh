#/bin/bash
docker pull opentokix/grafana:build 
if [ -z $1 ]
then
    docker build -t opentokix/grafana:${1} .
    PUSH_VERSION=Yes
fi

docker build -t opentokix/grafana:latest .

if [ -z $PUSH_VERSION ]
then
    docker push opentokix/grafana:${1}
fi

docker push opentokix/grafana:latest 

