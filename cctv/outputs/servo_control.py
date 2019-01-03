# import time
import json
import logging


try:
    import RPi.GPIO as gpio
except RuntimeError:
    from unittest.mock import Mock

    gpio = Mock()

from ..abstract import AbstractOutput

logger = logging.getLogger(__name__)


class ServoControl(AbstractOutput):
    def __init__(self):
        logger.info("initializing servo control")

        with open("cctv/config/servo.json", "r") as fd:
            servo = json.load(fd)
            self.servo = servo.get("pins")

        # use pinheader instead of GPIOx
        gpio.setmode(gpio.BOARD)

        # set pin to output
        gpio.setup(self.servo.item(["direction-pin"]), gpio.OUT)

    def start(self):
        logger.info("starting servo control")
        pass

    def stop(self):
        logger.info("stopping servo control")
        pass

    def terminate(self):
        logger.info("terminating servo control")
        pass

    def set_output(self, direction):
        gpio.output(self.servo["direction-pin"], direction)
