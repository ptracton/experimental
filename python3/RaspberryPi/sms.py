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
import datetime
import threading
from twilio.rest import TwilioRestClient
import database

class SMSReceiverThread (threading.Thread):
    """
    This class handles receiving messages via SMS and communicating
    with the Web Server about it
    """

    def __init__(self, config_file=None, response_queue=None, db_queue=None):
        """
        Constructor for class.
        """
        threading.Thread.__init__(self)
        self.response_queue = response_queue
        self.db_queue = db_queue
        self.thread_running = True
        config = configparser.RawConfigParser()
        config.read(config_file)
        self.account_sid = config.get("TWILIO", "SID")
        self.auth_token = config.get("TWILIO", "TOKEN")
        self.twilio_phone = config.get("TWILIO", "PHONE_NUMBER")
        self.client = TwilioRestClient(self.account_sid, self.auth_token)
        self.command_list = config.get("COMMANDS", "TERMS")
        return

    def kill(self):
        """
        Method used for killing the thread
        """
        self.thread_running = False
        return

    def run(self):
        """
        Main thread loop for handling messages
        """
        print("SMS Thread Running")
        while(self.thread_running):
            for message in self.client.messages.list():
                print("New TEXT Message!")
                print(message.body)
                print(message.date_sent)
                print("\n")

                data_dict = {}
                NOW = datetime.datetime.now()
                data_dict[0] = ("SMS_TEXT", message.body)
                data_dict[1] = ("SMS_DATE", """ "{}" """.format(
                    NOW.strftime("%m-%d-%Y")))
                data_dict[2] = ("SMS_TIME", """ time("{}") """.format(
                    NOW.strftime("%H:%M:%S")))

                db_message_data = database.DatabaseDataMessage(
                    table_name="sms",
                    data_dict=data_dict)
                db_message = database.DatabaseMessage(
                    command=database.DatabaseCommand.DB_INSERT_DATA,
                    message=db_message_data)
                db_queue.put(db_message)
                db_task.join(timeout=.65)
                del(db_message)
                del(db_message_data)
                self.client.messages.delete(message.sid)
                
        return

if __name__ == "__main__":
    import logging
    import os
    import queue
    
    print("SMS Thread Testing")

    try:
        os.remove("sms_test.log")
    except:
        pass

    logging.basicConfig(filename="sms_test.log",
                        level=logging.DEBUG,
                        format='%(asctime)s,%(levelname)s,%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    logging.info("Database Thread Testing Start")
    db_queue = queue.Queue()
    response_queue = queue.Queue()
    sms_task = SMSReceiverThread(config_file="/user/tractp1/.ucla.cfg",
                                 response_queue=response_queue,
                                 db_queue=db_queue)

    db = database.Database(database_queue=db_queue,
                           database_file_name="test_sms_thread.db")
    db_task = threading.Thread(target=db.run)
    db_task.start()

    message_data = database.DatabaseDataMessage()
    message_data.schema_file = "sms_table.sql"
    message = database.DatabaseMessage(
        command=database.DatabaseCommand.DB_CREATE_TABLE_SCHEMA,
        message=message_data)
    db_queue.put(message)
    db_task.join(timeout=.65)
    del(message_data)
    del(message)

    sms_thread = threading.Thread(target=sms_task.run, daemon=True)

    sms_thread.start()
    sms_thread.join()
