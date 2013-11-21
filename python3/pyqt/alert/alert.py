#! /usr/bin/env python3

import sys
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *

if __name__ == '__main__':
    print(":\n")

    
    app = QApplication(sys.argv)
    try:
        due = QTime.currentTime()
        message = "Alert!"
        if len(sys.argv) < 2:
            raise ValueError
        hours, mins = sys.argv[1].split(":")
        due = QTime(int(hours), int(mins))
        if not due.isValid():
            raise ValueError
        if len(sys.argv) > 2:
            message = " ".join(sys.argv[2:])
    except ValueError:
        message = "Usage: alert.pyw HH:MM [optional message]" # 24hr clock

    while QTime.currentTime() < due:
        time.sleep(20)

    label = QLabel("<font color=red size=72><b>" + message + "</b></font>")
    label.setWindowFlags(Qt.SplashScreen)
    label.show()
    QTimer.singleShot(10000, app.quit) # 10 seconds
    app.exec_()        
