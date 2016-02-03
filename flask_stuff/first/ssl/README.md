## This supplied crt/key is for 

{wildcard}.l.txq.se and that domain is for ::1 on your local machine 

example: _foobar.l.txq.se_ points to ::1 wich is ipv6 localhost. 

## How to create your own ssl certs 

Install openssl with your package manager 

apt-get install openssl 


*Generating a server key with pass phrase*

openssl genrsa -des3 -passout pass:x -out server.pass.key 2048

*Remove the pass phrase*

openssl rsa -passin pass:x -in server.pass.key -out server.key
rm server.pass.key

*Generate the cert signing request, based on your key*
openssl req -new -key server.key -out server.csr

Fill out any information, like your state and such. 

For CN write: * or some FQDN 

*Generate the actual cert based on your csr and key*

openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt


