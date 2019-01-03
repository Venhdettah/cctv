import logging

# from cctv.inputs import Camera_module
from cctv.inputs import User_switches

# from cctv.outputs import Display
from cctv.outputs import Stepper_control

logger = logging.getLogger(__name__)


class CameraSystem(object):
    def __init__(self):
        logger.info("initializing camera system")
        self.input_us = User_switches()
        # self.input_cm = Camera_module()
        # self.output_dp = Display()
        self.output.sc = Stepper_control()

        self.input_us.set_callback(self.input_received)
        pass

    def start(self):
        logger.info("start camera system")
        self.input_us.start()
        # self.input_cm.start()
        # self.output_dp.start()
        self.output_sc.start()
        pass

    def input_received(self, direction):
        try:
            self.output_sc.set_output(direction)
        except BaseException:
            logger.error("something went wrong in output sc")

    def stop(self):
        logger.info("stop camera system")
        self.input_us.stop()
        # self.input_cm.stop()
        # self.output_dp.stop()
        self.output_sc.stop()
        pass

    def terminate(self):
        logger.info("terminate camera system")
        self.input_us.terminate()
        # self.input_cm.terminate()
        # self.output_dp.terminate()
        self.output_sc.terminate()
        pass
