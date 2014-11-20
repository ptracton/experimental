# ! /usr/bin/env python3
'''
Testing out the way to use the Postgres class that wraps
around the psycopg2 modules
'''
import sys
#
# Our custom imports
#
sys.path.append("..\Library")
import Database

if __name__ == "__main__":
    print("db_testing")

    DATABASE = Database.Postgres.Postgres()
    DATABASE.database = "postgres"
    DATABASE.password = "python"
    DATABASE.username = "postgres"
    DATABASE.table_name = "stocks2"
    if not DATABASE.get_connection():
        print("connection or cursor failed")
        sys.exit(-1)

    TABLE = {"stock_name": "text",
             "stock_symbol": "text"
             }

    RETURN_CODE = DATABASE.create_table(table_dict=TABLE)
    print(RETURN_CODE)
    while not RETURN_CODE:
        DATABASE.drop_table(table_name="stocks2")
        RETURN_CODE = DATABASE.create_table(table_name="stocks2",
                                            table_dict=TABLE)

    DATABASE.insert_single_row(TABLE.keys(), ["Medtronic", "MDT"])
    DATABASE.insert_single_row(TABLE.keys(), ["Google", "GOOG"])

    MULTIPLE_ROWS = []
    MULTIPLE_ROWS.append(('Amazon', 'AMZ'))
    MULTIPLE_ROWS.append(('Yahoo', 'YHOO'))
    MULTIPLE_ROWS.append(('Microsoft', 'MSFT'))
    MULTIPLE_ROWS.append(('MRV', 'MRV'))
    DATABASE.insert_multiple_rows(TABLE, MULTIPLE_ROWS)
    DATABASE.delete_rows("stock_name", "MRV")
