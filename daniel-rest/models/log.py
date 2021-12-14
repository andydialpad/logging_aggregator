from flask import Flask
from flask_restful import Resource, Api, reqparse
import boto3
from boto3.dynamodb.conditions import Key

class Log(Resource):
  table = None

  def __init__(self):
    dynamodb = boto3.resource('dynamodb')
    self.table = dynamodb.Table('logging_aggregator')

  def get(self):
    responses = self.table.query(KeyConditionExpression=Key('host').eq('andynewman'))

    items = responses['Items']
    for item in items:
      item['last_modified'] = str(item.get('last_modified'))

    return {'data': items}, 200  # return data and 200 OK

  def post(self):
    parser = reqparse.RequestParser()  # initialize
    parser.add_argument('filename', required=True)  # add args
    parser.add_argument('host', required=True)
    parser.add_argument('city', required=True)
    args = parser.parse_args()  # parse arguments to dictionary


    return {'data': 'data.to_dict()'}, 200  # return data with 200 OK