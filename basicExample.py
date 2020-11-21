import logging
import json
from logging import LoggerAdapter


def getEnrichedLogger(name: str, extra: dict) -> LoggerAdapter:
    """get logger object that is enriched with the 'extra' dict
    https://medium.com/devops-dudes/python-logs-a-jsons-journey-to-elasticsearch-ffbabfd44b83

    Args:
        name (str): name of logger
        extra (dict): enrich dict, like {"app_name":"myApp", "server_ip":"10.10.10.10"}

    Returns:
        LoggerAdapter: LoggerAdapter object
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    streamHandler = logging.StreamHandler()
    basicDict = {
        "time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}
    fullDict = {**basicDict, **extra}
    streamFormatter = logging.Formatter(json.dumps(fullDict))
    streamHandler.setFormatter(streamFormatter)
    logger.addHandler(streamHandler)
    loggerAdapter = logging.LoggerAdapter(logger, extra)
    return loggerAdapter


logger = getEnrichedLogger(name="test_app", extra={"app_name": "myTestApp"})
logger.info("Hello World!!!")
try:
    x = 1/0
except Exception as e:
    logger.error("Some error occured", exc_info=e)
    # logger.exception("Some error occured")
