#! /usr/bin/env python3

from PyQt4 import QtCore
from PyQt4 import QtGui


class LabelAndEntry(QtGui.QWidget):

    def __init__(self, parent=None, label="Default", lineDefault=None):

        super(LabelAndEntry, self).__init__(parent)
        self.top_hbox = QtGui.QHBoxLayout()

        self.label = QtGui.QLabel(label)
        self.label.setAlignment(QtCore.Qt.AlignRight)
        
        self.entry = QtGui.QLineEdit(str(lineDefault))
        self.entry.setFixedWidth(150)
        self.entry.setMaximumWidth(150)
        self.entry.setAlignment(QtCore.Qt.AlignRight)
        
        self.top_hbox.addWidget(self.label)
        self.top_hbox.addWidget(self.entry)
        return

    def getLayout(self):
        """
        Return our layout for easy GUI integration
        """
        return self.top_hbox
    
