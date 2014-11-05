#! /usr/bin/env python3

"""
This is a simple demo program to show the various ways to get stock data
from Google or Yahoo
"""

import os
import os.path
import sys
import configparser
import logging

sys.path.append("../Library")
import Finance

if __name__ == "__main__":
    print("Getting Stocks")

    project_config_file = "stocks.cfg"
    if os.path.isfile(project_config_file):
        config_file = configparser.ConfigParser()
        try:
            config_file.read(project_config_file)
        except OSError:
            print("%s exists but we can not open or read it!" %
                  (project_config_file))
            sys.exit(-1)
    else:
        print("%s does not exist!" % (project_config_file))
        sys.exit(-1)

    #
    # Set up logging.  Attempt to get FILE and LEVEL from the LOGGING
    # section of the config file.  If any of this is missing, use defaults
    #
    if config_file.has_section('LOGGING'):
        if config_file.has_option('LOGGING', 'FILE'):
            log_file = config_file.get('LOGGING', 'FILE')
        else:
            log_file = "logging.log"

        if config_file.has_option('LOGGING', 'LEVEL'):
            log_level_str = config_file['LOGGING']['LEVEL']
            if log_level_str == "DEBUG":
                log_level = logging.DEBUG
            elif log_level_str == "INFO":
                log_level = logging.INFO
            elif log_level_str == "ERROR":
                log_level = logging.ERROR
            elif log_level_str == "WARNING":
                log_level = logging.WARNING
            elif log_level_str == "CRITCAL":
                log_level = logging.CRITICAL
        else:
            log_level = logging.INFO

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', filename=log_file,
                        level=log_level)

    logging.info("Get Stocks Starting!")

    #
    # Parse config file for list of stocks
    #
    if config_file.has_section('STOCKS'):
        if config_file.has_option('STOCKS', 'stocks'):
            cfg_list_of_stocks =\
                list(config_file.get('STOCKS', 'stocks').split(","))
        else:
            cfg_list_of_stocks = []

    list_of_stocks = []
    for s in cfg_list_of_stocks:
        stock = s.strip(' ')
        if config_file.has_section(stock):
            s = Finance.Stock.Stock()
            s.symbol = stock
            if config_file.has_option(stock, 'SHARES'):
                s.shares = config_file.get(stock, 'SHARES')

            if config_file.has_option(stock, 'PURCHASE'):
                s.purchase = config_file.get(stock, 'PURCHASE')

            if config_file.has_option(stock, 'NAME'):
                s.name = config_file.get(stock, 'NAME')

            list_of_stocks.append(s)
            del s
        else:
            print("MISSING Section %s" % stock)

    for x in list_of_stocks:
        yfname = str(x.name + "Yahoo.csv")
        x.getFromYahoo(filename=yfname)
        gfname = str(x.name + "Google.csv")
        x.getFromGoogle(filename=gfname)
