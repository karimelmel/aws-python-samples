import boto3
import botocore

# Function to associate GuardDuty child accounts with a GD Master.
# Works when GuardDuty is setup through organization 

# Get all regions and store in a variable
ec2_client = boto3.client('ec2')
regions = [region['RegionName']
    for region in ec2_client.describe_regions()['Regions']]


def enable_guardduty():
    for region in regions:
        print("Region:", region)
        client = boto3.client('guardduty', region_name=region)
        detectors = client.create_detector (
            Enable=True,
            FindingPublishingFrequency='FIFTEEN_MINUTES',
            DataSources= {
                'S3Logs': {
                    'Enable': True
                }
            },
                Tags={
                    'easyrisk_id' : '8989'
                })
        for detector in detectors['DetectorId']:
            try:
                print("Correct value is:", detectors['DetectorId'])
                client.update_organization_configuration(
                    DetectorId=detectors['DetectorId'],
                    AutoEnable=True,
                    DataSources={
                        'S3Logs': {
                            'AutoEnable': True
                        }
                    }
                )
            except botocore.exceptions.ClientError as error:
                print(error)
                continue

enable_guardduty()


# Missing the final piece where I wrap this to all accounts in the org
# + better error handling