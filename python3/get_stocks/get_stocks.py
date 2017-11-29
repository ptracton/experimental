#! /usr/bin/env python3
"""
This is a simple demo program to show the various ways to get stock data
from Google or Yahoo
"""

import sys
from PyQt4.QtGui import *
import UI

if __name__ == "__main__":
    print("Getting Stocks")

    app = QApplication(sys.argv)
    GUI = UI.UI()
    GUI.show()
    app.exec_()
