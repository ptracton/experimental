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
# Imports go here
#
import configparser
import datetime
import getpass
import logging
import queue
import threading
import twython
import database


class TwitterStreamer (twython.TwythonStreamer):
    """
    This class does ......
    """
    def __init__(self, app_key=None, app_secret=None, oauth_token=None,
                 oauth_token_secret=None, response_queue=None,
                 filter_list=None, db_queue=None):
        """
        Create our instance of the TwythonStreamer
        """
        twython.TwythonStreamer.__init__(self, app_key, app_secret,
                                         oauth_token, oauth_token_secret)
        self.response_queue = response_queue
        self.db_queue = db_queue
        self.filter_list = filter_list
        self.message_received = False
        return

    def on_success(self, data):
        """
        Come here when we receive a tweet with the right value
        """
        message = ""
        user_name = ""
        screen_name = ""

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
        db_queue.put(db_message)
        db_task.join(timeout=.65)
        del(db_message)
        del(db_message_data)
        self.message_received = True
        return

    def on_error(self, status_code, data):
        self.disconnect()
        print(status_code)


class TwitterThread():
    """
    Thread for handling receiving tweets
    """

    def __init__(self, config_file=None, response_queue=None, db_queue=None):

        """
        Constructor for this class
        """
        user_id = getpass.getuser()
        config = configparser.RawConfigParser()
        config.read("/home/%s/.ucla.cfg" % user_id)
        #config.read("/user/%s/.ucla.cfg" % user_id)

        self.CONSUMER_KEY = config.get("TWITTER", "CONSUMER_KEY")
        self.CONSUMER_SECRET = config.get("TWITTER", "CONSUMER_SECRET")
        self.ACCESS_TOKEN = config.get("TWITTER", "ACCESS_TOKEN")
        self.ACCESS_SECRET = config.get("TWITTER", "ACCESS_SECRET")
        self.command_list = config.get("COMMANDS", "TERMS")
        self.message_received = False
        self.thread_running = True
        self.response_queue = response_queue
        self.db_queue = db_queue
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
            try:
                print("Waiting on Tweet.....")
                stream = TwitterStreamer(app_key=self.CONSUMER_KEY,
                                         app_secret=self.CONSUMER_SECRET,
                                         oauth_token=self.ACCESS_TOKEN,
                                         oauth_token_secret=self.ACCESS_SECRET,
                                         response_queue=self.response_queue,
                                         db_queue=self.db_queue,
                                         filter_list=self.command_list)
                stream.statuses.filter(track=self.command_list)
            except:
                stream.disconnect()

        return

if __name__ == "__main__":
    import os
    import sys
    import time
    
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

    response_queue = queue.Queue()
    
    db_queue = queue.Queue()
    db = database.Database(database_queue=db_queue,
                           database_file_name="test_twitter_thread.db")
    db_task = threading.Thread(target=db.run)
    db_task.start()

    message_data = database.DatabaseDataMessage()
    message_data.schema_file = "twitter_table.sql"
    message = database.DatabaseMessage(
        command=database.DatabaseCommand.DB_CREATE_TABLE_SCHEMA,
        message=message_data)
    db_queue.put(message)
    db_task.join(timeout=.65)
    del(message_data)
    del(message)
    
    twitter_queue = queue.Queue()
    twitter_task = TwitterThread(response_queue=response_queue,
                                 db_queue=db_queue)
    twitter_thread = threading.Thread(target=twitter_task.run, daemon=True)
    twitter_thread.start()

    last_row_id = 0
    last_row = 0
    while(1):
        #
        # Get Last Row ID
        #
        while last_row_id == last_row:
            response_queue = queue.Queue()
            message_data = database.DatabaseDataMessage(
                table_name="twitter",
                caller_queue=response_queue)
            message = database.DatabaseMessage(
                command=database.DatabaseCommand.DB_GET_LAST_ROW_ID,
                message=message_data)
            db_queue.put(message)
            db_task.join(timeout=0.65)
            if response_queue.empty() is False:
                last_row = response_queue.get()
                if last_row > last_row_id:
                    print(last_row)
                    print(last_row_id)

        last_row_id = last_row

        del(message_data)
        del(message)
        del(response_queue)

        #
        # Get Data Back
        #
        print("\n\nGet Data Back")
        response_queue = queue.Queue()
        message_data = database.DatabaseDataMessage(table_name="twitter",
                                                    field="ID",
                                                    data=last_row_id,
                                                    caller_queue=response_queue)
        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_SELECT_DATA,
            message=message_data)
        db_queue.put(message)
        time.sleep(.5)

        while response_queue.empty():
            pass

        response_list = response_queue.get()
        response_text = response_list[0][1]
        response_date = response_list[0][2]
        response_time = response_list[0][3]
        print("Data Response List %s " % (str(response_list)))
        print(response_text)
        print(response_date)
        print(response_time)

        del(message_data)
        del(message)
        
    twitter_thread.join()
    twitter_task.kill()

    print("ALL DONE")
    sys.exit(0)
