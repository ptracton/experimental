#!/usr/bin/env python3

import sys
import time
import logging
import nose
import GoogleFinance


class Test_GoogleFinance:

    def __init__(self):
        pass

    def setup(self):

        self.google = GoogleFinance.GoogleFinance(symbol="goog", start_date="30 October 2014")
        return

    def teardown(self):
        #del self.empty
        del self.google
        return

    def test_ctor(self):
        #self.empty = GoogleFinance.GoogleFinance()
        #assert self.empty.symbol == None
        assert self.google.symbol == "GOOG"
        assert self.google.start_date == "30 October 2014"
        return

    def test_stock(self):
        '''
        Test case
        '''
        start_date = time.strptime("01 January 2015", "%d %B %Y")
        g = GoogleFinance.GoogleFinance(symbol="appl", start_date=start_date)
        assert g.symbol == "APPL"
        g.get_historical_stock_data()
        g.get_historical_stock_data(filename="test.csv")
        del(g)
        return
