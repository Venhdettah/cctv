import logging
import pygame
import pygame.camera

from threading import Thread

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

        pygame.init()
        pygame.camera.init()
        self.size = (320, 240)

        self.display = pygame.display.set_mode(self.size, pygame.FULLSCREEN)

        pygame.mouse.set_visible(0)
        self.camindex = 0
        self.camera = None
        self.init_cams(self.camindex)

    def init_cams(self, which_cam_idx):

        if self.camera is not None:
            self.camera.stop()

        # gets a list of available cameras.
        self.clist = pygame.camera.list_cameras()
        print(self.clist)

        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")

        try:
            cam_id = self.clist[which_cam_idx]
        except IndexError:
            cam_id = self.clist[0]

        # creates the camera of the specified size and in RGB colorspace
        self.camera = pygame.camera.Camera(cam_id, self.size, "RGB")

        # starts the camera
        self.camera.start()

        # self.clock = pygame.time.Clock()

        # create a surface to capture to.  for performance purposes, you want
        # the
        # bit depth to be the same as that of the display surface.
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

    def get_and_process(self):
        # if you don't want to tie the framerate to the camera, you can check
        # and
        # see if the camera has an image ready.  note that while this works
        # on most cameras, some will never return true.
        if 0 and self.camera.query_image():
            # capture an image

            self.snapshot = self.camera.get_image(self.snapshot)

        if 0:
            self.snapshot = self.camera.get_image(self.snapshot)
            # self.snapshot = self.camera.get_image()

            # blit it to the display surface.  simple!
            self.display.blit(self.snapshot, (0, 0))
        else:
            self.snapshot = self.camera.get_image()
            self.display.blit(self.snapshot, (0, 0))

        pygame.display.flip()

    def set_callback(self, callback):
        # setting callback
        self._callback = callback

    def start(self):
        logger.info("starting camera module")
        self.thread = Thread(target=self.camera_process)
        self.thread.start()

    def camera_process(self):
        self.going = True
        while self.going:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT or (
                    e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE
                ):
                    self.going = False
                if e.type == pygame.KEYDOWN:
                    if e.key in range(pygame.K_0, pygame.K_0 + 10):
                        self.init_cams(e.key - pygame.K_0)
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self.camindex += 1
                    if self.camindex >= len(self.clist):
                        self.camindex = 0
                    logging.info(self.camindex)
                    self.init_cams(self.camindex)
                    self._callback(self.camindex)

            self.get_and_process()
            # self.clock.tick()
            # print(self.clock.get_fps())

    def stop(self):
        logger.info("stopping camera module")

        # stop thread
        self.going = False

        # wait till thread is closed
        self.thread.join()

    def terminate(self):
        logger.info("terminating camera module")
        pygame.quit()
