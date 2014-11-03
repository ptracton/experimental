#! /usr/bin/env python3

'''
This class is designed to pull down the history of a stock
from Google's Finance Web Site
'''


import urllib.request
import datetime
import logging
import BaseFinance


class GoogleFinance:

    def __init__(self, symbol=None, start_date=None):

        # http://stackoverflow.com/questions/5081710/how-to-create-a-stock-quote-fetching-app-in-python
        # see http://www.goldb.org/goldblog/2007/09/14/PythonStockQuoteModule.aspx

        BaseFinance.BaseFinance.__init__(self)
        self.symbol = symbol.upper()
        self.start_date = start_date
        self.csv_base_string = "http://www.google.com/finance/historical?q="

        return

    def getStock(self, filename=None):
        today = datetime.datetime.today()
        url_string = self.csv_base_string + self.symbol
        url_string += "&startdate=%s-%s-%s" % (self.start_date.tm_year,
                                               self.start_date.tm_mon, self.start_date.tm_mday)
        url_string += "&enddate=%s-%s-%s" % (today.year, today.month, today.day)
        url_string += "&output=csv"
        # print(url_string)

        url_data = urllib.request.urlopen(url_string)
        # http://stackoverflow.com/questions/18664712/split-function-add-xef-xbb-xbf-n-to-my-list
        csv = (url_data.read()).decode("utf-8-sig").encode("utf-8")
        print(csv)
        # print(url_data.read())

        if filename is not None:
            try:
                f = open(filename, 'w')
                f.write(csv.decode("utf-8"))
                f.close()
            except:
                logging.error("%s: Failed to open %s for writing" %
                              (__name__, filename))
                print("Failed to open %s for writing!" % filename)
        return
