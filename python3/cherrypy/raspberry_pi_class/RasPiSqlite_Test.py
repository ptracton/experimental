#! /usr/bin/env python3

import datetime
import os
import sqlite3
import sys

import RasPiSqlite


if __name__ == "__main__":
    print("\nTesting RasPiSqlite\n")
    try:
        os.remove("test.db")
    except:
        print("Test.db not present, need to create it")

    #
    # Create DB
    #
    test_db = RasPiSqlite.RasPiSqlite("test.db", "test_table1.sql")
    test_db.CreateDB()
    columns = test_db.ListTableColumns(table_name="test")
    if columns != ['ID', 'TEST_TEXT', 'TEST_INT', 'TEST_FLOAT',
                   'TEST_BLOB', 'TEST_DATE',
                   'TEST_TIME']:
        print("CreateDB Failed")
        print(columns)
        sys.exit(-1)

    #
    # Create Table Dictionary
    #
    test_dict = {}
    test_dict[0] = "ID INTEGER PRIMARY KEY,"
    test_dict[1] = "TEXT20 CHARACTER(20),"
    test_dict[2] = "TEST_NUMERIC NUMERIC"
    test_db.CreateTableDictionary("second_test", test_dict)
    columns = test_db.ListTableColumns(table_name="second_test")
    if columns != ['ID', 'TEXT20', 'TEST_NUMERIC']:
        print("CreateTableDictionary Failed")
        print(columns)
        sys.exit(-1)

    #
    # Delete Table
    #
    test_db.DeleteTable("second_test")
    columns = test_db.ListTableColumns(table_name="second_test")
    if columns != []:
        print("DeleteTable Failed")
        print(columns)
        sys.exit(-1)

    #
    # Insert and Get Data
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
    test_db.InsertData(table_name="test", data_dict=data_dict)
    print(test_db.SelectData(table_name="test", field="TEST_INT", data=1234))

    del test_db

    #
    # Images
    #
    try:
        os.remove('cat2.png')
    except:
        print('cat2.png already gone')

    test_db = RasPiSqlite.RasPiSqlite("images_test.db", "images.sql")
    test_db.CreateDB()
    IMAGE_FILE = open('cat.png', 'rb')
    NOW = datetime.datetime.now()
    test_db.InsertImageDateTimeStamp("images",
                                     sqlite3.Binary(IMAGE_FILE.read()),
                                     NOW.strftime("%m-%d-%Y"),
                                     NOW.strftime("%H:%M:%S"))
    results = test_db.SelectAllData("images")
    IMAGE_OUT = open('cat2.png', 'wb')
    IMAGE_OUT.write(results[0][1])
    if not os.path.isfile('cat2.png'):
        print('Image Data Base Fail')
        sys.exit(-1)
    else:
        print("Image Data Base Works")

    print("\nAll Done\n\n")
