#!/usr/bin/env python3

# make sure to install these packages before running:
# pip install pandas
# pip install bokeh

# https://dev.socrata.com/foundry/data.lacity.org/kh8g-6365

import numpy as np
import pandas as pd
import datetime
import urllib
 
from bokeh.plotting import *
from bokeh.models import HoverTool
from collections import OrderedDict

query = ("https://data.lacity.org/resource/kh8g-6365.json")
raw_data = pd.read_json(query)	
print (raw_data)
