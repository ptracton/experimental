#! /usr/bin/env python3
"""
File: twitter.py
Author: Phil Tracton

This is a class for handling the Twitter Stream Queue.
Run this class in a thread and when the message in the
command list is recieved it is placed in the sqlite3
database via another queue

"""

#
# Imports
#
import configparser
import datetime
import logging
import time
import twython
import database
import SystemState


class TwitterStreamer (twython.TwythonStreamer):
    """
    This class is an extension of the twython.TwythonStreamer.
    The on_success method is called when we get a message from our
    list of commands and we can then process it.
    """
    def __init__(self, app_key=None, app_secret=None, oauth_token=None,
                 oauth_token_secret=None, response_queue=None,
                 filter_list=None, db_queue=None, system_queue=None):
        """
        Create our instance of the TwythonStreamer
        """
        twython.TwythonStreamer.__init__(self, app_key, app_secret,
                                         oauth_token, oauth_token_secret)
        self.response_queue = response_queue
        self.db_queue = db_queue
        self.filter_list = filter_list
        self.message_received = False
        self.SystemQueue = system_queue
        return

    def process_twitter_message(self, message_body=None):
        if message_body is None:
            return
        message_body_list = message_body.split(" ")
        message_body_upper = message_body_list[0].upper()
        data = ""
        
        print("BODY LIST {}".format(message_body_list))
        print("BODY UPPER {}".format(message_body_upper))

        if message_body_upper == "RASPI-LED":
            command = SystemState.SystemStateCommand.SYSTEM_STATE_LED
            print("TWITL_COMMAND = {}".format(command))

        elif message_body_upper == "RASPI-LCD":
            command = SystemState.SystemStateCommand.SYSTEM_STATE_LCD
            list1 = message_body_list[1:]
            data = ' '.join(str(e) for e in list1)
            print("TWITD_COMMAND = {}".format(command))
            
        elif message_body_upper == "RASPI-PICTURE":
            command = SystemState.SystemStateCommand.SYSTEM_STATE_Picture
            print("TWITP_COMMAND = {}".format(command))
        
        message = SystemState.SystemStateMessage(command=command, data=data)
        self.SystemQueue.put(message)
        return
    
    def on_success(self, data):
        """
        Come here when we receive a tweet with the right value
        TODO: only act if from the correct user account!
        """
        message = ""
        user_name = ""
        screen_name = ""
        print(data)
        if 'text' in data:
            message = data['text']
        if 'user' in data:
            if 'name' in data['user']:
                user_name = data['user']['name']
            if 'screen_name' in data['user']:
                screen_name = data['user']['screen_name']

        data_dict = {}
        NOW = datetime.datetime.now()
        data_dict[0] = ("TWITTER_TEXT", """ "{}" """.format(message))
        data_dict[1] = ("TWITTER_USER_NAME", """ "{}" """.format(user_name))
        data_dict[2] = ("TWITTER_SCREEN_NAME", """ "{}" """.format(
            screen_name))
        data_dict[3] = ("TWITTER_DATE", """ "{}" """.format(
            NOW.strftime("%m-%d-%Y")))
        data_dict[4] = ("TWITTER_TIME", """ time("{}") """.format(
            NOW.strftime("%H:%M:%S")))

        db_message_data = database.DatabaseDataMessage(
            table_name="twitter",
            data_dict=data_dict)
        db_message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_INSERT_DATA,
            message=db_message_data)
        self.db_queue.put(db_message)
        del(db_message)
        del(db_message_data)
        self.message_received = True
        self.process_twitter_message(message)
        return


class TwitterThread():
    """
    Thread for handling receiving tweets
    """

    def __init__(self, config_file=None, response_queue=None, db_queue=None,
                 system_queue=None):

        """
        Constructor for this class
        """
        config = configparser.RawConfigParser()
        config.read(config_file)

        self.CONSUMER_KEY = config.get("TWITTER", "CONSUMER_KEY")
        self.CONSUMER_SECRET = config.get("TWITTER", "CONSUMER_SECRET")
        self.ACCESS_TOKEN = config.get("TWITTER", "ACCESS_TOKEN")
        self.ACCESS_SECRET = config.get("TWITTER", "ACCESS_SECRET")
        self.command_list = config.get("COMMANDS", "TERMS")
        self.message_received = False
        self.thread_running = True
        self.response_queue = response_queue
        self.db_queue = db_queue
        self.SystemQueue = system_queue
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
        logging.info("Twitter Thread Starting %s" % (time.ctime()))
        print("Twitter Thread Starting %s" % (time.ctime()))
        while(self.thread_running):
            try:
                # print("Waiting on Tweet.....")
                # Don't check constantly or you will get a 420 error that you
                # are accessing twitter too often
                time.sleep(60)
                print("Checking Tweet %s" % (time.ctime()))
                stream = TwitterStreamer(app_key=self.CONSUMER_KEY,
                                         app_secret=self.CONSUMER_SECRET,
                                         oauth_token=self.ACCESS_TOKEN,
                                         oauth_token_secret=self.ACCESS_SECRET,
                                         response_queue=self.response_queue,
                                         db_queue=self.db_queue,
                                         system_queue = self.SystemQueue,
                                         filter_list=self.command_list)
                stream.statuses.filter(track=self.command_list)
            except:
                stream.disconnect()

        return
