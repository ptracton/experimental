#! /usr/bin/env python3

'''

@author: ptracton

'''

__author__ = 'ptracton'

import sys
import os
from PyQt4.QtGui import *


sys.path.append(os.getcwd() + "/STM32Lib")
print(sys.path)
import STM32Lib.GUI


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = STM32Lib.GUI.GUI()
    gui.show()
    app.exec_()

    pass
