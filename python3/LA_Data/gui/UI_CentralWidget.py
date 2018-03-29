#! /usr/bin/env python3

import PyQt5
import PyQt5.QtWidgets


class UI_CentralWidget(PyQt5.QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(UI_CentralWidget, self).__init__(parent)

        self.CityComboBox = PyQt5.QtWidgets.QComboBox()
        self.CityComboBox.addItems(['Los Angeles', 'Queens', 'Chicago'])

        self.DataSelectionComboBox = PyQt5.QtWidgets.QComboBox()
        self.DataSelectionComboBox.addItems(['Library', 'Police', 'Fire'])

        self.GetDataButton = PyQt5.QtWidgets.QPushButton("Get Data")
        vbox = PyQt5.QtWidgets.QVBoxLayout()

        vbox.addWidget(self.CityComboBox)
        vbox.addWidget(self.DataSelectionComboBox)
        vbox.addWidget(self.GetDataButton)

        self.setLayout(vbox)

        return
