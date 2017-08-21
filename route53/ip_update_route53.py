#!/usr/bin/env python2
"""Tool to handle route53 hosted domains.

Packages:

apt install python-configparser python-pip
pip install boto3
pip install dsnpython
"""
import configparser
import boto3
import sys
#from netifaces import AF_INET, AF_INET6
# AF_LINK, AF_PACKET, AF_BRIDGE
#import netifaces as ni
import dns.resolver
import getopt


def usage():
    """Automatic update script for route53."""
    exit_message(usage.__doc__, 0)


def exit_message(message, code):
    """Exit program with message and code."""
    print message
    sys.exit(code)


def readcredentials(credentials='/home/peter/credentials/route53.cred'):
    """Read credentials and other optional config options."""
    conf = {'access_key': 'undefined', 'secret': 'undefined'}
    cred = configparser.ConfigParser()

    try:
        cred.read(credentials)
    except Exception as e:
        exit_message(e, 1)

    if 'ROUTE53' in cred:
        conf['access_key'] = cred['ROUTE53']['access_key']
        conf['secret'] = cred['ROUTE53']['secret_access_key']
    return conf


def resolve_domain(domainname, version):
    """Check if the domain resolves correctly with google and opendns."""
    queryservers = ['8.8.8.8', '8.8.4.4', '208.67.222.222', '208.67.220.220']
    answers = []
    if version == 'ipv6':
        query_type = 'AAAA'
    else:
        query_type = 'A'
    for rdns in queryservers:
        for rdata in dns.resolver.query(domainname, query_type):
            answers.append(rdata)
    if len(list(set(answers))) == 1:
        return str(answers[0])
    else:
        return False


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


def update_route53(route53, domain, record, ip, version='ipv4'):
    """Update record in route 53 hosted zone."""
    if version == 'ipv4':
        type = "A"
    else:
        type = "AAAA"

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


def parse_options(argv):
    """Parse options."""
    try:
        opts, args = getopt.getopt(argv, 'h46:d:H:i:A:', ['help', 'ipv4', 'ipv6', 'domain=', 'hostname=', 'ip=', 'awskeys='])
    except getopt.GetoptError:
        print "Options error"
        sys.exit(1)
    options = {}
    options['version'] = 'ipv4'
    options['domain'] = 'opentokix.com'
    options['hostname'] = 'dynamic'
    options['ip'] = '127.0.0.1'

    for opt, arg in opts:
        if opt in ['-h', '--help']:
            usage()
        elif opt in ['-4', '--ipv4']:
            options['version'] = 'ipv4'
        elif opt in ['-6', '--ipv6']:
            options['version'] = 'ipv6'
        elif opt in ['-d', '--domain']:
            options['domain'] = arg
        elif opt in ['-H', '--hostname']:
            options['hostname'] = arg
        elif opt in ['-i', '--ip']:
            options['ip'] = arg
        elif opt in ['-A', '--awskeys']:
            options['awskeys'] = arg
    main(options)


def main(options):
    """Main function."""
    credentials = readcredentials(options['awskeys'])
    local_ip = options['ip']
    resolved = resolve_domain(options['hostname'] + "." + options['domain'], options['version'])
    if resolved == local_ip:
        print "No action needed local ip and resolved ip match, %s.%s points to %s" % (options['hostname'], options['domain'], local_ip)
        sys.exit(0)

    else:
        route53 = boto3.client('route53',
                               aws_access_key_id=credentials['access_key'],
                               aws_secret_access_key=credentials['secret'])
        response = update_route53(route53, options['domain'], options['hostname'], local_ip, options['version'])
        print response


if __name__ == '__main__':
    parse_options(sys.argv[1:])
