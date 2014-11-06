# ! /usr/bin/env python3
'''
Testing out the way to use the Postgres class that wraps
around the psycopg2 modules
'''
import sys
import Postgres

if __name__ == "__main__":
    print("db_testing")

    DATABASE = Postgres.Postgres()
    DATABASE.database = "postgres"
    DATABASE.password = "python"
    DATABASE.username = "postgres"
    if not DATABASE.get_connection():
        print("connection or cursor failed")
        sys.exit(-1)

    TABLE = {"stock_name": "text",
             "stock_symbol": "text"
             }

    RETURN_CODE = DATABASE.create_table(table_name="stocks2", table_dict=TABLE)
    while not RETURN_CODE:
        DATABASE.delete_table(table_name="stocks2")
        RETURN_CODE = DATABASE.create_table(table_name="stocks2",
                                            table_dict=TABLE)

    DATABASE.insert_single_row(TABLE.keys(), ["Medtronic", "MDT"])
    DATABASE.insert_single_row(TABLE.keys(), ["Google", "GOOG"])
