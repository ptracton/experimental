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
        self.thread_running = False
        config = configparser.RawConfigParser()
        config.read(config_file)
        self.account_sid = config.get("TWILIO", "SID")
        self.auth_token = config.get("TWILIO", "TOKEN")
        self.twilio_phone = config.get("TWILIO", "PHONE_NUMBER")
        self.client = TwilioRestClient(self.account_sid, self.auth_token)
        self.command_list = config.get("COMMANDS", "TERMS")
        self.message_received = False
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
        self.thread_running = True
        twilio_response_string = "Sent from your Twilio trial account - Hello from Twilio!"
        print("SMS Thread Running")
        while(self.thread_running):
            self.message_received = False
            for message in self.client.messages.list():
                #print("New TEXT Message!")
                #print(message.body)
                #print(message.date_sent)
                #print("\n")

                if message.body != twilio_response_string:
                    data_dict = {}
                    NOW = datetime.datetime.now()
                    data_dict[0] = ("SMS_TEXT", """ "{}" """.format(message.body))
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
                    self.message_received = True
        return

if __name__ == "__main__":
    import logging
    import os
    import queue
    import sys
    import time

    print("SMS Thread Testing")

    try:
        os.remove("sms_test.log")
        os.remove("test_sms_thread.db")
    except:
        pass

    logging.basicConfig(filename="sms_test.log",
                        level=logging.DEBUG,
                        format='%(asctime)s,%(levelname)s,%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    logging.info("SMS Thread Testing Start")
    db_queue = queue.Queue()
    response_queue = queue.Queue()
    sms_task = SMSReceiverThread(  #config_file="/user/tractp1/.ucla.cfg",
                                 config_file="/home/ptracton/.ucla.cfg",
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
    #sms_thread.join()
    #
    # You need to send a text message to trigger the next step
    #

    last_row_id = 0
    last_row = 0
    while (1):
        #
        # Get Last Row ID
        #
        #print("DBG: 0")
        while last_row_id == last_row:
            response_queue = queue.Queue()
            message_data = database.DatabaseDataMessage(
                table_name="sms",
                caller_queue=response_queue)
            message = database.DatabaseMessage(
                command=database.DatabaseCommand.DB_GET_LAST_ROW_ID,
                message=message_data)
            db_queue.put(message)
            db_task.join(timeout=0.65)
            if response_queue.empty() is False:
                last_row = response_queue.get()
                #print("Type of last_row %s is %s" % (type(last_row), str(last_row)))
                if last_row > last_row_id:
                    print(last_row)
                    print(last_row_id)
                    
        #print("DBG: 3")
        last_row_id = last_row
        
        del(message_data)
        del(message)
        del(response_queue)
        
        #
        # Get Data Back
        #
        print("\n\nGet Data Back")
        response_queue = queue.Queue()
        message_data = database.DatabaseDataMessage(table_name="sms",
                                                    field="ID",
                                                    data=last_row_id,
                                                    caller_queue=response_queue)
        #print("DBG: 4")
        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_SELECT_DATA,
            message=message_data)
        #print("DBG: 5")
        db_queue.put(message)
        #print("DBG: 6")
        time.sleep(.5)
        #print("DBG: 7")

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

    sms_task.kill()
    sys.exit(0)
