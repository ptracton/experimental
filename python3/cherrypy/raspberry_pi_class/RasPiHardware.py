#! /usr/bin/env python3

import datetime
import logging
import RPi.GPIO as GPIO
import RPLCD.common
from RPLCD.i2c import CharLCD
import database

class MotionSensorClass():
    """
    """

    def __init__(self):
        self.MotionInputPin = 16
        GPIO.setup(self.MotionInputPin, GPIO.IN)
        GPIO.add_event_detect(self.MotionInputPin, GPIO.RISING, callback=self.MotionSensorCallBack)
        return

    def MotionSensorCallBack(self, channel):
        now = datetime.datetime.now()
        print("MotionSensorClass: MotionSensorCallBack {}".format(channel,
                                                               now.strftime("%m-%d-%Y %H:%M:%S")))
        # Trigger camera to take picture
        return

class LCD():
    """
    """

    def __init__(self, db_queue=None):
        self.db_queue = db_queue
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
    def __init__(self, InputPin=18):
        self.InputPin = InputPin
        GPIO.setup(self.InputPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.InputPin, GPIO.FALLING, callback=self.ButtonCallBack, bouncetime=200)
        self.state = False
        return

    def ButtonCallBack(self, channel):
        now = datetime.datetime.now()
        print("PushButtonClass: PushButtonCallBack {}".format(channel,
                                                              now.strftime("%m-%d-%Y %H:%M:%S")))
        self.state = not self.state
        return
    
class RasPiHardware():
    """
    """

    def __init__(self, db_queue=None):
        self.db_queue = db_queue

        self.MotionSensorPowerPin = 24
        self.LCDPowerPin = 25

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(self.MotionSensorPowerPin, GPIO.OUT)
        GPIO.output(self.MotionSensorPowerPin, False)
        
        GPIO.setup(self.LCDPowerPin, GPIO.OUT)
        GPIO.output(self.LCDPowerPin, False)
        
        self.LED = LEDClass()
        self.PushButton = PushButtonClass()
        #self.LCD = PiLCD.PiLCD()
        self.lcd = CharLCD(0x27)
        self.lcd.write_string("Booting...")

        self.MotionSensor = MotionSensorClass()
        return

    def __del__(self):
        print("RasPiHardware Destructor")
        GPIO.cleanup()
        return
