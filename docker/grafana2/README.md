# go-carbon, carbonapi, grafana

This is a container with a full graphite/grafana stack. It runs go-carbon, and carbonapi and grafana.

Issue this command to pull the latest version of the container:

    docker pull opentokix/gografana:latest


### Login to grafana

* user: **admin**
* password: **admin**

### Running instruction

This will get your metrics stack running, and accessible on these ports, however your data will be lost if you kill the container. **Warning**

    docker run -p 2003:2003 -p 3000:3000 -d opentokix/gografana:latest

This is a more useful command, and will let you save your data in /srv/metrics and some subfolders in the host machine.

    docker run -d -v /srv/metrics:/data -p 2003:2003 -p 3000:3000 opentokix/gografana:latest

To install plugins, enter the container with: docker exec -it containerID /bin/bash
then execute:

    grafana-cli --pluginsDir=/data/grafana/plugins plugins install neocat-cal-heatmap-panel

When you have installed all your plugins, kill the container and restart it and your plugin will be available (or issue service restart grafana-server inside container)

Then you can send metrics to to port 2003 on the form "prefix.suffix value timestamp\n" as normal collectd/carbon.


First you have to do it add a datasource (Since grafana.db gets created upon first start). Add a graphite data source with the default localhost:8080 endpoint, everything else at default.

