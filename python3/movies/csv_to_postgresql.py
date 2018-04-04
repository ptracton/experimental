#! /usr/bin/env python3

# https://stackoverflow.com/questions/2987433/how-to-import-csv-file-data-into-a-postgresql-table

import pandas as pd
from sqlalchemy import create_engine
    
if __name__ == "__main__":

    engine = create_engine('postgresql://postgres:python@localhost:5432/postgres')
    
    df_movies = pd.read_csv('tmdb_5000_movies.csv')
    df_credits = pd.read_csv('tmdb_5000_credits.csv')
    df_movies.columns = [c.lower() for c in df_movies.columns] #postgres doesn't like capitals or spaces
    df_credits.columns = [c.lower() for c in df_credits.columns] #postgres doesn't like capitals or spaces



    
    df_movies.to_sql("Movies", engine)
    df_credits.to_sql("Credits", engine)
