"""
This file handles holding a title and some data from the database
"""

import PyQt5
import PyQt5.QtWidgets


class UI_MovieInfo(PyQt5.QtWidgets.QDialog):
    """
    This class holds the GUI elements
    """

    def __init__(self, parent=None, title=None):
        super(UI_MovieInfo, self).__init__(parent)

        # Create GUI Elements
        self.titleLabel = PyQt5.QtWidgets.QLabel(title)
        self.titleLabelFont = PyQt5.QtGui.QFont()
        self.titleLabelFont.setBold(True)
        self.titleLabel.setFont(self.titleLabelFont)
        
        self.infoLabel = PyQt5.QtWidgets.QLabel("Info")
        
        # Arrange them in Window
        self.hbox = PyQt5.QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.titleLabel)
        self.hbox.addWidget(self.infoLabel)

        return
    
    def getLayout(self):
        """
        Return the layout for display
        """
        return self.hbox
    
