import sys
from PyQt4.QtGui import *
import penUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = penUI.penUI()
    gui.show()
    app.exec_()
    pass


