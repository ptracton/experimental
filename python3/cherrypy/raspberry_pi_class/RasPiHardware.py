#! /usr/bin/env python3

import datetime
import time
import picamera
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
import database


class MotionSensorClass():
    """
    """

    def __init__(self, db_queue=None, power_pin=None):
        self.db_queue = db_queue
        self.MotionInputPin = 16
        self.PowerPin = power_pin
        GPIO.setup(self.MotionInputPin, GPIO.IN)

        self.state = False
        return

    def Enable(self):
        """
        """
        self.state = True
        GPIO.setup(self.PowerPin, GPIO.OUT)
        GPIO.output(self.PowerPin, self.state)
        return

    def Disable(self):
        """
        """
        self.state = False
        GPIO.setup(self.PowerPin, GPIO.OUT)
        GPIO.output(self.PowerPin, self.state)
        return


class LCDClass():
    """
    """

    def __init__(self, db_queue=None, power_pin=None):
        self.db_queue = db_queue
        self.PowerPin = power_pin
        self.state = False
        return

    def Enable(self):
        """
        """
        self.state = True
        GPIO.setup(self.PowerPin, GPIO.OUT)
        GPIO.output(self.PowerPin, self.state)
        return

    def Disable(self):
        """
        """
        self.state = False
        GPIO.setup(self.PowerPin, GPIO.OUT)
        GPIO.output(self.PowerPin, self.state)
        return

    def WriteDisplay(self, string=None):
        if string is None:
            return
        print("LCDClass: WriteDisplay {}".format(string))
        lcd = CharLCD(0x27)
        lcd.clear()
        lcd.write_string(string)
        return


class LEDClass():
    """
    """
    def __init__(self, LEDPin=23):
        """
        """
        print("LEDClass Init")
        self.LEDPin = 23
        self.state = False
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LEDPin, GPIO.OUT)
        GPIO.output(self.LEDPin, self.state)
        return

    def toggle(self):
        """
        """
        self.state = not self.state
        print("LED Toggle {}".format(self.state))
        GPIO.output(self.LEDPin, self.state)
        return


class PushButtonClass():
    """
    """
    def __init__(self, db_queue=None, InputPin=18):
        self.db_queue = db_queue
        self.InputPin = InputPin
        GPIO.setup(self.InputPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.state = False
        return


class CameraClass():
    """
    Class for dealing with the camera on a Raspberry Pi
    """

    def __init__(self, db_queue=None, x=1920, y=1280):
        """
        Constructor to make camera instance
        """
        self.db_queue = db_queue
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


class RasPiHardware():
    """
    """

    def __init__(self, db_queue=None):
        self.db_queue = db_queue

        MotionSensorPowerPin = 24
        LCDPowerPin = 14

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        self.Camera = CameraClass(db_queue)
        self.LED = LEDClass(db_queue)
        self.PushButton = PushButtonClass(db_queue)

        self.LCD = LCDClass(db_queue=db_queue, power_pin=LCDPowerPin)
        self.LCD.Disable()

        self.MotionSensor = MotionSensorClass(db_queue=db_queue,
                                              power_pin=MotionSensorPowerPin)
        self.MotionSensor.Disable()

        GPIO.add_event_detect(18, GPIO.FALLING, callback=self.ButtonCallBack,
                              bouncetime=200)
        GPIO.add_event_detect(16, GPIO.RISING,
                              callback=self.MotionSensorCallBack)
        return

    def __del__(self):
        print("RasPiHardware Destructor")
        self.LCD.Disable()
        self.MotionSensor.Disable()
        GPIO.cleanup()
        return
    
    def TakePicture(self, channel=None, name=None):
        """
        """
        now = datetime.datetime.now()
        now_string = now.strftime("%m-%d-%Y %H:%M:%S")
        filename = "images/"+name+"_"+now_string+".jpg"
        self.Camera.simple_picture(filename=filename)

        image_message = database.DatabaseImageMessage(
            table_name="images", image_name=filename,
            date=now.strftime("%m-%d-%Y"),
            time=now.strftime("%H:%M:%S"))
        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_INSERT_IMAGE_DATA,
            message=image_message)
        self.db_queue.put(message)
        return

    def ButtonCallBack(self, channel):
        now = datetime.datetime.now()
        print("PushButtonCallBack {}".format(
            channel,
            now.strftime("%m-%d-%Y %H:%M:%S")))
        # Trigger camera to take picture
        self.TakePicture(channel, "push_button")

        sensor_message = database.DatabaseSensorMessage(
            table_name="buttons",
            sensor_id=channel, sensor_data=True,
            date=now.strftime("%m-%d-%Y"),
            time=now.strftime("%H:%M:%S"))
        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_INSERT_SENSOR_DATA,
            message=sensor_message)
        self.db_queue.put(message)

        return

    def MotionSensorCallBack(self, channel):
        print("MotionSensorClass: MotionSensorCallBack {}".format(channel))
        self.TakePicture(channel, "motion_sensor")

        return
