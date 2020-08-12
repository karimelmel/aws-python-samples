import boto3
import botocore
import time

# Karim El-Melhaoui
# Retrieves information from an AWS Organizations Master account.
# Creates a DynamoDB table and populates the retrieved information into DynamoDB.

def get_organizationmembers():
    client = boto3.client('organizations')
    response = client.list_accounts()
    return response


def create_table():
    client = boto3.client('dynamodb')
    try:
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
    except botocore.exceptions.ClientError as error:
        print(error)
    else:
        print('Table has been created..')
        return response
    


def populate_table():
    time.sleep(10) # wait to ensure table has been created.
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('OrganizationInfo')
    orgmembers = get_organizationmembers()
    for i in orgmembers['Accounts']:
        print(i['Id'])
        try:
            table.put_item(
                Item = {
                'Name': i['Name'],
                'Email': i['Email'],
                'AccountId': i['Id'],
                'Status' : i['Status'],
                'JoinedMethod' : i['JoinedMethod'],
                }
            )
        except botocore.exceptions.ClientError as error:
            print(error)
        else:
            continue
    print('Tables have updated populated with account information. Raw data:')
    print('\n', orgmembers)


if __name__ == "__main__":
    create_table()
    populate_table()
