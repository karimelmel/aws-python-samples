import boto3
import botocore

client = boto3.client('organizations')

def get_organizationmembers():
    response = client.list_accounts()
    return response



def create_table():
    client = boto3.client('dynamodb')
    response = client.create_table(
        AttributeDefinitions=[
            {
            'AttributeName' : 'AccountId',
            'AttributeType' : 'S',
            'AttributeName' : 'Email',
            'AttributeType' : 'S',
            'AttributeName' : 'Name',
            'AttributeType' : 'S'
            },
        ],
        TableName = 'OrganizationInfo',
        KeySchema=[
            {
                'AttributeName' : 'Name',
                'KeyType' : 'HASH',
            },
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    return response



# need to fix syntax so it can loop over dict.

#table = create_table()
#print(table)

def populate_table():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('OrganizationInfo')
    orgmembers = get_organizationmembers()
    print(orgmembers)
    for orgmember in orgmembers['Accounts']:
        response = table.put_item(
            Item = {
                'Name': orgmember['Name'],
               # 'Email': orgmember['Email'],
               # 'AccountId': orgmember['Id'],
            }
        )
        return response
populate_table()

