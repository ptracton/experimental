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

    @property
    def table_name(self):
        '''
        Get the table_name
        '''
        return self._table_name

    @table_name.setter
    def table_name(self, value):
        '''
        Set the table_name
        '''
        self._table_name = value
        print(self.table_name)
        return

    def _sql_type_to_python(self, data):
        if data is None:
            return None
        if data is "text":
            return "%s"
        if data is "text":
            return "%d"
        else:
            return None

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

    def _execute_and_commit(self, command=None, data=None, many=False):
        '''
        Excutes and commits the specified command
        '''

        if command is None:
            print("%s command is %s" % (__file__, command))
            return
        print("Execute and commit: %s" % command)
        try:
            if many:
                self.cursor.executemany(command, data)
            else:
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

    # def _executemany_and_commit(self, command):
    #     '''
    #     Excutes and commits the specified command
    #     '''
    #     try:
    #         self.cursor.executemany(command)
    #         self.connection.commit()
    #     except psycopg2.ProgrammingError as err:
    #         self.connection.rollback()
    #         print("%s Exception %s " % (__name__, err))
    #         return False
    #     except psycopg2.InternalError as err:
    #         self.connection.rollback()
    #         print("%s Exception %s " % (__name__, err))
    #         return False
    #     return True

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

        if table_name is not None:
            self._table_name = table_name

        if self.table_name is None:
            return False

        table_string = "create table " + self._table_name + "("
        for key, value in table_dict.items():
            table_string += "%s %s," % (key, value)

        table_string = table_string[:-1]
        table_string += ");"
        if not self._execute_and_commit(table_string):
            print("Failed to create table %s" % table_name)
            return False

        return True

    def drop_table(self, table_name=None):
        '''
        Drop the specified table
        '''
        if table_name is None:
            return False

        table_string = "drop table " + table_name + ";"
        if not self._execute_and_commit(table_string):
            print("Failed to delete table %s" % table_name)
            return False

        return True

    def drop_database(self, database_name=None):
        '''
        Drop the specified database
        '''
        if database_name is None:
            return False

        table_string = "drop database " + database_name + ";"
        if not self._execute_and_commit(table_string):
            print("Failed to delete table %s" % database_name)
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

        for index in columns:
            command_string += index + ","
        command_string = command_string[:-1]

        command_string += ") values ("

        for index in data:
            command_string += "\'" + index + "\',"
        command_string = command_string[:-1]

        command_string += ");"
        print(command_string)
        if not self._execute_and_commit(command_string):
            print("Failed to insert single row into %s" % self._table_name)
            return False
        return True

    def insert_multiple_rows(self, columns, data):
        '''
        Insert multiple rows of data into our table.
        Input data columns is a DICT of columns(keys) and their types (values)
        INPUT data is expected to be a LIST of tuples!
        '''
        if self.cursor is None:
            return False
        if columns is None:
            return False
        if data is None:
            return False

        command_string = "insert into " + self._table_name + " ( "

        for index in columns:
            command_string += index + ","
        command_string = command_string[:-1]

        command_string += ") values ("

        for index in columns.values():
            command_string += self._sql_type_to_python(index) + ","

        command_string = command_string[:-1]
        command_string += ")  "

        print(command_string)
        print(data)
        if not self._execute_and_commit(command=command_string,
                                        data=data, many=True):
            print("Failed to insert multiple rows into %s" % self._table_name)
            return False

        return True

    def update_data(self, columns=None, data=None,
                    qualifier=False, qual=None, qual_data=None):
        '''
        Update existing data in database
        '''
        if self.cursor is None:
            return False
        if columns is None:
            return False
        if data is None:
            return False

        command_string = "update " + self.table_name + " set = \'" +\
                         str(data) + "\' "
        if qualifier:
            command_string += " where " + qual + " = \'" +\
                              qual_data + "\';"

        print(command_string)
        if not self._execute_and_commit(command_string):
            print("Failed to delete row in %s" % self._table_name)
            return False
        return True

    def delete_rows(self, columns=None, data=None):
        '''
        Deletes the rows that have this data in the specified column
        '''
        if self.cursor is None:
            return False
        if columns is None:
            return False
        if data is None:
            return False

        command_string = "delete from " + self.table_name + " where " +\
                         columns + " = \'" + data + "\';"
        print(command_string)
        if not self._execute_and_commit(command_string):
            print("Failed to delete row in %s" % self._table_name)
            return False
        return True
