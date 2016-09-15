#!/usr/bin/env python2
import configparser
import boto3

def readconfig():
    conf = { 'access_key': 'undefined', 'secret': 'undefined' }
    config = config = configparser.ConfigParser()
    config.read('/home/peter/credentials/aws.cred')
    if 'ROUTE53' in config:
        conf['access_key'] = config['ROUTE53']['access_key']
        conf['secret'] = config['ROUTE53']['secret_access_key']
    return conf


def update_ot(route53, record, ip):
   response = route53.change_resource_record_sets(
	HostedZoneId='',
	ChangeBatch={
	    'Comment': 'Python test dns record',
	    'Changes': [
		{
		    'Action': 'UPSERT',
		    'ResourceRecordSet': {
			'Name': record,
			'Type': 'A',
			'TTL': 300,
			'ResourceRecords': [
			    {
				'Value': ip
			    },
			],
		    }
		},
	    ]
	}
    )



def main():
    """Main function."""
    conf = readconfig()
    route53 = boto3.client('route53',
                           aws_access_key_id=conf['access_key'],
                           aws_secret_access_key=conf['secret'])
    response = update_ot(route53, 'bar.opentokix.com', '185.35.77.26')
    print response

if __name__ == '__main__':
    main()


