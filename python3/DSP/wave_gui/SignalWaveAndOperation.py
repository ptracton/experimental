#! /usr/bin/env python3

import numpy as np
from PyQt4 import QtCore
from PyQt4 import QtGui
import SignalOperation_UI
import QtMpl

import sys
sys.path.append('../Signal')
import Signal


class SignalWaveAndOperation(QtGui.QWidget):

    def __init__(self, parent=None, label="Default"):
        super(SignalWaveAndOperation, self).__init__(parent)
                
        self.top_hbox = QtGui.QHBoxLayout()

        self.signalOperation = SignalOperation_UI.SignalOperation_UI()
        self.mplGraph = QtMpl.QtMpl(parent)
        self.top_hbox.addLayout(self.signalOperation.getLayout())
        self.top_hbox.addWidget(self.mplGraph)

        self.Signal = Signal.Signal()
        
        return

    def getLayout(self):
        """
        Return our layout for easy GUI integration
        """
        return self.top_hbox
    

