FROM ubuntu:xenial
MAINTAINER Peter Eriksson petereriksson.net@gmail.com
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y ansible ruby-serverspec
WORKDIR /
RUN echo "localhost ansible_connection=local" > /etc/localhost.inv
COPY serverspec/ /opt/
COPY entrypoint.sh /root/
CMD [ "/root/entrypoint.sh" ]
