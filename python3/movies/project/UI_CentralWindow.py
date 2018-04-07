"""
This file handles holding the main GUI elements
"""

import PyQt5
import PyQt5.QtWidgets

import UI_MovieInfo

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

        # Set up the various HBOX and VBOX
        hboxSearch = PyQt5.QtWidgets.QHBoxLayout()
        hboxInfo1 = PyQt5.QtWidgets.QHBoxLayout()
        hboxInfo2 = PyQt5.QtWidgets.QHBoxLayout()
        hboxInfo3 = PyQt5.QtWidgets.QHBoxLayout()
        hboxInfoAndPoster = PyQt5.QtWidgets.QHBoxLayout()
        vboxInfo = PyQt5.QtWidgets.QVBoxLayout()
        vbox = PyQt5.QtWidgets.QVBoxLayout()

        # hboxSearch is the layer for entering movie information
        # and running the search
        hboxSearch.addWidget(enterMovieLabel)
        hboxSearch.addWidget(self.enterMovieLineEdit)
        hboxSearch.addWidget(self.enterMoviePushButton)

        # hboxInfo is the layer for presenting the results from the search
        self.directorInformation = UI_MovieInfo.UI_MovieInfo(title="Director:")
        self.actorInformation = UI_MovieInfo.UI_MovieInfo(title="Actor:")
        self.releaseDateInformation = UI_MovieInfo.UI_MovieInfo(title="Release Date:")
        
        self.budgetInformation = UI_MovieInfo.UI_MovieInfo(title="Budget:")
        self.revenueInformation = UI_MovieInfo.UI_MovieInfo(title="Revenue:")
        self.runTimeInformation = UI_MovieInfo.UI_MovieInfo(title="Run Time:")

        self.voteCountInformation = UI_MovieInfo.UI_MovieInfo(title="Vote Count:")
        self.voteAverageInformation = UI_MovieInfo.UI_MovieInfo(title="Vote Average:")
        self.statusInformation = UI_MovieInfo.UI_MovieInfo(title="Status:")
        
        hboxInfo1.addLayout(self.directorInformation.getLayout())
        hboxInfo1.addLayout(self.actorInformation.getLayout())
        hboxInfo1.addLayout(self.releaseDateInformation.getLayout())

        hboxInfo2.addLayout(self.budgetInformation.getLayout())
        hboxInfo2.addLayout(self.revenueInformation.getLayout())
        hboxInfo2.addLayout(self.runTimeInformation.getLayout())

        hboxInfo3.addLayout(self.voteCountInformation.getLayout())
        hboxInfo3.addLayout(self.voteAverageInformation.getLayout())
        hboxInfo3.addLayout(self.statusInformation.getLayout())

        self.posterLabel = PyQt5.QtWidgets.QLabel("Poster Goes Here")
        self.pixmap = PyQt5.QtGui.QPixmap()

        hboxInfoAndPoster.addWidget(self.posterLabel)
        vboxInfo.addLayout(hboxInfo1)
        vboxInfo.addLayout(hboxInfo2)
        vboxInfo.addLayout(hboxInfo3)
        hboxInfoAndPoster.addLayout(vboxInfo)
        
        vbox.addLayout(hboxSearch)
        vbox.addLayout(hboxInfoAndPoster)

        
        # Put into layout to view
        self.setLayout(vbox)
        return

    def updatePoster(self, posterFileName=None):
        self.pixmap.load(posterFileName)
        scaledPixmap = self.pixmap.scaled(self.posterLabel.size(), PyQt5.QtCore.Qt.KeepAspectRatio)
        self.posterLabel.setPixmap(self.pixmap)
        self.posterLabel.setScaledContents(False)
        return
