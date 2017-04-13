#! /usr/bin/env python3

import enum
import time

import database
import RasPiHardware
   
class SystemStateCommand(enum.Enum):
    """
    """
    SYSTEM_STATE_SystemEnabled = 1
    SYSTEM_STATE_LED = 2
    SYSTEM_STATE_LCD = 3
    SYSTEM_STATE_MotionSensor = 4
    SYSTEM_STATE_GetState = 5

    
class SystemStateMessage():
    """
    """
    def __init__(self, command=None, data=None, response_queue=None):
        self.command = command
        self.data = data
        self.response_queue = response_queue
        return

    
class SystemState():
    """
    This class is used to keep track of the state of the various
    parts of the Rasperry Pi system
    """
    def __init__(self, db_queue=None):
        self.SystemEnabled = False
        self.db_queue=db_queue
#        self.LED = False
#        self.LCD = ""
#        self.MotionSensor = False
        self.Hardware = RasPiHardware.RasPiHardware(db_queue)
        return
    
    def __str__(self):
        string = "SystemEnabled = {}\n".format(self.SystemEnabled)
        string += "LED = {}\n".format(self.Hardware.LED.state)
        string += "LCD = {}\n".format(self.Hardware.LCD.state)
        string += "MotionSensor = {}\n".format(self.Hardware.MotionSensor.state)
        return string

    
class SystemStateThread():
    """
    Thread for managing the system state class
    """
    def __init__(self, SystemStateQueue=None, db_queue=None):
        self.SystemStateQueue = SystemStateQueue
        self.db_queue = db_queue
        self.SystemState = SystemState(db_queue)
        self.thread_running = True
        self.__DEBUG__ = False
        return

    def kill(self):
        """
        Terminate the thread
        """
        if self.__DEBUG__ is True:
            print("SystemStateThread.kill() thread ready to be killed")
        self.thread_running = False
        return

    def run(self):
        """
        Thread entry point
        """
        print("SystemState Thread Running.....")
        while(self.thread_running):
            if self.__DEBUG__ is True:
                print("SystemStateThread.run() Waiting on Queue")
            if self.SystemStateQueue.empty() is False:
                if self.__DEBUG__ is True:
                    print("SystemStateThread.run() Received Message")
                message = self.SystemStateQueue.get()
                if self.__DEBUG__ is True:
                    print("SystemState Command {}".format(message.command))
                if message.command == SystemStateCommand.SYSTEM_STATE_SystemEnabled:
                    self.SystemState.SystemEnabled = not self.SystemState.SystemEnabled
                    if self.SystemState:
                        self.SystemState.Hardware.MotionSensor.Enable()
                        self.SystemState.Hardware.LCD.Enable()
                    else:
                        self.SystemState.Hardware.MotionSensor.Disable()
                        self.SystemState.Hardware.LCD.Disable()
                elif message.command == SystemStateCommand.SYSTEM_STATE_LED:
                    if self.SystemState:
                        print("SystemCommand: LED !")
                        self.SystemState.LED = message.data
                        self.SystemState.Hardware.LED.toggle()
                    else:
                        print("System NOT enabled for LED command")
                elif message.command == SystemStateCommand.SYSTEM_STATE_LCD:
                    if self.SystemState:
                        self.SystemState.Hardware.LCD.Enable()
                        self.SystemState.Hardware.LCD.WriteDisplay(message.data)
                elif message.command == SystemStateCommand.SYSTEM_STATE_MotionSensor:
                    self.SystemState.MotionSensor = message.data
                elif message.command == SystemStateCommand.SYSTEM_STATE_GetState:
                    if message.response_queue is not None:
                        message.response_queue.put(self.SystemState)
                else:
                    print("SystemState Thread Error")
            else:
                time.sleep(1)
        if self.__DEBUG__ is True:
            print("SystemStateThread Terminate")
        return
