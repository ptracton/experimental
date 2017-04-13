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

    def __init__(self, db_queue=None, power_pin=None):
        self.db_queue=db_queue
        self.MotionInputPin = 16
        self.PowerPin = power_pin
        GPIO.setup(self.MotionInputPin, GPIO.IN)
        GPIO.add_event_detect(self.MotionInputPin, GPIO.RISING, callback=self.MotionSensorCallBack)
        self.state = False
        return

    def Enable(self):
        """
        """
        self.state=True
        GPIO.setup(self.PowerPin, GPIO.OUT)
        GPIO.output(self.PowerPin, self.state)
        return

    def Disable(self):
        """
        """
        self.state=False
        GPIO.setup(self.PowerPin, GPIO.OUT)
        GPIO.output(self.PowerPin, self.state)
        return
    
    def MotionSensorCallBack(self, channel):
        now = datetime.datetime.now()
        print("MotionSensorClass: MotionSensorCallBack {}".format(channel,
                                                               now.strftime("%m-%d-%Y %H:%M:%S")))
        # Trigger camera to take picture
        return

class LCDClass():
    """
    """

    def __init__(self, db_queue=None, power_pin=None):
        self.db_queue = db_queue
        self.PowerPin = power_pin
        self.state=False
        return

    def Enable(self):
        """
        """
        self.state=True
        GPIO.setup(self.PowerPin, GPIO.OUT)
        GPIO.output(self.PowerPin, self.state)
        return

    def Disable(self):
        """
        """
        self.state=False
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
        self.db_queue=db_queue
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

        MotionSensorPowerPin = 24
        LCDPowerPin = 14

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        
     
        
        self.LED = LEDClass(db_queue)
        self.PushButton = PushButtonClass(db_queue)
        self.LCD=LCDClass(db_queue=db_queue, power_pin=LCDPowerPin)
        self.LCD.Disable()
        self.MotionSensor = MotionSensorClass(db_queue=db_queue, power_pin=MotionSensorPowerPin)
        self.MotionSensor.Disable()
        return

    def __del__(self):
        print("RasPiHardware Destructor")
        GPIO.cleanup()
        return
