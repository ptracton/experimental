"""
FILE: ORM.py

This file handles all SQLAlchemy ORM related operations and classes for
the UCLA Extension Python Programming 1 Movie Project

"""

import logging
import os
import traceback

import pandas as pd

import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

# Global Setup
user = "postgres"
password = os.environ['PASSWORD']
host = "localhost"
port = 5432
db = "postgres"
url = 'postgresql://{}:{}@{}:{}/{}'

# Select one of the db strings depending on which database you wish
# use.  The first one is Postgresql the second is Sqlite3
db_string = url.format(user, password, host, port, db)
#db_string = 'sqlite:///movie_project.db'

db = sqlalchemy.create_engine(db_string)
base = sqlalchemy.ext.declarative.declarative_base()
inspector = sqlalchemy.inspect(db)
Session = sqlalchemy.orm.sessionmaker(db)
session = Session()
base.metadata.create_all(db)


def tableExists(inspector=None, table=None):
    """
    Returns true if this table exists in this database
    and false otherwise
    """
    return (table in inspector.get_table_names())


def csvToTable(fileName=None, tableName=None, db=None):
    """
    Read this fileName, expected to be a CSV file, and put it
    into the tableName of this database 
    """
    try:
        df_csv = pd.read_csv(fileName)
        df_csv.columns = [c.lower() for c in df_csv.columns]
        df_csv.to_sql(tableName, db)
        logging.info("PASSED to create table {} from CSV file {}".format(
            tableName, fileName))
        return True
    except Exception:
        logging.error("FAILED to create table {} from CSV file {}".format(
            tableName, fileName))
        print(traceback.format_exc())
        logging.error(traceback.format_exc())
        return False


class Movies(base):
    """
    This class is the Movies table in the database.
    Data from: https://www.kaggle.com/tmdb/tmdb-movie-metadata/data
    """

    __tablename__ = "Movies"
    id = sqlalchemy.Column(sqlalchemy.Numeric, primary_key=True)

    budget = sqlalchemy.Column(sqlalchemy.Numeric)
    popularity = sqlalchemy.Column(sqlalchemy.Numeric)
    runtime = sqlalchemy.Column(sqlalchemy.Numeric)
    vote_average = sqlalchemy.Column(sqlalchemy.Numeric)
    vote_count = sqlalchemy.Column(sqlalchemy.Numeric)
    revenue = sqlalchemy.Column(sqlalchemy.Numeric)

    genres = sqlalchemy.Column(sqlalchemy.String)
    homepage = sqlalchemy.Column(sqlalchemy.String)
    title = sqlalchemy.Column(sqlalchemy.String)
    tagline = sqlalchemy.Column(sqlalchemy.String)
    status = sqlalchemy.Column(sqlalchemy.String)

    release_date = sqlalchemy.Column(sqlalchemy.Date)


class Credits(base):
    """
    This class is the Credits table in the database.
    Data from: https://www.kaggle.com/tmdb/tmdb-movie-metadata/data
    """
    __tablename__ = "Credits"
    movie_id = sqlalchemy.Column(sqlalchemy.Numeric, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    cast = sqlalchemy.Column(sqlalchemy.String)
    crew = sqlalchemy.Column(sqlalchemy.String)
