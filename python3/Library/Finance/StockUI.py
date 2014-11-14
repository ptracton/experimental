#! /usr/bin/env python3

"""
UI class for a Stock.  This will have an instantiation of a stock to handle it
"""

import copy
#
# The GUI libraries since we build some GUI components here
#
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class StockUI:

    def __init__(self, parent=None, stock=None):

        self.stock = copy.copy(stock)

        self.stock_layout = QHBoxLayout()

        name_label = QLabel("Stock Name:")
        self.stock_name_label = QLabel(self.stock.name)
        symbol_label = QLabel("Stock Symbol:")
        self.symbol_label = QLabel(self.stock.symbol)

        self.google_button = QPushButton("Google")
        self.yahoo_button = QPushButton("Yahoo")

        self.stock_layout.addWidget(name_label)
        self.stock_layout.addWidget(self.stock_name_label)
        self.stock_layout.addWidget(symbol_label)
        self.stock_layout.addWidget(self.symbol_label)
        self.stock_layout.addWidget(self.google_button)
        self.stock_layout.addWidget(self.yahoo_button)

        #
        # connect signals and slots
        #
        QObject.connect(self.google_button, SIGNAL("clicked()"),
                        self.googleButtonClicked)
        QObject.connect(self.yahoo_button, SIGNAL("clicked()"),
                        self.yahooButtonClicked)

        return

    def getLayout(self):
        """
        Return our layout for easy GUI integration
        """
        return self.stock_layout

    def googleButtonClicked(self):
        '''
        Handles the google button getting clicked.
        This will download the historical stock
        data
        '''
        file_name = self.stock.name + "Google.csv"
        self.stock.get_historical_stock_data_from_google(filename=file_name)
        file_name = self.stock.name + "_Profile_Google.html"
        self.stock.get_profile_from_google(filename=file_name)
        return

    def yahooButtonClicked(self):
        '''
        Handles the google button getting clicked.
        This will download the historical stock
        data
        '''
        file_name = self.stock.name + "Yahoo.csv"
        self.stock.get_historical_stock_data_from_yahoo(filename=file_name)
        file_name = self.stock.name + "_Profile_Yahoo.html"
        self.stock.get_profile_from_yahoo(filename=file_name)
        return
