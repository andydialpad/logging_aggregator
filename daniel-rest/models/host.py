import config
from boto3.dynamodb.conditions import Key
from models.entity import Entity
from flask import request


class Host(Entity):

    def get(self, host=None):
        if not self.is_authorized(request):
            return {}, 403

        attribute_identifier = 'filename'
        query_kwargs = {
            'KeyConditionExpression': Key('host').eq(host),
            'ProjectionExpression': "#host, filename",
            'ExpressionAttributeNames': {
                "#host": "host"
            },
        }

        query_result = self.retrieve_query(attribute_identifier=attribute_identifier,
            query_kwargs=query_kwargs)
        urls = self.generate_urls(query_result, host)
        return {'data': urls}, 200

    def generate_urls(self, items, host):
        for item in items:
            self.generate_url(item, host)
        return items

    def generate_url(self, item, host):
        if item and item.get('filename'):
            item['url'] = config.get_rest_api_server(
                ) +'hosts/'+ host + '/logs?file=' + item.get('filename')