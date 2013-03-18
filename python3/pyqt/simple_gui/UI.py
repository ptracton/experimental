'''
Created on Mar 18, 2013

@author: tractp1
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class UI(QDialog):
    '''
    classdocs
    '''


    def __init__(self, parent = None):
        '''
        Constructor
        '''
        #
        # Call contstructor of our Super Class, we inherit from QDialog
        #
        super(UI, self).__init__(parent)

        #######################################################################
        #
        # DATE Editor
        #
        #######################################################################
        self.StartDateLabel = QLabel("Start Date")
        self.EndDateLabel = QLabel("End Date")

        self.StartDate = QDateEdit()
        self.StartDate.setCalendarPopup(True)
        self.EndDate = QDateEdit(QDate.currentDate())
        self.EndDate.setCalendarPopup(True)

        top_layout = QVBoxLayout()
        date_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        left_layout.addWidget(self.StartDateLabel)
        left_layout.addWidget(self.EndDateLabel)
        right_layout.addWidget(self.StartDate)
        right_layout.addWidget(self.EndDate)

        date_layout.addLayout(left_layout)
        date_layout.addLayout(right_layout)

        #######################################################################
        #
        # Dial
        #
        #######################################################################
        self.Dial = QDial()
        self.Dial.setValue(0)
        self.Dial.setMaximum(1024)
        self.DialLabel = QLabel("Dial %d" % self.Dial.value())

        dial_layout = QHBoxLayout()
        dial_left_layout = QVBoxLayout()
        dial_right_layout = QVBoxLayout()

        dial_left_layout.addWidget(self.DialLabel)
        dial_right_layout.addWidget(self.Dial)
        dial_layout.addLayout(dial_left_layout)
        dial_layout.addLayout(dial_right_layout)

        # Connect signals to make things happen
        self.connect(self.Dial, SIGNAL("valueChanged(int)"), self.updateDial)

        #######################################################################
        #
        # Time, Timer, Time Editor
        #
        #######################################################################
        print("%s" % QTime.currentTime().toString("hh:mm:ss"))
        self.TimeLabel = QLabel("Time:")
        self.TimeValue = QLabel("%s" % QTime.currentTime().toString("hh:mm:ss"))
        self.Timer = QTimer()
        self.Timer.setSingleShot(False)
        self.Timer.start(1000)

        time_layout = QHBoxLayout()
        time_left_layout = QVBoxLayout()
        time_right_layout = QVBoxLayout()
        time_left_layout.addWidget(self.TimeLabel)
        time_right_layout.addWidget(self.TimeValue)
        time_layout.addLayout(time_left_layout)
        time_layout.addLayout(time_right_layout)

        self.connect(self.Timer, SIGNAL("timeout()"), self.updateTime)

        #######################################################################
        #
        # Top Level Display
        #
        #######################################################################
        top_layout.addLayout(date_layout)
        top_layout.addLayout(dial_layout)
        top_layout.addLayout(time_layout)
        self.setLayout(top_layout)

        self.setWindowTitle("GUI TESTING")

        return

    def updateTime(self):
        self.TimeValue.setText("%s" % QTime.currentTime().toString("hh:mm:ss"))
        return

    def updateDial(self):
        self.DialLabel.setText("Dial %d" % self.Dial.value())
        return
