#! /usr/bin/env python3

'''
Created on Apr 27, 2013

@author: ptracton
'''

import sys
from PyQt4.QtGui import *
import AppGui

if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = AppGui.AppGui()
    gui.show()
    app.exec_()    
    
    pass
