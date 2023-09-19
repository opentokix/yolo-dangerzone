#!/usr/bin/env python3
# Very simple tool to add A or AAAA records in a azure hosted zone from the command line.
import click
import os
import logging
import ipaddress
from azure.mgmt.dns import DnsManagementClient
from azure.common.credentials import ServicePrincipalCredentials

logger = logging.getLogger('azure_dns_tool')
logger.setLevel(logging.ERROR)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_azure_principal():
  """Get Azure credentials from environment variables"""
  subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID')
  credentials = ServicePrincipalCredentials(
      client_id=os.environ.get('AZURE_CLIENT_ID'),
      secret=os.environ.get('AZURE_CLIENT_SECRET'),
      tenant=os.environ.get('AZURE_TENANT_ID')
  )
  return credentials, subscription_id


def get_available_zones(dns_client, subscription_id):
    """Get zones handled by this account, for some basic checks. Put result in a dict"""
    z = {}
    response = dns_client.zones.list_by_subscription(subscription_id)
    zones = response
    for i in range(len(zones)):
        z[zones[i].name] = zones[i].id
    if not z:
        logger.error("No zones possible")
        exit(1)
    else:
        logger.debug(z)
        return z


def get_resource_group_for_zone(dns_client, zone_id):
    """Get the resource group for a zone"""
    zone = dns_client.zones.get(zone_id)
    return zone.resource_group


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


def add_rrset(dns_client, zone_id, fqdn, ip):
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
    try:
        dns_client.record_sets.create_or_update(
            resource_group_name='myresourcegroup',
            zone_name=fqdn,
            relative_record_set_name=fqdn,
            record_type=record_type,
            parameters={
                'ttl': 300,
                'arecords': [{
                    'ipv4_address': ip
                }]
            }
        )
    except Exception as e:
        logger.error(e)
        exit(1)
    logger.info(f"Added {record_type} record for {fqdn} with IP {ip}")


@click.command()
@click.option('--fqdn', prompt='FQDN', help='FQDN to add')
@click.option('--ip', '-i', prompt='IP', help='IP to add')
@click.option('--verbose', is_flag=True, help='Verbose output')
def main(ip, fqdn, verbose):
  """Add A or AAAA records to Azure DNS"""
  ask_for_comfirmation()
  if verbose:
    logger.setLevel(logging.DEBUG)
  credentials, subscription_id = get_azure_principal()
  dns_client = DnsManagementClient(credentials, subscription_id)
  zones = get_available_zones(dns_client, subscription_id)
  zone_id = sanitycheck_of_zone(zones, fqdn)
  resource_group = get_resource_group_for_zone(dns_client, zone_id)
  add_rrset(dns_client, zone_id, fqdn, ip)

def ask_for_comfirmation():
  print("This is written blind, no testing, not even once")
  print("DONT USE THIS TOOL!")
  print("You have been warned!")
  print("=====================================")
  print("This tool is totally untested, do you want to run (y/n):")
  answer = input()
  if answer == "y":
    return True
  else:
      print("Good choice, bye!"")
      exit(1)

if __name__ == '__main__':
    main()