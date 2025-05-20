#!/usr/bin/env python3

import boto3
import click
import ipaddress
import logging
import sys
from botocore.exceptions import BotoCoreError, ClientError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--ip', '-i', required=True, default=None,
              help="The IP address your A or AAAA record should point to")
@click.option('--aws_access', '-A', required=True, default=None,
              help="AWS Access Key, needs Route53 permissions.")
@click.option('--aws_secret', '-S', required=True, default=None,
              help="AWS Secret Key, needs Route53 permissions.")
def main(ip, aws_access, aws_secret):
    """
    Search all Route 53 hosted zones for A and AAAA records matching the specified IP address.
    """
    try:
        # Validate IP address
        try:
            ip_obj = ipaddress.ip_address(ip)
            record_type = 'A' if ip_obj.version == 4 else 'AAAA'
            logger.info(f"Searching for {record_type} records matching IP: {ip}")
        except ValueError:
            logger.error(f"Invalid IP address provided: {ip}")
            sys.exit(1)

        # Initialize boto3 client
        try:
            client = boto3.client(
                'route53',
                aws_access_key_id=aws_access,
                aws_secret_access_key=aws_secret
            )
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to create Route 53 client: {e}")
            sys.exit(1)

        # List hosted zones
        try:
            hosted_zones = client.list_hosted_zones()['HostedZones']
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to list hosted zones: {e}")
            sys.exit(1)

        if not hosted_zones:
            logger.info("No hosted zones found.")
            return

        # Iterate through hosted zones
        for zone in hosted_zones:
            zone_id = zone['Id'].split('/')[-1]
            zone_name = zone['Name']
            logger.info(f"Searching zone: {zone_name} (ID: {zone_id})")

            paginator = client.get_paginator('list_resource_record_sets')
            try:
                for page in paginator.paginate(HostedZoneId=zone_id):
                    for record in page['ResourceRecordSets']:
                        if record['Type'] in ['A', 'AAAA']:
                            for rr in record.get('ResourceRecords', []):
                                if rr['Value'] == ip:
                                    print(f"Match found in zone '{zone_name}':")
                                    print(f"  Name: {record['Name']}")
                                    print(f"  Type: {record['Type']}")
                                    print(f"  TTL: {record.get('TTL', 'N/A')}")
                                    print(f"  Value: {rr['Value']}\n")
            except (BotoCoreError, ClientError) as e:
                logger.error(f"Failed to list records for zone {zone_name}: {e}")
                continue

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main(auto_envvar_prefix='ROUTE53')
