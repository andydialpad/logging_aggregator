from flask_restful import Resource
import boto3
import config

class Entity(Resource):
    table = None

    def __init__(self, table=None):
        if table:
            self.table = table
        else:
            dynamodb = boto3.resource('dynamodb')
            self.table = dynamodb.Table('logging_aggregator')

    def is_authorized(self, request):
        if config.is_prod():
            print (request.headers)
            return request.headers.get('Authorization').lower() == 'Bearer SECRETCODE'.lower()


        return True # For non-production

    def retrieve_table_scan(self, scan_kwargs, attribute_identifier=None):
        response = self.table.scan(**scan_kwargs)
        items = response.get('Items', [])
        while not scan_kwargs.get('Limit') and 'LastEvaluatedKey' in response:
            response = self.table.scan(**scan_kwargs, ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response.get('Items'))
        if attribute_identifier:
            items = self.deduplicate_list(attribute_identifier, items)
        return items

    def retrieve_query(self, query_kwargs, attribute_identifier=None):
        response = self.table.query(**query_kwargs)
        items = response.get('Items', [])

        while not query_kwargs.get('Limit') and 'LastEvaluatedKey' in response:
            response = self.table.query(**query_kwargs,
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response.get('Items'))
        if attribute_identifier:
            items = self.deduplicate_list(attribute_identifier, items)
        return items

    def deduplicate_list(self, attribute_identifier, items):
        seen_hosts = []
        result = []
        for item in items:
            if not item[attribute_identifier] in seen_hosts:
                seen_hosts.append(item[attribute_identifier])
                result.append(item)

        return result
