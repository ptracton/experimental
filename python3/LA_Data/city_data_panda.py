#!/usr/bin/env python3

# make sure to install these packages before running:
# pip install pandas
# pip install bokeh

# https://dev.socrata.com/foundry/data.lacity.org/kh8g-6365

# import numpy as np
import json
import os
import pandas


if __name__ == "__main__":

    json_file = "test.json"

    if not os.path.isfile(json_file):
        query = ("https://data.lacity.org/resource/kh8g-6365.json")
        raw_data = pandas.read_json(query)
        f = open('test.json', 'w')
        json.dump(pandas.DataFrame.to_json(raw_data), f)
    else:
        with open(json_file, 'r') as infile:
            top_level_dict = json.load(infile)
        df = pandas.read_json(top_level_dict)
        print(type(df))
        print(df.info())
        print(df.dtypes)
        print(df.describe())
        print(df.head())
        print(df.tail(3))
