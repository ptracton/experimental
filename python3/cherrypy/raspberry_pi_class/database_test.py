#! /usr/bin/env python3

import datetime
import logging
import os
import time
import threading
import queue
import database

if __name__ == "__main__":
    
    print("Database Thread Testing!")

    try:
        os.remove("database_test.log")
    except:
        pass

    logging.basicConfig(filename="database_test.log",
                        level=logging.DEBUG,
                        format='%(asctime)s,%(levelname)s,%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    logging.info("Database Thread Testing Start")
    db_queue = queue.Queue()
    response_queue = queue.Queue()

    db = database.Database(database_queue=db_queue,
                           database_file_name="test_db_thread.db")
    db_task = threading.Thread(target=db.run)
    db_task.start()

    #
    # Create Table via Schema
    #
    print("\n\nCreate Table Via Schema")
    message_data = database.DatabaseDataMessage()
    message_data.schema_file = "test_table1.sql"
    message = database.DatabaseMessage(
        command=database.DatabaseCommand.DB_CREATE_TABLE_SCHEMA,
        message=message_data)
    db_queue.put(message)
    db_task.join(timeout=.65)
    del(message_data)
    del(message)

    #
    # Insert Data into Table
    #
    print("\n\nInsert Data into Table")
    NOW = datetime.datetime.now()
    data_dict = {}
    data_dict[0] = ("TEST_TEXT", """ "This is some text to test with" """)
    data_dict[1] = ("TEST_INT", 1234)
    data_dict[2] = ("TEST_FLOAT", 3.1415)
    data_dict[3] = ("TEST_BLOB", """ "???????????" """)
    data_dict[4] = ("TEST_DATE", """ "{}" """.format(NOW.strftime("%m-%d-%Y")))
    data_dict[5] = ("TEST_TIME", """ time("{}") """.format(
        NOW.strftime("%H:%M:%S")))

    message_data = database.DatabaseDataMessage(table_name="test",
                                                data_dict=data_dict)
    message = database.DatabaseMessage(
        command=database.DatabaseCommand.DB_INSERT_DATA,
        message=message_data)
    db_queue.put(message)
    db_task.join(timeout=.65)
    del(message)
    del(message_data)

    #
    # Get Data Back
    #
    print("\n\nGet Data Back")
    message_data = database.DatabaseDataMessage(table_name="test",
                                                field="TEST_INT",
                                                data=1234,
                                                caller_queue=response_queue)

    message = database.DatabaseMessage(
        command=database.DatabaseCommand.DB_SELECT_DATA,
        message=message_data)

    db_queue.put(message)
    time.sleep(.5)
    db_task.join(timeout=0.65)

    while not response_queue.empty():
        print(response_queue.get())
    del(message_data)
    del(message)

    #
    # Get Last Row ID
    #
    message_data = database.DatabaseDataMessage(table_name="test",
                                                caller_queue=response_queue)
    message = database.DatabaseMessage(
        command=database.DatabaseCommand.DB_GET_LAST_ROW_ID,
        message=message_data)
    db_queue.put(message)
    db_task.join(timeout=0.65)
    while not response_queue.empty():
        print(response_queue.get())
    del(message_data)
    del(message)

    #
    # Delete Table
    #
    print("\n\nDelete Table")
    message_data = database.DatabaseDataMessage(table_name="test")
    message = database.DatabaseMessage(
        command=database.DatabaseCommand.DB_DELETE_TABLE,
        message=message_data)
    db_queue.put(message)
    db_task.join(timeout=0.65)
    del(message_data)
    del(message)

    #
    # Kill thread
    #
    time.sleep(1)
    message = database.DatabaseMessage()
    db.kill()
    db_queue.put(message)
    db_task.join()
    print("Database Thread State: {}".format(db_task.is_alive()))
