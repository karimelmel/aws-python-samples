import boto3
import botocore

# Simple function to disable GuardDuty detectors in all regions.
# Continues on error, such as in the event where GuardDuty does not exist in a region.

# Get all regions and store in a variable
ec2_client = boto3.client('ec2')
regions = [region['RegionName']
    for region in ec2_client.describe_regions()['Regions']]


def delete_guardduty():
    for region in regions:
        print("Region:", region)
        client = boto3.client('guardduty', region_name=region)
        detectors = client.list_detectors()
        print(detectors)
        for detector in detectors['DetectorIds']:
            try:
                client.delete_detector(
                    DetectorId=detector
                )
            except botocore.exceptions.ClientError as error:
                print(error)
                continue

if __name__ == "__main__":
    delete_guardduty()
