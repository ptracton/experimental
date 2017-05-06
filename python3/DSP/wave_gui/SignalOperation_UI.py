#! /usr/bin/env python3

from PyQt4 import QtGui
import LabelAndComboBox


class SignalOperation_UI(QtGui.QDialog):

    def __init__(self, parent=None):
        super(SignalOperation_UI, self).__init__(parent)

        self.top_vbox = QtGui.QVBoxLayout()

        optionsList = ["ADD", "SUB", "MULT", "CONV", "FFT"]
        self.operations = LabelAndComboBox.LabelAndComboBox(
            label="Operations", optionsList=optionsList
        )

        self.executeButton = QtGui.QPushButton("Execute")

        self.top_vbox.addLayout(self.operations.getLayout())
        self.top_vbox.addWidget(self.executeButton)
        return

    def getLayout(self):
        """
        Return our layout for easy GUI integration
        """
        return self.top_vbox
