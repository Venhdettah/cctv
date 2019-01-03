import threading
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
            self.servo_config = servo.get("servo-config")

        # timer
        self.timer = None

        # servo position var
        self.position = 6.5

        # use pinheader instead of GPIOx
        gpio.setmode(gpio.BOARD)

        # set pin to output
        gpio.setup(self.servo["direction-pin"], gpio.OUT)

        # make pwm instance
        self.servo["_pwm-pin"] = gpio.PWM(
            self.servo["direction-pin"], self.servo_config["frequency"]
        )

    def start(self):
        logger.info("starting servo control")
        self.servo["_pwm-pin"].start(0)

    def stop(self):
        logger.info("stopping servo control")
        self.servo["_pwm-pin"].stop()
        pass

    def terminate(self):
        logger.info("terminating servo control")
        pass

    def set_output(self, rotation_data):
        direction = rotation_data["direction"]
        speed = rotation_data["speed"]

        if direction == "left":
            if self.position >= self.servo_config["max-angle"]:
                logger.warning("servo cannot turn left any further")
            self.position += speed

        elif direction == "right":
            if self.position <= self.servo_config["min-angle"]:
                logger.warning("servo cannot turn right any further")
            self.position -= speed

        else:
            logger.warning("invalid direction: {}".format(direction))
            return None

        self.position = max(self.position, self.servo_config["min-angle"])
        self.position = min(self.position, self.servo_config["max-angle"])

        self._set_servo()

    def _set_servo(self):
        if self.timer:
            self.timer.cancel()

        self.servo["_pwm-pin"].ChangeDutyCycle(self.position)

        self.timer = threading.Timer(0.5, self._stop_servo)
        self.timer.start()
        logger.info("Servo occupied")

    def _stop_servo(self):
        self.servo["_pwm-pin"].ChangeDutyCycle(0)
        logger.info("Servo in free rotation")
        self.current_direction = None
