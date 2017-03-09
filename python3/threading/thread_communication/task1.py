#! /usr/bin/env python3
"""
File: template_class.py
Author: YOUR NAME GOES HERE

This is an example template of how a python program should be structured.
It is a good starting point for any new coders.

You should change this comment to reflect what will be in the file
"""

#
# Imports go here
#
import task2


class Task1Message():
    """
    Message structure to pass to task 1
    """
    def __init__(self, message=""):
        self.message = message
        return

    
class Task1 ():
    """
    This class does ......
    """

    def __init__(self, other_task_queue=None):
        """
        Constructor does.....
        """
        self.run_forever = True
        self.other_task_queue = other_task_queue
        return

    def kill(self):
        """
        Kill this thread
        """
        self.run_forever = False
        
        return
    
    def run(self, message_q):
        """
        Thread entry point
        """
        
        print("Task1 Running.....")
        task2_message = task2.Task2Message("Task 1 --> Task 2")
        while(self.run_forever):
            message = message_q.get()
            print("TASK1:\t %s" % (message.message))
            self.other_task_queue.put(task2_message)
        print("Terminate Task 1")
        return
