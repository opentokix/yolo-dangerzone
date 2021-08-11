#!/usr/bin/env python3
# Very simple tool to add A or AAAA records in a route53 hosted zone from the command line.
import boto3
import click
import os
import logging
import ipaddress

logger = logging.getLogger('route53_tool')
logger.setLevel(logging.ERROR)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_available_zones(route53):
    """Get zones handled by this account, for some basic checks. Put result in a dict"""
    z = {}
    response = route53.list_hosted_zones()
    zones = response['HostedZones']
    for i in range(len(zones)):
        z[zones[i]['Name']] = zones[i]['Id']
    if not z:
        logger.error("No zones possible")
        exit(1)
    else:
        logger.debug(z)
        return z

def sanitycheck_of_zone(zones, fqdn):
    """Make sure you own the zone you are trying to add records in."""
    if fqdn.count('.') < 2:
        logger.error("You need a hostname. ie: hostname.domain.tld, not only domain.tld")
        exit(1)
    wip = fqdn.split('.')
    zone = wip[-2:]
    zone = f"{zone[0]}.{zone[1]}."
    for key in zones:
        if zone == key:
            logger.debug(f"Zone ID: {zones[zone]}")
            return str(zones[zone])
    logger.error(f"What are you doing? You don't control {zone}")
    exit(1)


def add_rrset(route53, zone_id, fqdn, ip):
    """Adding the resource record, also check if its A or AAAA to be added."""
    try:
        address = ipaddress.ip_address(ip)
    except:
        logger.error(f"[ {ip} ] is not a valid ipaddress")
    logger.debug(f"{address} is ip version {address.version}")
    if address.version == 4:
        record_type = "A"
    elif address.version == 6:
        record_type = "AAAA"
    else:
        logger.error("Unknown IP")
        exit(1)

    response = route53.change_resource_record_sets(
        HostedZoneId=zone_id, ChangeBatch={'Comment': 'Autoupdated record', 'Changes': [
        {'Action': 'UPSERT', 'ResourceRecordSet': {
            'Name': fqdn, 'Type': record_type, 'TTL': 300, 'ResourceRecords':
            [
                {'Value': ip},
            ],
        }
        },
        ]})
    return response

@click.command()
@click.option('--ip', '-i', required=True, default=None, help="The ip-number your A or AAAA record should point to")
@click.option('--fqdn', required=True, help="Fully qualitifed domain name of the A or AAAA record to be added.")
@click.option('--verbose', '-V', is_flag=True, default=False, help="Verbose flag to get debug info")
def main(ip, fqdn, verbose):
    """This is where the magic happens."""
    if verbose:
        logger.setLevel(logging.DEBUG)
    AWS_ACCESS = os.environ['ROUTE53_ACCESS']
    AWS_SECRET = os.environ['ROUTE53_SECRET']
    logger.debug(fqdn)
    route53 = boto3.client('route53', aws_access_key_id=AWS_ACCESS, aws_secret_access_key=AWS_SECRET)
    zone_id = sanitycheck_of_zone(get_available_zones(route53), fqdn)
    logger.info(add_rrset(route53, zone_id, fqdn, ip))

if __name__ == '__main__':
    main()
