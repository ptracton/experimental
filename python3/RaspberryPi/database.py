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
import enum
import logging
import time
import RasPiSqlite


class DatabaseDataMessage():
    """
    This is the messages received by the Database class fir
    storing in the SQLite Database
    """

    def __init__(self, table_name=None, data_dict=None,
                 schema_file=None, field=None, data=None, date=None,
                 caller_queue=None):
        self.data_dict = data_dict
        self.schema_file = schema_file
        self.caller_queue = caller_queue
        self.field = field
        self.data = data
        self.date = date
        return


class DatabaseSensorMessage():
    """
    This is the messages received by the Database class fir
    storing in the SQLite Database
    """

    def __init__(self, table_name=None, sensor_id=None,
                 sensor_data=None,
                 date=None, time=None):
        
        self.table_name = table_name
        self.sensor_id = sensor_id
        self.sensor_data = sensor_data
        self.date = date
        self.time = time
        return


class DatabaseImageMessage():
    """
    """

    def __init__(self, table_name=None, image=None,
                 date=None, time=None):
        """
        """
        self.table_name = table_name
        self.image = image
        self.date = date
        self.time = time
        return

    
class DatabaseCommand(enum.Enum):
    """
    Command Messages for the database
    """
    DB_INSERT_DATA = 1
    DB_INSERT_SENSOR_DATA = 2
    DB_INSERT_IMAGE_DATA = 3
    DB_CREATE_TABLE_SCHEMA = 4
    DB_CREATE_TABLE_DICT = 5
    DB_DELETE_TABLE = 6
    DB_SELECT_DATA = 7
    DB_SELECT_ALL_DATA = 8
    DB_SELECT_TODAYS_DATA = 9
    DB_GET_LAST_ROW_ID = 10
    DB_LIST_TABLE_COLUMNS = 11

    
class DatabaseMessage():
    """
    Wrapper class for a database message
    """
    def __init__(self, command=None, message=None):
        self.command = command
        self.message = message
        return


class Database ():
    """
    This is the database class for interfacing with the SQLite database
    """

    def __init__(self, database_queue=None, database_file_name=None):
        """
        Constructor does.....
        """
        self.database_queue = database_queue
        self.thread_running = True
        self.db = RasPiSqlite.RasPiSqlite(db_file_name=database_file_name)
        self.db.CreateDB()
        return

    def CreateTableSchema(self, schema_file=None):
        """
        Create a new table based on a schema
        """
        self.db.schema_file_name = schema_file
        self.db.CreateTableSchema()
        return

    def CreateTableDictionary(self, table_name=None, table_dict=None):
        """
        Create a new table based on a dictionary
        """
        self.db.CreateTableDictionary(table_name=table_name,
                                      table_dict=table_dict)
        return

    def clean_up_thread(self):
        """
        Clean up actions when thread ends
        """
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

        logging.info("Database Thread Up and Running")
        while (self.thread_running):
            if (self.database_queue.empty() is False):
                message = self.database_queue.get()
                print(message.message)
                if message.message == DatabaseMessage.DB_INSERT_DATA:
                    self.db.InsertData(table_name=message.message.table_name,
                                       data_dict=message.message.data_dict)

                elif message.message == DatabaseMessage.DB_INSERT_SENSOR_DATA:
                    self.db.InsertSensorData(table_name=message.message.table_name,
                                             sensor_id=message.message.sensor_id,
                                             sensor_data=message.message.sensor_data,
                                             date=message.message.date,
                                             time=message.message.time)

                elif message.message == DatabaseMessage.DB_INSERT_IMAGE_DATA:
                    self.db.InsertImageDateTimeStamp(table_name=message.message.table_name,
                                                     image=message.message.image,
                                                     date=message.message.date,
                                                     time=message.message.time)

                elif message.message == DatabaseMessage.DB_CREATE_TABLE_SCHEMA:
                    self.db.schema_file_name = message.message.schema_file
                    self.db.CreateTableSchema()

                elif message.message == DatabaseMessage.DB_CREATE_TABLE_DICT:
                    self.db.CreateTableDictionary(table_name=message.message.table_name,
                                                  table_dict=message.message.data_dict)

                elif message.message == DatabaseMessage.DB_DELETE_TABLE:
                    self.db.DeleteTable(table_name=message.message.table_name)

                elif message.message == DatabaseMessage.SELECT_DATA:
                    results = self.db.SelectData(table_name=message.message.table_name,
                                                 field=message.message.field,
                                                 data=message.message.data)
                    if message.message.caller_queue is not None:
                        message.message.caller_queue.put(results)

                elif message.message == DatabaseMessage.DB_SELECT_ALL_DATA:
                    results = self.db.SelectAllData(table_name=message.message.table_name)

                    if message.message.caller_queue is not None:
                        message.message.caller_queue.put(results)

                elif message.message == DatabaseMessage.DB_SELECT_TODAYS_DATA:
                    results = self.db.SelectTodaysData(table_name=message.message.table_name,
                                                    date=message.message.date)

                    if message.message.caller_queue is not None:
                        message.message.caller_queue.put(results)

                elif message.message == DatabaseMessage.DB_GET_LAST_ROW_ID:
                    results = self.db.GetLastRowID(table_name=message.message.table_name)

                    if message.message.caller_queue is not None:
                        message.message.caller_queue.put(results)

                else:
                    print("MESSAGE ERROR: %s" % (message.message))
            else:
                time.sleep(1)

        self.clean_up_thread()
        return


if __name__ == "__main__":
    import datetime
    import os
    import threading
    import queue
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
    
    db = Database(database_queue=db_queue,
                  database_file_name="test_db_thread.db")
    db_task = threading.Thread()

    #
    # Create Table via Schema
    #
    db_task.start()
    message_data = DatabaseDataMessage()
    message_data.schema_file = "test_table1.sql"
    message = DatabaseMessage(command=DatabaseCommand.DB_CREATE_TABLE_SCHEMA,
                              message=message_data)
    db_queue.put(message)
    del(message_data)
    del(message)

    #
    # Insert Data into Table
    #
    NOW = datetime.datetime.now()
    data_dict = {}
    data_dict[0] = ("TEST_TEXT", """ "This is some text to test with" """)
    data_dict[1] = ("TEST_INT", 1234)
    data_dict[2] = ("TEST_FLOAT", 3.1415)
    data_dict[3] = ("TEST_BLOB", """ "???????????" """)
    data_dict[4] = ("TEST_DATE", """ "{}" """.format(NOW.strftime("%m-%d-%Y")))
    data_dict[5] = ("TEST_TIME", """ time("{}") """.format(
        NOW.strftime("%H:%M:%S")))
    print(data_dict)

    message_data = DatabaseDataMessage(table_name="test",
                                       data_dict=data_dict)
    message = DatabaseMessage(command=DatabaseCommand.DB_INSERT_DATA,
                              message=message_data)
    db_queue.put(message)
    del(message)
    del(message_data)

    #
    # Get Data Back
    #

    message_data = DatabaseDataMessage(table_name="test",
                                       field="TEST_INT",
                                       data=1234)
    message = DatabaseMessage(command=DatabaseCommand.DB_SELECT_DATA,
                              message=message_data)

    db_queue.put(message)
    if not response_queue.empty():
        print(response_queue.get())
