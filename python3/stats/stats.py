#! /usr/bin/env python3

import datetime
import random
import statistics

import pandas
#import pandas_datareader
import pandas_datareader.data as web
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print ("Stats")
    data = [random.randint(0,100) for x in range(100)]
    print (data)
    print (statistics.mean(data))
    print (statistics.median(data))
    try:
        print (statistics.mode(data))
    except statistics.StatisticsError:
        print ("Mode error")
    print (statistics.stdev(data))
    print (statistics.variance(data))


    start = datetime.datetime(2002, 7, 1)
    end = datetime.datetime(2016, 9, 10)
    stock_data = web.get_data_yahoo('MDT', start=start, end=end)
    #print (stock_data)
    #print (type(stock_data))
    #print (stock_data.keys())
    #print (stock_data.axes)
    #print (stock_data.max())
    first_day = stock_data.ix[0:1]
    print(stock_data.mean(axis=1))
    stock_data.plot(subplots = True, figsize = (8, 8));
    plt.legend(loc = 'best')
    plt.show()
