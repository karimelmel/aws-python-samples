import boto3
import botocore

client = boto3.client('organizations')

def get_organizationmembers():
    response = client.list_accounts()
    return response


# outstanding work