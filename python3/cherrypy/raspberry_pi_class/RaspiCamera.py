#! /usr/bin/env python3

"""
Class: RaspiCamera

This is a simple wrapper class around the picamera class

"""

import os
import sys
import time
import picamera


class RaspiCamera():
    """
    Class for dealing with the camera on a Raspberry Pi
    """

    def __init__(self, x=1920, y=1280):
        """
        Constructor to make camera instance
        """
        self.camera = picamera.PiCamera()
        self.camera.resolution = (x, y)
        return

    def simple_picture(self, filename=None):
        """
        Take an immediate picture and save to filename
        """
        if filename is None:
            return
        time.sleep(2)
        self.camera.capture(filename)


if __name__ == "__main__":
    """
    RaspiCamera class test code
    """
    print("\nTesting RaspiCamera Class\n")
    camera = RaspiCamera()

    """
    TEST 1: Simple image capture and storing
    """
    print("Starting Test 1")
    filename = "test1_image.png"
    if os.path.exists(filename):
        os.remove(filename)
    camera.simple_picture(filename)
    if not os.path.exists(filename):
        print("Test 1 FAILED to create %s" % filename)
        sys.exit(-1)

    """
    TEST 2: Take picture and resize
    """
    print("Starting Test 2")
    filename = "test2_image.png"
    if os.path.exists(filename):
        os.remove(filename)
#   camera.picture_resize(filename, 1024, 768)
    if not os.path.exists(filename):
        print("Test 2 FAILED to create %s" % filename)
        sys.exit(-1)

    camera.camera.close()
    print ("Done")
    sys.exit(0)
