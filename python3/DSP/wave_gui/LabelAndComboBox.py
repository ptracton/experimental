#! /usr/bin/env python3

from PyQt4 import QtCore
from PyQt4 import QtGui


class LabelAndComboBox(QtGui.QWidget):

    def __init__(self, parent=None, label="Default", optionsList=None):

        super(LabelAndComboBox, self).__init__(parent)
        self.top_hbox = QtGui.QHBoxLayout()

        self.label = QtGui.QLabel(label)
        self.label.setAlignment(QtCore.Qt.AlignRight)
        
        self.entry = QtGui.QComboBox()
        self.entry.addItems(optionsList)
        
        self.top_hbox.addWidget(self.label)
        self.top_hbox.addWidget(self.entry)
        return

    def getLayout(self):
        """
        Return our layout for easy GUI integration
        """
        return self.top_hbox
    
