# This script is based on the one they created by Masudur Rahaman Sayem, Akeef Khan
# https://aws.amazon.com/jp/blogs/big-data/connect-to-amazon-msk-serverless-from-your-on-premises-network/

import base64
import boto3
import json
import os
import random

def convertjson(payload):
    try:
        aa=json.loads(payload)
        return aa
    except:
        return 'err'

def lambda_handler(event, context):
    print(event)
    keyList = event['records'].keys()
    for key in keyList:
        base64records = event['records'][key]
        
        raw_records = [base64.b64decode(x["value"]).decode('utf-8') for x in base64records]
        
        for record in raw_records:
            item = json.loads(record)
            deviceid=item['deviceid']
            interface=item['interface']
            interfacestatus=item['interfacestatus']
            cpuusage=item['cpuusage']
            memoryusage=item['memoryusage']
            event_time=item['event_time']
            
            dynamodb = boto3.client('dynamodb')
            table_name = 'device_status'
            item = {
                'deviceid': {'S': deviceid},  
                'interface': {'S': interface},               
                'interface': {'S': interface},
                'interfacestatus': {'S': interfacestatus},
                'cpuusage': {'S': cpuusage},          
                'memoryusage': {'S': memoryusage},
                'event_time': {'S': event_time},
            }
            
            # Write the item to the DynamoDB table
            response = dynamodb.put_item(
                TableName=table_name,
                Item=item
            )
            
            print(f"Item written to DynamoDB")