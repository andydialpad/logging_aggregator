import pytest
from botocore.stub import Stubber
import boto3
from models.log import Log
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


def test_get_logs(mocker, ddb_stub):
    ddb_stub.add_response(
        "query", {
            "Items": [
                test_util.create_item(filename="test_filename",
                                      hostname="test_hostname",
                                      last_modified="123",
                                      logging_data="LOGGING DATA")
            ]
        })

    result = Log(Table).get_with_args()

    assert result[1] == 200
    assert result[0]['data'][0]['host'] == 'test_hostname'
    assert result[0]['data'][0]['filename'] == 'test_filename'
    assert result[0]['data'][0]['last_modified'] == '123'
    assert result[0]['data'][0]['logline'] == 'LOGGING DATA'


def test_get_logs_shows_newest_first(mocker, ddb_stub):
    ddb_stub.add_response(
        "query", {
            "Items": [
                test_util.create_item("test_filename", "test_hostname", "123",
                                      "LOGGING DATA"),
                test_util.create_item("test_filename", "test_hostname", "456",
                                      "LATER LINE")
            ]
        })

    result = Log(Table).get_with_args()

    assert result[0]['data'][0]['last_modified'] == '456'
    assert result[0]['data'][0]['logline'] == 'LATER LINE'

    assert result[0]['data'][1]['last_modified'] == '123'
    assert result[0]['data'][1]['logline'] == 'LOGGING DATA'



def test_get_logs_count(mocker, ddb_stub):
    ddb_stub.add_response(
        "query", {
            "Items": [
                test_util.create_item("test_filename", "test_hostname", "123",
                                      "LOGGING DATA"),
                test_util.create_item("test_filename", "test_hostname", "989",
                                      "LATEST_LINE"),
                test_util.create_item("test_filename", "test_hostname", "456",
                                      "LATER LINE")
            ]
        })

    result = Log(Table).get_with_args(args={'count': 2})

    assert result[0]['data'][0]['last_modified'] == '989'
    assert result[0]['data'][0]['logline'] == 'LATEST_LINE'
    assert len(result[0]['data']) == 2
