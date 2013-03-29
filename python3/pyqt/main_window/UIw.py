'''
Created on Mar 28, 2013

@author: tractp1
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class UIw(QMainWindow):
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
        super(UIw, self).__init__(parent)

        self.image = QImage()
        self.filename = None
        self.recentFiles = ""

        self.imageLabel = QLabel()
        self.imageLabel.setMinimumSize(200, 200)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setCentralWidget(self.imageLabel)

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.clear()
        fileNewAction = self.createAction("&New...", self.fileNew,
                QKeySequence.New, "filenew", "Create an image file")
        fileOpenAction = self.createAction("&Open...", self.fileOpen,
                QKeySequence.Open, "fileopen",
                "Open an existing image file")
        fileSaveAction = self.createAction("&Save", self.fileSave,
                QKeySequence.Save, "filesave", "Save the image")
        fileSaveAsAction = self.createAction("Save &As...",
                self.fileSaveAs, icon = "filesaveas",
                tip = "Save the image using a new name")
        filePrintAction = self.createAction("&Print", self.filePrint,
                QKeySequence.Print, "fileprint", "Print the image")
        fileQuitAction = self.createAction("&Quit", self.close,
                "Ctrl+Q", "filequit", "Close the application")

        self.fileMenuActions = (fileNewAction, fileOpenAction, fileSaveAction, fileSaveAsAction, filePrintAction, fileQuitAction)
        self.addActions(self.fileMenu, self.fileMenuActions)

        self.fileMenu = self.menuBar().addMenu("&Edit")
        self.fileMenu = self.menuBar().addMenu("&Other")

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
                                      fileSaveAsAction))
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")


        self.setWindowTitle("Image Changer")
        return

    def fileSave(self):
        return

    def fileSaveAs(self):
        return

    def filePrint(self):
        return

    def fileClose(self):
        self.close()
        return

    def fileNew(self):
        return

    def fileOpen(self):
        return

    def createAction(self, text, slot = None, shortcut = None, icon = None,
                     tip = None, checkable = False, signal = "triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/{0}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action


    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)
