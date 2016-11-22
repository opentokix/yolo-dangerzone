#!/usr/bin/env python2
"""Tool to handle route53 hosted domains."""
import configparser
import boto3
from subprocess import check_output
import sys

def readconfig():
    """Read credentials and other optional config options."""
    conf = {'access_key': 'undefined', 'secret': 'undefined'}
    config = configparser.ConfigParser()
    config.read('/home/peter/credentials/aws.cred')
    if 'ROUTE53' in config:
        conf['access_key'] = config['ROUTE53']['access_key']
        conf['secret'] = config['ROUTE53']['secret_access_key']
    try:
        config.read('/home/peter/credentials/route53_dyn.conf')
        for k, v in config:
            print "key: %s value: %s" % (k, v)
    except:
        print sys.exc_info()[0]
        print "Config Error"
        sys.exit(3)

    return conf


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


def update_ot(route53, domain, record, ip):
    """Update record in route 53 hosted zone."""
    full_record = record + '.' + domain + '.'
    response = route53.change_resource_record_sets(
        HostedZoneId=get_zone_id(route53, domain), ChangeBatch={'Comment': 'Python test dns record', 'Changes': [
            {'Action': 'UPSERT', 'ResourceRecordSet': {
                'Name': full_record, 'Type': 'A', 'TTL': 300, 'ResourceRecords':
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
    #route53 = boto3.client('route53',
                           #aws_access_key_id=conf['access_key'],
                           #aws_secret_access_key=conf['secret'])
    #response = update_ot(route53, 'meodo.com', 'foo', '185.35.77.26')
    print conf



if __name__ == '__main__':
    main()
