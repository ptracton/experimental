#!/usr/bin/env python3

import os
import sys
import time
import logging
import stat
import nose.proxy
import GoogleFinance


class Test_GoogleFinance:

    def __init__(self):
        pass

    def setup(self):
        start_date = time.strptime("30 October 2014", "%d %B %Y")
        self.google = GoogleFinance.GoogleFinance(
            symbol="goog",
            start_date=start_date)
        return

    def teardown(self):
        #del self.empty
        del self.google
        return

    def test_ctor(self):
        #self.empty = GoogleFinance.GoogleFinance()
        #assert self.empty.symbol == None
        assert self.google.symbol == "GOOG"
        #assert self.google.start_date == "30 October 2014"
        return

    def test_stock(self):
        '''
        Test case
        '''
        # self.google.get_historical_stock_data()
        try:
            os.remove("test.csv")
        except FileNotFoundError:
            pass

        self.google.get_historical_stock_data(filename="test.csv")
        size = 0
        try:
            csv = open("test.csv", "r")
            lines = csv.readlines()
            csv.close()
            size = len(lines)
        except:
            size = 0
        assert size > 1

        os.chmod("test.csv", stat.S_IRUSR | stat.S_IROTH | stat.S_IRGRP)
        self.google.get_historical_stock_data(filename="test.csv")
        return
