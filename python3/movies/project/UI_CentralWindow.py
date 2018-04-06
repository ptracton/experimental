"""
This file handles holding the main GUI elements
"""

import PyQt5
import PyQt5.QtWidgets


class UI_CentralWindow(PyQt5.QtWidgets.QDialog):
    """
    This class holds the GUI elements
    """

    def __init__(self, parent=None):
        super(UI_CentralWindow, self).__init__(parent)

        # Create GUI Elements
        enterMovieLabel = PyQt5.QtWidgets.QLabel("Movie to Look up")
        self.enterMovieLineEdit = PyQt5.QtWidgets.QLineEdit()
        self.enterMoviePushButton = PyQt5.QtWidgets.QPushButton(
            "Look Up Movie")

        # Arrange them in Window
        hbox = PyQt5.QtWidgets.QHBoxLayout()
        hbox.addWidget(enterMovieLabel)
        hbox.addWidget(self.enterMovieLineEdit)
        hbox.addWidget(self.enterMoviePushButton)

        # Put into layout to view
        self.setLayout(hbox)
        return
