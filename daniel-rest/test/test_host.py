import pytest
from botocore.stub import Stubber
import boto3
from models.host import Host
import test_util
session = boto3.Session()
dynamodb = session.resource("dynamodb", region_name='us-west-2')
Table = dynamodb.Table(name="logging_aggregator")


@pytest.fixture
def ddb_stub():
    ddb_stub = Stubber(Table.meta.client)
    ddb_stub.activate()
    yield ddb_stub
    ddb_stub.deactivate()


def test_get_host(mocker, ddb_stub):
    ddb_stub.add_response(
        "query", {
            "Items": [test_util.create_item(hostname='test_hostname', filename='test_filename')]
        })

    result = Host(Table).get("test_hostname")

    assert result[1] == 200
    assert result[0]['data'][0]['filename'] == 'test_filename'
    assert result[0]['data'][0]['host'] == 'test_hostname'
    assert result[0]['data'][0][
        'url'] == 'http://127.0.0.1:3032/hosts/test_hostname/logs?file=test_filename'
