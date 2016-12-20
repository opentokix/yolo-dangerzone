#!/usr/bin/env python2
"""Tool to handle route53 hosted domains."""
import configparser
import boto3
from subprocess import check_output
import sys
from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces as ni


def readconfig():
    """Read credentials and other optional config options."""
    conf = {'access_key': 'undefined', 'secret': 'undefined'}
    cred = configparser.ConfigParser()
    try:
        cred.read('/home/peter/credentials/route53.cred')
    except e:
        print e
        sys.exit(1)
    if 'ROUTE53' in cred:
        conf['access_key'] = cred['ROUTE53']['access_key']
        conf['secret'] = cred['ROUTE53']['secret_access_key']
    return conf


def get_if_addr(interface="eth0", version="ipv4"):
    """Returning the address of the interface, defaults to ipv4."""
    if version == 'ipv6':
        v = "AF_INET6"
    else:
        v = "AF_INET"
    return ni.ifaddresses(interface)[v][0]['addr']


def get_available_zones(route53):
    """Get zones handled by this account, for some basic checks."""
    response = route53.list_hosted_zones()
    return response


def get_zone_id(route53, domain):
    """Return the hostid for a domainname."""
    # return jsondata['HostedZones'][]
    response = route53.list_hosted_zones()
    search_domain = domain + "."
    for i in range(len(response['HostedZones'])):
        if response['HostedZones'][i]['Name'] == search_domain:
            return response['HostedZones'][i]['Id']


def update_ot(route53, domain, record, ip, version=4):
    """Update record in route 53 hosted zone."""
    if version == 4:
        type == "A"
    if version == 6:
        type == "AAAA"

    full_record = record + '.' + domain + '.'
    response = route53.change_resource_record_sets(
        HostedZoneId=get_zone_id(route53, domain), ChangeBatch={'Comment': 'Autoupdated record', 'Changes': [
            {'Action': 'UPSERT', 'ResourceRecordSet': {
                'Name': full_record, 'Type': type, 'TTL': 300, 'ResourceRecords':
                [
                    {'Value': ip},
                ],
            }
            },
        ]})
    return response


def main():
    """Main function."""
    conf = readconfig()
    """
    #route53 = boto3.client('route53',
                           #aws_access_key_id=conf['access_key'],
                           #aws_secret_access_key=conf['secret'])
    #response = update_ot(route53, 'meodo.com', 'foo', '185.35.77.26')
    """
    print conf


if __name__ == '__main__':
    main()
