#! /usr/bin/env python3

import datetime
import logging
import os
import queue
import sys
import time
import threading
import unittest

import database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db_queue = queue.Queue()
        self.response_queue = queue.Queue()

        self.db = database.Database(database_queue=self.db_queue,
                                    database_file_name="test_db_thread.db")
        self.db.__DEBUG__ = True
        self.db_task = threading.Thread(target=self.db.run)
        self.db_task.start()

    def tearDown(self):
        self.message = database.DatabaseMessage()
        self.db.kill()
        self.db_queue.put(self.message)
        self.db_task.join()
        del(self.response_queue)
        del(self.db)
        del(self.db_task)
        return
    
    def test_DatabaseDataMessageDefaultValues(self):
        message = database.DatabaseDataMessage()
        self.assertIsNone(message.table_name)
        self.assertIsNone(message.data_dict)
        self.assertIsNone(message.schema_file)
        self.assertIsNone(message.caller_queue)
        self.assertIsNone(message.field)
        self.assertIsNone(message.data)
        self.assertIsNone(message.date)

    def test_DatabaseDataMessageString(self):
        message = database.DatabaseDataMessage(
            table_name="Test String")
        self.assertEqual(str(message), "Table Name = Test String")
        return

    def test_DatabaseMessageDefaultValues(self):
        message = database.DatabaseMessage()
        self.assertIsNone(message.message)
        self.assertIsNone(message.command)
        return
    
    def test_DatabaseSensorMessageDefaultValuse(self):
        message = database.DatabaseSensorMessage()
        self.assertIsNone(message.table_name)
        self.assertIsNone(message.sensor_id)
        self.assertIsNone(message.sensor_data)
        self.assertIsNone(message.date)
        self.assertIsNone(message.time)
        return

    def test_DatabaseImageMessageDefaultValuse(self):
        message = database.DatabaseImageMessage()
        self.assertIsNone(message.table_name)
        self.assertIsNone(message.image)
        self.assertIsNone(message.date)
        self.assertIsNone(message.time)
        return
        
    def test_DatabaseCreateTableSchema(self):
        message_data = database.DatabaseDataMessage()
        message_data.schema_file = "test_table1.sql"
        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_CREATE_TABLE_SCHEMA,
            message=message_data)
        self.db_queue.put(message)

        message_data = database.DatabaseDataMessage(
            table_name="test",
            caller_queue=self.response_queue)
        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_LIST_TABLE_COLUMNS,
            message=message_data)
        self.db_queue.put(message)
        while self.response_queue.empty():
            pass
        data = self.response_queue.get()
        print(data)
        self.assertListEqual(data, ['ID', 'TEST_TEXT',
                                    'TEST_INT', 'TEST_FLOAT',
                                    'TEST_BLOB', 'TEST_DATE', 'TEST_TIME'])
        return
    
    def test_DatabaseCreateTableDict(self):
        message_data = database.DatabaseDataMessage()
        NOW = datetime.datetime.now()
        data_dict = {}
        data_dict[0] = ("TEST_TEXT", """ "This is some text to test with" """)
        data_dict[1] = ("TEST_INT", 1234)
        data_dict[2] = ("TEST_FLOAT", 3.1415)
        data_dict[3] = ("TEST_BLOB", """ "???????????" """)
        data_dict[4] = ("TEST_DATE", """ "{}" """.format(
            NOW.strftime("%m-%d-%Y")))
        data_dict[5] = ("TEST_TIME", """ time("{}") """.format(
            NOW.strftime("%H:%M:%S")))
        message_data.data_dict = data_dict
        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_CREATE_TABLE_DICT,
            message=message_data)
        self.db_queue.put(message)

        message_data = database.DatabaseDataMessage(
            table_name="test",
            caller_queue=self.response_queue)
        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_LIST_TABLE_COLUMNS,
            message=message_data)
        self.db_queue.put(message)
        while self.response_queue.empty():
            pass
        data = self.response_queue.get()
        print(data)
        self.assertListEqual(data, ['ID', 'TEST_TEXT',
                                    'TEST_INT', 'TEST_FLOAT',
                                    'TEST_BLOB', 'TEST_DATE', 'TEST_TIME'])
        return

    def test_DatabaseDeleteTable(self):

        # Create Table
        message_data = database.DatabaseDataMessage()
        message_data.schema_file = "test_table1.sql"
        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_CREATE_TABLE_SCHEMA,
            message=message_data)
        self.db_queue.put(message)

        # Confirm that worked
        message_data = database.DatabaseDataMessage(
            table_name="test",
            caller_queue=self.response_queue)
        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_LIST_TABLE_COLUMNS,
            message=message_data)
        self.db_queue.put(message)
        while self.response_queue.empty():
            pass
        data = self.response_queue.get()
        print(data)
        self.assertListEqual(data, ['ID', 'TEST_TEXT',
                                    'TEST_INT', 'TEST_FLOAT',
                                    'TEST_BLOB', 'TEST_DATE', 'TEST_TIME'])

        # Delete table
        message_data = database.DatabaseDataMessage(
            table_name="test",
            caller_queue=self.response_queue)
        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_DELETE_TABLE,
            message=message_data)
        self.db_queue.put(message)

        # Confirm it deleted
        message_data = database.DatabaseDataMessage(
            table_name="test",
            caller_queue=self.response_queue)
        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_LIST_TABLE_COLUMNS,
            message=message_data)
        self.db_queue.put(message)
        while self.response_queue.empty():
            pass
        data = self.response_queue.get()
        print(data)
        self.assertListEqual(data, [])
        return

    def test_DatabaseInsertAndSelectData(self):
        # Create Table
        message_data = database.DatabaseDataMessage(
            caller_queue=self.response_queue)
        message_data.schema_file = "test_table1.sql"
        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_CREATE_TABLE_SCHEMA,
            message=message_data)
        self.db_queue.put(message)

        # Populate Table
        message_data = database.DatabaseDataMessage(
            table_name="test",
            caller_queue=self.response_queue)
        NOW = datetime.datetime.now()
        data_dict = {}
        data_dict[0] = ("TEST_TEXT", """ "This is some text to test with" """)
        data_dict[1] = ("TEST_INT", 1234)
        data_dict[2] = ("TEST_FLOAT", 3.1415)
        data_dict[3] = ("TEST_BLOB", """ "???????????" """)
        data_dict[4] = ("TEST_DATE", """ "{}" """.format(
            NOW.strftime("%m-%d-%Y")))
        data_dict[5] = ("TEST_TIME", """ time("{}") """.format(
            NOW.strftime("%H:%M:%S")))
        message_data.data_dict = data_dict
        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_INSERT_DATA,
            message=message_data)
        self.db_queue.put(message)
        time.sleep(1)

        # Retrieve data and check
        del(message)
        del(self.response_queue)
        self.response_queue = queue.Queue()
        message_data = database.DatabaseDataMessage(
            table_name="test",
            field="TEST_INT",
            data=1234,
            caller_queue=self.response_queue)

        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_SELECT_DATA,
            message=message_data)

        self.db_queue.put(message)
        print("WAITING.....")
