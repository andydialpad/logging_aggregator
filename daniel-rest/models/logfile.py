import config
from flask_restful import Resource, Api, reqparse
import boto3
from boto3.dynamodb.conditions import Key
from flask import request


class LogFile(Resource):
    table = None

    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('logging_aggregator')

    def get(self, host):

        scan_kwargs = {
            'FilterExpression': Key('host').eq(host),
            'ProjectionExpression': "#host, filename",
            'ExpressionAttributeNames': {
                "#host": "host"
            }
        }

        response = self.table.scan(**scan_kwargs)
        items = response.get('Items', [])
        for item in items:
            items['parent'] = config.get_rest_api_server() + "hosts" + ""
        print(items)

        return {'data': {}}, 200  # return data and 200 OK
