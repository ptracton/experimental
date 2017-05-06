#! /usr/bin/env python3

import configparser
import logging
import os
import queue
import sys
import threading

import database
import twitter

if __name__ == "__main__":
    print("Twitter Thread Testing!")

    try:
        os.remove("twitter_test.log")
    except:
        pass

    config_file = "/home/ptracton/.ucla.cfg"
    config = configparser.RawConfigParser()
    config.read(config_file)

    logging.basicConfig(filename="twitter_test.log",
                        level=logging.DEBUG,
                        format='%(asctime)s,%(levelname)s,%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    logging.info("Twitter Thread Testing Start")

    db_queue = queue.Queue()
    response_queue = queue.Queue()

    db = database.Database(database_queue=db_queue,
                           database_file_name="test_twitter_thread.db")
    db_task = threading.Thread(target=db.run)
    db_task.start()

    twitter_queue = queue.Queue()
    twitter_task = twitter.TwitterThread(config_file=config_file,
                                         response_queue=response_queue,
                                         db_queue=db_queue)
    twitter_thread = threading.Thread(target=twitter_task.run, daemon=True)
    twitter_thread.start()

    print("Create Twitter Table")
    message_data = database.DatabaseDataMessage()
    message_data.schema_file = "twitter_table.sql"
    message = database.DatabaseMessage(
        command=database.DatabaseCommand.DB_CREATE_TABLE_SCHEMA,
        message=message_data)
    db_queue.put(message)
    
    message_data = database.DatabaseDataMessage(table_name="twitter",
                                                caller_queue=response_queue)
    message = database.DatabaseMessage(
        command=database.DatabaseCommand.DB_GET_LAST_ROW_ID,
        message=message_data)
    db_queue.put(message)
    db_task.join(timeout=0.65)
    while not response_queue.empty():
        print(response_queue.get())
