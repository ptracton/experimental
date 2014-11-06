'''
This is a wrapper class around psycopg2 to make it easy to work with a
postgres sql database
'''
#! /usr/bin/env python3

import psycopg2


class Postgres:

    '''
    Wrapper around psycopg2 to make transaction with Postrgres simple
    '''

    def __init__(self, database=None, user=None, password=None):
        self._database = database
        self._username = user
        self._password = password
        self.connection = None
        self.cursor = None
        self._table_name = None
        return

    @property
    def database(self):
        '''
        Get the database name
        '''
        return self._database

    @database.setter
    def database(self, value):
        '''
        Set the database name
        '''
        self._database = value
        return

    @property
    def username(self):
        '''
        Get the username
        '''
        return self._username

    @username.setter
    def username(self, value):
        '''
        Set the username
        '''
        self._username = value
        return

    @property
    def password(self):
        '''
        Get the password
        '''
        return self._password

    @password.setter
    def password(self, value):
        '''
        Set the password
        '''
        self._password = value
        return

    def get_connection(self):
        '''
        Attempt to get a connection to the database, if we do
        self.connection is good and we get a cursor,
        otherwise they are both  None
        '''
        try:
            self.connection = psycopg2.connect(
                database=self.database, user=self.username,
                password=self.password)
            self.cursor = self.connection.cursor()
        except psycopg2.ProgrammingError as err:
            print("%s Exception %s " % (__name__, err))
            self.connection = None
            self.cursor = None
            return False
        except psycopg2.OperationalError as err:
            print("%s Exception %s " % (__name__, err))
            self.connection = None
            self.cursor = None
            return False

        return True

    def _execute_and_commit(self, command):
        '''
        Excutes and commits the specified command
        '''
        try:
            self.cursor.execute(command)
            self.connection.commit()
        except psycopg2.ProgrammingError as err:
            self.connection.rollback()
            print("%s Exception %s " % (__name__, err))
            return False
        except psycopg2.InternalError as err:
            self.connection.rollback()
            print("%s Exception %s " % (__name__, err))
            return False
        return True

    def create_table(self, table_name=None, table_dict=None):
        '''
        create a table in our current environment with the table_name.
        the columns are specified in the table_dict with each key being a
        column and the value being the type of data in the column.
        '''
        if self.cursor is None:
            return False
        if table_dict is None:
            return False
        self._table_name = table_name
        table_string = "create table " + table_name + "("
        for key, value in table_dict.items():
            table_string += "%s %s," % (key, value)

        table_string = table_string[:-1]
        table_string += ");"
        if not self._execute_and_commit(table_string):
            print("Failed to create table %s" % table_name)
            return False

        return True

    def delete_table(self, table_name=None):
        '''
        Delete the specified table
        '''
        if table_name is None:
            return False

        table_string = "drop table " + table_name + ";"
        if not self._execute_and_commit(table_string):
            print("Failed to delete table %s" % table_name)
            return False

        return True

    def insert_single_row(self, columns, data):
        '''
        Insert a single row of data into our table.
        Input data is expected to be a LIST!
        '''
        if self.cursor is None:
            return False
        if columns is None:
            return False
        if data is None:
            return False

        command_string = "insert into " + self._table_name + " ( "

        for x in columns:
            command_string += x + ","
        command_string = command_string[:-1]

        command_string += ") values ("

        for x in data:
            command_string += "\'" + x + "\',"
        command_string = command_string[:-1]

        command_string += ");"
        print(command_string)
        if not self._execute_and_commit(command_string):
            print("Failed to insert single row into %s" % self._table_name)
            return False
        return True
