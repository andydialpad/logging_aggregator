import config
from models.entity import Entity
from flask import request

class Hosts(Entity):
    def get(self):
        if not self.is_authorized(request):
            return {}, 403
        # Deduplicate list
        attribute_identifier = 'host'

        scan_kwargs = {
            'ProjectionExpression': "#host",
            'ExpressionAttributeNames': {
                "#host": "host"
            }
        }

        return {'data': self.generate_urls(
            self.retrieve_table_scan(attribute_identifier=attribute_identifier,
                                     scan_kwargs=scan_kwargs))}, 200

    def generate_urls(self, items):
        for item in items:
            self.generate_url(item)
        return items

    def generate_url(self, item):
        if item and item.get('host'):
            item['url'] = config.get_rest_api_server() + 'hosts/' + item.get('host') + '/'
