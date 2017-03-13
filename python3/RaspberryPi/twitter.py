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
import configparser
import getpass
import logging
import queue
import threading
import twython


class TwitterStreamer (twython.TwythonStreamer):
    """
    This class does ......
    """
    def __init__(self, response_queue=None, filter_list=None):
        twython.TwythonStreamer.__init__(self)
        self.response_queue = response_queue
        self.filter_list = filter_list
        return

    def on_success(self, data):
        """
        Come here when we receive a tweet with the right value
        """
        if 'text' in data:
            print(data['text'].encode('utf-8'))
        return

    def on_error(self, status_code, data):
        self.disconnect()
        print(status_code)


class TwitterThread(threading.Thread):
    """
    Thread for handling receiving tweets
    """

    def __init__(self):

        """
        Constructor for this class
        """

        threading.Thread.__init__(self)
        user_id = getpass.getuser()
        config = configparser.RawConfigParser()
        #config.read("/home/%s/.ucla.cfg" % user_id)
        config.read("/user/%s/.ucla.cfg" % user_id)

        self.CONSUMER_KEY = config.get("TWITTER", "CONSUMER_KEY")
        self.CONSUMER_SECRET = config.get("TWITTER", "CONSUMER_SECRET")
        self.ACCESS_TOKEN = config.get("TWITTER", "ACCESS_TOKEN")
        self.ACCESS_SECRET = config.get("TWITTER", "ACCESS_SECRET")
        self.terms = config.get("TWITTER", "TERMS")
        self.thread_running = True
        return

    def kill(self):
        """
        Terminate this thread
        """
        self.thread_running = False
        return

    def run(self):
        """
        Thread entry point
        """
        logging.info("Twitter Thread Starting")

        while(self.thread_running):
            stream = TwitterStreamer(self.CONSUMER_KEY, self.CONSUMER_SECRET,
                                     self.ACCESS_TOKEN, self.ACCESS_SECRET)
            stream.statuses.filter(track=self.TERMS)
            
        return

if __name__ == "__main__":
    import os

    print("Twitter Thread Testing!")
    try:
        os.remove("twitter_test.log")
    except:
        pass

    logging.basicConfig(filename="twitter_test.log",
                        level=logging.DEBUG,
                        format='%(asctime)s,%(levelname)s,%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    logging.info("Twitter Thread Testing Start")

    twitter_queue = queue.Queue()
    twitter_inst = TwitterThread()
    twitter_thread = threading.Thread(target=twitter_inst.run, daemon=True)
    twitter_thread.start()

    twitter_thread.join()


    print("ALL DONE")
