#!/usr/bin/env python3

import sys
import PyQt5
import UI

if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    gui = UI.UI()
    gui.show()
    app.exec_()
