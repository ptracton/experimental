#! /usr/bin/env python3

import enum
import time

   
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
    def __init__(self):
        self.SystemEnabled = False
        self.LED = False
        self.LCD = ""
        self.MotionSensor = False
        return
    
    def __str__(self):
        string = "SystemEnabled = {}\n".format(self.SystemEnabled)
        string += "LED = {}\n".format(self.LED)
        string += "LCD = {}\n".format(self.LCD)
        string += "MotionSensor = {}\n".format(self.MotionSensor)
        return string

    
class SystemStateThread():
    """
    Thread for managing the system state class
    """
    def __init__(self, SystemStateQueue=None):
        self.SystemStateQueue = SystemStateQueue
        self.SystemState = SystemState()
        self.thread_running = True
        return

    def kill(self):
        """
        Terminate the thread
        """
        self.thread_running = False
        return

    def run(self):
        """
        Thread entry point
        """
        print("SystemState Thread Running.....")
        while(self.thread_running):
            if self.SystemStateQueue.empty() is False:
                message = self.SystemStateQueue.get()
                print("SystemState Command {}".format(message.command))
                if message.command == SystemStateCommand.SYSTEM_STATE_SystemEnabled:
                    self.SystemState.SystemEnabled = message.data
                elif message.command == SystemStateCommand.SYSTEM_STATE_LED:
                    self.SystemState.LED = message.data
                elif message.command == SystemStateCommand.SYSTEM_STATE_LCD:
                    self.SystemState.LCD = message.data
                elif message.command == SystemStateCommand.SYSTEM_STATE_MotionSensor:
                    self.SystemState.MotionSensor = message.data
                elif message.command == SystemStateCommand.SYSTEM_STATE_GetState:
                    if message.response_queue is not None:
                        message.response_queue.put(self.SystemState)
                else:
                    print("SystemState Thread Error")
            else:
                time.sleep(1)
        return
