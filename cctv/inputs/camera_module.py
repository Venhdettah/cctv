# import time
# import json
import logging


# try:
#    import RPi.GPIO as gpio
# except RuntimeError:
#    from unittest.mock import Mock
#
#    gpio = Mock()

from ..abstract import AbstractInput

logger = logging.getLogger(__name__)


class CameraModule(AbstractInput):
    def __init__(self):
        logger.info("initializing camera module")

    def start(self):
        logger.info("starting camera module")

    def cleanup(self):
        logger.info("cleanup camera module")