#        while self.response_queue.empty():
        results = self.response_queue.get()
        print(results)
        self.assertEqual(results[0][0], 1)
        self.assertEqual(results[0][1], "This is some text to test with")
        self.assertEqual(results[0][2], 1234)
        self.assertEqual(results[0][3], 3.1415)
        self.assertEqual(results[0][4], "???????????")
        self.assertEqual(results[0][5], NOW.strftime("%m-%d-%Y"))
        self.assertEqual(results[0][6], NOW.strftime("%H:%M:%S"))
        return

    def test_DatabaseInsertandSelectAllDataAndGetLastRow(self):
        # Create Table
        message_data = database.DatabaseDataMessage(
            caller_queue=self.response_queue)
        message_data.schema_file = "test_table1.sql"
        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_CREATE_TABLE_SCHEMA,
            message=message_data)
        self.db_queue.put(message)

        # Populate Table
        message_data = database.DatabaseDataMessage(
            table_name="test",
            caller_queue=self.response_queue)
        NOW = datetime.datetime.now()
        data_dict = {}
        data_dict[0] = ("TEST_TEXT", """ "This is some text to test with" """)
        data_dict[1] = ("TEST_INT", 1234)
        data_dict[2] = ("TEST_FLOAT", 3.1415)
        data_dict[3] = ("TEST_BLOB", """ "???????????" """)
        data_dict[4] = ("TEST_DATE", """ "{}" """.format(
            NOW.strftime("%m-%d-%Y")))
        data_dict[5] = ("TEST_TIME", """ time("{}") """.format(
            NOW.strftime("%H:%M:%S")))
        message_data.data_dict = data_dict
        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_INSERT_DATA,
            message=message_data)
        self.db_queue.put(message)
        time.sleep(1)

        del(message)
        del(self.response_queue)
        self.response_queue = queue.Queue()
        message_data = database.DatabaseDataMessage(
            table_name="test",
            caller_queue=self.response_queue)
        NOW2 = datetime.datetime.now()
        data_dict = {}
        data_dict[0] = ("TEST_TEXT",
                        """ "This is some more text to test with" """)
        data_dict[1] = ("TEST_INT",  5678)
        data_dict[2] = ("TEST_FLOAT", 2.8181)
        data_dict[3] = ("TEST_BLOB", """ "??***********" """)
        data_dict[4] = ("TEST_DATE", """ "{}" """.format(
            NOW2.strftime("%m-%d-%Y")))
        data_dict[5] = ("TEST_TIME", """ time("{}") """.format(
            NOW2.strftime("%H:%M:%S")))
        message_data.data_dict = data_dict
        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_INSERT_DATA,
            message=message_data)
        self.db_queue.put(message)
        time.sleep(1)

        # Retrieve data and check
        del(message)
        del(self.response_queue)
        self.response_queue = queue.Queue()
        message_data = database.DatabaseDataMessage(
            table_name="test",
            caller_queue=self.response_queue)

        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_SELECT_ALL_DATA,
            message=message_data)

        self.db_queue.put(message)
        print("WAITING.....")
