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

    def __init__(self):
        """
        Constructor does.....
        """
        self.run_forever = True
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
        while(self.run_forever):
            message = message_q.get()
            print(message.message)
        print("Terminate Task 1")
        return
