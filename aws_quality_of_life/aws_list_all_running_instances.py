#!/usr/bin/env python3
"""List all instances in your aws account, with state and type."""
import boto3


def main():
    """Only one dirty main."""
    print("Listing all instances running or not in all regions")
    print("Region:")
    regions = []
    metadata = boto3.client('ec2')
    response = metadata.describe_regions()
    for r in response['Regions']:
        regions.append(r['RegionName'])
    #regions = ['eu-central-1', 'eu-west-2']
    for region in regions:
        ec2 = boto3.client('ec2', region)
        response = ec2.describe_instances()
        print(region)

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                id = (instance["InstanceId"])
                state = ec2.describe_instance_status(InstanceIds=[id])


                if len(state['InstanceStatuses']) != 0:
                    print("  |- id:", id, "State:", state['InstanceStatuses'][0]['InstanceState']['Name'], "Type:", instance['InstanceType'])
                else:
                    print("  |- id:", id, "State: Available but not running", "Type:", instance['InstanceType'])


if __name__ == '__main__':
    main()
