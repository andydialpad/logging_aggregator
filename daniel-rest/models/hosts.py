import config
from models.entity import Entity


class Hosts(Entity):
    def get(self):

        # Deduplicate list
        attribute_identifier = 'host'

        scan_kwargs = {
            'ProjectionExpression': "#host",
            'ExpressionAttributeNames': {
                "#host": "host"
            }
        }

        return self.retrieve(attribute_identifier, scan_kwargs, self.generate_url)

    def generate_url(self, item):
        item['url'] = config.get_rest_api_server(
        ) + 'hosts/' + item['host'] + '/'
