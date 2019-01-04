import json
import logging
import logging.config
import signal
import time

from cctv.system import CameraSystem

with open("cctv/config/logging_config.json", "r") as fd:
    logging.config.dictConfig(json.load(fd))
logger = logging.getLogger(__name__)


class ServiceExit(Exception):
    pass


def service_shutdown(signum, frame):
    logging.info("caught signal {}".format(signum))

    # raise custom exception to cleanly terminate all threads
    raise ServiceExit


def ignore_signal(signum, frame):
    logging.info("caught signal {}".format(signum))
    pass


def main():
    # initialize signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    signal.signal(signal.SIGHUP, ignore_signal)

    # initalizing CCTV
    logger.info("initializing CCTV & controls")
    cctv = CameraSystem()

    # starting CCTV
    logger.info("starting CCTV system")
    cctv.start()

    # wait until the input listener stops
    try:
        while True:
            time.sleep(0.01)
    except ServiceExit:
        pass

    # stopping CCTV
    logger.info("stopping CCTV & controls")
    cctv.stop()

    # terminating CCTV
    logger.info("terminating CCTV system")
    cctv.terminate()
    return


if __name__ == "__main__":
    logger.info("running main")
    main()
