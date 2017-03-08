#! /usr/bin/env python3

import datetime
import threading
import time


def Thread1():
    """
    First thread
    """
    while(1):
        print("Thread 1: %s" % datetime.datetime.now().strftime("%c"))
        time.sleep(1)


def Thread2():
    """
    """
    while(1):
        print("Thread 2: %s" % datetime.datetime.now().strftime("%c"))
        time.sleep(2)
    
if __name__ == "__main__":
    print("Simple Thread Example")
    thread_1 = threading.Thread(target=Thread1)
    thread_2 = threading.Thread(target=Thread2)

    thread_1.start()
    thread_2.start()

    while (1):
        pass
