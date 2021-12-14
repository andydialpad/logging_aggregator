import config
from flask_restful import Resource, Api, reqparse
import boto3
from boto3.dynamodb.conditions import Key
from flask import request


class Host(Resource):
    table = None

    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('logging_aggregator')

    def get(self, host=None):
        print(host)

        responses = self.table.query(
            KeyConditionExpression=Key('host').eq(host),
            ProjectionExpression="#host, filename",
            ExpressionAttributeNames={"#host": "host"},
        )

        items = responses['Items']


        for item in items:
            item['url'] = config.get_rest_api_server(
            ) + host + '/files' + item['filename'] + "/"

        return {'data': items}, 200  # return data and 200 OK
