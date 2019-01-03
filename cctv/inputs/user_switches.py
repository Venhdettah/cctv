import time
import json
import logging

try:
    import RPi.GPIO as gpio
except RuntimeError:
    from unittest.mock import Mock

    gpio = Mock()

from ..abstract import AbstractInput

logger = logging.getLogger(__name__)


class UserSwitches(AbstractInput):
    def __init__(self):
        logger.info("initializing user switches")

        with open("cctv/config/switches.json", "r") as fd:
            switches = json.load(fd)
            self.switches_pins = switches.get("pins")

        # use pinheader instead of GPIOx
        gpio.setmode(gpio.BOARD)

        # set pin to input
        gpio.setup(self.switches_pins.item(["k1-pin"]), gpio.IN)
        gpio.setup(self.switches_pins.item(["k2-pin"]), gpio.IN)
        gpio.setup(self.switches_pins.item(["k3-pin"]), gpio.IN)

    def set_callback(self, callback):
        # setting callback
        self._callback = callback

    def start(self):
        logger.info("starting user switches")

        while True:
            if gpio.input(self.switches_pins.item(["k1-pin"])):
                logger.info("K1 button pressed")
                # send data to something

            if gpio.input(self.switches_pins.item(["k2-pin"])):
                logger.info("K2 button pressed")
                direction = 0
                # send data to stepper

            if gpio.input(self.switches_pins.item(["k3-pin"])):
                logger.info("K3 button pressed")
                direction = 1
                # send data to stepper
            time.sleep(0.1)
            self._callback(direction)

    def terminate(self):
        logger.info("terminating user switches")

        # cleanup gpio
        gpio.cleanup()

        # cleanup objects
        del self.switches_pins
        del self._callback
