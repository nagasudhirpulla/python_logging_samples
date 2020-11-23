import logging
import sys
from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.formatter import LogstashFormatter
from config import getConfig
import json

# logging configuration
appConfig = getConfig()
host: str = appConfig["logstash_host"]
port: int = appConfig["logstash_port"]

# formatting for log stash
logstash_formatter = LogstashFormatter(
    message_type='python-logstash',
    extra_prefix='dev',
    extra=dict(application='example-app', environment='production'))

test_logger = logging.getLogger('python-logstash-logger')
test_logger.setLevel(logging.INFO)

streamHandler = logging.StreamHandler()
# streamHandler.setFormatter(logstash_formatter)
test_logger.addHandler(streamHandler)

logstashHandler = AsynchronousLogstashHandler(
    host, port, database_path='logstash.db')
logstashHandler.setFormatter(logstash_formatter)
test_logger.addHandler(logstashHandler)

# If you don't want to write to a SQLite database, then you do
# not have to specify a database_path.
# NOTE: Without a database, messages are lost between process restarts.
# test_logger.addHandler(AsynchronousLogstashHandler(host, port))

test_logger.error('python-logstash-async: test logstash error message.')
test_logger.info('python-logstash-async: test logstash info message.')
test_logger.warning('python-logstash-async: test logstash warning message.')

# add extra field to logstash message
extra = dict(
    test_string="python_version-" + repr(sys.version_info),
    test_boolean=True,
    test_dict={"a": 1, "b": "c"},
    test_float=1.23,
    test_integer=123,
    test_list=[1, 2, "3"]
)
test_logger.info('python-logstash: test extra fields', extra=extra)

try:
    x = 1 / 0
except Exception as e:
    test_logger.error("Some error occured", exc_info=e)
    x = 1
