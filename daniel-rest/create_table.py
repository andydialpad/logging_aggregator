import boto3
from boto3.dynamodb.conditions import Key

def create_table(dynamodb):


  table = dynamodb.create_table(
    TableName='logging_aggregator',
    KeySchema=[
      {
        'AttributeName': 'host',
        'KeyType': 'HASH'
        },
      {
        'AttributeName': 'filename',
        'KeyType': 'RANGE'  # Sort key
        },

      ],
    AttributeDefinitions=[
      {
        'AttributeName': 'host',
        'AttributeType': 'N'
        },
      {
        'AttributeName': 'filename',
        'AttributeType': 'S'
        },

      ],
    ProvisionedThroughput={
      'ReadCapacityUnits': 1,
      'WriteCapacityUnits': 1,
      }
    )
  return table

# TODO, add global second index for last_modified (currently done in aws console)