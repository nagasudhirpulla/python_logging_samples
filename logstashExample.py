import logging
import sys
from logstash_async.handler import AsynchronousLogstashHandler
from config import getConfig
import json

appConfig = getConfig()
host: str = appConfig["logstash_host"]
port: int = appConfig["logstash_port"]

test_logger = logging.getLogger('python-logstash-logger')
test_logger.setLevel(logging.INFO)
# test_logger.addHandler(AsynchronousLogstashHandler(
#     host, port, database_path='logstash.db'))
test_logger.addHandler(logging.StreamHandler())

# If you don't want to write to a SQLite database, then you do
# not have to specify a database_path.
# NOTE: Without a database, messages are lost between process restarts.
# test_logger.addHandler(AsynchronousLogstashHandler(host, port))

test_logger.error('python-logstash-async: test logstash error message.')
test_logger.info('python-logstash-async: test logstash info message.')
test_logger.warning('python-logstash-async: test logstash warning message.')

# add extra field to logstash message
extra = {
    'test_string': 'python version: ' + repr(sys.version_info),
    'test_boolean': True,
    'test_dict': {'a': 1, 'b': 'c'},
    'test_float': 1.23,
    'test_integer': 123,
    'test_list': [1, 2, '3'],
}
test_logger.info('python-logstash: test extra fields', extra=extra)