# import time
import json
import logging
import subprocess

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
            self.switches_config = switches.get("switch-config")

        # use pinheader instead of GPIOx
        gpio.setmode(gpio.BOARD)

        # set pin to input
        gpio.setup(
            self.switches_pins["k1-pin"], gpio.IN, pull_up_down=gpio.PUD_UP
        )
        gpio.setup(
            self.switches_pins["k2-pin"], gpio.IN, pull_up_down=gpio.PUD_UP
        )
        gpio.setup(
            self.switches_pins["k3-pin"], gpio.IN, pull_up_down=gpio.PUD_UP
        )

    def set_callback(self, callback):
        # setting callback
        self._callback = callback

    def gpio_callback(self, switch):
        if switch == self.switches_pins["k1-pin"]:
            logger.info("K1 button pressed")
            # restart python script for development
            subprocess.run(["systemctl", "restart", "cctv"])

        elif switch == self.switches_pins["k2-pin"]:
            # logger.info("K2 button pressed")
            rotation_data = {
                "direction": "left",
                "speed": self.switches_config["speed"],
            }
            # send data to servo
            self._callback(rotation_data)

        elif switch == self.switches_pins["k3-pin"]:
            # logger.info("K3 button pressed")
            rotation_data = {
                "direction": "right",
                "speed": self.switches_config["speed"],
            }
            # send data to servo
            self._callback(rotation_data)

        else:
            logger.warning(
                "input received on unknown channel: {}".format(switch)
            )

    def start(self):
        logger.info("starting user switches")

        gpio.add_event_detect(
            self.switches_pins["k1-pin"],
            gpio.RISING,
            callback=self.gpio_callback,
        )
        gpio.add_event_detect(
            self.switches_pins["k2-pin"],
            gpio.RISING,
            callback=self.gpio_callback,
        )
        gpio.add_event_detect(
            self.switches_pins["k3-pin"],
            gpio.RISING,
            callback=self.gpio_callback,
        )

    def stop(self):
        gpio.remove_event_detect(self.switches_pins["k1-pin"])
        gpio.remove_event_detect(self.switches_pins["k2-pin"])
        gpio.remove_event_detect(self.switches_pins["k3-pin"])

    def terminate(self):
        logger.info("terminating user switches")

        # cleanup gpio
        gpio.cleanup()

        # cleanup objects
        del self.switches_pins
        del self._callback
