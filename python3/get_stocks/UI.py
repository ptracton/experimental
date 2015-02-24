#! /usr/bin/env python3

"""
This is the top level GUI component of get_stocks
"""

#
# Python Standard Library imports
#
import os
import os.path
import sys
import configparser
import logging

#
# 3rd party imports
#
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#
# Our custom imports
#
sys.path.append("c:\\Users\tractp1\\src\\software\\experimental\\python3\\Library\\Finance")
sys.path.append("..\Library")
import Finance


class UI(QDialog):

    def __init__(self, parent=None):
        super(UI, self).__init__(parent)

        #
        # Read and parse config file
        #
        self.config_file = "stocks.cfg"
        self.configuration = None
        if not self._start_config_file():
            print("config file failure, terminating application")
            sys.exit(0)

        #
        # config file must be working, lets start logging
        #
        self._start_logging()

        #
        # layOut is out top level GUI item
        #
        self.layOut = QVBoxLayout()

        #
        # Get our initial list of stocks
        #
        self.list_of_stocks = []
        stocks = []
        stocks = self._get_stocks_from_config()
        for x in stocks:
            stock_ui = Finance.StockUI.StockUI(stock=x)
            self.list_of_stocks.append(stock_ui)
            self.layOut.addLayout(stock_ui.getLayout())
            del stock_ui

        #
        # Get the GUI ip and running
        #
        self.setLayout(self.layOut)
        self.setWindowTitle("Learning Python Stock Application")
        pass

        pass

    def _start_config_file(self):
        """
        Read in our configuration file.  return true if we can open and read it
        return false for anything else
        """
        if os.path.isfile(self.config_file):
            self.configuration = configparser.ConfigParser()
            try:
                self.configuration.read(self.config_file)
            except OSError:
                print("%s exists but we can not open or read it!" %
                      (self.config_file))
                return False
        else:
            print("%s does not exist!" % (self.config_file))
            return False

        return True

    def _start_logging(self):
        '''
        Start our logging.  Get the log file and level from our configuration file
        '''

        if self.configuration.has_section('LOGGING'):
            if self.configuration.has_option('LOGGING', 'FILE'):
                LOG_FILE = self.configuration.get('LOGGING', 'FILE')
            else:
                LOG_FILE = "logging.log"

            if self.configuration.has_option('LOGGING', 'LEVEL'):
                LOG_LEVEL_STR = self.configuration['LOGGING']['LEVEL']
                if LOG_LEVEL_STR == "DEBUG":
                    LOG_LEVEL = logging.DEBUG
                elif LOG_LEVEL_STR == "INFO":
                    LOG_LEVEL = logging.INFO
                elif LOG_LEVEL_STR == "ERROR":
                    LOG_LEVEL = logging.ERROR
                elif LOG_LEVEL_STR == "WARNING":
                    LOG_LEVEL = logging.WARNING
                elif LOG_LEVEL_STR == "CRITCAL":
                    LOG_LEVEL = logging.CRITICAL
                else:
                    LOG_LEVEL = logging.INFO

        logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', filename=LOG_FILE,
                            level=LOG_LEVEL)

        logging.info("Get Stocks Starting!")

        return

    def _get_stocks_from_config(self):
        #
        # Parse config file for list of stocks
        #
        if self.configuration.has_section('STOCKS'):
            if self.configuration.has_option('STOCKS', 'stocks'):
                CFG_LIST_OF_STOCKS =\
                    list(self.configuration.get('STOCKS', 'stocks').split(","))
            else:
                CFG_LIST_OF_STOCKS = []

        LIST_OF_STOCKS = []
        for s in CFG_LIST_OF_STOCKS:
            stock = s.strip(' ')
            if self.configuration.has_section(stock):
                s = Finance.Stock.Stock()
                s.symbol = stock
                if self.configuration.has_option(stock, 'SHARES'):
                    s.shares = self.configuration.get(stock, 'SHARES')

                if self.configuration.has_option(stock, 'PURCHASE'):
                    s.purchase = self.configuration.get(stock, 'PURCHASE')

                if self.configuration.has_option(stock, 'NAME'):
                    s.name = self.configuration.get(stock, 'NAME')
                # print(s)
                LIST_OF_STOCKS.append(s)
                del s
            else:
                print("MISSING Section %s" % stock)

        return LIST_OF_STOCKS
