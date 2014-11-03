#! /usr/bin/env python3

'''
This is our Stock class.  It is designed to hold a single stock and the
details around it
'''
import time
import logging

import Finance


class Stock:

    '''
    This class will hold 1 stock from the config file
    '''

    def __init__(self, symbol=None, name=None, purchase=None, shares=None):
        self._name = name
        self._symbol = symbol
        self._purchase = purchase
        self._shares = shares
        return

    @property
    def symbol(self):
        '''
        Get the stock symbol
        '''
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        '''
        Set the stock symbol
        '''
        self._symbol = value
        return

    @property
    def name(self):
        '''
        Get the stock name
        '''
        return self._name

    @name.setter
    def name(self, value):
        '''
        Set the stock name
        '''
        self._name = value
        return

    @property
    def shares(self):
        '''
        Get the number of shares
        '''
        return self._shares

    @shares.setter
    def shares(self, value):
        '''
        Set the number of shares.
        If it is a string convert to integer.
        If it is an integer, store it.
        Else set to 0
        '''
        if isinstance(value, str):
            self._shares = int(value)
        elif isinstance(value, int):
            self._shares = value
        else:
            self._shares = 0
        return

    @property
    def purchase(self):
        '''
        Get the purchase date
        '''
        # return str("%s-%s-%s" % (self._purchase[1], self._purchase[2], self._purchase[0]))
        return self._purchase

    @purchase.setter
    def purchase(self, value):
        '''
        Set the purchase date
        '''
        if isinstance(value, str):
            self._purchase = time.strptime(value, "%d %B %Y")
        return

    def __str__(self):
        return str("%s: %d shares on %s" % (self.name,
                                            self.shares, self.purchase))

    def getFromGoogle(self):
        '''
        Get this stock's history from Google
        '''
        g = Finance.GoogleFinance.GoogleFinance()
        return

    def getFromYahoo(self, filename=None):
        '''
        Get this stock's history from Yahoo
        '''

        logging.info("%s: Get %s from Yahoo" %
                     (__name__, self.symbol))

        yahoo = Finance.YahooFinance.YahooFinance(symbol=self.symbol,
                                                  start_date=self.purchase)
        yahoo.getStock(filename=filename)
        return

    def getFromGoogle(self, filename=None):
        '''
        Get this stock's history from Yahoo
        '''

        logging.info("%s: Get %s from Google" %
                     (__name__, self.symbol))

        google = Finance.GoogleFinance.GoogleFinance(symbol=self.symbol,
                                                     start_date=self.purchase)
        google.getStock(filename=filename)
        return
