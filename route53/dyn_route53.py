#!/usr/bin/env python2
"""Tool to handle route53 hosted domains."""
import configparser
import boto3
import sys
from netifaces import AF_INET, AF_INET6
# AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces as ni
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
        cred.read('/home/peter/credentials/route53.cred')
    except Exception as e:
        exit_message(e, 1)

    if 'ROUTE53' in cred:
        conf['access_key'] = cred['ROUTE53']['access_key']
        conf['secret'] = cred['ROUTE53']['secret_access_key']
    return conf


def resolve_domain(domainname):
    """Check if the domain resolves correctly with google and opendns."""
    queryservers = ['8.8.8.8', '8.8.4.4', '208.67.222.222', '208.67.220.220']
    answers = []

    for rdns in queryservers:
        for rdata in dns.resolver.query(domainname):
            answers.append(rdata)
    if len(list(set(answers))) == 1:
        return answers[0]
    else:
        return False


def get_if_addr(interface="eth0", version="ipv4"):
    """Returning the address of the interface, defaults to ipv4."""
    if version == 'ipv6':
        return ni.ifaddresses(interface)[AF_INET6][0]['addr']
    else:
        return ni.ifaddresses(interface)[AF_INET][0]['addr']


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
    print type
    print full_record
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
        opts, args = getopt.getopt(argv, 'h46:d:H:i:A:', ['help', 'ipv4', 'ipv6', 'domain=', 'hostname=', 'interface=', 'awskeys='])
    except getopt.GetoptError:
        print "Options error"
        sys.exit(1)
    options = {}
    options['version'] = 'ipv4'
    options['domain'] = 'opentokix.com'
    options['hostname'] = 'dynamic'
    options['interface'] = 'eth0'

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
        elif opt in ['-i', '--interface']:
            options['interface'] = arg
        elif opt in ['-A', '--awskeys']:
            options['awskeys'] = arg
    main(options)


def main(options):
    """Main function."""
    credentials = readcredentials(options['awskeys'])
    local_ip = get_if_addr(options['interface'], options['version'])
    resolved = resolve_domain(options['domain'])
    if resolved is not False:
        resolved_ip = resolved
    if resolved_ip == local_ip:
        sys.exit(0)
    else:
        route53 = boto3.client('route53',
                               aws_access_key_id=credentials['access_key'],
                               aws_secret_access_key=credentials['secret'])
        response = update_route53(route53, options['domain'], options['hostname'], local_ip, options['version'])
        print response


if __name__ == '__main__':
    parse_options(sys.argv[1:])
