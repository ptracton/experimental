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
import twython

        
class RasPiTwitterStreamer (twython.TwythonStreamer):
    """
    This class does ......
    """

    def __init__(self, config_file=None):
        """
        Constructor does.....
        """
        user_id = getpass.getuser()
        config = configparser.RawConfigParser()
        config.read("/home/%s/.ucla.cfg" % user_id)

        self.CONSUMER_KEY = config.get("TWITTER", "CONSUMER_KEY")
        self.CONSUMER_SECRET = config.get("TWITTER", "CONSUMER_SECRET")
        self.ACCESS_TOKEN = config.get("TWITTER", "ACCESS_TOKEN")
        self.ACCESS_SECRET = config.get("TWITTER", "ACCESS_SECRET")
        
        return

    def kill(self):
        return
    
    def run(self):
        return
