import config
from flask_restful import Resource, Api, reqparse
import boto3
from boto3.dynamodb.conditions import Key
from flask import request


class Entity(Resource):
  table = None

  def __init__(self):
    dynamodb = boto3.resource('dynamodb')
    self.table = dynamodb.Table('logging_aggregator')

  def retrieve(self, attribute_identifier, scan_kwargs, generate_url):
    response = self.table.scan(**scan_kwargs)
    items = response.get('Items', [])
    items = self.deduplicate_list(attribute_identifier, items, generate_url)
    return {'data': items}, 200

  def deduplicate_list(self, attribute_identifier, items, url_generator):
    print(items)

    seen_hosts = []
    result = []
    for item in items:
      if not item[attribute_identifier] in seen_hosts:
        url_generator(item)
        seen_hosts.append(item[attribute_identifier])
        print('added to dedup,  %s' % item[attribute_identifier])
        result.append(item)

    return result
