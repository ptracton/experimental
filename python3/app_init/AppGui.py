
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import App
import AppConfigGUI

class AppGui(QMainWindow):
    """
    """

    def __init__(self, parent = None):
        #
        # Call contstructor of our Super Class, we inherit from QDialog
        #
        super(AppGui, self).__init__(parent)
        print ("STARTING GUI")
        
        ########################################################################
        #
        # Create instance of the "Application" and make sure it has either loaded
        # its configuration or created a new one
        #
        ########################################################################
        self.app = App.App()
        self.Configure()

        TopLayout = QVBoxLayout()

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)
        
        self.FileMenu = self.menuBar().addMenu("&File")
        self.FileMenu.clear()
        FileNewAction = self.CreateAction("&New...", self.FileNew,
                                          QKeySequence.New, "filenew", "Create an image file")
        FileOpenAction = self.CreateAction("&Open...", self.FileOpen,
                                           QKeySequence.Open, "fileopen",
                                           "Open an existing image file")
        FileSaveAction = self.CreateAction("&Save", self.FileSave,
                                           QKeySequence.Save, "filesave", "Save the image")
        FileSaveAsAction = self.CreateAction("Save &As...",
                                             self.FileSaveAs, icon = "filesaveas",
                                             tip = "Save the image using a new name")
        FileQuitAction = self.CreateAction("&Quit", self.FileQuit,
                                           "Ctrl+Q", "FileQuit", "Close the application")
        
        self.FileMenuActions = (FileNewAction, FileOpenAction, FileSaveAction, FileSaveAsAction, FileQuitAction)
        self.AddActions(self.FileMenu, self.FileMenuActions)

        self.FileMenu = self.menuBar().addMenu("&Edit")
        self.FileMenu = self.menuBar().addMenu("&Other")

        FileToolbar = self.addToolBar("File")
        FileToolbar.setObjectName("FileToolBar")
        self.AddActions(FileToolbar, (FileNewAction, FileOpenAction,
                                      FileSaveAsAction))
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")

        self.setWindowTitle("Application")

        return

    def FileNew(self):
        return

    def FileOpen(self):
        return

    def FileSave(self):
        return

    def FileSaveAs(self):
        return

    def FileQuit(self):
        self.close()
        return

    def AddActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)


    def CreateAction(self, text, slot = None, shortcut = None, icon = None,
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
                        
    def Configure(self):
        if self.app.appConfig.ConfigExists():
            print ("Found it")
        else:
            print ("Config does not exist")
            appConfigGUI = AppConfigGUI.AppConfigGUI(parent = self)
            appConfigGUI.exec_()
