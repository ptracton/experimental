#! /usr/bin/env python3
"""
File: database.py
Author: Phil Tracton

This is a class meant to run as a thread for interacting
with an sqlite3 database

"""

#
# Imports go here
#
import enum
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
        self.table_name = table_name
        self.data_dict = data_dict
        self.schema_file = schema_file
        self.caller_queue = caller_queue
        self.field = field
        self.data = data
        self.date = date
        return

    def __str__(self):
        string = "Table Name = %{}".format(self.table_name)
        return string


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


def DatabaseCommandToString(command):
    string = "UNKNOWN COMMAND"
    if command == DatabaseCommand.DB_INSERT_DATA:
        string = "DB INSERT DATA"
    elif command == DatabaseCommand.DB_INSERT_SENSOR_DATA:
        string = "DB INSERT SENSOR DATA"
    elif command == DatabaseCommand.DB_INSERT_IMAGE_DATA:
        string = "DB INSERT IMAGE DATA"
    elif command == DatabaseCommand.DB_CREATE_TABLE_DICT:
        string = "DB CREATE TABLE DICT"
    elif command == DatabaseCommand.DB_CREATE_TABLE_SCHEMA:
        string = "DB CREATE TABLE SCHEMA"
    elif command == DatabaseCommand.DB_DELETE_TABLE:
        string = "DB DELETE TABLE"
    elif command == DatabaseCommand.DB_SELECT_DATA:
        string = "DB SELECT DATA"
    elif command == DatabaseCommand.DB_SELECT_ALL_DATA:
        string = "DB SELECT ALL DATA"
    elif command == DatabaseCommand.DB_SELECT_TODAYS_DATA:
        string = "DB SELECT TODAYS DATA"
    elif command == DatabaseCommand.DB_GET_LAST_ROW_ID:
        string = "DB GET LAST ROW ID"
    elif command == DatabaseCommand.DB_LIST_TABLE_COLUMNS:
        string = "DB LIST TABLE COLUMNS"
    return string


class DatabaseMessage():
    """
    Wrapper class for a database message
    """
    def __init__(self, command=None, message=None):
        self.command = command
        self.message = message
        return

    def __str__(self):
        string = "Command %s" % DatabaseCommandToString(self.command)
        return string


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
        self.database_file_name = database_file_name
        self.db = RasPiSqlite.RasPiSqlite(db_file_name=self.database_file_name)
        self.db.CreateDB()
        self.active = False
        self.__DEBUG__ = False
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

        print("Database Thread Up and Running")

        while (self.thread_running):
            self.active = False
            if (self.database_queue.empty() is False):
                message = self.database_queue.get()
                self.active = True
                if self.__DEBUG__:
                    print("Command {}".format(message))
                if message.command == DatabaseCommand.DB_INSERT_DATA:
                    self.db.InsertData(table_name=message.message.table_name,
                                       data_dict=message.message.data_dict)

                elif message.command == DatabaseCommand.DB_INSERT_SENSOR_DATA:
                    self.db.InsertSensorData(
                        table_name=message.message.table_name,
                        sensor_id=message.message.sensor_id,
                        sensor_data=message.message.sensor_data,
                        date=message.message.date,
                        time=message.message.time)

                elif message.command == DatabaseCommand.DB_INSERT_IMAGE_DATA:
                    self.db.InsertImageDateTimeStamp(
                        table_name=message.message.table_name,
                        image=message.message.image,
                        date=message.message.date,
                        time=message.message.time)

                elif message.command == DatabaseCommand.DB_CREATE_TABLE_SCHEMA:
                    self.db.schema_file_name = message.message.schema_file
                    self.db.CreateTableSchema()

                elif message.command == DatabaseCommand.DB_CREATE_TABLE_DICT:
                    self.db.CreateTableDictionary(
                        table_name=message.message.table_name,
                        table_dict=message.message.data_dict)

                elif message.command == DatabaseCommand.DB_DELETE_TABLE:
                    self.db.DeleteTable(table_name=message.message.table_name)

                elif message.command == DatabaseCommand.DB_SELECT_DATA:
                    results = self.db.SelectData(
                        table_name=message.message.table_name,
                        field=message.message.field,
                        data=message.message.data)
                    if message.message.caller_queue is not None:
                        message.message.caller_queue.put(results)

                elif message.command == DatabaseCommand.DB_SELECT_ALL_DATA:
                    print("COMMAND: DB Select All Data")
                    results = self.db.SelectAllData(
                        table_name=message.message.table_name)

                    if message.message.caller_queue is not None:
                        message.message.caller_queue.put(results)

                elif message.command == DatabaseCommand.DB_SELECT_TODAYS_DATA:
                    results = self.db.SelectTodaysData(
                        table_name=message.message.table_name,
                        date=message.message.date)

                    if message.message.caller_queue is not None:
                        message.message.caller_queue.put(results)

                elif message.command == DatabaseCommand.DB_GET_LAST_ROW_ID:
                    results = self.db.GetLastRowID(
                        table_name=message.message.table_name)

                    if message.message.caller_queue is not None:
                        message.message.caller_queue.put(results)

                else:
                    print("MESSAGE ERROR: %s" % (message.message))
            else:
                time.sleep(1)

        self.clean_up_thread()
        return


