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
        self.position = {}

        # use pinheader instead of GPIOx
        gpio.setmode(gpio.BOARD)

        self.servo["_pwm-pins"] = {}

        self.camera_index = "0"

        for index, pin in self.servo["direction-pins"].items():

            # set pin to output
            gpio.setup(pin, gpio.OUT)

            # make pwm instance
            self.servo["_pwm-pins"][index] = gpio.PWM(
                pin, self.servo_config["frequency"]
            )

            # set camera position center
            self.position[index] = 6.5

    def start(self):
        logger.info("starting servo control")

        for index, pin in self.servo["direction-pins"].items():
            self.servo["_pwm-pins"][index].start(0)

    def stop(self):
        logger.info("stopping servo control")

        for index, pin in self.servo["direction-pins"].items():
            self.servo["_pwm-pins"][index].stop()
        pass

    def terminate(self):
        logger.info("terminating servo control")
        pass

    def set_output(self, rotation_data):
        direction = rotation_data["direction"]
        speed = rotation_data["speed"]

        if direction == "left":
            if (
                self.position[self.camera_index]
                >= self.servo_config["max-angle"]
            ):
                logger.warning("servo cannot turn left any further")
            self.position[self.camera_index] += speed

        elif direction == "right":
            if (
                self.position[self.camera_index]
                <= self.servo_config["min-angle"]
            ):
                logger.warning("servo cannot turn right any further")
            self.position[self.camera_index] -= speed

        else:
            logger.warning("invalid direction: {}".format(direction))
            return None

        self.position[self.camera_index] = max(
            self.position[self.camera_index], self.servo_config["min-angle"]
        )
        self.position[self.camera_index] = min(
            self.position[self.camera_index], self.servo_config["max-angle"]
        )

        self._set_servo()

    def set_servo(self, camera_index):
        if self.timer:
            self.timer.cancel()

        self._stop_servo()

        self.camera_index = str(camera_index)

    def _set_servo(self):
        if self.timer:
            self.timer.cancel()

        self.servo["_pwm-pins"][self.camera_index].ChangeDutyCycle(
            self.position[self.camera_index]
        )

        self.timer = threading.Timer(0.5, self._stop_servo)
        self.timer.start()
        logger.info("Servo {} occupied".format(self.camera_index))

    def _stop_servo(self):
        self.servo["_pwm-pins"][self.camera_index].ChangeDutyCycle(0)
        logger.info("Servo {} in free rotation".format(self.camera_index))
        self.current_direction = None
