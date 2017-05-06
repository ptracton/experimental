#! /usr/bin/env python3

from PyQt4 import QtGui
from PyQt4 import QtCore
import UI_central


class UI(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(UI, self).__init__(parent)
        self.statusBar().showMessage('Started ')

        self.central = UI_central.UI_central()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        helpMenu = menubar.addMenu('&Help')
        exitAction = QtGui.QAction(
            QtGui.QIcon('application-exit.png'),
            '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
        fileMenu.addAction(exitAction)

        aboutAction = QtGui.QAction('&About', self)
        aboutAction.setShortcut('Ctrl+A')
        aboutAction.setStatusTip('About')
        #aboutAction.triggered.connect(self.aboutAction)
        #helpMenu.addAction(aboutAction)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(aboutAction)

        self.setCentralWidget(self.central)
        self.setWindowTitle('Waveform Demo')
        self.show()
        
        return
