#! /usr/bin/env python3

import os
import sys
import psycopg2
import Postgres

if __name__ == "__main__":
    print("db_testing")

    database = Postgres.Postgres()
    database.database = "postgres"
    database.password = "python"
    database.username = "postgres"
    database.get_connection()

    table = {"stock_name": "text",
             "stock_symbol": "text"
             }
    return_code = database.delete_table(table_name="stocks")
    return_code = database.delete_table(table_name="stocks2")
    return_code = database.create_table(table_name="stocks2", table_dict=table)


#    connection = psycopg2.connect(database="postgres", user="postgres", password="python")
#    cursor = connection.cursor()

#    try:
#        cursor.execute("create table stocks(name text, symbol text);")
#        connection.commit()
#    except psycopg2.ProgrammingError:
#        print("Table already exists")
