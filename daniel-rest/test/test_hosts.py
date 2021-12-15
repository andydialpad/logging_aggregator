import pytest
from botocore.stub import Stubber
import boto3
from models.hosts import Hosts

session = boto3.Session()
dynamodb = session.resource("dynamodb", region_name='us-west-2')
Table = dynamodb.Table(name="logging_aggregator")


@pytest.fixture
def ddb_stub():
    ddb_stub = Stubber(Table.meta.client)
    ddb_stub.activate()
    yield ddb_stub
    ddb_stub.deactivate()


def test_get_hosts(mocker, ddb_stub):
    ddb_stub.add_response(
        "scan", {
            "Items": [{
                "host": {
                    "S": "test_hostname"
                }
            }, {
                "host": {
                    "S": "other_hostname"
                }
            }]
        })

    result = Hosts(Table).get()

    assert result[1] == 200
    assert result[0]['data'][0]['host'] == 'test_hostname'
    assert result[0]['data'][1]['host'] == 'other_hostname'


def test_get_hosts_removes_duplicates(mocker, ddb_stub):
  ddb_stub.add_response(
    "scan", {
      "Items": [{
        "host": {
          "S": "test_hostname"
          }
        }, {
        "host": {
          "S": "test_hostname"
          }
        }]
      })

  result = Hosts(Table).get()

  assert result[0]['data'][0]['host'] == 'test_hostname'
  assert len(result[0]['data']) == 1
