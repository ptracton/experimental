#! /usr/bin/env python3

'''
This class is designed to pull down the history of a stock
from Yahoo's Finance Web Site
'''

import urllib.request
import datetime

import BaseFinance


class YahooFinance(BaseFinance.BaseFinance):

    '''
    This is a class to manage pulling down a stock's history from Yahoo's
    Finance web site
    '''

    def __init__(self, symbol=None, start_date=None):

        # http://cliffngan.net/a/13
        # super().__init__()
        BaseFinance.BaseFinance.__init__(self)
        self.symbol = symbol.upper()
        self.start_date = start_date
        self.csv_base_string = "http://real-chart.finance.yahoo.com/table.csv?s="
        return

    def getStock(self, filename=None):
        """
        Get's the historical stock prices from the specified start date through
        today
        """

        today = datetime.datetime.today()
        start_string = str("&a=%d&c=%d&b=%d" %
                           (self.start_date.tm_mon - 1, self.start_date.tm_year, self.start_date.tm_mday))
        end_string = str("&e=%d&d=%d&f=%d&g=d" %
                         (today.day, today.month - 1, today.year))
        url_string = self.csv_base_string + self.symbol + \
            start_string + end_string + "&ignore=.csv"
        print(url_string)
        url_data = urllib.request.urlopen(url_string)
        csv = (url_data.read()).decode("utf-8-sig").encode("utf-8")
        print(csv)
        if filename is not None:
            try:
                f = open(filename, 'w')
                f.write(csv.decode("utf-8"))
                f.close()
            except:
                print("Failed to open %s for writing!" % filename)
                logging.error("%s: Failed to open %s for writing" %
                              (__name__, filename))
