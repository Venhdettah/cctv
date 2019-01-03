# import time
# import json
import logging


# try:
#    import RPi.GPIO as gpio
# except RuntimeError:
#    from unittest.mock import Mock
#
#    gpio = Mock()

from ..abstract import AbstractOutput

logger = logging.getLogger(__name__)


class Display(AbstractOutput):
    def __init__(self):
        logger.info("initializing display")
        pass

    def start(self):
        logger.info("starting display")
        pass

    def stop(self):
        logger.info("stopping display")
        pass

    def terminate(self):
        logger.info("terminating display")
        pass
