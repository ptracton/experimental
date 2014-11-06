#! /usr/bin/env python3

'''
Nose testing of the Postgres class
command: nosetests -v Test_Postgres
'''
import Postgres


class Test_Postgres:

    '''
    Nose tests for the Postgres module
    '''

    def __init__(self):
        self.dut = None

    def setup(self):
        '''
        This function is ran before each test case
        '''
        print("Setup")
        self.dut = Postgres.Postgres()
        self.dut.database = "postgres"
        self.dut.password = "python"
        self.dut.username = "postgres"

    def teardown(self):
        '''
        This function is ran after each test case
        '''
        print("Tear Down")
        del self.dut

    def test_get_connection(self):
        '''
        This function tests our ability to connect to a database.
        It shows the correct connection and various fail methods
        '''
        assert self.dut.get_connection() == True

        self.dut.database = "other"
        assert self.dut.get_connection() == False
        self.dut.database = "postgres"

        self.dut.password = "other"
        assert self.dut.get_connection() == False
        self.dut.password = "python"

        self.dut.username = "other"
        assert self.dut.get_connection() == False
        self.dut.username = "postgres"

    def test_create_and_delete_table(self):
        '''
        create and delete tables in the database.
        demonstrate you can not create a table twice
        demonstrate you can not delete a table twice
        '''
        table_name = "test1"
        table_dict = {"first": "text",
                      "second": "int"
                      }
        self.dut.get_connection()
        assert self.dut.create_table(table_name, table_dict) == True
        assert self.dut.create_table(table_name, table_dict) == False

        assert self.dut.delete_table(table_name) == True
        assert self.dut.delete_table(table_name) == False
        assert self.dut.delete_table(None) == False

        temp_cursor = self.dut.cursor
        self.dut.cursor = None
        assert self.dut.create_table(table_name, table_dict) == False

        self.dut.cursor = temp_cursor
        assert self.dut.create_table(table_name, None) == False
