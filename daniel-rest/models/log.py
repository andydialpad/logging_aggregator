from boto3.dynamodb.conditions import Key, Attr
from flask import request
from models.entity import Entity


class Log(Entity):
    def get(self, host=None):
        if not self.is_authorized(request):
            return {},403
        args = request.args
        return self.get_with_args(args, host)

    def get_with_args(self, args={}, host=None):
        log_filter = args.get('filter')
        element_count = args.get('count')
        file = args.get('file')
        query_kwargs = {
            'KeyConditionExpression': Key('host').eq(host),
            'ProjectionExpression': "#host, logline, last_modified, filename",
            'ExpressionAttributeNames': {
                "#host": "host",
                },
            }
        if file:
            query_kwargs['FilterExpression'] = Attr("filename").eq(file)
        if log_filter:
            query_kwargs['FilterExpression'] = Attr("logline").contains(log_filter)
        # if element_count:
        #     query_kwargs['Limit'] = int(element_count)
        return {'data':self.sort(self.retrieve_query(query_kwargs=query_kwargs), element_count=element_count)}, 200

    def sort(self, items, element_count=None):
        items.sort(key=lambda itm: itm.get('last_modified'), reverse=True)
        for item in items:
            item['last_modified'] = str(item['last_modified'])
        if element_count:
            max_elements = len(items) if len(items) < int(element_count) else int(element_count)
            items = items[0:max_elements]
        return items
