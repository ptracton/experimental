#! /usr/bin/env python3

import queue
import threading

import SystemState
        
if __name__ == "__main__":
    import sys
    
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
