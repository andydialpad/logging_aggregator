from decimal import Decimal
import boto3


class Datastore:

    table = None

    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('logging_aggregator')

    def save(self, log):

        self.table.put_item(Item=self.create_datastore_entity(log))

    def save_batch(self, logs):

        items = []
        for log in logs:
            items.append(self.create_datastore_entity(log))

        with self.table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)

    def create_datastore_entity(self, log):
        return {
            'filename': log.filename,
            'last_modified': Decimal(log.last_modified),
            'data': log.data,
            'id': str(log.Key)
        }
