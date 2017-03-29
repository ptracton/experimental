#! /usr/bin/env python3

import logging
import queue
import threading
import database
import os
import sys
import time

import twitter

if __name__ == "__main__":
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
    twitter_task = twitter.TwitterThread(
        config_file="/home/ptracton/.ucla.cfg",
        response_queue=response_queue,
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
