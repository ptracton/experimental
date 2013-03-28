'''
Created on Mar 28, 2013

@author: tractp1
'''
import sys
from PyQt4.QtGui import *
import UIw

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setOrganizationName("Tracton Corp.")
    app.setOrganizationDomain("tracton.com")
    app.setApplicationName("Window Demo")
    gui = UIw.UIw()
    gui.show()
    app.exec_()
    pass
