#! /usr/bin/env python3

import logging
import queue
import sys
import threading
import unittest
import SystemState


class TestSystemState(unittest.TestCase):
    
    def setUp(self):
        
        self.SystemStateQueue = queue.Queue()
        self.response_queue = queue.Queue()
        self.SystemStateInst = SystemState.SystemStateThread(
            SystemStateQueue=self.SystemStateQueue)
        self.SystemStateThread = threading.Thread(
            target=self.SystemStateInst.run,
            daemon=True)
        self.SystemStateInst.__DEBUG__ = True
        self.SystemStateThread.start()
        return

    def tearDown(self):
        self.SystemStateInst.kill()
        message = SystemState.SystemStateMessage(
            command=SystemState.SystemStateCommand.SYSTEM_STATE_GetState,
            response_queue=self.response_queue)
        self.SystemStateQueue.put(message)
        self.SystemStateThread.join()
        del(self.response_queue)
        del(self.SystemStateInst)
        del(self.SystemStateQueue)
        del(self.SystemStateThread)
        return

    def test_SystemStateDefaultValues(self):
        state = SystemState.SystemState()
        self.assertFalse(state.SystemEnabled)
        self.assertFalse(state.LED)
        self.assertFalse(state.MotionSensor)
        self.assertEqual(state.LCD, "")
        return

    def test_SystemStateMessageDefaultValues(self):
        message = SystemState.SystemStateMessage()
        self.assertIsNone(message.command)
        self.assertIsNone(message.data)
        self.assertIsNone(message.response_queue)
        return

    def test_SetAndGetSystemState(self):
        message = SystemState.SystemStateMessage(
            command=SystemState.SystemStateCommand.SYSTEM_STATE_SystemEnabled,
            data=True)
        self.SystemStateQueue.put(message)

        message = SystemState.SystemStateMessage(
            command=SystemState.SystemStateCommand.SYSTEM_STATE_MotionSensor,
            data=True)
        self.SystemStateQueue.put(message)
        
        message = SystemState.SystemStateMessage(
            command=SystemState.SystemStateCommand.SYSTEM_STATE_LED,
            data=True)
        self.SystemStateQueue.put(message)

        message = SystemState.SystemStateMessage(
            command=SystemState.SystemStateCommand.SYSTEM_STATE_LCD,
            data="LCD Display")
        self.SystemStateQueue.put(message)

        message = SystemState.SystemStateMessage(
            command=SystemState.SystemStateCommand.SYSTEM_STATE_GetState,
            response_queue=self.response_queue)
        print("Putting Message")
        self.SystemStateQueue.put(message)
        
        print("Wait on Response")
        while self.response_queue.empty():
            pass
        
        response = self.response_queue.get()
        print(str(response))
        self.assertTrue(response.SystemEnabled)
        self.assertTrue(response.MotionSensor)
        self.assertTrue(response.LED)
        self.assertEqual(response.LCD, "LCD Display")
        return

    
if __name__ == "__main__":

    logging.basicConfig(filename="SystemState_test.log",
                        level=logging.DEBUG,
                        format='%(asctime)s,%(levelname)s,%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    logging.info("SystemState Thread Testing Start")

    unittest.main()
    print("\nALL TESTS DONE\n")
    sys.exit(0)
    
    SystemStateQueue = queue.Queue()
    response_queue = queue.Queue()
    SystemStateInst = SystemState.SystemStateThread(
        SystemStateQueue=SystemStateQueue)
    
    SystemStateThread = threading.Thread(target=SystemStateInst.run,
                                         daemon=True)
    SystemStateThread.start()
    
    message = SystemState.SystemStateMessage(
        command=SystemState.SystemStateCommand.SYSTEM_STATE_GetState,
        response_queue=response_queue)
    print("Putting Message")
    SystemStateQueue.put(message)

    print("Wait on Response")
    while response_queue.empty():
        pass

    response = response_queue.get()
    print(str(response))

    message = SystemState.SystemStateMessage(
        command=SystemState.SystemStateCommand.SYSTEM_STATE_SystemEnabled,
        data=True)
    print("Putting Message")
    SystemStateQueue.put(message)

    message = SystemState.SystemStateMessage(
        command=SystemState.SystemStateCommand.SYSTEM_STATE_LCD,
        data=True)
    print("Putting Message")
    SystemStateQueue.put(message)

    message = SystemState.SystemStateMessage(
        command=SystemState.SystemStateCommand.SYSTEM_STATE_MotionSensor,
        data=True)
    print("Putting Message")
    SystemStateQueue.put(message)
    
    message = SystemState.SystemStateMessage(
        command=SystemState.SystemStateCommand.SYSTEM_STATE_LCD,
        data="LCD TESTING")
    print("Putting Message")
    SystemStateQueue.put(message)

    message = SystemState.SystemStateMessage(
        command=SystemState.SystemStateCommand.SYSTEM_STATE_GetState,
        response_queue=response_queue)
    print("Putting Message")
    SystemStateQueue.put(message)
    
    print("Wait on Response")
    while response_queue.empty():
        pass
    
    response = response_queue.get()
    print(str(response))

    SystemStateInst.kill()
    SystemStateQueue.put(message)
    SystemStateThread.join()
    print("Thread State: {}".format(SystemStateThread.is_alive()))
    sys.exit(0)
