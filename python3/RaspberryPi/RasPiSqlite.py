#! /usr/bin/env python3

"""
Class: RasPiSqlite

This is a simple wrapper class for dealing with Sqlite.
It is part of a Raspberry Pi Project

"""

import datetime
import logging
import os
import sys
import sqlite3


class RasPiSqlite():
    """
    Class for dealing with Sqlite databases on a Raspberry Pi
    """

    def __init__(self, db_file_name=None, schema_file_name=None):
        """
        Set up the various class wide variables
        """
        self.db_file_name = db_file_name
        self.schema_file_name = schema_file_name
        self.conn = None
        self.cur = None
        self._db_is_new = True
        self._db_is_ready = False
        return

    def __del__(self):
        """
        Close the connection and delete this instance
        """
        if self._db_is_ready:
            self.cur.close()

        return

    def ExecuteSQLQuery(self, query=None, data=""):
        """
        Execute the specified query.  If the DB is not ready or the query
        fails, return False.  If it works, return True
        """
        if query is None or self._db_is_ready is False:
            return False
        logging.info("RasPiSqlite: ExecuteQuery {}".format(query))
        try:
            self.cur.execute(query, data)
            self.conn.commit()
        except Exception as e:
            logging.debug(str(e))
            logging.debug("Failed to execute query %s" % query)
            self.conn.rollback()
            return False

        return True

    def CreateDB(self):
        """
        If the database is new attempt to use the schema file to
        create it.  If there is no schema file, then no tables are in
        the database.
        """
        if self.db_file_name is None:
            return False

        logging.info("RasPiSqlite: CreateDB")

        self._db_is_new = not os.path.exists(self.db_file_name)

        if self._db_is_new is True:
            self.conn = sqlite3.connect(self.db_file_name)
            self.cur = self.conn.cursor()
            if self.schema_file_name is not None:
                self.CreateTableSchema()
            self._db_is_ready = True
        else:
            self.conn = sqlite3.connect(self.db_file_name)
            self.cur = self.conn.cursor()
            self._db_is_ready = True

        return True

    def CreateTableSchema(self):
        """
        With the specified schema table create the table in teh database
        """
        print("RasPiSqlite: Create Table Schema")

        try:
            f = open(self.schema_file_name, 'r')
            schema = f.read()
            self.conn.executescript(schema)
            self.conn.commit()
        except:
            print("Failed to execute schema {}".format(self.schema_file_name))
            return False

        return True

    def CreateTableDictionary(self, table_name=None, table_dict=None):
        """
        Create a new table based on the dictionary passed in
        """
        print("RasPiSqlite: CreateTableDictionary")
        query_string = "CREATE TABLE {table_name} (".format(
            table_name=table_name)

        for k in sorted(table_dict.keys()):
            query_string += "{}".format(table_dict[k])

        query_string += ");"
        print(query_string)
        self.ExecuteSQLQuery(query_string)
        return

    def DeleteTable(self, table_name=None):
        """
        Delete specified table from the database
        """
        if table_name is None or self._db_is_ready is False:
            return False

        print("RasPiSqlite: DropTable %s" % table_name)
        query_string = "DROP TABLE {}".format(table_name)
        self.ExecuteSQLQuery(query_string)

        return True

    def ListTableColumns(self, table_name=None):
        """
        Return a list of the column names for this table
        """
        if table_name is None or self._db_is_ready is False:
            return False

        print("PiSqlite: ListTableColumns")
        query_string = 'PRAGMA TABLE_INFO({table})'.format(table=table_name)
        if self.ExecuteSQLQuery(query_string):
            names = [tup[1] for tup in self.cur.fetchall()]
            return names
        else:
            return False

    def InsertData(self, table_name=None, data_dict=None):
        """
        Insert data into table with columns and data in dictionary
        """

        if table_name is None or data_dict is None or self._db_is_ready is False:
            return False
        print("RasPiSqlite: InsertData {table}".format(table=table_name))

        query_string = "INSERT into {table} (".format(table=table_name)

        for k in sorted(data_dict.keys()):
            query_string += "{}, ".format(data_dict[k][0])
        query_string = query_string[:-2]
        query_string += ") VALUES ("

        for k in sorted(data_dict.keys()):
            query_string += "{}, ".format(data_dict[k][1])

        query_string = query_string[:-2]
        query_string += ")"
        print(query_string)
        self.ExecuteSQLQuery(query_string)
        return True

    def GetLastRowID(self, table_name=None):
        """
        Get the last row id from a table
        """

        if table_name is None or self._db_is_ready is False:
            return

        query_string = "SELECT * FROM {table} WHERE ID = (SELECT MAX(ID) FROM {table})".format(table=table_name)

        self.ExecuteSQLQuery(query_string)
        results = self.cur.fetchone()
        if results is None:
            results = [0]

        return results[0]

    def InsertSensorData(self, table_name=None, sensor_id=None,
                         sensor_data=None,
                         date=None, time=None):
        """
        Insert sensor information into its table
        """

        if table_name is None or self._db_is_ready is False:
            return

        row_id = self.GetLastRowID(table_name)
        row_id = row_id + 1
        query_string = "INSERT into {table} VALUES (?,?,?,?,?)".format(
            table=table_name)
        self.ExecuteSQLQuery(query_string,
                             [row_id, sensor_id, sensor_data, date, time])
        return

    def InsertImageDateTimeStamp(self, table_name=None, image=None,
                                 date=None, time=None):
        """
        Insert an image with date and time stamp
        """

        if table_name is None or image is None or date is None or time is None or self._db_is_ready is False:
            return

        row_id = self.GetLastRowID(table_name)
        row_id = row_id + 1

        query_string = "INSERT INTO {table} VALUES(?, ?, ?, ?)".format(
            table=table_name)
        self.ExecuteSQLQuery(query_string, [row_id, image, date, time])
        return

    def SelectData(self, table_name=None, field=None, data=None):
        """
        Select data from this table where field and data match.
        Returns all rows!
        """
        if table_name is None or field is None or data is None or self._db_is_ready is False:
            return False
        print("RasPiSqlite: SelectData {} {} {} ".format(table_name, field, data))

        query_string = "SELECT * FROM {table} WHERE {field}={data}".format(
            table=table_name,
            field=field, data=data)
        self.ExecuteSQLQuery(query_string)
        results = self.cur.fetchall()
        return results

    def SelectTodaysData(self, table_name=None, date=None):
        """
        Get all of today's data from a table
        """

        return self.SelectData(table_name=table_name,
                               field="IMAGE_DATE", data=date)

    def SelectAllData(self, table_name=None):
        if table_name is None or self._db_is_ready is False:
            return

        query_string = "SELECT * FROM {table}".format(table=table_name)
        self.ExecuteSQLQuery(query_string)
        results = self.cur.fetchall()
        return results

if __name__ == "__main__":
    print("\nTesting RasPiSqlite\n")
    try:
        os.remove("test.db")
    except:
        print("Test.db not present, need to create it")

    #
    # Create DB
    #
    test_db = RasPiSqlite("test.db", "test_table1.sql")
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

    test_db = RasPiSqlite("images_test.db", "images.sql")
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
    
