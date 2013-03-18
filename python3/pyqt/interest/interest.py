'''
Created on Mar 18, 2013

@author: tractp1
'''

import sys
from PyQt4.QtGui import *
import InterestUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = InterestUI.InterestUI()
    gui.show()
    app.exec_()
    pass
