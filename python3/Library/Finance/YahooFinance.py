#! /usr/bin/env python3

'''
This class is designed to pull down the history of a stock
from Yahoo's Finance Web Site
'''

import urllib.request
import datetime
import logging
import re
from bs4 import BeautifulSoup


class YahooFinance:

    '''
    This is a class to manage pulling down a stock's history from Yahoo's
    Finance web site
    '''

    def __init__(self, symbol=None, start_date=None):

        # http://cliffngan.net/a/13
        self.symbol = symbol.upper()
        self.start_date = start_date
        self.base_url = "http://real-chart.finance.yahoo.com/table.csv?s="
        return

    def get_historical_stock_data(self, filename=None):
        """
        Get's the historical stock prices from the specified start date through
        today
        """

        today = datetime.datetime.today()
        start_string = str("&a=%d&c=%d&b=%d" %
                           (self.start_date.tm_mon - 1,
                            self.start_date.tm_year, self.start_date.tm_mday))
        end_string = str("&e=%d&d=%d&f=%d&g=d" %
                         (today.day, today.month - 1, today.year))
        url_string = self.base_url + self.symbol + \
            start_string + end_string + "&ignore=.csv"
        url_data = urllib.request.urlopen(url_string)
        csv = (url_data.read()).decode("utf-8-sig").encode("utf-8")
        if filename is not None:
            try:
                file_handle = open(filename, 'w')
                file_handle.write(csv.decode("utf-8"))
                file_handle.close()
            except OSError:
                print("Failed to open %s for writing!" % filename)
                error_string = "%s: Failed to open %s for writing" %\
                    (__name__, filename)
                logging.error(error_string)
        return

    def get_profile(self, filename=None):
        '''
        Get the company profile information
        '''
        url_string = "http://finance.yahoo.com/q/pr?s=" + self.symbol
        try:
            url_open = urllib.request.urlopen(url_string)
            web_page = url_open.read()
        except urllib.error.URLError:
            print("Failed to get %s" % url_string)
            print("Failed to get %s" % url_string)
            error_string = "%s: Failed to get %s" %\
                           (__name__, url_string)
            logging.error(error_string)
            return False

        if filename is not None:
            try:
                profile = open(filename, "wb")  # open file in binary mode
                profile.write(web_page)
                profile.close()
            except OSError:
                print("Failed to open %s for writing!" % filename)
                error_string = "%s: Failed to open %s for writing" %\
                    (__name__, filename)
                logging.error(error_string)
                return False

        soup = BeautifulSoup(web_page)
        text = soup.get_text()
        print(type(text))
        print(soup.get_text().encode('ascii', 'ignore'))
        print(soup.head)
        print(soup.a)
        print(soup.b)
        print(soup.find_all(text=re.compile("Key Executives")))
        return False
