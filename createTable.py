# This script is based on the one they created by Masudur Rahaman Sayem, Akeef Khan
# https://aws.amazon.com/jp/blogs/big-data/connect-to-amazon-msk-serverless-from-your-on-premises-network/

import os
import boto3

region = os.environ.get('AWS_REGION')

if region is None:
    print("AWS_REGION environment variable is not set.")
    region = "us-west-2"  

dynamodb = boto3.client('dynamodb', region_name=region)
table_name = 'device_status'
key_schema = [
    {
        'AttributeName': 'deviceid',
        'KeyType': 'HASH'
    }
]
attribute_definitions = [
    {
        'AttributeName': 'deviceid',
        'AttributeType': 'S'
    }
]
# Create the table with on-demand capacity mode
dynamodb.create_table(
    TableName=table_name,
    KeySchema=key_schema,
    AttributeDefinitions=attribute_definitions,
    BillingMode='PAY_PER_REQUEST'
)
print(f"Table '{table_name}' created with on-demand capacity mode.")
