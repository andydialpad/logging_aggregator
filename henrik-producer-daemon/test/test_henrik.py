import datetime
import unittest
from app import App
from models.log import Log
import os

class TestHenrik(unittest.TestCase):
  EXAMPLE_FILENAME = 'example_metadata'
  TEST_TIMESTAMP = 1639323944.6201484


  def test_write_metadata(self):
    metadata = {'syslog': {'last_modified' : self.TEST_TIMESTAMP}}
    App.write_metadata(metadata, self.EXAMPLE_FILENAME)
    result = App.get_metadata(self.EXAMPLE_FILENAME)
    self.assertEqual(self.TEST_TIMESTAMP, result.get('syslog')['last_modified'])

  def test_log_entity(self):
    log = Log(filename='test', data='line', last_modified=self.TEST_TIMESTAMP)
    self.assertEqual('test', log.filename)
    self.assertEqual('line', log.data)
    self.assertEqual(self.TEST_TIMESTAMP, log.last_modified)