#        while self.response_queue.empty():
        results = self.response_queue.get()
        print(results)
        self.assertEqual(results[0][0], 1)
        self.assertEqual(results[0][1], "This is some text to test with")
        self.assertEqual(results[0][2], 1234)
        self.assertEqual(results[0][3], 3.1415)
        self.assertEqual(results[0][4], "???????????")
        self.assertEqual(results[0][5], NOW.strftime("%m-%d-%Y"))
        self.assertEqual(results[0][6], NOW.strftime("%H:%M:%S"))

        self.assertEqual(results[1][0], 2)
        self.assertEqual(results[1][1], "This is some more text to test with")
        self.assertEqual(results[1][2], 5678)
        self.assertEqual(results[1][3], 2.8181)
        self.assertEqual(results[1][4], "??***********")
        self.assertEqual(results[1][5], NOW2.strftime("%m-%d-%Y"))
        self.assertEqual(results[1][6], NOW2.strftime("%H:%M:%S"))

        # Get last row id
        del(message)
        del(self.response_queue)
        self.response_queue = queue.Queue()
        message_data = database.DatabaseDataMessage(
            table_name="test",
            caller_queue=self.response_queue)

        message = database.DatabaseMessage(
            command=database.DatabaseCommand.DB_GET_LAST_ROW_ID,
            message=message_data)

        self.db_queue.put(message)
        print("WAITING.....")
#        while self.response_queue.empty():
        results = self.response_queue.get()
        print(results)
        self.assertEqual(results, 2)
        return
        
    
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

    unittest.main()
    print("\nALL TESTS DONE\n")
    sys.exit(0)
    
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
