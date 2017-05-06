#! /usr/bin/env python3


import sys
from PyQt4 import QtGui
import UI


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    gui = UI.UI()
    gui.show()
    sys.exit(app.exec_())
