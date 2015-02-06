#!/usr/bin/env python3

import os
import sys
import time
import logging
import stat
import nose.proxy
import GoogleFinance


class Test_GoogleFinance:

    def setup(self):
        '''
        create a GoogleFinance object
        '''
        start_date = time.strptime("30 October 2014", "%d %B %Y")
        self.google = GoogleFinance.GoogleFinance(
            symbol="goog",
            start_date=start_date)
        return

    def teardown(self):
        '''
        delete the GoogleFinance object from this test run
        '''
        del self.google
        return

    def test_ctor(self):
        '''
        Test the constructor
        '''
        assert self.google.symbol == "GOOG"
        print(self.google.start_date.tm_year)
        assert self.google.start_date.tm_year == 2014
        assert self.google.start_date.tm_mon == 10
        assert self.google.start_date.tm_mday == 30
        return

    def test_stock(self):
        '''
        Test case
        '''
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
