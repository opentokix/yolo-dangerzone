# Route 53 tools 

### dyn_route53.py

This is a small utility to run in cron or similar to update a record at aws route 53 for dynamic ips.

It will check against google and opendns resolvers for the name and if it match your local ip it will not update any records. 

When the ip and domain does not match it will update the record with the local ip of the supplied interface. 

deps: 
boto3
dns.resolvers 
netifaces 
configparser 
getopt 


## Example command line 

This will update dynamic.opentokix.com with ip from the interface extbr

Dual stack support, but has to be run twice to take both ipv4 and ipv6 from a single interface. 

<pre>
./dyn_route53.py --interface=extbr --domain=opentokix.com --hostname=dynamic --awskeys="/root/aws.cred" --ipv4
</pre>


## Configfile layout for aws credentials 
<pre>
[ROUTE53]
access_key = ACCESS_KEY_HERE
secret_access_key = SECRET_ACCESS_KEY_HERE
<pre>



