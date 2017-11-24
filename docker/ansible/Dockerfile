FROM ubuntu:xenial
MAINTAINER Peter Eriksson petereriksson.net@gmail.com
RUN apt-get update && apt-get -y upgrade
RUN apt-get install ansible
RUN mkdir /ansible 
WORKDIR /ansible
RUN echo "localhost ansible_connection=local" > /etc/localhost.inv
CMD ['ansible-playbook', '-i', '/etc/localhost.inv', '/ansible/playbook.yml' ]
