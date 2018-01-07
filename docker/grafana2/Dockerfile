FROM debian:stretch
WORKDIR /data
EXPOSE 2003
EXPOSE 3000
COPY pkg/*.deb /tmp/
RUN apt-get update 
RUN apt-get -y upgrade 
RUN apt-get -y install memcached libfontconfig
RUN ls -l /tmp/
RUN for i in $(ls /tmp/*.deb); do dpkg -i $i; done
RUN apt-get -y -f install 
RUN rm -f /tmp/*.deb
RUN mkdir /etc/carbonapi
COPY configs/carbonapi.yaml /etc/carbonapi/
COPY configs/go-carbon.conf /etc/go-carbon/
COPY configs/storage-aggregation.conf /etc/go-carbon/
COPY configs/storage-schemas.conf /etc/go-carbon/
COPY configs/grafana.ini /etc/grafana/
COPY entrypoint.sh /root/entrypoint.sh
CMD [ "/root/entrypoint.sh" ]
