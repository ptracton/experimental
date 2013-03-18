'''
Created on Mar 18, 2013

@author: tractp1
'''

import sys
from PyQt4.QtGui import *
import UI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = UI.UI()
    gui.show()
    app.exec_()
    pass
