import json
import ptvsd
import sys
import requests
import boto3

ptvsd.enable_attach(address=('0.0.0.0', 5678), redirect_output=True)

print("waiting for debugger to attach...")

sys.stdout.flush()

ptvsd.wait_for_attach()

print("attached")

# import requests

def create_dynamo_table(event, context, table_name_value, enable_streams=False, read_capacity=1, write_capacity=1,region='us-west-2'):

    table_name = table_name_value
    print('creating table: ' + table_name)
    responseObject = {}
    responseObject['headers'] = {}
    responseObject['headers']['content-type'] = 'application/json'
    
    try:
        
        client = boto3.client(service_name='dynamodb', region_name=region)
        table = (client.create_table(TableName=table_name,
                                    AttributeDefinitions=[
                                        {'AttributeName': 'EventId', 'AttributeType': 'S'},
                                        {'AttributeName': 'EventDay', 'AttributeType': 'N' }
                                        ],
                                    KeySchema=[{'AttributeName': 'EventId', 'KeyType': 'HASH'},
                                        {'AttributeName': 'EventDay','KeyType': 'RANGE'},
                                        ], 
                                    ProvisionedThroughput={'ReadCapacityUnits': read_capacity, 'WriteCapacityUnits': write_capacity}))

        print(table)
        responseObject['statusCode'] = 200
        responseObject['body'] = json.dumps(table)
    except Exception as e:
        print(str(type(e)))
        print(e.__doc__)
        responseObject['statusCode'] = 500
        responseObject['body'] = json.dumps(e.__doc__)
        
    return responseObject
        
def create_handler(event, context):
    table_name = 'user-visits'
    return create_dynamo_table(event, context, table_name, False, 1, 1)
