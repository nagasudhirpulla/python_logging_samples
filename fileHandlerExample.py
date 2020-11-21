import logging
from logging.handlers import RotatingFileHandler
from logging import LoggerAdapter
import json


def getEnrichedLogger(name: str, fPath: str, maxBytes: int, backupCount: int, extra: dict) -> LoggerAdapter:
    """get logger object that is enriched with the 'extra' dict
    https://medium.com/devops-dudes/python-logs-a-jsons-journey-to-elasticsearch-ffbabfd44b83

    Args:
        name (str): name of logger
        extra (dict): enrich dict, like {"app_name":"myApp", "server_ip":"10.10.10.10"}
        maxBytes (int): max size of log file
        backupCount (int): number of files to be retained

    Returns:
        LoggerAdapter: LoggerAdapter object
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    streamHandler = logging.StreamHandler()
    fileHandler = RotatingFileHandler(
        fPath, maxBytes=maxBytes, backupCount=100)
    fileHandler.namer = lambda name: name.replace(".log", "") + ".log"
    basicDict = {
        "time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}
    fullDict = {**basicDict, **extra}
    streamFormatter = logging.Formatter(json.dumps(fullDict))
    streamHandler.setFormatter(streamFormatter)
    fileHandler.setFormatter(streamFormatter)
    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)
    loggerAdapter = logging.LoggerAdapter(logger, extra)
    return loggerAdapter


logger = getEnrichedLogger(
    "test", 'log/test.log', 50, 100, {"app_name": "myTestApp"})

logger.info("Hello World!!!")
try:
    x = 1/0
except Exception as e:
    logger.error("Some error occured", exc_info=e)
    # logger.exception("Some error occured")
